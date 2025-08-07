import os
import shutil
import threading
import time
import traceback
import logging

logging.basicConfig(level=logging.INFO)

from flask import Flask, request, send_file, after_this_request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from Ai_controller import main, gestion_archivos

app = Flask(__name__)
CORS(app, origins="*")


# 🔧 MANEJADOR GLOBAL DE ERRORES
@app.errorhandler(500)
def handle_internal_error(e):
    """Asegura que todos los errores 500 devuelvan JSON"""
    logging.error(f"❌ Error 500: {str(e)}")
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor'
    }), 500


@app.errorhandler(404)
def handle_not_found(e):
    """Maneja errores 404 como JSON"""
    return jsonify({
        'success': False,
        'error': 'Endpoint no encontrado'
    }), 404


@app.route('/')
def pong():
    logging.info('PONG')
    return jsonify({'message': 'pong'}), 200


@app.route('/prompt', methods=['POST'])
def generar_archivo():
    try:
        # 🔍 VALIDACIÓN MEJORADA DE ENTRADA
        if not request.is_json:
            logging.error("❌ Request no es JSON")
            return jsonify({
                'success': False,
                'error': 'Content-Type debe ser application/json'
            }), 400

        datos = request.get_json()
        if not datos:
            logging.error("❌ Body JSON vacío")
            return jsonify({
                'success': False,
                'error': 'Body JSON requerido'
            }), 400

        prompt = datos.get('prompt', '').strip()
        nombre_archivo_web = datos.get('nombre', '').strip()

        logging.info(f'🟢 Prompt recibido: {prompt}')
        logging.info(f'📝 Nombre archivo: {nombre_archivo_web}')

        # 🚨 VALIDACIONES
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'El campo "prompt" es requerido y no puede estar vacío'
            }), 400

        if not nombre_archivo_web:
            return jsonify({
                'success': False,
                'error': 'El campo "nombre" es requerido y no puede estar vacío'
            }), 400

        if len(prompt) > 1000:  # Límite de caracteres
            return jsonify({
                'success': False,
                'error': 'El prompt no puede exceder 1000 caracteres'
            }), 400

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
            return jsonify({
                'success': False,
                'error': 'Error al generar el archivo'
            }), 500

        # Programar limpieza
        threading.Thread(
            target=borrar_carpeta_con_retraso,
            args=(nombre_random,),
            daemon=True
        ).start()

        logging.info(f"✅ Respuesta exitosa - ruta: {ruta_descarga}")
        return jsonify({
            'success': True,
            'ruta': ruta_descarga,
            'mensaje': 'Archivo generado correctamente'
        }), 200

    except Exception as e:
        # 🚨 MANEJO ROBUSTO DE ERRORES
        error_msg = str(e)
        logging.error(f"❌ ERROR EN /prompt: {error_msg}")
        logging.error(f"📊 Traceback: {traceback.format_exc()}")

        # NUNCA devolver el error real en producción por seguridad
        return jsonify({
            'success': False,
            'error': 'Error interno al procesar la solicitud',
            'debug': error_msg if app.debug else None  # Solo en modo debug
        }), 500


@app.route('/download', methods=['GET', 'HEAD'])
def devolver_archivo():
    try:
        nombre_random = request.args.get('file')
        if not nombre_random:
            return jsonify({
                "success": False,
                "error": "Parámetro 'file' requerido"
            }), 400

        filename = secure_filename(nombre_random)
        ruta_archivo = os.path.join("structures", filename)

        logging.info(f"📥 Solicitud de descarga: {ruta_archivo}")

        if request.method == "HEAD":
            if os.path.isfile(ruta_archivo):
                return '', 200
            else:
                return '', 404

        if not os.path.isfile(ruta_archivo):
            return jsonify({
                "success": False,
                "error": "Archivo no encontrado"
            }), 404

        return send_file(
            ruta_archivo,
            as_attachment=True,
            download_name='estructura_generada.schem',
            mimetype="application/octet-stream"
        )

    except Exception as e:
        logging.error(f"❌ ERROR EN /download: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Error al descargar archivo"
        }), 500


# 🔧 ENDPOINT DE HEALTH CHECK
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time()
    }), 200


if __name__ == "__main__":
    logging.info("🚀 SILKTOUCH AI INICIANDO...")
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"

    logging.info(f"🌐 Puerto: {port}")
    logging.info(f"🐛 Debug: {debug_mode}")

    app.run(host='0.0.0.0', port=port, debug=debug_mode)