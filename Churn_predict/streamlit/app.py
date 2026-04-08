import streamlit as st
import base64
from PIL import Image
import matplotlib.pyplot as plt
import os

# ---------------------- 설정 ----------------------
# 배경 이미지 + 오버레이

def set_background_with_overlay(image_path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
                              url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

# 사용자 정의 스타일

def set_styles():
    st.markdown("""
        <style>
        h1, h2, h3, h4, h5, .big-label, .champ-card, .stTextInput > div > div > input {
            color: #00aaff !important;
            text-shadow: 1px 1px 3px black;
        }

        h1, h2, h3, h4, h5 {
            font-family: 'Friz Quadrata Std', serif;
        }

        .champ-card {
            background-color: rgba(0, 0, 0, 0.65);
            padding: 15px;
            border-radius: 15px;
            box-shadow: 0px 0px 12px #000000bb;
            text-align: center;
            margin-bottom: 20px;
            transition: transform 0.3s ease-in-out;
        }

        .champ-card:hover {
            transform: scale(1.03);
        }

        </style>
    """, unsafe_allow_html=True)

# 오디오 자동 재생

def autoplay_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay loop>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """
        st.markdown(md, unsafe_allow_html=True)

# ---------------------- 예시 데이터 ----------------------
champions_data = [
    {"name": "Ahri", "kda": [8.2, 7.4, 9.1], "win": "71%", "img": "assets/ahri.jpg", "role": "Mid"},
    {"name": "Yasuo", "kda": [5.1, 6.3, 5.7], "win": "48%", "img": "assets/yasuo.jpg", "role": "Mid"},
    {"name": "Lux", "kda": [7.4, 7.9, 8.3], "win": "65%", "img": "assets/lux.jpg", "role": "Support"},
    {"name": "Jax", "kda": [6.0, 5.5, 6.4], "win": "59%", "img": "assets/jax.jpg", "role": "Top"},
    {"name": "Jhin", "kda": [9.1, 8.7, 9.5], "win": "75%", "img": "assets/jhin.jpg", "role": "ADC"},
]

roles = ["All", "Top", "Mid", "Jungle", "ADC", "Support"]
search_history = []

# ---------------------- 실행 ----------------------
set_background_with_overlay("assets/background2.jpg")
set_styles()
autoplay_audio("assets/lol_theme.mp3")

st.markdown("<h1> 리그오브레전드 전적 대시보드</h1>", unsafe_allow_html=True)
summoner_name = st.text_input("소환사명을 입력하세요", "Hide on bush")

selected_role = st.selectbox("라인별 필터", roles)
filtered_champs = [c for c in champions_data if c["role"] == selected_role] if selected_role != "All" else champions_data

if st.button("전적 조회"):
    if summoner_name not in search_history:
        search_history.append(summoner_name)

    st.markdown(f"<h3> {summoner_name}님의 챔피언 성적 요약</h3>", unsafe_allow_html=True)

    cols = st.columns(len(filtered_champs))
    for i, col in enumerate(cols):
        with col:
            champ = filtered_champs[i]
            st.markdown("<div class='champ-card'>", unsafe_allow_html=True)
            st.image(champ["img"], caption=champ["name"], use_column_width=True)
            st.markdown(f"<div class='big-label'>승률: {champ['win']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 최근 10판 전적")
    st.markdown("- 🟩 승리: 7판  \n- 🟥 패배: 3판  \n- ⭐ MVP 횟수: 4회")

    st.markdown("---")
    st.markdown("### 챔피언별 KDA 추이 (최근 3게임)")
    fig, ax = plt.subplots()
    for champ in filtered_champs:
        ax.plot([1, 2, 3], champ["kda"], label=champ["name"])

    ax.set_xlabel("Game")
    ax.set_ylabel("KDA")
    ax.set_title("KDA Change Rate")
    ax.legend()
    st.pyplot(fig)

# ---------------------- 북마크 기능 ----------------------
st.markdown("---")
st.markdown("###  내 검색 히스토리")
if search_history:
    for user in search_history:
        st.markdown(f"- {user}")
else:
    st.markdown("검색된 소환사명이 없습니다.")
