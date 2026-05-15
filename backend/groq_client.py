import os, json, base64, logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a 3D scene analyst. Convert the main object in the image into a detailed 3D representation using geometric primitives for Three.js.

GOLDEN RULE: Every part must be positioned relative to a shared center at [0,0,0]. Parts must be CONNECTED — no floating parts, no gaps larger than the part itself.

CORRECT EXAMPLES (study the positions carefully):

=== CHAIR ===
- seat:      box,      pos [0, 1.0, 0],      scale [2.5, 0.2, 2.5], color #c87941, pattern solid
- backrest:  box,      pos [0, 2.5, -1.1],   scale [2.5, 2.5, 0.2], color #8B4513, pattern wood
- leg_fl:    cylinder, pos [-1.0, 0.4, 1.0], scale [0.2, 0.8, 0.2], color #8B4513, pattern wood
- leg_fr:    cylinder, pos [1.0, 0.4, 1.0],  scale [0.2, 0.8, 0.2], color #8B4513, pattern wood
- leg_bl:    cylinder, pos [-1.0, 0.4, -1.0],scale [0.2, 0.8, 0.2], color #8B4513, pattern wood
- leg_br:    cylinder, pos [1.0, 0.4, -1.0], scale [0.2, 0.8, 0.2], color #8B4513, pattern wood

=== HOUSE ===
- walls:     box,      pos [0, 2.0, 0],      scale [5.0, 4.0, 4.0], color #f5f0e8, pattern solid
- roof:      box,      pos [0, 4.8, 0],      scale [5.5, 1.5, 4.5], rotation [0,0,0.2], color #8B4513, pattern stripes
- door:      box,      pos [0, 0.9, 2.01],   scale [0.8, 1.8, 0.1], color #5C3317, pattern wood
- window_l:  box,      pos [-1.5, 2.2, 2.01],scale [1.0, 1.0, 0.1], color #87CEEB, pattern glass
- window_r:  box,      pos [1.5, 2.2, 2.01], scale [1.0, 1.0, 0.1], color #87CEEB, pattern glass
- chimney:   box,      pos [1.5, 5.5, -0.5], scale [0.6, 1.5, 0.6], color #888888, pattern brick

=== DOG (sitting) ===
- body:      sphere,   pos [0, 1.8, 0],      scale [2.5, 2.2, 2.0], color #d4a96a, pattern fur
- head:      sphere,   pos [0, 3.5, 0.6],    scale [1.8, 1.8, 1.8], color #d4a96a, pattern fur
- snout:     sphere,   pos [0, 3.2, 1.5],    scale [0.8, 0.6, 0.8], color #c49050, pattern solid
- ear_l:     box,      pos [-0.8, 4.2, 0.3], scale [0.5, 0.9, 0.2], rotation [0.2,0,0.3], color #b07830, pattern fur
- ear_r:     box,      pos [0.8, 4.2, 0.3],  scale [0.5, 0.9, 0.2], rotation [0.2,0,-0.3], color #b07830, pattern fur
- paw_l:     sphere,   pos [-0.7, 0.4, 1.0], scale [0.7, 0.4, 0.9], color #c49050, pattern solid
- paw_r:     sphere,   pos [0.7, 0.4, 1.0],  scale [0.7, 0.4, 0.9], color #c49050, pattern solid

=== CAR ===
- body:      box,      pos [0, 0.8, 0],      scale [5.5, 1.6, 2.5], color from image, pattern solid
- cabin:     box,      pos [0.2, 2.0, 0],    scale [3.0, 1.2, 2.3], color slightly darker, pattern solid
- windshield:box,      pos [1.2, 2.0, 1.16], scale [1.8, 1.1, 0.1], color #88aaff, pattern glass
- wheel_fl:  cylinder, pos [-1.8, 0.4, 1.35],scale [0.8, 0.5, 0.8], rotation [1.5708,0,0], color #111111, pattern wheel
- wheel_fr:  cylinder, pos [-1.8, 0.4,-1.35],scale [0.8, 0.5, 0.8], rotation [1.5708,0,0], color #111111, pattern wheel
- wheel_rl:  cylinder, pos [1.8, 0.4, 1.35], scale [0.8, 0.5, 0.8], rotation [1.5708,0,0], color #111111, pattern wheel
- wheel_rr:  cylinder, pos [1.8, 0.4,-1.35], scale [0.8, 0.5, 0.8], rotation [1.5708,0,0], color #111111, pattern wheel

=== CARDBOARD BOX ===
- main_body: box,      pos [0, 1.5, 0],      scale [3.0, 3.0, 3.0], color #c8863c, pattern solid
- flap_top_f:box,      pos [0, 3.05, 0.76],  scale [3.0, 0.1, 1.5], rotation [0.3,0,0], color #b87030, pattern solid
- flap_top_b:box,      pos [0, 3.05,-0.76],  scale [3.0, 0.1, 1.5], rotation [-0.3,0,0], color #b87030, pattern solid
- tape:      box,      pos [0, 3.1, 0],      scale [0.3, 0.15, 3.1], color #ddcc88, pattern solid
- tape_h:    box,      pos [0, 3.1, 0],      scale [3.1, 0.15, 0.3], color #ddcc88, pattern solid

