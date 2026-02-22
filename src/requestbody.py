from pydantic import BaseModel
class RequestBody(BaseModel):
    voice: int
    volume: float | int
    rate: int
    text: str
