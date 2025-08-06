import os

from anthropic import Anthropic

def ask_claude(peticion, ruta_del_mundo, nombre_random):
    api_key = os.environ.get("API_KEY", ""  )
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
        import os
        import json

        # Datos que quieres guardar
        datos = {{
          "x1": 98,
          "y1": 170,
          "z1": 20090,
          "x2": 78,
          "y2": 210,
          "z2": 20076
        }}

        # Ruta al archivo JSON en la misma carpeta del script
        ruta = os.path.join("{nombre_random}", "datos.json")

        # Guardar los datos en el JSON
        with open(ruta, "w", encoding="utf-8") as json_file:
            json.dump(datos, json_file, indent=4, ensure_ascii=False)


        Aquí te dejo un ejemplo para guiarte de como se programa en python con amulet-core:
        import amulet
        from amulet.api.block import Block
        # Ruta del mundo
        import amulet
        from amulet.api.block import Block
        import math
        import random

        # Load the Minecraft world
        world_path = "{ruta_del_mundo}"
        world = amulet.load_level(world_path)
        dimension = "minecraft:overworld"
    
        # Base coordinates
        base_x, base_z = 0, 0
        ground_y = 100  # Higher for floating effect
    
        # MAGICAL FANTASY BLOCKS - Premium materials
        # Stone varieties
        quartz_block = Block("minecraft", "quartz_block")
        chiseled_quartz = Block("minecraft", "chiseled_quartz_block")
        quartz_pillar = Block("minecraft", "quartz_pillar")
        white_concrete = Block("minecraft", "white_concrete")
        light_gray_concrete = Block("minecraft", "light_gray_concrete")
        pink_concrete = Block("minecraft", "pink_concrete")
        purple_concrete = Block("minecraft", "purple_concrete")
        magenta_concrete = Block("minecraft", "magenta_concrete")
    
        # Mystical materials
        prismarine = Block("minecraft", "prismarine")
        dark_prismarine = Block("minecraft", "dark_prismarine")
        prismarine_bricks = Block("minecraft", "prismarine_bricks")
        sea_lantern = Block("minecraft", "sea_lantern")
        glowstone = Block("minecraft", "glowstone")
        amethyst_block = Block("minecraft", "amethyst_block")
    
        # Glass varieties
        glass = Block("minecraft", "glass")
        white_stained_glass = Block("minecraft", "white_stained_glass")
        light_blue_stained_glass = Block("minecraft", "light_blue_stained_glass")
        cyan_stained_glass = Block("minecraft", "cyan_stained_glass")
        purple_stained_glass = Block("minecraft", "purple_stained_glass")
        magenta_stained_glass = Block("minecraft", "magenta_stained_glass")
    
        # Nature blocks
        oak_log = Block("minecraft", "oak_log")
        birch_log = Block("minecraft", "birch_log")
        cherry_log = Block("minecraft", "cherry_log")
        oak_leaves = Block("minecraft", "oak_leaves")
        cherry_leaves = Block("minecraft", "cherry_leaves")
        azalea_leaves = Block("minecraft", "azalea_leaves")
        flowering_azalea_leaves = Block("minecraft", "flowering_azalea_leaves")
    
        # Architectural elements
        quartz_stairs = Block("minecraft", "quartz_stairs")
        white_concrete_stairs = Block("minecraft", "white_concrete_stairs")
        quartz_slab = Block("minecraft", "quartz_slab")
        white_concrete_slab = Block("minecraft", "white_concrete_slab")
    
        # Special blocks
        air = Block("minecraft", "air")
        water = Block("minecraft", "water")
        chain = Block("minecraft", "chain")
        lantern = Block("minecraft", "lantern")
        end_rod = Block("minecraft", "end_rod")
    
    
        def place(x, y, z, block):
            cx, cz = x >> 4, z >> 4
            try:
                chunk = world.get_chunk(cx, cz, dimension)
            except:
                chunk = world.create_chunk(cx, cz, dimension)
            lx, lz = x % 16, z % 16
            chunk.blocks[lx, y, lz] = chunk.block_palette.get_add_block(block)
            world.put_chunk(chunk, dimension)
    
    
        # Clear massive area for the floating city
        for dx in range(-150, 150):
            for dz in range(-150, 150):
                for dy in range(0, 150):
                    place(base_x + dx, ground_y + dy, base_z + dz, air)
    
        # FLOATING ISLANDS - Multiple levels and sizes
        island_data = [
            # (center_x, center_z, center_y, radius, height, island_type)
            (0, 0, 40, 35, 15, "main"),  # Main central island
            (-60, -40, 60, 25, 12, "tower"),  # Northwest tower island
            (60, -40, 50, 20, 10, "garden"),  # Northeast garden island
            (-60, 60, 45, 22, 11, "crystal"),  # Southwest crystal island
            (80, 70, 65, 18, 9, "temple"),  # Southeast temple island
            (0, -80, 35, 15, 8, "bridge"),  # North connector island
            (0, 90, 55, 16, 8, "sanctuary"),  # South sanctuary island
            (-90, 0, 70, 12, 7, "outpost"),  # West outpost
            (100, 0, 30, 14, 8, "spire"),  # East spire island
        ]
    
    
        def create_floating_island(center_x, center_z, center_y, radius, height, island_type):
    
            # Island base terrain
            for dx in range(-radius - 5, radius + 6):
                for dz in range(-radius - 5, radius + 6):
                    distance = math.sqrt(dx * dx + dz * dz)
                    if distance <= radius:
                        # Irregular height variation
                        noise = math.sin(dx * 0.3) * math.cos(dz * 0.3) * 3
                        island_height = int(height + noise * (1 - distance / radius))
    
                        for dy in range(island_height):
                            y_pos = center_y - island_height // 2 + dy
    
                            # Island layers
                            if dy < island_height * 0.3:
                                # Bottom - dark stone
                                block = dark_prismarine
                            elif dy < island_height * 0.7:
                                # Middle - regular stone
                                block = prismarine_bricks
                            else:
                                # Top - light stone/grass
                                if island_type == "crystal":
                                    block = amethyst_block
                                elif island_type == "garden":
                                    block = quartz_block
                                else:
                                    block = white_concrete
    
                            place(base_x + center_x + dx, ground_y + y_pos, base_z + center_z + dz, block)
    
                        # Island surface
                        surface_y = center_y + island_height // 2
                        if distance < radius * 0.8:
                            if island_type == "crystal":
                                place(base_x + center_x + dx, ground_y + surface_y, base_z + center_z + dz,
                                      light_blue_stained_glass)
                            else:
                                place(base_x + center_x + dx, ground_y + surface_y, base_z + center_z + dz, white_concrete)
    
    
        # Create all floating islands
        for island in island_data:
            create_floating_island(*island)
    
        # MAIN CENTRAL PALACE - The crown jewel
        palace_x, palace_z, palace_y = 0, 0, 55
        palace_width, palace_depth = 30, 30
        palace_height = 45
    
        # Palace foundation platform
        for dx in range(-palace_width // 2 - 3, palace_width // 2 + 4):
            for dz in range(-palace_depth // 2 - 3, palace_depth // 2 + 4):
                place(base_x + palace_x + dx, ground_y + palace_y, base_z + palace_z + dz, chiseled_quartz)
    
        # Palace main structure
        for dx in range(-palace_width // 2, palace_width // 2 + 1):
            for dz in range(-palace_depth // 2, palace_depth // 2 + 1):
                if abs(dx) == palace_width // 2 or abs(dz) == palace_depth // 2:
                    # Palace walls with magical pattern
                    for dy in range(1, palace_height):
                        if dy % 6 == 0:
                            wall_block = chiseled_quartz
                        elif dy % 6 == 3:
                            wall_block = amethyst_block
                        else:
                            wall_block = quartz_block
    
                        place(base_x + palace_x + dx, ground_y + palace_y + dy, base_z + palace_z + dz, wall_block)
                else:
                    # Interior floors at multiple levels
                    for floor_y in [8, 18, 28, 38]:
                        place(base_x + palace_x + dx, ground_y + palace_y + floor_y, base_z + palace_z + dz, quartz_slab)
    
        # Palace towers (4 corner towers)
        tower_positions = [(-12, -12), (12, -12), (-12, 12), (12, 12)]
        for tower_dx, tower_dz in tower_positions:
            tower_x = palace_x + tower_dx
            tower_z = palace_z + tower_dz
            tower_height = 55
    
            # Tower structure
            for dx in range(-3, 4):
                for dz in range(-3, 4):
                    if abs(dx) == 3 or abs(dz) == 3:
                        for dy in range(palace_height, palace_height + tower_height):
                            if dy % 8 == 0:
                                tower_block = chiseled_quartz
                            elif dy % 8 == 4:
                                tower_block = amethyst_block
                            else:
                                tower_block = white_concrete
    
                            place(base_x + tower_x + dx, ground_y + palace_y + dy, base_z + tower_z + dz, tower_block)
    
            # Magical crystal spire on each tower
            spire_height = 15
            for dy in range(spire_height):
                spire_size = max(1, 3 - dy // 3)
                spire_y = palace_y + palace_height + tower_height + dy
    
                for dx in range(-spire_size, spire_size + 1):
                    for dz in range(-spire_size, spire_size + 1):
                        if abs(dx) == spire_size or abs(dz) == spire_size or spire_size == 1:
                            if dy % 3 == 0:
                                spire_block = sea_lantern
                            else:
                                spire_block = amethyst_block
    
                            place(base_x + tower_x + dx, ground_y + spire_y, base_z + tower_z + dz, spire_block)
    
        # CRYSTAL BRIDGES connecting islands
        bridge_connections = [
            # (start_island_idx, end_island_idx, bridge_type)
            (0, 1, "crystal"),  # Main to northwest
            (0, 2, "glass"),  # Main to northeast
            (0, 3, "crystal"),  # Main to southwest
            (0, 4, "light"),  # Main to southeast
            (0, 5, "glass"),  # Main to north
            (0, 6, "crystal"),  # Main to south
            (1, 7, "light"),  # Northwest to west
            (2, 8, "glass"),  # Northeast to east
        ]
    
    
        def build_magical_bridge(start_pos, end_pos, bridge_type):
            start_x, start_z, start_y = start_pos
            end_x, end_z, end_y = end_pos
    
            distance = math.sqrt((end_x - start_x) ** 2 + (end_z - start_z) ** 2)
            steps = int(distance * 1.5)  # More detail
    
            for i in range(steps + 1):
                progress = i / max(steps, 1)
    
                # Bridge path with curve
                bridge_x = int(start_x + (end_x - start_x) * progress)
                bridge_z = int(start_z + (end_z - start_z) * progress)
    
                # Magical arc - bridges curve upward in the middle
                height_offset = int(15 * math.sin(progress * math.pi))
                bridge_y = int(start_y + (end_y - start_y) * progress + height_offset)
    
                # Bridge width
                for width_offset in range(-2, 3):
                    bridge_x_offset = bridge_x + width_offset
    
                    # Bridge materials based on type
                    if bridge_type == "crystal":
                        if width_offset == 0:
                            bridge_block = sea_lantern
                        else:
                            bridge_block = cyan_stained_glass
                    elif bridge_type == "glass":
                        if width_offset == 0:
                            bridge_block = glowstone
                        else:
                            bridge_block = white_stained_glass
                    else:  # light bridge
                        if width_offset == 0:
                            bridge_block = end_rod
                        else:
                            bridge_block = light_blue_stained_glass
    
                    place(base_x + bridge_x_offset, ground_y + bridge_y, base_z + bridge_z, bridge_block)
    
                    # Bridge supports every few blocks
                    if i % 8 == 0 and abs(width_offset) == 2:
                        for support_dy in range(-5, 0):
                            place(base_x + bridge_x_offset, ground_y + bridge_y + support_dy, base_z + bridge_z, chain)
    
    
        # Build all bridges
        for start_idx, end_idx, bridge_type in bridge_connections:
            start_island = island_data[start_idx]
            end_island = island_data[end_idx]
    
            start_pos = (start_island[0], start_island[1], start_island[2] + start_island[4] // 2)
            end_pos = (end_island[0], end_island[1], end_island[2] + end_island[4] // 2)
    
            build_magical_bridge(start_pos, end_pos, bridge_type)
    
        # MAGICAL WATERFALLS falling into the void
        waterfall_positions = [
            # (x, z, start_y, fall_distance)
            (-35, -35, 65, 40),  # Northwest island
            (35, -35, 60, 35),  # Northeast island
            (-35, 35, 55, 30),  # Southwest island
            (45, 45, 70, 45),  # Southeast island
            (0, -45, 50, 25),  # North island
            (0, 50, 65, 35),  # South island
        ]
    
        for fall_x, fall_z, start_y, fall_distance in waterfall_positions:
            # Create waterfall source
            for dx in range(-2, 3):
                for dz in range(-2, 3):
                    if abs(dx) <= 1 and abs(dz) <= 1:
                        place(base_x + fall_x + dx, ground_y + start_y, base_z + fall_z + dz, water)
    
            # Waterfall stream
            for dy in range(fall_distance):
                fall_y = start_y - dy
    
                # Water stream with varying width
                stream_width = max(1, 3 - dy // 10)
                for dx in range(-stream_width, stream_width + 1):
                    for dz in range(-stream_width, stream_width + 1):
                        if abs(dx) <= stream_width and abs(dz) <= stream_width:
                            place(base_x + fall_x + dx, ground_y + fall_y, base_z + fall_z + dz, water)
    
        # FLOATING GARDENS with magical trees
        garden_islands = [2, 3, 6]  # Garden, crystal, and sanctuary islands
    
    
        def create_magical_tree(x, z, base_y, tree_type):
            tree_height = 15 + random.randint(-3, 5)
    
            # Magical trunk
            trunk_blocks = {{
                "cherry": cherry_log,
                "crystal": amethyst_block,
                "light": glowstone
            }}
    
            trunk_block = trunk_blocks.get(tree_type, oak_log)
    
            for dy in range(tree_height):
                place(base_x + x, ground_y + base_y + dy, base_z + z, trunk_block)
    
            # Magical canopy
            canopy_radius = 6
            canopy_blocks = {{
                "cherry": cherry_leaves,
                "crystal": cyan_stained_glass,
                "light": white_stained_glass
            }}
    
            canopy_block = canopy_blocks.get(tree_type, flowering_azalea_leaves)
    
            for dx in range(-canopy_radius, canopy_radius + 1):
                for dz in range(-canopy_radius, canopy_radius + 1):
                    for dy in range(5):
                        distance = math.sqrt(dx * dx + dz * dz)
                        if distance <= canopy_radius:
                            canopy_y = base_y + tree_height - 3 + dy
                            place(base_x + x + dx, ground_y + canopy_y, base_z + z + dz, canopy_block)
    
            # Magical effects around tree
            for angle in range(0, 360, 60):
                effect_x = x + int(8 * math.cos(math.radians(angle)))
                effect_z = z + int(8 * math.sin(math.radians(angle)))
                effect_y = base_y + tree_height + 2
    
                place(base_x + effect_x, ground_y + effect_y, base_z + effect_z, end_rod)
    
    
        # Plant magical trees on garden islands
        for island_idx in garden_islands:
            island = island_data[island_idx]
            island_x, island_z, island_y, radius = island[0], island[1], island[2], island[3]
    
            tree_types = ["cherry", "crystal", "light"]
            tree_type = tree_types[island_idx % 3]
    
            # Multiple trees per island
            tree_count = 8 + island_idx * 2
            for i in range(tree_count):
                angle = (360 / tree_count) * i
                tree_distance = radius * 0.6
                tree_x = island_x + int(tree_distance * math.cos(math.radians(angle)))
                tree_z = island_z + int(tree_distance * math.sin(math.radians(angle)))
    
                create_magical_tree(tree_x, tree_z, island_y + island[4] // 2 + 1, tree_type)
    
        # FLOATING RUINS AND MYSTERIOUS STRUCTURES
        ruin_positions = [
            # Scattered ruins floating independently
            (-120, -80, 80, "temple"),
            (130, -70, 40, "obelisk"),
            (-100, 110, 90, "arch"),
            (120, 95, 25, "platform"),
            (0, -120, 100, "spire"),
            (-80, -120, 60, "rings"),
        ]
    
    
        def build_floating_ruin(x, z, y, ruin_type):
            if ruin_type == "temple":
                # Ancient temple structure
                for dx in range(-8, 9):
                    for dz in range(-8, 9):
                        if abs(dx) == 8 or abs(dz) == 8:
                            for dy in range(15):
                                if dy % 4 == 0:
                                    ruin_block = chiseled_quartz
                                else:
                                    ruin_block = quartz_pillar
                                place(base_x + x + dx, ground_y + y + dy, base_z + z + dz, ruin_block)
    
                # Temple top with crystal
                place(base_x + x, ground_y + y + 15, base_z + z, sea_lantern)
    
            elif ruin_type == "obelisk":
                # Tall crystal obelisk
                obelisk_height = 25
                for dy in range(obelisk_height):
                    size = max(1, 4 - dy // 5)
                    for dx in range(-size, size + 1):
                        for dz in range(-size, size + 1):
                            if abs(dx) == size or abs(dz) == size or size == 1:
                                if dy % 5 == 0:
                                    obelisk_block = amethyst_block
                                else:
                                    obelisk_block = purple_stained_glass
                                place(base_x + x + dx, ground_y + y + dy, base_z + z + dz, obelisk_block)
    
            elif ruin_type == "arch":
                # Magical floating archway
                arch_width = 12
                arch_height = 15
    
                for dx in range(-arch_width // 2, arch_width // 2 + 1):
                    for dy in range(arch_height):
                        # Create arch shape
                        distance_from_center = abs(dx)
                        max_height_at_distance = arch_height - (distance_from_center * distance_from_center // 3)
    
                        if dy <= max_height_at_distance:
                            if dx == -arch_width // 2 or dx == arch_width // 2 or dy == max_height_at_distance:
                                place(base_x + x + dx, ground_y + y + dy, base_z + z, quartz_pillar)
                                place(base_x + x + dx, ground_y + y + dy, base_z + z + 1, quartz_pillar)
    
            elif ruin_type == "rings":
                # Floating ring structures
                ring_radius = 6
                for ring_level in range(3):
                    ring_y = y + ring_level * 8
                    for angle in range(0, 360, 15):
                        ring_x = x + int(ring_radius * math.cos(math.radians(angle)))
                        ring_z = z + int(ring_radius * math.sin(math.radians(angle)))
    
                        place(base_x + ring_x, ground_y + ring_y, base_z + ring_z, magenta_stained_glass)
    
    
        # Build all floating ruins
        for ruin_x, ruin_z, ruin_y, ruin_type in ruin_positions:
            build_floating_ruin(ruin_x, ruin_z, ruin_y, ruin_type)
    
        # MAGICAL LIGHTING SYSTEM
        light_positions = []
    
        # Palace lighting
        for dx in range(-palace_width // 2, palace_width // 2 + 1, 5):
            for dz in range(-palace_depth // 2, palace_depth // 2 + 1, 5):
                if abs(dx) == palace_width // 2 or abs(dz) == palace_depth // 2:
                    light_positions.append((palace_x + dx, palace_z + dz, palace_y + palace_height + 2))
    
        # Tower tops
        for tower_dx, tower_dz in tower_positions:
            light_positions.append((palace_x + tower_dx, palace_z + tower_dz, palace_y + palace_height + 55 + 15))
    
        # Island perimeter lighting
        for island in island_data:
            island_x, island_z, island_y, radius = island[0], island[1], island[2], island[3]
    
            for angle in range(0, 360, 30):
                light_x = island_x + int((radius + 2) * math.cos(math.radians(angle)))
                light_z = island_z + int((radius + 2) * math.sin(math.radians(angle)))
                light_y = island_y + island[4] // 2 + 3
    
                light_positions.append((light_x, light_z, light_y))
    
        # Floating light orbs in empty space
        for i in range(50):
            orb_x = random.randint(-140, 140)
            orb_z = random.randint(-140, 140)
            orb_y = random.randint(20, 120)
    
            light_positions.append((orb_x, orb_z, orb_y))
    
        # Place all magical lighting
        for light_x, light_z, light_y in light_positions:
            # Alternate between different magical light sources
            light_types = [sea_lantern, glowstone, end_rod, lantern]
            light_block = light_types[hash((light_x, light_z, light_y)) % len(light_types)]
    
            place(base_x + light_x, ground_y + light_y, base_z + light_z, light_block)
    
        # ATMOSPHERIC DETAILS - Floating particles and mystical elements
        particle_positions = []
    
        # Magical floating crystals
        for i in range(100):
            crystal_x = random.randint(-130, 130)
            crystal_z = random.randint(-130, 130)
            crystal_y = random.randint(30, 110)
    
            # Small floating crystal clusters
            place(base_x + crystal_x, ground_y + crystal_y, base_z + crystal_z, amethyst_block)
    
            # Crystal supports
            for support_dy in range(1, 4):
                if random.random() < 0.7:
                    place(base_x + crystal_x, ground_y + crystal_y - support_dy, base_z + crystal_z, purple_stained_glass)
    
        # Floating lily pads in mid-air (magical effect)
        for i in range(30):
            lily_x = random.randint(-100, 100)
            lily_z = random.randint(-100, 100)
            lily_y = random.randint(40, 90)
    
            # Magical floating platforms
            for dx in range(-2, 3):
                for dz in range(-2, 3):
                    if abs(dx) + abs(dz) <= 2:
                        place(base_x + lily_x + dx, ground_y + lily_y, base_z + lily_z + dz, cyan_stained_glass)
    
        # Save and close
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
            print(chunk.delta.text, end="", flush=True)

    return full_text