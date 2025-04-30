

import db.session as ds
import pandas as pd

filename = "df_merged_pre_final"
df = pd.read_csv(f"{filename}.csv")

ds.store(filename, df)