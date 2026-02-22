import fastapi
from fastapi import staticfiles
import uvicorn
import pyttsx3

engine = pyttsx3.Engine()
app = fastapi.FastAPI()

app.mount("/", staticfiles.StaticFiles(directory="./static", html=True))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
