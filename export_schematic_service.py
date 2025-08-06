import os

import amulet
from amulet.api.errors import ChunkLoadError
from amulet.api.selection import SelectionBox, SelectionGroup
from amulet.level.formats.sponge_schem import SpongeSchemFormatWrapper


def schem_export(x1, y1, z1, x2, y2, z2, ruta, ruta_salida, nombre_random):
    # Coordenadas de tu estructura
    # x1, y1, z1 = 98, 170, 20090
    # x2, y2, z2 = 78, 210, 20076

    # Ruta del mundo
    world_path = ruta # r'C:\Users\jorge\AppData\Roaming\.minecraft\saves\New'
    world = amulet.load_level(world_path)
    dimension = "minecraft:overworld"

    # Plataforma y versión externa
    platform = world.level_wrapper.platform
    version = world.level_wrapper.version

    # Crear la selección
    box = SelectionBox(
        (min(x1, x2), min(y1, y2), min(z1, z2)),
        (max(x1, x2) + 1, max(y1, y2) + 1, max(z1, z2) + 1)
    )
    selection = SelectionGroup([box])

    # Ruta de salida del archivo .schem
    output_path = os.path.abspath(f"{ruta_salida}/{nombre_random}.schem")

    # Crear el wrapper del archivo Sponge Schematic
    wrapper = SpongeSchemFormatWrapper(output_path)
    wrapper.create_and_open(platform, version, selection, True)
    wrapper.translation_manager = world.translation_manager
    wrapper_dimension = wrapper.dimensions[0]

    # Exportar chunks dentro de la selección
    for cx, cz in selection.chunk_locations():
        try:
            chunk = world.get_chunk(cx, cz, dimension)
            wrapper.commit_chunk(chunk, wrapper_dimension)
        except ChunkLoadError:
            print(f"⚠️ No se pudo cargar el chunk ({cx}, {cz})")
            continue

    # Guardar y cerrar
    wrapper.save()
    wrapper.close()
    world.close()

    print(f"✅ Estructura exportada correctamente a: {output_path}")
    return output_path