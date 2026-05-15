import logging
import os
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq_client import analyze_image_to_3d
from scene_builder import validate_and_clean_scene

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = FastAPI(title="Image-to-3D API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}

@app.get("/health")
def health():
    return {"status": "ok", "model": "groq/llama-4-scout"}

@app.post("/api/generate-3d")
async def generate_3d(
    file: UploadFile = File(...),
    detail_level: str = Form(default="medium")
):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")
    if detail_level not in ("low", "medium", "high"):
        detail_level = "medium"
    try:
        image_bytes = await file.read()
        if len(image_bytes) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image too large. Max 10MB.")
        logger.info(f"Processing image: {file.filename}, detail: {detail_level}")
        scene = analyze_image_to_3d(image_bytes, file.content_type, detail_level)
        scene = validate_and_clean_scene(scene)
        logger.info(f"Generated scene with {len(scene.get('objects', []))} objects")
        return {"success": True, "scene": scene}
    except ValueError as e:
        logger.error(f"JSON parse error: {e}")
        raise HTTPException(status_code=422, detail="Failed to parse 3D scene from AI response.")
    except Exception as e:
        logger.error(f"Generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class PromptEditRequest(BaseModel):
    scene: dict
    prompt: str

@app.post("/api/edit-scene")
async def edit_scene(req: PromptEditRequest):
    try:
        from groq import Groq
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        scene_str = str(req.scene)
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": """You are a 3D scene editor. 
You will receive a JSON scene and a user edit command.
Apply the edit and return the MODIFIED scene as valid JSON only.
No markdown, no explanation. Return only the JSON object.
Rules:
- Only change what the user asked
- Keep all other properties identical
- Valid types: box, sphere, cylinder, cone, torus, plane
- Colors must be hex strings
- Pattern types: solid, wood, fur, fabric, glass, wheel, windows, metal, brick, stripes, dots, checker, football, basketball"""},
                {"role": "user", "content": f"Scene: {scene_str}\n\nEdit command: {req.prompt}\n\nReturn modified JSON only:"}
            ],
            max_tokens=2500
        )
        raw = response.choices[0].message.content.strip()
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        import json
        edited = json.loads(raw.strip())
        edited = validate_and_clean_scene(edited)
        return {"success": True, "scene": edited}
    except Exception as e:
        logger.error(f"Edit error: {e}")
        raise HTTPException(status_code=500, detail=str(e))