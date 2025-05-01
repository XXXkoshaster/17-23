
# this is needed to store ind db all csv's owr team made in notebooks 🥲🥲🥲

import db.session as ds
import pandas as pd

csvs = ["table_predictions", "organizations", "kad_arbitr", "finances", "egrul"]

for csv in csvs:
    
    print(f"reading {csv}")
    df = pd.read_csv(f"{csv}.csv")
    
    print(f"writing {csv}")
    ds.store(csv, df)
    
    print()