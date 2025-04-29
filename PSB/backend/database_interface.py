
class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

import pandas as pd
from dotenv import load_dotenv, dotenv_values

# load variables from .env
load_dotenv()

config = dotdict(dotenv_values(".env"))

from sqlalchemy import create_engine

engine = create_engine(f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.ADDRESS}:{config.PORT}/{config.POSTGRES_DB}")

# important for chunk reading aother wise its all loaded in memory
conn = engine.connect().execution_options(stream_results=True)

def load_organizarion(table_name, inn):
    return pd.read_sql(f"select * from {table_name} where Column1={inn}", con=conn)

def load(table_name):
    return pd.read_sql(f"select * from {table_name}", con=conn).drop("index", axis=1)

def load_chunks(table_name, chunksize):
    for chunk in pd.read_sql(f"select * from {table_name}", con=conn, chunksize=chunksize):
        yield chunk.drop("index", axis=1)

def store(table_name, df):
    df.to_sql(table_name, con=engine, if_exists="replace")



if __name__ == "__main__":
    
    original_data = pd.read_csv("egrul_final.csv")

    store("egrul_final", original_data)

    # read by chunks
    for chunk_data_from_db in load_chunks("egrul_final", 1000):
        print(chunk_data_from_db.info())