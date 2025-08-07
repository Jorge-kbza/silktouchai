import os
import shutil
import threading
import time
import traceback
import logging

logging.basicConfig(level=logging.INFO)

from flask import Flask, request, send_file, after_this_request, jsonify, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename

from Ai_controller import main, gestion_archivos

app = Flask(__name__)

# 🔧 CORS MEJORADO - ESTO ES CLAVE
CORS(app,
     origins=["*"],
     methods=["GET", "POST", "HEAD", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "Accept"],
     supports_credentials=False
)

# 🔧 MANEJADOR GLOBAL DE ERRORES
@app.errorhandler(500)
def handle_internal_error(e):
    """Asegura que todos los errores 500 devuelvan JSON"""
    logging.error(f"❌ Error 500: {str(e)}")
    response = jsonify({
        'success': False,
        'error': 'Error interno del servidor'
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 500

@app.errorhandler(404)
def handle_not_found(e):
    """Maneja errores 404 como JSON"""
    response = jsonify({
        'success': False,
        'error': 'Endpoint no encontrado'
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 404

# 🔧 MANEJAR PREFLIGHT REQUESTS
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization,Accept")
        response.headers.add('Access-Control-Allow-Methods', "GET,POST,HEAD,OPTIONS")
        return response

@app.route('/')
def pong():
    logging.info('🟢 PONG')
    response = jsonify({'message': 'pong'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

@app.route('/prompt', methods=['POST', 'OPTIONS'])
def generar_archivo():
    # Manejar preflight
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization,Accept")
        response.headers.add('Access-Control-Allow-Methods', "POST,OPTIONS")
        return response

    try:
        # 🔍 VALIDACIÓN MEJORADA DE ENTRADA
        if not request.is_json:
            logging.error("❌ Request no es JSON")
            response = jsonify({
                'success': False,
                'error': 'Content-Type debe ser application/json'
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400

        datos = request.get_json()
        if not datos:
            logging.error("❌ Body JSON vacío")
            response = jsonify({
                'success': False,
                'error': 'Body JSON requerido'
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400

        prompt = datos.get('prompt', '').strip()
        nombre_archivo_web = datos.get('nombre', '').strip()

        logging.info(f'🟢 Prompt recibido: {prompt}')
        logging.info(f'📝 Nombre archivo: {nombre_archivo_web}')

        # 🚨 VALIDACIONES
        if not prompt:
            response = jsonify({
                'success': False,
                'error': 'El campo "prompt" es requerido y no puede estar vacío'
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400

        if not nombre_archivo_web:
            response = jsonify({
                'success': False,
                'error': 'El campo "nombre" es requerido y no puede estar vacío'
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400

        if len(prompt) > 1000:  # Límite de caracteres
            response = jsonify({
                'success': False,
                'error': 'El prompt no puede exceder 1000 caracteres'
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400

        # 🔧 PROCESAMIENTO
        logging.info("📁 Creando carpeta...")
        ruta, nombre_random = gestion_archivos()
        logging.info(f"📁 Carpeta creada: {ruta}")

        # 🤖 EJECUTAR IA
        logging.info("🤖 Ejecutando IA...")
        ruta_archivo = main(ruta, nombre_random, prompt, nombre_archivo_web)
        logging.info(f"📦 Archivo generado: {ruta_archivo}")

        # 🧹 LIMPIEZA CON MEJOR MANEJO
        def borrar_carpeta_con_retraso(carpeta):
            try:
                time.sleep(30)
                if os.path.exists(carpeta):
                    shutil.rmtree(carpeta)
                    logging.info(f"✅ Carpeta {carpeta} eliminada después de 30s")
                else:
                    logging.info(f"⚠️ Carpeta {carpeta} ya no existe")
            except Exception as e:
                logging.error(f"⚠️ Error al borrar carpeta {carpeta}: {e}")

        # 📤 RESPUESTA EXITOSA
        ruta_descarga = f'structures/{nombre_archivo_web}.schem'

        # Verificar que el archivo realmente se creó
        if not os.path.exists(ruta_descarga):
            logging.error(f"❌ Archivo no fue creado: {ruta_descarga}")
            response = jsonify({
                'success': False,
                'error': 'Error al generar el archivo'
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 500

        # Programar limpieza
        threading.Thread(
            target=borrar_carpeta_con_retraso,
            args=(nombre_random,),
            daemon=True
        ).start()

        logging.info(f"✅ Respuesta exitosa - ruta: {ruta_descarga}")
        response = jsonify({
            'success': True,
            'ruta': ruta_descarga,
            'mensaje': 'Archivo generado correctamente'
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200

    except Exception as e:
        # 🚨 MANEJO ROBUSTO DE ERRORES
        error_msg = str(e)
        logging.error(f"❌ ERROR EN /prompt: {error_msg}")
        logging.error(f"📊 Traceback: {traceback.format_exc()}")

        # NUNCA devolver el error real en producción por seguridad
        response = jsonify({
            'success': False,
            'error': 'Error interno al procesar la solicitud',
            'debug': error_msg if app.debug else None  # Solo en modo debug
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/download', methods=['GET', 'HEAD', 'OPTIONS'])
def devolver_archivo():
    # Manejar preflight
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization,Accept")
        response.headers.add('Access-Control-Allow-Methods', "GET,HEAD,OPTIONS")
        return response

    try:
        # 🔧 Corregir el parámetro y mensaje
        ruta_archivo = request.args.get('ruta')
        if not ruta_archivo:
            response = jsonify({
                "success": False,
                "error": "Parámetro 'ruta' requerido"
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400

        logging.info(f"📥 Solicitud de descarga: {ruta_archivo}")

        # 🔍 HEAD request - solo verificar si existe
        if request.method == "HEAD":
            if os.path.isfile(ruta_archivo):
                logging.info(f"✅ HEAD - Archivo existe: {ruta_archivo}")
                response = make_response('', 200)
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
            else:
                logging.info(f"❌ HEAD - Archivo no encontrado: {ruta_archivo}")
                response = make_response('', 404)
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response

        # 📥 GET request - descargar archivo
        if not os.path.isfile(ruta_archivo):
            logging.error(f"❌ GET - Archivo no encontrado: {ruta_archivo}")
            response = jsonify({
                "success": False,
                "error": f"Archivo no encontrado: {os.path.basename(ruta_archivo)}"
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 404

        # 📤 Enviar archivo para descarga
        logging.info(f"📤 Enviando archivo para descarga: {ruta_archivo}")
        return send_file(
            ruta_archivo,
            as_attachment=True,
            download_name='estructura_generada.schem',
            mimetype="application/octet-stream"
        )

    except Exception as e:
        logging.error(f"❌ ERROR EN /download: {str(e)}")
        logging.error(f"📊 Traceback: {traceback.format_exc()}")
        response = jsonify({
            "success": False,
            "error": "Error interno al procesar descarga"
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

# 🔧 ENDPOINT DE HEALTH CHECK
@app.route('/health')
def health_check():
    response = jsonify({
        'status': 'healthy',
        'timestamp': time.time()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

# 🔧 AGREGAR HEADERS CORS A TODAS LAS RESPUESTAS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    return response

if __name__ == "__main__":
    logging.info("🚀 SILKTOUCH AI INICIANDO...")
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"

    logging.info(f"🌐 Puerto: {port}")
    logging.info(f"🐛 Debug: {debug_mode}")

    app.run(host='0.0.0.0', port=port, debug=debug_mode)