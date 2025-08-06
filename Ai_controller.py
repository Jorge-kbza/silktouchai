import json
import os
import re
import shutil
import uuid

from Ai_service import ask_claude
from export_schematic_service import schem_export

def gestion_archivos():
    carpeta_original = "SilkTouchWorld"
    nombre_random = str(uuid.uuid4())[:8]
    ruta_carpeta_copia = os.path.join(nombre_random, carpeta_original)
    os.makedirs(nombre_random, exist_ok=True)
    shutil.copytree(carpeta_original, ruta_carpeta_copia)

    # Datos que quieres guardar
    datos = {"x1": 0, "y1": 0,"z1": 0, "x2": 0, "y2": 0, "z2": 0}

    # Ruta al archivo JSON en la misma carpeta del script
    ruta = os.path.join(nombre_random, "datos.json")

    # Guardar los datos en el JSON
    with open(ruta, "w", encoding="utf-8") as json_file:
        json.dump(datos, json_file, indent=4, ensure_ascii=False)

    # Devolvemos la ruta al mundo de MC y el nombre de la carpeta
    return ruta_carpeta_copia, nombre_random

def main(ruta, nombre_random, peticion):
    full_text = ask_claude(peticion, ruta, nombre_random)

    # Ahora extraemos el bloque de código
    codigo = re.search(r"```python\s*(.*?)```", full_text, re.DOTALL)

    if codigo:
        solo_codigo = codigo.group(1)
        try:
            # Ejecutamos el codigo de Claude
            exec(solo_codigo, globals())

            # Cargar el archivo JSON desde la misma carpeta
            with open(os.path.join(nombre_random, "datos.json"), "r", encoding="utf-8") as json_file:
                datos = json.load(json_file)

            # Exportamos a .schem y devolvemos la ruta donde se encuentra el archivo
            output_path = schem_export(int(datos['x1']), int(datos['y1']), int(datos['z1']), int(datos['x2']), int(datos['y2']), int(datos['z2']),
                         ruta, "structures", nombre_random)
            return output_path

        except Exception as e:
            print(f"\n⚠️ Error al ejecutar el código: {e}")
    else:
        print("\n⚠️ No se encontró un bloque de código en la respuesta.")
        print(full_text)
        return None

if __name__ == '__main__':
    print("Hola Mundo")
    """
    # Creamos la nueva carpeta que contendra la copia del mundo, JSON y .schem
    ruta, nombre_random = gestion_archivos()
    # Claude genera y ejecuta el codigo generado mediante el prompt y crea el archivo .schem
    output_path = main(ruta,  nombre_random)
    # Enviamos el archivo a la web para descargar"""