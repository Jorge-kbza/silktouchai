import os

from anthropic import Anthropic

def ask_claude(peticion, ruta_del_mundo, nombre_random):

    api_key = os.environ.get("API_KEY")  # <- accede a la variable
    client = Anthropic(api_key=api_key)

    reglas = f"""
            Quiero que crees esta estructura usando Python y Amulet-Core, para minecraft. No olvides:
            - No es necesario que uses prints ni expliques el codigo
            - Haz la construccion completa, e competente, escatima en gastos
            - Los interiores no son tan importantes, importa mas la fachada, el exterior
            - Siempre definir todos los bloques usados explícitamente, ya que a veces olvidas definir bloques y da errores, en caso de error usa un bloque de tierra
            - No tener errores de sintaxis ni ejecución.
            - El código debe ejecutarse directamente sin fallos.
            - No te olvides del world.save() y world.close()
            - No uses las propiedades de los bloques, es decir, no pongas esto: "facing": "north", sin orientaciones ni nada
            - El mundo de minecraft será un mundo plano
            - No es necesario que limpies la zona, construye directamente

            - Lo mas importante, debes guardar las coordenadas en donde se encuentra la estructura creada en json, siguiendo exactamente este modelo:

    	import amulet
    from amulet.api.block import Block
    import math
    import random
    import os
    import json

    # Cargar el mundo de Minecraft
    world_path = "{ruta_del_mundo}"
    world = amulet.load_level(world_path)
    dimension = "minecraft:overworld"

    # Coordenadas base del castillo
    base_x, base_z = 0, 0
    ground_y = 65

    # Definir todos los bloques explícitamente
    stone_bricks = Block("minecraft", "stone_bricks")
    chiseled_stone_bricks = Block("minecraft", "chiseled_stone_bricks")
    cracked_stone_bricks = Block("minecraft", "cracked_stone_bricks")
    mossy_stone_bricks = Block("minecraft", "mossy_stone_bricks")
    cobblestone = Block("minecraft", "cobblestone")
    mossy_cobblestone = Block("minecraft", "mossy_cobblestone")
    oak_planks = Block("minecraft", "oak_planks")
    dark_oak_planks = Block("minecraft", "dark_oak_planks")
    oak_log = Block("minecraft", "oak_log")
    dark_oak_log = Block("minecraft", "dark_oak_log")
    iron_bars = Block("minecraft", "iron_bars")
    glass = Block("minecraft", "glass")
    glowstone = Block("minecraft", "glowstone")
    torch = Block("minecraft", "torch")
    lantern = Block("minecraft", "lantern")
    air = Block("minecraft", "air")
    grass_block = Block("minecraft", "grass_block")
    dirt = Block("minecraft", "dirt")
    stone = Block("minecraft", "stone")
    andesite = Block("minecraft", "andesite")
    polished_andesite = Block("minecraft", "polished_andesite")
    quartz_block = Block("minecraft", "quartz_block")
    chiseled_quartz_block = Block("minecraft", "chiseled_quartz_block")
    white_concrete = Block("minecraft", "white_concrete")
    light_gray_concrete = Block("minecraft", "light_gray_concrete")
    gray_concrete = Block("minecraft", "gray_concrete")
    red_concrete = Block("minecraft", "red_concrete")
    oak_stairs = Block("minecraft", "oak_stairs")
    stone_brick_stairs = Block("minecraft", "stone_brick_stairs")
    cobblestone_stairs = Block("minecraft", "cobblestone_stairs")
    oak_slab = Block("minecraft", "oak_slab")
    stone_brick_slab = Block("minecraft", "stone_brick_slab")
    oak_door = Block("minecraft", "oak_door")
    iron_door = Block("minecraft", "iron_door")
    water = Block("minecraft", "water")
    blue_concrete = Block("minecraft", "blue_concrete")
    cyan_concrete = Block("minecraft", "cyan_concrete")


    def place_block(x, y, z, block):
        cx, cz = x >> 4, z >> 4
        try:
            chunk = world.get_chunk(cx, cz, dimension)
        except:
            chunk = world.create_chunk(cx, cz, dimension)
        lx, lz = x % 16, z % 16
        chunk.blocks[lx, y, lz] = chunk.block_palette.get_add_block(block)
        world.put_chunk(chunk, dimension)


    def create_circular_wall(center_x, center_z, center_y, radius, height, thickness, wall_block):
        for angle in range(360):
            for t in range(thickness):
                x = center_x + int((radius - t) * math.cos(math.radians(angle)))
                z = center_z + int((radius - t) * math.sin(math.radians(angle)))
                for y in range(center_y, center_y + height):
                    place_block(x, y, z, wall_block)


    def create_tower(center_x, center_z, base_y, radius, height, tower_block, roof_block):
        # Base de la torre
        for dx in range(-radius - 1, radius + 2):
            for dz in range(-radius - 1, radius + 2):
                distance = math.sqrt(dx * dx + dz * dz)
                if distance <= radius + 1:
                    x, z = center_x + dx, center_z + dz
                    for y in range(base_y, base_y + height):
                        if distance <= radius:
                            if distance >= radius - 2:  # Paredes
                                place_block(x, y, z, tower_block)
                            elif y == base_y or (y - base_y) % 10 == 0:  # Pisos
                                place_block(x, y, z, oak_planks)

        # Techo cónico
        roof_height = radius + 5
        for dy in range(roof_height):
            roof_radius = max(1, radius - dy // 2)
            for angle in range(0, 360, 5):
                x = center_x + int(roof_radius * math.cos(math.radians(angle)))
                z = center_z + int(roof_radius * math.sin(math.radians(angle)))
                place_block(x, base_y + height + dy, z, roof_block)

        # Ventanas
        for level in range(2, height, 8):
            for angle in range(0, 360, 90):
                window_x = center_x + int(radius * math.cos(math.radians(angle)))
                window_z = center_z + int(radius * math.sin(math.radians(angle)))
                place_block(window_x, base_y + level, window_z, glass)
                place_block(window_x, base_y + level + 1, window_z, glass)


    def create_rectangular_structure(x1, z1, x2, z2, base_y, height, wall_block, floor_block):
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_z, max_z = min(z1, z2), max(z1, z2)

        for x in range(min_x, max_x + 1):
            for z in range(min_z, max_z + 1):
                # Paredes
                if x == min_x or x == max_x or z == min_z or z == max_z:
                    for y in range(base_y, base_y + height):
                        place_block(x, y, z, wall_block)
                # Pisos
                else:
                    for floor_level in range(base_y, base_y + height, 5):
                        place_block(x, floor_level, z, floor_block)


    # ESTRUCTURA PRINCIPAL DEL CASTILLO

    # 1. BASE Y TERRENO
    castle_radius = 80
    for dx in range(-castle_radius, castle_radius + 1):
        for dz in range(-castle_radius, castle_radius + 1):
            distance = math.sqrt(dx * dx + dz * dz)
            if distance <= castle_radius:
                place_block(base_x + dx, ground_y - 1, base_z + dz, grass_block)
                place_block(base_x + dx, ground_y - 2, base_z + dz, dirt)

    # 2. MURALLA EXTERIOR PRINCIPAL (Circular)
    main_wall_radius = 70
    main_wall_height = 25
    create_circular_wall(base_x, base_z, ground_y, main_wall_radius, main_wall_height, 3, stone_bricks)

    # Almenas en la muralla exterior
    for angle in range(0, 360, 8):
        x = base_x + int(main_wall_radius * math.cos(math.radians(angle)))
        z = base_z + int(main_wall_radius * math.sin(math.radians(angle)))
        if angle % 16 == 0:  # Almenas más altas
            place_block(x, ground_y + main_wall_height, z, stone_bricks)
            place_block(x, ground_y + main_wall_height + 1, z, stone_bricks)

    # 3. TORRES DE LAS MURALLAS (8 torres alrededor)
    tower_angles = [0, 45, 90, 135, 180, 225, 270, 315]
    wall_towers = []

    for angle in tower_angles:
        tower_x = base_x + int((main_wall_radius + 5) * math.cos(math.radians(angle)))
        tower_z = base_z + int((main_wall_radius + 5) * math.sin(math.radians(angle)))
        wall_towers.append((tower_x, tower_z))
        create_tower(tower_x, tower_z, ground_y, 8, 35, stone_bricks, red_concrete)

    # 4. MURALLA INTERIOR
    inner_wall_radius = 45
    inner_wall_height = 20
    create_circular_wall(base_x, base_z, ground_y, inner_wall_radius, inner_wall_height, 2, chiseled_stone_bricks)

    # 5. TORRES INTERMEDIAS (4 torres entre murallas)
    intermediate_tower_angles = [30, 120, 210, 300]
    intermediate_towers = []

    for angle in intermediate_tower_angles:
        tower_x = base_x + int(57 * math.cos(math.radians(angle)))
        tower_z = base_z + int(57 * math.sin(math.radians(angle)))
        intermediate_towers.append((tower_x, tower_z))
        create_tower(tower_x, tower_z, ground_y, 6, 30, mossy_stone_bricks, dark_oak_planks)

    # 6. TORRE CENTRAL PRINCIPAL (LA MÁS IMPRESIONANTE)
    central_tower_radius = 15
    central_tower_height = 60

    # Base de la torre central con decoración
    for dx in range(-central_tower_radius - 3, central_tower_radius + 4):
        for dz in range(-central_tower_radius - 3, central_tower_radius + 4):
            distance = math.sqrt(dx * dx + dz * dz)
            if distance <= central_tower_radius + 3:
                x, z = base_x + dx, base_z + dz
                # Fundación elevada
                for y in range(ground_y, ground_y + 5):
                    if distance <= central_tower_radius + 2:
                        place_block(x, y, z, polished_andesite)

    # Torre central principal
    create_tower(base_x, base_z, ground_y + 5, central_tower_radius, central_tower_height, chiseled_stone_bricks,
                 quartz_block)

    # Añadir detalles decorativos a la torre central
    for level in range(10, central_tower_height, 15):
        for angle in range(0, 360, 30):
            detail_x = base_x + int((central_tower_radius + 2) * math.cos(math.radians(angle)))
            detail_z = base_z + int((central_tower_radius + 2) * math.sin(math.radians(angle)))
            place_block(detail_x, ground_y + 5 + level, detail_z, chiseled_quartz_block)
            place_block(detail_x, ground_y + 5 + level + 1, detail_z, chiseled_quartz_block)

    # 7. SUB-TORRES EN LA TORRE CENTRAL
    sub_tower_angles = [0, 120, 240]
    for angle in sub_tower_angles:
        sub_tower_x = base_x + int(25 * math.cos(math.radians(angle)))
        sub_tower_z = base_z + int(25 * math.sin(math.radians(angle)))
        create_tower(sub_tower_x, sub_tower_z, ground_y, 10, 45, white_concrete, cyan_concrete)

    # 8. ESTRUCTURAS INTERIORES

    # Salón principal (rectangular)
    hall_width = 20
    hall_length = 30
    hall_height = 15
    create_rectangular_structure(
        base_x - hall_width // 2, base_z - hall_length // 2 - 35,
        base_x + hall_width // 2, base_z + hall_length // 2 - 35,
        ground_y, hall_height, stone_bricks, oak_planks
    )

    # Barracones
    barracks_width = 12
    barracks_length = 25
    create_rectangular_structure(
        base_x - 35, base_z - barracks_length // 2,
        base_x - 35 + barracks_width, base_z + barracks_length // 2,
        ground_y, 12, cobblestone, dark_oak_planks
    )

    create_rectangular_structure(
        base_x + 35 - barracks_width, base_z - barracks_length // 2,
        base_x + 35, base_z + barracks_length // 2,
        ground_y, 12, cobblestone, dark_oak_planks
    )

    # 9. PUENTE Y ENTRADA PRINCIPAL
    gate_angle = 180  # Entrada al sur
    gate_x = base_x + int(main_wall_radius * math.cos(math.radians(gate_angle)))
    gate_z = base_z + int(main_wall_radius * math.sin(math.radians(gate_angle)))

    # Abrir la puerta en la muralla
    for dx in range(-4, 5):
        for dy in range(8):
            place_block(gate_x + dx, ground_y + dy, gate_z, air)

    # Puente de entrada
    for bridge_dx in range(-3, 4):
        for bridge_dz in range(15):
            place_block(gate_x + bridge_dx, ground_y - 1, gate_z + bridge_dz, stone_bricks)
            # Barandillas del puente
            if abs(bridge_dx) == 3:
                place_block(gate_x + bridge_dx, ground_y, gate_z + bridge_dz, iron_bars)
                place_block(gate_x + bridge_dx, ground_y + 1, gate_z + bridge_dz, iron_bars)

    # Torres de entrada
    create_tower(gate_x - 8, gate_z, ground_y, 6, 30, stone_bricks, red_concrete)
    create_tower(gate_x + 8, gate_z, ground_y, 6, 30, stone_bricks, red_concrete)

    # 10. FOSO CON AGUA
    foso_inner_radius = main_wall_radius + 8
    foso_outer_radius = main_wall_radius + 15

    for dx in range(-foso_outer_radius, foso_outer_radius + 1):
        for dz in range(-foso_outer_radius, foso_outer_radius + 1):
            distance = math.sqrt(dx * dx + dz * dz)
            if foso_inner_radius <= distance <= foso_outer_radius:
                x, z = base_x + dx, base_z + dz
                # Excavar el foso
                for y in range(ground_y - 4, ground_y):
                    place_block(x, y, z, air)
                # Llenar con agua
                place_block(x, ground_y - 4, z, water)
                place_block(x, ground_y - 3, z, water)

    # 11. ILUMINACIÓN DEL CASTILLO
    light_positions = []

    # Antorchas en las murallas
    for angle in range(0, 360, 20):
        # Muralla exterior
        x = base_x + int(main_wall_radius * math.cos(math.radians(angle)))
        z = base_z + int(main_wall_radius * math.sin(math.radians(angle)))
        place_block(x, ground_y + main_wall_height - 2, z, torch)

        # Muralla interior
        x = base_x + int(inner_wall_radius * math.cos(math.radians(angle)))
        z = base_z + int(inner_wall_radius * math.sin(math.radians(angle)))
        place_block(x, ground_y + inner_wall_height - 2, z, torch)

    # Linternas en las torres
    for tower_x, tower_z in wall_towers:
        place_block(tower_x, ground_y + 35 + 8, tower_z, lantern)

    for tower_x, tower_z in intermediate_towers:
        place_block(tower_x, ground_y + 30 + 6, tower_z, lantern)

    # Iluminación en la torre central
    place_block(base_x, ground_y + 5 + central_tower_height + central_tower_radius + 5, base_z, glowstone)

    # 12. DETALLES FINALES Y DECORACIÓN

    # Banderas en las torres (usando lana de colores)
    red_wool = Block("minecraft", "red_wool")
    blue_wool = Block("minecraft", "blue_wool")
    white_wool = Block("minecraft", "white_wool")

    for tower_x, tower_z in wall_towers:
        for flag_dy in range(3):
            place_block(tower_x, ground_y + 35 + 10 + flag_dy, tower_z, red_wool)
            place_block(tower_x + 1, ground_y + 35 + 10 + flag_dy, tower_z, blue_wool)

    # Jardines internos
    for garden_spots in range(20):
        garden_x = base_x + random.randint(-inner_wall_radius + 5, inner_wall_radius - 5)
        garden_z = base_z + random.randint(-inner_wall_radius + 5, inner_wall_radius - 5)
        distance_from_center = math.sqrt((garden_x - base_x) ** 2 + (garden_z - base_z) ** 2)
        if distance_from_center > 20:  # No interferir con la torre central
            place_block(garden_x, ground_y, garden_z, grass_block)
            if random.random() < 0.3:
                place_block(garden_x, ground_y + 1, garden_z, Block("minecraft", "oak_sapling"))

    # GUARDAR COORDENADAS
    min_x = base_x - main_wall_radius - 15
    max_x = base_x + main_wall_radius + 15
    min_z = base_z - main_wall_radius - 15
    max_z = base_z + main_wall_radius + 15
    min_y = ground_y - 4
    max_y = ground_y + central_tower_height + central_tower_radius + 10

    # Datos de coordenadas
    datos = {{
        "x1": min_x,
        "y1": min_y,
        "z1": min_z,
        "x2": max_x,
        "y2": max_y,
        "z2": max_z
    }}

    # Ruta al archivo JSON en la misma carpeta del script
    ruta = os.path.join("{nombre_random}", "datos.json")

    # Guardar los datos en el JSON
    with open(ruta, "w", encoding="utf-8") as json_file:
        json.dump(datos, json_file, indent=4, ensure_ascii=False)

    # Guardar y cerrar el mundo
    world.save()
    world.close()        

    """

    prompt = peticion + reglas

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=15000,
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    # Variable para concatenar texto
    full_text = ""

    # Iterar chunks
    for chunk in response:
        if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'text') and chunk.delta.text:
            full_text += chunk.delta.text

    return full_text