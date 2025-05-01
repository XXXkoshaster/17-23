from pydantic import BaseModel

class Organization(BaseModel):
    inn: int
    
class Chunk(BaseModel):
    start: int
    end: int
