

# not for production, details in src file
# import store__data_in_db


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

@app.post("/load_chunk_organizations")
async def get_chunk(chunk: Chunk):
    return di.load_chunk("organizations", chunk.start, chunk.end).to_dict("records")


@app.post("/load_organizarion_prediction")
async def get_organization(organization: Organization):
    return di.load_by_column("table_predictions", "inn", organization.inn).to_dict("records")

@app.post("/load_organizarion_finance")
async def get_organization(organization: Organization):
    return di.load_by_column("finances", "inn", organization.inn).to_dict("records")

@app.post("/load_organizarion")
async def get_organization(organization: Organization):
    return di.load_by_column("organizations", "inn", organization.inn).to_dict("records")

@app.post("/load_organizarion_kad_arbitr")
async def get_organization(organization: Organization):
    return di.load_by_column("kad_arbitr", "inn", organization.inn).to_dict("records")

@app.post("/load_organizarion_egrul")
async def get_organization(organization: Organization):
    return di.load_by_column("egrul", "inn", organization.inn).to_dict("records")

