from pydantic import BaseModel

class Organization(BaseModel):
    inn: str
    
class Chunk(BaseModel):
    start: int
    end: int