=== BOTTLE ===
- body:      cylinder, pos [0, 2.25, 0],     scale [1.5, 4.5, 1.5], color from image, pattern metal
- shoulder:  cylinder, pos [0, 4.7, 0],      scale [1.0, 0.8, 1.0], color from image, pattern solid
- neck:      cylinder, pos [0, 5.3, 0],      scale [0.6, 0.8, 0.6], color from image, pattern solid
- cap:       cylinder, pos [0, 5.8, 0],      scale [0.7, 0.4, 0.7], color #222222, pattern ridged
- label:     box,      pos [0, 2.25, 0.78],  scale [1.4, 2.0, 0.05], color #ffffff, pattern label

=== BUILDING ===
- main:      box,      pos [0, 4.0, 0],      scale [4.0, 8.0, 4.0], color from image, pattern windows
- top_slab:  box,      pos [0, 8.3, 0],      scale [4.4, 0.3, 4.4], color #cccccc, pattern solid
- base:      box,      pos [0, 0.15, 0],     scale [4.8, 0.3, 4.8], color #aaaaaa, pattern solid

=== BEDROOM ===
- floor:     box,      pos [0, -0.1, 0],     scale [10.0, 0.2, 8.0], color #c8a06a, pattern wood
- bed_base:  box,      pos [0, 0.6, 0],      scale [4.5, 1.0, 6.5], color #8B4513, pattern wood
- mattress:  box,      pos [0, 1.2, 0.3],    scale [4.3, 0.4, 5.8], color #f0f0f0, pattern fabric
- blanket:   box,      pos [0, 1.5, 0.8],    scale [4.2, 0.2, 4.5], color #c06060, pattern fabric
- pillow_l:  box,      pos [-1.0, 1.7,-2.2], scale [1.8, 0.4, 1.2], color #ffffff, pattern fabric
- pillow_r:  box,      pos [1.0, 1.7,-2.2],  scale [1.8, 0.4, 1.2], color #ffffff, pattern fabric
- headboard: box,      pos [0, 2.2, -3.1],   scale [4.5, 2.2, 0.3], color #8B4513, pattern wood

NOW analyze the uploaded image carefully. Identify the object. Apply the same part-by-part logic.

STRICT POSITIONING RULES:
1. All parts share center near [0, y, 0] — no part at x>6 or z>6
2. Parts must TOUCH neighbors — no gaps
3. Legs/base: y = half their height
4. Stacked parts: y = bottom_part_y + (bottom_scale_y/2) + (own_scale_y/2)
5. ALL car wheels: rotation [1.5708, 0, 0], y=0.4
6. Building: ONLY stack vertically, all x=0 z=0
7. Ball objects (football/soccer/basketball/tennis): ONE sphere only, correct pattern
8. Sample EXACT colors from the image

AVAILABLE PATTERN TYPES: solid, football, basketball, tennis, wood, fur, fabric, glass, wheel, windows, ridged, label, metal, brick, stripes, dots, checker

Return ONLY valid JSON (no markdown):
{
  "scene_title": "Short title",
  "background_color": "#0d0d1a",
  "ambient_light": {"color": "#ffffff", "intensity": 1.5},
  "directional_light": {"color": "#ffffff", "intensity": 3.0, "position": [5, 10, 5]},
  "objects": [
    {
      "id": "obj_1",
      "label": "part name",
      "type": "box|sphere|cylinder|cone|torus|plane",
      "position": [x, y, z],
      "rotation": [rx, ry, rz],
      "scale": [sx, sy, sz],
      "color": "#hexcolor",
      "metalness": 0.0,
      "roughness": 0.6,
      "opacity": 1.0,
      "pattern": {"type": "pattern_type", "colors": ["#hex1", "#hex2"]}
    }
  ],
  "camera": {"position": [0, 3, 8], "fov": 55},
  "description": "One sentence description"
}"""

def analyze_image_to_3d(image_bytes: bytes, mime_type: str, detail_level: str = "medium") -> dict:
    detail_instruction = {
        "low": "Use 2-4 objects, simple shapes only.",
        "medium": "Use 4-7 objects following the examples exactly.",
        "high": "Use 6-10 objects with maximum part detail and accurate colors."
    }.get(detail_level, "Use 4-7 objects.")

    b64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT + f"\nDetail level: {detail_instruction}"},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{b64}"}},
                {"type": "text", "text": "Analyze this image carefully. What is the main object? Now reconstruct it part by part following the positioning rules. Return JSON only."}
            ]}
        ],
        max_tokens=2500
    )

    raw = response.choices[0].message.content.strip()
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw.strip())