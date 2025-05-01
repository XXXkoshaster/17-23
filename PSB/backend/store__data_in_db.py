

import db.session as ds
import pandas as pd

csvs = ["table_predictions", "organizations", "kad_arbitr", "finances", "egrul"]

for csv in csvs:
    
    print(f"reading {csv}")
    df = pd.read_csv(f"{csv}.csv")
    
    print(f"writing {csv}")
    ds.store(csv, df)
    
    print()