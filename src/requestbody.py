from pydantic import BaseModel
class RequestBody(BaseModel):
    def __init__(self, voice: int, volume: float, rate: int, text: str):
        self.voice = voice
        self.volume = volume
        self.rate = rate
        self.text = text
