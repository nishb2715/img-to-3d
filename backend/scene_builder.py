import copy

OVERRIDES = {
    "bedroom": {
    "scene_title": "Bedroom",
    "background_color": "#0d0d1a",
    "ambient_light": {"color": "#ffffff", "intensity": 1.5},
    "directional_light": {"color": "#ffffff", "intensity": 3.0, "position": [5, 10, 5]},
    "objects": [
        {"id":"obj_1","label":"floor","type":"box",
         "position":[0,0.0,0],"rotation":[0,0,0],"scale":[12.0,0.2,9.0],
         "color":"#c8a06a","metalness":0.0,"roughness":0.8,"opacity":1.0,
         "pattern":{"type":"wood","colors":["#c8a06a","#a07848"]}},
        {"id":"obj_2","label":"bed_frame","type":"box",
         "position":[0,0.6,0],"rotation":[0,0,0],"scale":[4.5,1.0,6.5],
         "color":"#8B4513","metalness":0.0,"roughness":0.8,"opacity":1.0,
         "pattern":{"type":"wood","colors":["#8B4513","#6B3410"]}},
        {"id":"obj_3","label":"mattress","type":"box",
         "position":[0,1.25,0.3],"rotation":[0,0,0],"scale":[4.3,0.4,5.8],
         "color":"#f0ece0","metalness":0.0,"roughness":0.9,"opacity":1.0,
         "pattern":{"type":"fabric","colors":["#f0ece0","#d8d4c8"]}},
        {"id":"obj_4","label":"blanket","type":"box",
         "position":[0,1.55,0.8],"rotation":[0,0,0],"scale":[4.2,0.2,4.5],
         "color":"#b04040","metalness":0.0,"roughness":0.9,"opacity":1.0,
         "pattern":{"type":"fabric","colors":["#b04040","#8a2020"]}},
        {"id":"obj_5","label":"pillow_l","type":"box",
         "position":[-1.0,1.65,-2.2],"rotation":[0,0,0],"scale":[1.8,0.4,1.2],
         "color":"#ffffff","metalness":0.0,"roughness":0.9,"opacity":1.0,
         "pattern":{"type":"fabric","colors":["#ffffff","#e8e8e8"]}},
        {"id":"obj_6","label":"pillow_r","type":"box",
         "position":[1.0,1.65,-2.2],"rotation":[0,0,0],"scale":[1.8,0.4,1.2],
         "color":"#ffffff","metalness":0.0,"roughness":0.9,"opacity":1.0,
         "pattern":{"type":"fabric","colors":["#ffffff","#e8e8e8"]}},
        {"id":"obj_7","label":"headboard","type":"box",
         "position":[0,2.4,-3.1],"rotation":[0,0,0],"scale":[4.5,2.5,0.3],
         "color":"#8B4513","metalness":0.0,"roughness":0.8,"opacity":1.0,
         "pattern":{"type":"wood","colors":["#8B4513","#6B3410"]}},
        {"id":"obj_8","label":"sidetable_l","type":"box",
         "position":[-3.2,0.8,0],"rotation":[0,0,0],"scale":[1.2,1.4,1.2],
         "color":"#a0622a","metalness":0.0,"roughness":0.8,"opacity":1.0,
         "pattern":{"type":"wood","colors":["#a0622a","#7a4418"]}},
        {"id":"obj_9","label":"sidetable_r","type":"box",
         "position":[3.2,0.8,0],"rotation":[0,0,0],"scale":[1.2,1.4,1.2],
         "color":"#a0622a","metalness":0.0,"roughness":0.8,"opacity":1.0,
         "pattern":{"type":"wood","colors":["#a0622a","#7a4418"]}},
        {"id":"obj_10","label":"lamp_l","type":"cylinder",
         "position":[-3.2,1.9,0],"rotation":[0,0,0],"scale":[0.15,0.8,0.15],
         "color":"#cccccc","metalness":0.5,"roughness":0.3,"opacity":1.0,
         "pattern":{"type":"metal","colors":["#cccccc","#aaaaaa"]}},
        {"id":"obj_11","label":"lampshade_l","type":"cone",
         "position":[-3.2,2.5,0],"rotation":[0,0,0],"scale":[0.5,0.5,0.5],
         "color":"#ffffcc","metalness":0.0,"roughness":0.8,"opacity":1.0,
         "pattern":{"type":"solid","colors":["#ffffcc"]}}
    ],
    "camera":{"position":[0,4,10],"fov":60},
    "description":"A bedroom with bed, pillows, blanket, headboard and side tables."
},

"lamp": {
    "scene_title": "Desk Lamp",
    "background_color": "#0d0d1a",
    "ambient_light": {"color": "#ffffff", "intensity": 1.5},
    "directional_light": {"color": "#ffffff", "intensity": 3.0, "position": [5, 10, 5]},
    "objects": [
        {"id":"obj_1","label":"base","type":"cylinder",
         "position":[0,0.2,0],"rotation":[0,0,0],"scale":[1.2,0.3,1.2],
         "color":"#cccccc","metalness":0.7,"roughness":0.3,"opacity":1.0,
         "pattern":{"type":"metal","colors":["#cccccc","#aaaaaa"]}},
        {"id":"obj_2","label":"pole_lower","type":"cylinder",
         "position":[0,1.3,0],"rotation":[0,0,0],"scale":[0.12,2.0,0.12],
         "color":"#bbbbbb","metalness":0.7,"roughness":0.3,"opacity":1.0,
         "pattern":{"type":"metal","colors":["#bbbbbb","#999999"]}},
        {"id":"obj_3","label":"arm","type":"box",
         "position":[0.6,2.4,0],"rotation":[0,0,0.4],"scale":[1.2,0.1,0.1],
         "color":"#bbbbbb","metalness":0.7,"roughness":0.3,"opacity":1.0,
         "pattern":{"type":"metal","colors":["#bbbbbb","#999999"]}},
        {"id":"obj_4","label":"shade","type":"cone",
         "position":[1.2,2.1,0],"rotation":[0,0,-0.5],"scale":[0.9,1.0,0.9],
         "color":"#f0f0e0","metalness":0.0,"roughness":0.7,"opacity":1.0,
         "pattern":{"type":"solid","colors":["#f0f0e0"]}},
        {"id":"obj_5","label":"bulb","type":"sphere",
         "position":[1.2,2.0,0],"rotation":[0,0,0],"scale":[0.3,0.3,0.3],
         "color":"#ffffaa","metalness":0.0,"roughness":0.3,"opacity":0.9,
         "pattern":{"type":"solid","colors":["#ffffaa"]}}
    ],
    "camera":{"position":[0,3,8],"fov":55},
    "description":"A desk lamp with base, pole, arm and shade."
},

"side_table": {
    "scene_title": "Side Table",
    "background_color": "#0d0d1a",
    "ambient_light": {"color": "#ffffff", "intensity": 1.5},
    "directional_light": {"color": "#ffffff", "intensity": 3.0, "position": [5, 10, 5]},
    "objects": [
        {"id":"obj_1","label":"tabletop","type":"cylinder",
         "position":[0,2.6,0],"rotation":[0,0,0],"scale":[3.0,0.15,3.0],
         "color":"#f0f0f0","metalness":0.1,"roughness":0.4,"opacity":1.0,
         "pattern":{"type":"solid","colors":["#f0f0f0"]}},
        {"id":"obj_2","label":"leg_fl","type":"cylinder",
         "position":[-0.9,1.3,0.9],"rotation":[0.15,0,-0.15],"scale":[0.12,2.6,0.12],
         "color":"#c8a06a","metalness":0.0,"roughness":0.7,"opacity":1.0,
         "pattern":{"type":"wood","colors":["#c8a06a","#a07848"]}},
        {"id":"obj_3","label":"leg_fr","type":"cylinder",
         "position":[0.9,1.3,0.9],"rotation":[0.15,0,0.15],"scale":[0.12,2.6,0.12],
         "color":"#c8a06a","metalness":0.0,"roughness":0.7,"opacity":1.0,
         "pattern":{"type":"wood","colors":["#c8a06a","#a07848"]}},
        {"id":"obj_4","label":"leg_bl","type":"cylinder",
         "position":[-0.9,1.3,-0.9],"rotation":[-0.15,0,-0.15],"scale":[0.12,2.6,0.12],
         "color":"#c8a06a","metalness":0.0,"roughness":0.7,"opacity":1.0,
         "pattern":{"type":"wood","colors":["#c8a06a","#a07848"]}},
        {"id":"obj_5","label":"leg_br","type":"cylinder",
         "position":[0.9,1.3,-0.9],"rotation":[-0.15,0,0.15],"scale":[0.12,2.6,0.12],
         "color":"#c8a06a","metalness":0.0,"roughness":0.7,"opacity":1.0,
         "pattern":{"type":"wood","colors":["#c8a06a","#a07848"]}}
    ],
    "camera":{"position":[0,3,8],"fov":55},
    "description":"A round side table with angled wooden legs."
},

"bookshelf": {
    "scene_title": "Bookshelf",
    "background_color": "#0d0d1a",
    "ambient_light": {"color": "#ffffff", "intensity": 1.5},
    "directional_light": {"color": "#ffffff", "intensity": 3.0, "position": [5, 10, 5]},
    "objects": [
        {"id":"obj_1","label":"back_panel","type":"box",
         "position":[0,4.0,-0.4],"rotation":[0,0,0],"scale":[5.0,8.0,0.15],
         "color":"#c8863c","metalness":0.0,"roughness":0.8,"opacity":1.0,
         "pattern":{"type":"wood","colors":["#c8863c","#a0622a"]}},
        {"id":"obj_2","label":"left_side","type":"box",
         "position":[-2.45,4.0,0.2],"rotation":[0,0,0],"scale":[0.15,8.0,1.2],
         "color":"#c8863c","metalness":0.0,"roughness":0.8,"opacity":1.0,
         "pattern":{"type":"wood","colors":["#c8863c","#a0622a"]}},
        {"id":"obj_3","label":"right_side","type":"box",
         "position":[2.45,4.0,0.2],"rotation":[0,0,0],"scale":[0.15,8.0,1.2],
         "color":"#c8863c","metalness":0.0,"roughness":0.8,"opacity":1.0,
         "pattern":{"type":"wood","colors":["#c8863c","#a0622a"]}},
        {"id":"obj_4","label":"shelf_bottom","type":"box",
         "position":[0,0.2,0.2],"rotation":[0,0,0],"scale":[5.0,0.15,1.2],
         "color":"#c8863c","metalness":0.0,"roughness":0.8,"opacity":1.0,
         "pattern":{"type":"wood","colors":["#c8863c","#a0622a"]}},
        {"id":"obj_5","label":"shelf_mid1","type":"box",
         "position":[0,2.6,0.2],"rotation":[0,0,0],"scale":[5.0,0.15,1.2],
         "color":"#c8863c","metalness":0.0,"roughness":0.8,"opacity":1.0,
         "pattern":{"type":"wood","colors":["#c8863c","#a0622a"]}},
        {"id":"obj_6","label":"shelf_mid2","type":"box",
         "position":[0,5.2,0.2],"rotation":[0,0,0],"scale":[5.0,0.15,1.2],
         "color":"#c8863c","metalness":0.0,"roughness":0.8,"opacity":1.0,
         "pattern":{"type":"wood","colors":["#c8863c","#a0622a"]}},
        {"id":"obj_7","label":"shelf_top","type":"box",
         "position":[0,7.9,0.2],"rotation":[0,0,0],"scale":[5.0,0.15,1.2],
         "color":"#c8863c","metalness":0.0,"roughness":0.8,"opacity":1.0,
         "pattern":{"type":"wood","colors":["#c8863c","#a0622a"]}},
        {"id":"obj_8","label":"books_row1","type":"box",
         "position":[0,1.4,0.1],"rotation":[0,0,0],"scale":[4.6,2.2,0.8],
         "color":"#4466aa","metalness":0.0,"roughness":0.7,"opacity":1.0,
         "pattern":{"type":"stripes","colors":["#4466aa","#cc4444"]}},
        {"id":"obj_9","label":"books_row2","type":"box",
         "position":[0,3.9,0.1],"rotation":[0,0,0],"scale":[4.6,2.4,0.8],
         "color":"#448844","metalness":0.0,"roughness":0.7,"opacity":1.0,
         "pattern":{"type":"stripes","colors":["#448844","#884488"]}},
        {"id":"obj_10","label":"books_row3","type":"box",
         "position":[0,6.5,0.1],"rotation":[0,0,0],"scale":[4.6,2.2,0.8],
         "color":"#aa7722","metalness":0.0,"roughness":0.7,"opacity":1.0,
         "pattern":{"type":"stripes","colors":["#aa7722","#226688"]}}
    ],
    "camera":{"position":[0,4,10],"fov":60},
    "description":"A wooden bookshelf with three shelves filled with colorful books."
},

"plant": {
    "scene_title": "Potted Plant",
    "background_color": "#0d0d1a",
    "ambient_light": {"color": "#ffffff", "intensity": 1.5},
    "directional_light": {"color": "#ffffff", "intensity": 3.0, "position": [5, 10, 5]},
    "objects": [
        {"id":"obj_1","label":"pot","type":"cylinder",
         "position":[0,0.8,0],"rotation":[0,0,0],"scale":[1.8,1.5,1.8],
         "color":"#ffffff","metalness":0.1,"roughness":0.5,"opacity":1.0,
         "pattern":{"type":"solid","colors":["#ffffff"]}},
        {"id":"obj_2","label":"soil","type":"cylinder",
         "position":[0,1.55,0],"rotation":[0,0,0],"scale":[1.7,0.15,1.7],
         "color":"#3d2010","metalness":0.0,"roughness":1.0,"opacity":1.0,
         "pattern":{"type":"solid","colors":["#3d2010"]}},
        {"id":"obj_3","label":"foliage_main","type":"sphere",
         "position":[0,3.2,0],"rotation":[0,0,0],"scale":[2.8,2.2,2.8],
         "color":"#2d8a2d","metalness":0.0,"roughness":0.9,"opacity":1.0,
         "pattern":{"type":"dots","colors":["#2d8a2d","#1a6b1a"]}},
        {"id":"obj_4","label":"foliage_left","type":"sphere",
         "position":[-1.3,2.8,0.3],"rotation":[0,0,0],"scale":[1.6,1.4,1.5],
         "color":"#2a8020","metalness":0.0,"roughness":0.9,"opacity":1.0,
         "pattern":{"type":"dots","colors":["#2a8020","#186018"]}},
        {"id":"obj_5","label":"foliage_right","type":"sphere",
         "position":[1.3,2.8,0.3],"rotation":[0,0,0],"scale":[1.6,1.4,1.5],
         "color":"#2a8020","metalness":0.0,"roughness":0.9,"opacity":1.0,
         "pattern":{"type":"dots","colors":["#2a8020","#186018"]}},
        {"id":"obj_6","label":"foliage_back","type":"sphere",
         "position":[0,3.0,-0.8],"rotation":[0,0,0],"scale":[1.8,1.6,1.4],
         "color":"#228022","metalness":0.0,"roughness":0.9,"opacity":1.0,
         "pattern":{"type":"dots","colors":["#228022","#145014"]}}
    ],
    "camera":{"position":[0,3,8],"fov":55},
    "description":"A round white pot with lush green foliage."
},
    "football": {
        "scene_title": "Football",
        "background_color": "#0d0d1a",
        "ambient_light": {"color": "#ffffff", "intensity": 1.5},
        "directional_light": {"color": "#ffffff", "intensity": 3.0, "position": [5, 10, 5]},
        "objects": [{"id":"obj_1","label":"ball","type":"sphere",
            "position":[0,1.5,0],"rotation":[0,0,0],"scale":[3.0,3.0,3.0],
            "color":"#ffffff","metalness":0.0,"roughness":0.4,"opacity":1.0,
            "pattern":{"type":"football","colors":["#111111","#ffffff"]}}],
        "camera":{"position":[0,3,8],"fov":55},
        "description":"A black and white football."
    },
    "basketball": {
        "scene_title": "Basketball",
        "background_color": "#0d0d1a",
        "ambient_light": {"color": "#ffffff", "intensity": 1.5},
        "directional_light": {"color": "#ffffff", "intensity": 3.0, "position": [5, 10, 5]},
        "objects": [{"id":"obj_1","label":"ball","type":"sphere",
            "position":[0,1.5,0],"rotation":[0,0,0],"scale":[3.0,3.0,3.0],
            "color":"#e8671b","metalness":0.0,"roughness":0.5,"opacity":1.0,
            "pattern":{"type":"basketball","colors":["#e8671b","#111111"]}}],
        "camera":{"position":[0,3,8],"fov":55},
        "description":"An orange basketball."
    },
    "tennis": {
        "scene_title": "Tennis Ball",
        "background_color": "#0d0d1a",
        "ambient_light": {"color": "#ffffff", "intensity": 1.5},
        "directional_light": {"color": "#ffffff", "intensity": 3.0, "position": [5, 10, 5]},
        "objects": [{"id":"obj_1","label":"ball","type":"sphere",
            "position":[0,1.5,0],"rotation":[0,0,0],"scale":[3.0,3.0,3.0],
            "color":"#ccff00","metalness":0.0,"roughness":0.6,"opacity":1.0,
            "pattern":{"type":"tennis","colors":["#ccff00","#ffffff"]}}],
        "camera":{"position":[0,3,8],"fov":55},
        "description":"A yellow-green tennis ball."
    },
    "car": {
        "scene_title": "Car",
        "background_color": "#0d0d1a",
        "ambient_light": {"color": "#ffffff", "intensity": 1.5},
        "directional_light": {"color": "#ffffff", "intensity": 3.0, "position": [5, 10, 5]},
        "objects": [
            {"id":"obj_1","label":"body","type":"box",
             "position":[0,0.8,0],"rotation":[0,0,0],"scale":[5.5,1.6,2.5],
             "color":"#2255cc","metalness":0.3,"roughness":0.4,"opacity":1.0,
             "pattern":{"type":"solid","colors":["#2255cc"]}},
            {"id":"obj_2","label":"cabin","type":"box",
             "position":[0.2,2.0,0],"rotation":[0,0,0],"scale":[3.0,1.2,2.3],
             "color":"#1a44aa","metalness":0.3,"roughness":0.4,"opacity":1.0,
             "pattern":{"type":"solid","colors":["#1a44aa"]}},
            {"id":"obj_3","label":"windshield","type":"box",
             "position":[1.2,2.0,1.16],"rotation":[0,0,0],"scale":[1.8,1.1,0.1],
             "color":"#88aaff","metalness":0.0,"roughness":0.1,"opacity":0.6,
             "pattern":{"type":"glass","colors":["#88aaff"]}},
            {"id":"obj_4","label":"wheel_fl","type":"cylinder",
             "position":[-1.8,0.4,1.35],"rotation":[1.5708,0,0],"scale":[0.8,0.5,0.8],
             "color":"#111111","metalness":0.0,"roughness":0.9,"opacity":1.0,
             "pattern":{"type":"wheel","colors":["#111111","#888888"]}},
            {"id":"obj_5","label":"wheel_fr","type":"cylinder",
             "position":[-1.8,0.4,-1.35],"rotation":[1.5708,0,0],"scale":[0.8,0.5,0.8],
             "color":"#111111","metalness":0.0,"roughness":0.9,"opacity":1.0,
             "pattern":{"type":"wheel","colors":["#111111","#888888"]}},
            {"id":"obj_6","label":"wheel_rl","type":"cylinder",
             "position":[1.8,0.4,1.35],"rotation":[1.5708,0,0],"scale":[0.8,0.5,0.8],
             "color":"#111111","metalness":0.0,"roughness":0.9,"opacity":1.0,
             "pattern":{"type":"wheel","colors":["#111111","#888888"]}},
            {"id":"obj_7","label":"wheel_rr","type":"cylinder",
             "position":[1.8,0.4,-1.35],"rotation":[1.5708,0,0],"scale":[0.8,0.5,0.8],
             "color":"#111111","metalness":0.0,"roughness":0.9,"opacity":1.0,
             "pattern":{"type":"wheel","colors":["#111111","#888888"]}}
        ],
        "camera":{"position":[0,3,8],"fov":55},
        "description":"A car with four wheels."
    },
    "building": {
        "scene_title": "Building",
        "background_color": "#0d0d1a",
        "ambient_light": {"color": "#ffffff", "intensity": 1.5},
        "directional_light": {"color": "#ffffff", "intensity": 3.0, "position": [5, 10, 5]},
        "objects": [
            {"id":"obj_1","label":"main_tower","type":"box",
             "position":[0,4.0,0],"rotation":[0,0,0],"scale":[4.0,8.0,4.0],
             "color":"#4488aa","metalness":0.2,"roughness":0.5,"opacity":1.0,
             "pattern":{"type":"windows","colors":["#4488aa","#87CEEB"]}},
            {"id":"obj_2","label":"top_slab","type":"box",
             "position":[0,8.3,0],"rotation":[0,0,0],"scale":[4.4,0.3,4.4],
             "color":"#cccccc","metalness":0.0,"roughness":0.6,"opacity":1.0,
             "pattern":{"type":"solid","colors":["#cccccc"]}},
            {"id":"obj_3","label":"base","type":"box",
             "position":[0,0.15,0],"rotation":[0,0,0],"scale":[4.8,0.3,4.8],
             "color":"#aaaaaa","metalness":0.0,"roughness":0.7,"opacity":1.0,
             "pattern":{"type":"solid","colors":["#aaaaaa"]}}
        ],
        "camera":{"position":[0,5,12],"fov":55},
        "description":"A modern multi-story building."
    },
    "house": {
        "scene_title": "House",
        "background_color": "#0d0d1a",
        "ambient_light": {"color": "#ffffff", "intensity": 1.5},
        "directional_light": {"color": "#ffffff", "intensity": 3.0, "position": [5, 10, 5]},
        "objects": [
            {"id":"obj_1","label":"walls","type":"box",
             "position":[0,2.0,0],"rotation":[0,0,0],"scale":[5.0,4.0,4.0],
             "color":"#f5f0e8","metalness":0.0,"roughness":0.8,"opacity":1.0,
             "pattern":{"type":"solid","colors":["#f5f0e8"]}},
            {"id":"obj_2","label":"roof","type":"box",
             "position":[0,5.0,0],"rotation":[0,0,0],"scale":[5.8,1.8,4.8],
             "color":"#8B5E3C","metalness":0.0,"roughness":0.8,"opacity":1.0,
             "pattern":{"type":"wood","colors":["#8B5E3C","#6B3E1C"]}},
            {"id":"obj_3","label":"door","type":"box",
             "position":[0,0.9,2.01],"rotation":[0,0,0],"scale":[0.9,1.8,0.1],
             "color":"#5C3317","metalness":0.0,"roughness":0.9,"opacity":1.0,
             "pattern":{"type":"wood","colors":["#5C3317","#3d2010"]}},
            {"id":"obj_4","label":"window_l","type":"box",
             "position":[-1.5,2.5,2.01],"rotation":[0,0,0],"scale":[1.0,1.0,0.1],
             "color":"#87CEEB","metalness":0.0,"roughness":0.1,"opacity":0.7,
             "pattern":{"type":"glass","colors":["#87CEEB"]}},
            {"id":"obj_5","label":"window_r","type":"box",
             "position":[1.5,2.5,2.01],"rotation":[0,0,0],"scale":[1.0,1.0,0.1],
             "color":"#87CEEB","metalness":0.0,"roughness":0.1,"opacity":0.7,
             "pattern":{"type":"glass","colors":["#87CEEB"]}},
            {"id":"obj_6","label":"chimney","type":"box",
             "position":[1.5,6.2,-0.5],"rotation":[0,0,0],"scale":[0.6,1.5,0.6],
             "color":"#888888","metalness":0.0,"roughness":0.8,"opacity":1.0,
             "pattern":{"type":"brick","colors":["#888888","#666666"]}}
        ],
        "camera":{"position":[0,3,10],"fov":55},
        "description":"A small house with roof, door, windows and chimney."
    },
    "dog": {
        "scene_title": "Dog",
        "background_color": "#0d0d1a",
        "ambient_light": {"color": "#ffffff", "intensity": 1.5},
        "directional_light": {"color": "#ffffff", "intensity": 3.0, "position": [5, 10, 5]},
        "objects": [
            {"id":"obj_1","label":"body","type":"sphere",
             "position":[0,1.8,0],"rotation":[0,0,0],"scale":[2.5,2.2,2.0],
             "color":"#d4a96a","metalness":0.0,"roughness":0.8,"opacity":1.0,
             "pattern":{"type":"fur","colors":["#d4a96a","#b07830"]}},
            {"id":"obj_2","label":"head","type":"sphere",
             "position":[0,3.5,0.5],"rotation":[0,0,0],"scale":[1.8,1.8,1.8],
             "color":"#d4a96a","metalness":0.0,"roughness":0.8,"opacity":1.0,
             "pattern":{"type":"fur","colors":["#d4a96a","#b07830"]}},
            {"id":"obj_3","label":"snout","type":"sphere",
             "position":[0,3.1,1.4],"rotation":[0,0,0],"scale":[0.9,0.7,0.8],
             "color":"#c49050","metalness":0.0,"roughness":0.8,"opacity":1.0,
             "pattern":{"type":"solid","colors":["#c49050"]}},
            {"id":"obj_4","label":"ear_l","type":"box",
             "position":[-0.75,4.0,0.1],"rotation":[0.1,0,0.2],"scale":[0.5,0.9,0.2],
             "color":"#b07830","metalness":0.0,"roughness":0.8,"opacity":1.0,
             "pattern":{"type":"fur","colors":["#b07830","#8a5c20"]}},
            {"id":"obj_5","label":"ear_r","type":"box",
             "position":[0.75,4.0,0.1],"rotation":[0.1,0,-0.2],"scale":[0.5,0.9,0.2],
             "color":"#b07830","metalness":0.0,"roughness":0.8,"opacity":1.0,
             "pattern":{"type":"fur","colors":["#b07830","#8a5c20"]}},
            {"id":"obj_6","label":"paw_l","type":"sphere",
             "position":[-0.7,0.5,1.2],"rotation":[0,0,0],"scale":[0.7,0.4,0.9],
             "color":"#c49050","metalness":0.0,"roughness":0.8,"opacity":1.0,
             "pattern":{"type":"solid","colors":["#c49050"]}},
            {"id":"obj_7","label":"paw_r","type":"sphere",
             "position":[0.7,0.5,1.2],"rotation":[0,0,0],"scale":[0.7,0.4,0.9],
             "color":"#c49050","metalness":0.0,"roughness":0.8,"opacity":1.0,
             "pattern":{"type":"solid","colors":["#c49050"]}}
        ],
        "camera":{"position":[0,3,8],"fov":55},
        "description":"A sitting dog made of geometric primitives."
    },
    "chair": {
        "scene_title": "Chair",
        "background_color": "#0d0d1a",
        "ambient_light": {"color": "#ffffff", "intensity": 1.5},
        "directional_light": {"color": "#ffffff", "intensity": 3.0, "position": [5, 10, 5]},
        "objects": [
            {"id":"obj_1","label":"seat","type":"box",
             "position":[0,1.0,0],"rotation":[0,0,0],"scale":[2.5,0.25,2.5],
             "color":"#c87941","metalness":0.0,"roughness":0.7,"opacity":1.0,
             "pattern":{"type":"solid","colors":["#c87941"]}},
            {"id":"obj_2","label":"backrest","type":"box",
             "position":[0,2.5,-1.1],"rotation":[0,0,0],"scale":[2.5,2.5,0.2],
             "color":"#8B4513","metalness":0.0,"roughness":0.8,"opacity":1.0,
             "pattern":{"type":"wood","colors":["#8B4513","#6B3410"]}},
            {"id":"obj_3","label":"leg_fl","type":"cylinder",
             "position":[-1.0,0.4,1.0],"rotation":[0,0,0],"scale":[0.2,0.8,0.2],
             "color":"#8B4513","metalness":0.0,"roughness":0.8,"opacity":1.0,
             "pattern":{"type":"wood","colors":["#8B4513","#6B3410"]}},
            {"id":"obj_4","label":"leg_fr","type":"cylinder",
             "position":[1.0,0.4,1.0],"rotation":[0,0,0],"scale":[0.2,0.8,0.2],
             "color":"#8B4513","metalness":0.0,"roughness":0.8,"opacity":1.0,
             "pattern":{"type":"wood","colors":["#8B4513","#6B3410"]}},
            {"id":"obj_5","label":"leg_bl","type":"cylinder",
             "position":[-1.0,0.4,-1.0],"rotation":[0,0,0],"scale":[0.2,0.8,0.2],
             "color":"#8B4513","metalness":0.0,"roughness":0.8,"opacity":1.0,
             "pattern":{"type":"wood","colors":["#8B4513","#6B3410"]}},
            {"id":"obj_6","label":"leg_br","type":"cylinder",
             "position":[1.0,0.4,-1.0],"rotation":[0,0,0],"scale":[0.2,0.8,0.2],
             "color":"#8B4513","metalness":0.0,"roughness":0.8,"opacity":1.0,
             "pattern":{"type":"wood","colors":["#8B4513","#6B3410"]}}
        ],
        "camera":{"position":[0,3,8],"fov":55},
        "description":"A wooden chair with seat, backrest and four legs."
    }
}

