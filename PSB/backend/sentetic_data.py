import pandas as pd
import random 

import db.session as ds


company_names = ["some company", "dum dums", "goofy IT team", "OOO dota players best", "OOO cup org"]
reasons = [
    "just bad", "tragic accident", "hell that was unexpected", "WOW", "idk", "tom spiled a cup of tea on our servers...", "serious reson i gess"
]



def get_final_data(num):
    data = pd.DataFrame()
    for i in range(num):
        data = data._append({"inn": random.randint(10**10,9*10**10), "name": random.choice(company_names), "default_score": random.uniform(0,1), "reason":random.choice(reasons)}, ignore_index=True)

    # print(data)
    return data



def get_organization_data():
    data = pd.DataFrame()
    for i in range(10):
        data = data._append({"inn": random.randint(10**10,9*10**10), "name": random.choice(company_names), "default_score": random.uniform(0,1), "reason":random.choice(reasons)}, ignore_index=True)

    # print(data)
    return data



if __name__ == "__main__":
    # ds.store("sentetic_data",get_final_data(4))
    # get_organization_data()

    df = ds.load_chunk("sentetic_data", 0, 0)
    print(df)

    # df = ds.load("sentetic_data")
    # print(df)

    df["name"] = "WUIUIUIU"
    df = ds.store_chunk("sentetic_data",df)
