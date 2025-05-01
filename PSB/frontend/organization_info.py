
import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.colors as pcolors
import requests 
import json 
import numpy

import plotly.figure_factory as ff



def preload_organization_data(inn):
    res = requests.post("http://127.0.0.1:80/load_organizarion_prediction", json={"inn": inn})

    scoring_data = pd.DataFrame(res.json())
    scoring_data = scoring_data[["inn", "prdiction", "1200_mean", "1200_std", 
                                "1200_growth", "1300_mean", "1300_std", "1300_growth", "1500_mean", 
                                "1500_std", "1500_growth", "1600_mean", "1600_std", "1600_growth", "1700_mean", 
                                "1700_std", "1700_growth", "2100_mean", "2100_growth", "2110_mean", "2110_std", 
                                "2110_growth", "2200_mean", "2200_growth", "2400_mean", "2400_std", "2400_growth",
                                "current_ratio", "quick_ratio", "equity_ratio", "roa", "roe", "ros", "asset_turnover",
                                "top5_features", "z_score"]]
    
    res = requests.post("http://127.0.0.1:80/load_organizarion_finance", json={"inn": inn})

    finance_data = pd.DataFrame(res.json())
    
    res = requests.post("http://127.0.0.1:80/load_organizarion", json={"inn": inn})

    organizatin_data = pd.DataFrame(res.json())
    organizatin_data = organizatin_data[["name", "region","okved", "status"]]

    return (pd.concat([scoring_data, organizatin_data, finance_data], axis=1), finance_data)


# some how we get it
inn = 5075011400

data, finance_data = preload_organization_data(inn)
score = data["prdiction"].values[0]
name = data["name"].values[0]
status = data["status"].values[0]
region = data["region"].values[0]
okved = data["okved"].values[0]



st.set_page_config(page_title='Кредитный скоринг организации',  layout='wide')

st.markdown(f"## *Кредитный скоринг организации*")

st.divider()

col1, col2 = st.columns(2)

with col1:
    col11, col12 = col1.columns(2)
    col11.text("ИНН")
    col12.text(inn)

    col11.text("Название")
    col12.text(name)

    col11.text("Текущий статус")
    col12.text(status)

    col11.text("Регион регистрации")
    col12.text(region)

    col11.text("Вид деятельности")
    col12.text(okved)
    
    col1.divider()

    score = score * 3
    if score < 1:
        # t1.error(f"{score/3:2.2f}")
        col1.metric("**Риск дефолта**", f"{score/3:2.2f}", border=True)
    elif score < 2:
        # t1.warning(f"{score/3:2.2f}")
        col1.metric("**Риск дефолта**", f"{score/3:2.2f}", border=True)
    else:
        # t1.success(f"{score/3:2.2f}")
        col1.metric("**Риск дефолта**", f"{score/3:2.2f}", border=True)

    col1.markdown("### Значимые факторы")

    factors = json.loads(data["top5_features"].values[0])

    col11, col12 = col1.columns(2)
    
    for i in range(len(factors)):
        factor = factors[i]
        col = col11
        if i%2 == 1: col = col12
        col.metric(f"{factor[0].replace("_", " ")}", f"{numpy.abs(factor[2]):2.2f}",f"{numpy.sign(factor[2])}"[0], border=True)



with col2:
    
    print(finance_data.keys())
    print(finance_data)
    
    years = list(range(2020,2025))
    key1 = list(map(lambda x: f"{x}_1300", years))
    key2 = list(map(lambda x: f"{x}_1600", years))
    key3 = list(map(lambda x: f"{x}_1700", years))
    key4 = list(map(lambda x: f"{x}_2110", years))
    key5 = list(map(lambda x: f"{x}_2400", years))
    
    df = pd.DataFrame({"Итоговый капитал":finance_data[key1].values[0]/1000,
                       "Активный балнс":finance_data[key2].values[0]/1000,
                       "Пассивный балнс":finance_data[key3].values[0]/1000,
                       "Выручка":finance_data[key4].values[0]/1000,
                       "Чистая прибыль (убыток)":finance_data[key5].values[0]/1000,
                        "год": years })
    

    
    # lables = {
    #     "1300": "Итоговый капитал",
    #     "1600": "Активный балнс",
    #     "1700": "Пассивный балнс",
    #     "2210": "Выручка",
    #     "2400": "Чистая прибыль (убыток)"
    # }
    # print(df)
    # print(finance_data[key1].values[0])
    fig = px.line(df, 
                x="год",
                y=["Итоговый капитал", "Активный балнс", "Пассивный балнс", "Выручка", "Чистая прибыль (убыток)"],
                title="Отчетные суммы",
                markers=True)
    fig.update_layout(
        yaxis=dict(
            title=dict(
                text="Сумма, тыс. руб."
            ),
            tickformat='d'
        ),
        xaxis_tickformat ='d',
        # separators=".",

    )
    # for year in range(2020, 2025):
    #     for k in finance_data.keys():
    #         pass

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    economics_metrix = {
        "current_ratio": "Кэффициент текущей ликвидности",
        "quick_ratio":"Кэффициент быстрой ликвидности",
        "equity_ratio": "Кэффициент финнасовой независимости", 
        "roa": "Рентабельность активов", 
        "roe":"Рентабельность собственного капитала", 
        "ros":"Рентабельность продаж", 
        "asset_turnover":"Оборачеваемость активов",
        "z_score":"Оборачеваемость активов"
    }
    
    container = col2.container(height=400)
    col21, col22 = container.columns(2)
    for key,val in economics_metrix.items():
        col21.text(val)
        col22.text(data[key].values[0])

# ["1000"]["1100"]["СумОтч"]
    # st.plotly_chart()



# print(data["top5_features"].values[0], type(data["top5_features"].values[0]))
# for i,reason in enumerate(data["top5_features"].values[0]):
    # print(reason)
    # t3.metric(f"", f"{reason}", f"{influence:2.2f}", border=True)

# t1,t2,t3,t4,t5 = st.columns(5) 



# t1,t2,t3,t4,t5 = st.columns(5) 

# a.metric("Temperature", "30°F", "-9°F", border=True)
# b.metric("Wind", "4 mph", "2 mph", border=True)






# st.table(data)
