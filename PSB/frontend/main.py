
import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests 


st.set_page_config(page_title='Кредитный Скоринг',  layout='wide')

t1,t2 = st.columns((1,1)) 

t1.markdown("## *Кредитный скоринг*")

t2.text_input("ИНН, название, причина отказа, ...")


res = requests.post("http://0.0.0.0:80/load_chunk", json={"start":0,"end":1})
print(res.ok)
print(res)
# print(res.json())

scoring_data = pd.DataFrame(res.json())
scoring_data = scoring_data[["inn", "prdiction", "1200_mean", "1200_std", 
                             "1200_growth", "1300_mean", "1300_std", "1300_growth", "1500_mean", 
                             "1500_std", "1500_growth", "1600_mean", "1600_std", "1600_growth", "1700_mean", 
                             "1700_std", "1700_growth", "2100_mean", "2100_growth", "2110_mean", "2110_std", 
                             "2110_growth", "2200_mean", "2200_growth", "2400_mean", "2400_std", "2400_growth",
                               "current_ratio", "quick_ratio", "equity_ratio", "roa", "roe", "ros", "asset_turnover"]]

st.table(scoring_data[["inn","prdiction","current_ratio"]])