KEYWORD_MAP = {
    "football":   ["football", "soccer ball", "soccer"],
    "basketball": ["basketball"],
    "tennis":     ["tennis ball", "tennis"],
    "car":        ["car", "suv", "vehicle", "automobile", "sedan", "hatchback", "truck"],
    "building":   ["building", "skyscraper", "tower", "apartment", "office block"],
    "house":      ["house", "home", "cottage", "bungalow", "cabin"],
    "dog":        ["dog", "pug", "puppy", "canine", "labrador", "bulldog", "retriever"],
    "chair":      ["chair", "stool"],
    "bedroom":    ["bedroom", "bed room", "sleeping room"],
    "lamp":       ["lamp", "desk lamp", "floor lamp", "light fixture", "table lamp"],
    "side_table": ["side table", "end table", "nightstand", "accent table", "coffee table"],
    "bookshelf":  ["bookshelf", "bookcase", "shelf", "shelving", "book shelf"],
    "plant":      ["plant", "potted plant", "flower pot", "houseplant", "pot"],
}


def detect_override(scene: dict) -> str | None:
    title = (scene.get("scene_title", "") + " " + scene.get("description", "")).lower()
    labels = " ".join(o.get("label", "") for o in scene.get("objects", [])).lower()
    text = title + " " + labels
    for key, keywords in KEYWORD_MAP.items():
        if any(kw in text for kw in keywords):
            return key
    return None


