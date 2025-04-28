import pandas as pd
import random 



company_names = ["some company", "dum dums", "goofy IT team", "OOO dota players best", "OOO cup org"]
reasons = [
    "just bad", "tragic accident", "hell that was unexpected", "WOW", "idk", "tom spiled a cup of tea on our servers...", "serious reson i gess"
]



def get_final_data():
    data = pd.DataFrame()
    for i in range(10):
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
    get_final_data()
    get_organization_data()