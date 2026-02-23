import fastapi
from fastapi import staticfiles
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import uvicorn
import io
import os
import sys
import tempfile
import subprocess

class RequestBody(BaseModel):
    text: str
    model: str

app = fastapi.FastAPI()

def speakToFile(text: str, model: str, path: str):
    proc = subprocess.run(
        ["piper-tts", "-m", model, "-f", path, text],
        capture_output=True,
        text=True
    )

    proc.check_returncode()

@app.get("/api/models")
async def getmodels():
    modelDir = os.listdir(sys.argv[1])
    models = []
    for entry in modelDir:
        if entry.endswith(".onnx") and f"{entry}.json" in modelDir:
            models.append(entry.removesuffix(".onnx"))

    return models

@app.post("/api/speak")
async def speak(body: RequestBody):
    with tempfile.NamedTemporaryFile(mode="w+b", delete=True, suffix=".wav") as f:
        if body.text.strip() == "":
            return JSONResponse(
                {"detail": "Spoken text may not be empty."},
                400
            )

        try:
            speakToFile(body.text, sys.argv[1] + os.path.sep + body.model, f.name)
        except subprocess.CalledProcessError:
            return JSONResponse(
                {"detail": f"Could not find model '{body.model}'"},
                422
            )

        f.flush()
        f.seek(0)

        buf = io.BytesIO(f.read())
        return StreamingResponse(buf)

app.mount("/", staticfiles.StaticFiles(directory="./static", html=True))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        print("This application requires a path to the Piper Model.")
