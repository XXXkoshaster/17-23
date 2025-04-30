

import db.session as di
from models.model import Organization, Chunk 

from fastapi import FastAPI



app = FastAPI()

@app.post("/download")
async def download(chunk: Chunk):
    return di.load_chunk("table_predictions", chunk.start, chunk.end).to_csv()

@app.post("/load_chunk")
async def get_chunk(chunk: Chunk):
    return di.load_chunk("table_predictions", chunk.start, chunk.end).to_dict("records")

@app.post("/load_organization")
async def get_organization(organization: Organization):
    return di.load_organizarion("table_predictions", organization.inn).to_dict("records")
