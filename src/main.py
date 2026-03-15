import fastapi
from fastapi import staticfiles
from fastapi.responses import JSONResponse, StreamingResponse

from pydantic import BaseModel
import uvicorn
from piper import PiperVoice

import wave
import io
import os
import sys


class RequestBody(BaseModel):
    text: str
    model: str


app = fastapi.FastAPI()


voices: dict[str, PiperVoice] = {}


def load_voices(voice_dir: str, storage: dict[str, PiperVoice]):
    for entry in os.listdir(voice_dir):
        if entry.endswith(".onnx") and f"{entry}.json" in os.listdir(voice_dir):
            print(f"Loading model: {entry} into RAM...")
            storage[entry.removesuffix(".onnx")] = PiperVoice.load(voice_dir + os.path.sep + entry)


def synthesize_to_stream(text: str, model: str):
    voice = voices[model]
    audio = voice.synthesize(text)

    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(voice.config.sample_rate)

        for chunk in audio:
            f.writeframes(chunk.audio_int16_bytes)

    buffer.seek(0)
    return buffer


@app.get("/health")
async def gethealth():
    return {"status": "UP"}


@app.get("/api/models")
async def getmodels():
    voices_list = []
    for key in voices.keys():
        voices_list.append(key)

    return voices_list


@app.post("/api/speak")
async def speak(body: RequestBody):
    if body.text.strip() == "":
        return JSONResponse(
            {"detail": "Spoken text may not be empty."},
            400
        )
    try:
        return StreamingResponse(
            synthesize_to_stream(body.text, body.model),
            media_type="audio/wav"
        )
    except KeyError:
        return JSONResponse(
            {"error": "The Model that you entered could not be found."},
            404
        )

app.mount("/", staticfiles.StaticFiles(directory="./static", html=True))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        load_voices(sys.argv[1], voices)
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        print("This application requires a path to the Piper Model Folder.")
        exit(1)
