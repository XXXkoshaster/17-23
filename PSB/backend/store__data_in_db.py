

import db.session as ds
import pandas as pd

filename = "table_predictions"
df = pd.read_csv(f"{filename}.csv")

ds.store(filename, df)