def apply_color_from_scene(override: dict, original: dict) -> dict:
    """Only steal dominant color for car."""
    if override["scene_title"] == "Car":
        try:
            ai_color = original["objects"][0].get("color", None)
            if ai_color and ai_color not in ("#ffffff", "#000000", "#111111", "#0d0d1a"):
                override["objects"][0]["color"] = ai_color
                override["objects"][0]["pattern"]["colors"][0] = ai_color
        except Exception:
            pass
    return override


def validate_and_clean_scene(scene: dict) -> dict:
    override_key = detect_override(scene)
    if override_key:
        result = copy.deepcopy(OVERRIDES[override_key])
        result = apply_color_from_scene(result, scene)
        return result

    valid_types = {"box", "sphere", "cylinder", "cone", "torus", "plane"}
    objects = scene.get("objects", [])
    if not objects:
        return scene

    for obj in objects:
        obj["type"] = obj.get("type", "box") if obj.get("type") in valid_types else "box"
        obj["opacity"]   = max(0.1, min(1.0, obj.get("opacity", 1.0)))
        obj["metalness"] = max(0.0, min(1.0, obj.get("metalness", 0.0)))
        obj["roughness"] = max(0.0, min(1.0, obj.get("roughness", 0.6)))

        for key in ["position", "rotation", "scale"]:
            val = obj.get(key, [0, 0, 0])
            obj[key] = val if isinstance(val, list) and len(val) == 3 else [0, 0, 0]

        obj["scale"] = [max(0.3, min(8.0, s)) for s in obj["scale"]]

        if not obj.get("pattern"):
            obj["pattern"] = {"type": "solid"}

    # Auto-center
    positions = [o["position"] for o in objects]
    cx = sum(p[0] for p in positions) / len(positions)
    cy = min(p[1] for p in positions)
    cz = sum(p[2] for p in positions) / len(positions)

    for obj in objects:
        obj["position"][0] = round(obj["position"][0] - cx, 3)
        obj["position"][1] = round(obj["position"][1] - cy, 3)
        obj["position"][2] = round(obj["position"][2] - cz, 3)

    for obj in objects:
        obj["position"] = [
            max(-8, min(8,  obj["position"][0])),
            max(0,  min(15, obj["position"][1])),
            max(-8, min(8,  obj["position"][2]))
        ]

    scene["background_color"] = "#0d0d1a"
    scene["camera"] = {"position": [0, 3, 8], "fov": 55}
    return scene