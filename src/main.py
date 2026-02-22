import fastapi
from fastapi import staticfiles
from fastapi.responses import StreamingResponse
import uvicorn
import pyttsx3
import io
import tempfile

app = fastapi.FastAPI()

@app.get("/api/speak/{text}")
async def speak(text: str):
    with tempfile.NamedTemporaryFile(mode="w+b", delete=True, suffix=".wav") as f:
        engine = pyttsx3.init()
        engine.save_to_file(text, f.name)
        engine.runAndWait()

        f.flush()
        f.seek(0)

        buf = io.BytesIO(f.read())
        return StreamingResponse(buf)

app.mount("/", staticfiles.StaticFiles(directory="./static", html=True))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
