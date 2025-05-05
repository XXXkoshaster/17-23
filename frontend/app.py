import streamlit as st

st.set_page_config(layout="wide", page_title="idChess Editor")

# --- Custom CSS for styling ---
st.markdown('''
    <style>
    .main {background-color: #fff;}
    .sidebar .sidebar-content {background-color: #fff;}
    .stButton>button {background-color: #27c26c; color: white;}
    .stTextInput>div>input, .stTextArea>div>textarea {
        border: 1px solid #222; border-radius: 8px; padding: 6px;
    }
    .stSelectbox>div>div>div {border-radius: 8px;}
    .stProgress>div>div>div {background: linear-gradient(90deg, #27c26c 0%, #b6f5d8 100%);}
    .st-bb {background: #27c26c; color: white; border-radius: 8px;}
    .st-bb:hover {background: #1e9e54;}
    .stRadio>div>label {font-weight: bold;}
    </style>
''', unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.markdown('<h1 style="color:#27c26c;">idChess</h1>', unsafe_allow_html=True)
menu = ["Домой", "Библиотека", "<b>Редактор</b>", "Настройки", "Мой Профиль", "Работа в Friflex"]
for item in menu:
    st.sidebar.markdown(f"<div style='margin-bottom: 10px;'>{item}</div>", unsafe_allow_html=True)

st.sidebar.markdown('<div style="margin-top:40px;"><button style="background:#27c26c;color:white;border:none;border-radius:8px;padding:6px 16px;">Топ мейкеры</button></div>', unsafe_allow_html=True)
for i in range(5):
    st.sidebar.image("https://img.icons8.com/ios-filled/50/cccccc/user-male-circle.png", width=32)
    st.sidebar.progress(0)

# --- Top search bar ---
col_search, col_btn = st.columns([8,1])
with col_search:
    st.text_input("", placeholder="Поиск", key="search_bar")
with col_btn:
    st.button("Поиск", use_container_width=True)

# --- Main layout ---
col_left, col_center, col_right = st.columns([1.2,2.5,1.5])

with col_center:
    st.markdown("<div style='height:320px; background:#eaeaea; border-radius:12px; display:flex; align-items:center; justify-content:center;'><span style='color:#aaa;'>[Видео/Изображение]</span></div>", unsafe_allow_html=True)
    st.progress(0.2, text="1 / 5")
    cols = st.columns(5)
    for i, c in enumerate(cols):
        if i == 0:
            c.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Chess_board_opening_staunton.jpg/320px-Chess_board_opening_staunton.jpg", width=80)
        else:
            c.markdown("<div style='height:80px; background:#eaeaea; border-radius:8px;'></div>", unsafe_allow_html=True)
    st.button("Сгенерировать", use_container_width=True)

with col_right:
    st.text_input("// Название", key="title")
    st.text_area("// Описание", key="desc", height=80)
    st.text_area("// Хэштеги", key="tags", height=40)
    st.markdown("<b>Параметры</b>", unsafe_allow_html=True)
    st.selectbox("#Язык", ["русский", "английский", "немецкий"], key="lang")
    st.selectbox("#Голос", ["Скала Джонсон", "Морган Фриман", "Алиса"], key="voice")
    col_speed1, col_speed2, col_speed3 = st.columns([1,2,1])
    with col_speed1:
        st.button("-", key="speed_minus")
    with col_speed2:
        st.slider("#Скорость", 50, 150, 100, key="speed")
    with col_speed3:
        st.button("+", key="speed_plus")
    st.file_uploader("#Музыка", key="music")
    st.text_area("#Дополнительный промт", key="extra_prompt", height=40)
    st.button("Применить", use_container_width=True)

with col_center:
    st.button("Опубликовать", use_container_width=True) 