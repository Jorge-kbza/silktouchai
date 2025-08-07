import os
import shutil
import threading
import time
import traceback

from flask import Flask, request, send_file, after_this_request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from Ai_controller import main, gestion_archivos
app = Flask(__name__)
CORS(app, origins="*")

@app.route('/')
def pong():
    print('PONG')
    return jsonify({'message': 'pong'}), 200

@app.route('/prompt', methods=['POST'])
def generar_archivo():
    try:
        datos = request.json
        prompt = datos.get('prompt')
        nombre_archivo_web = datos.get('nombre')
        print('🟢 Prompt recibido:', prompt)

        if not prompt:
            return jsonify({'success': False, 'error': 'No se envió texto'}), 400

        # Creamos carpeta
        ruta, nombre_random = gestion_archivos()
        print(f"📁 Carpeta creada: {ruta}")

        # Ejecutamos IA y generamos archivo
        ruta_archivo = main(ruta, nombre_random, prompt, nombre_archivo_web)
        print(f"📦 Archivo generado: {ruta_archivo}")

        def borrar_carpeta_con_retraso(carpeta):
            time.sleep(30)
            try:
                shutil.rmtree(carpeta)
                print(f"✅ Carpeta {carpeta} eliminada")
            except Exception as e:
                print(f"⚠️ Error al borrar carpeta: {e}")

        @after_this_request
        def cleanup(response):
            threading.Thread(target=borrar_carpeta_con_retraso, args=(nombre_random,), daemon=True).start()
            return response

        return send_file(
            f'{nombre_archivo_web}.schem',
            as_attachment=True,  # Fuerza descarga
            download_name="estructura_generada.schem",  # Nombre que verá el usuario
            mimetype="application/octet-stream"  # Tipo de archivo binario
        )


    except Exception as e:
        print(f"❌ ERROR EN /prompt: {e}")
        traceback.print_exc()  # <--- Añade esto
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/download', methods=['GET', 'HEAD'])
def devolver_archivo():
    nombre_random = request.args.get('file')
    if not nombre_random:
        return jsonify({"success": False, "error": "Falta el nombre del archivo"}), 400

    filename = secure_filename(nombre_random)
    ruta_archivo = os.path.join("structures", filename)

    if request.method == "HEAD":
        if os.path.isfile(ruta_archivo):
            return '', 200
        else:
            return '', 404  # <- CAMBIA ESTO DE 403 A 404

    if not os.path.isfile(ruta_archivo):
        return jsonify({"success": False, "error": "Archivo no encontrado"}), 404

    return send_file(
        ruta_archivo,
        as_attachment=True,
        download_name='estructura_generada.schem',
        mimetype="application/octet-stream"
    )

if __name__ == "__main__":
    print("HOLA MUNDO SILKTOUCH AI OPERATIVO AAAAAAAAAAAAAAAa")
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
