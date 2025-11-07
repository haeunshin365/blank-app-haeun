import random
import streamlit as st
import pandas as pd

st.set_page_config(page_title="주사위 2개 수학 게임", page_icon="🎲")

st.title("� 주사위 2개 수학 게임")
st.write("두 개의 주사위를 던져 나온 합을 맞혀 보세요. 맞히면 점수를 얻습니다. '힌트 보기'로 각 합의 확률을 확인할 수 있습니다.")

# 세션 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "rounds" not in st.session_state:
    st.session_state.rounds = 0
if "history" not in st.session_state:
    st.session_state.history = []  # 최근 플레이 기록(최신순)

# 두 주사위 합의 경우의 수 분포
sum_counts = {s: c for s, c in zip(range(2, 13), [1,2,3,4,5,6,5,4,3,2,1])}
total_outcomes = 36

with st.form("dice_form"):
    guess = st.number_input("합을 예측하세요 (2-12):", min_value=2, max_value=12, value=7, step=1)
    show_hint = st.checkbox("힌트 보기: 이 합의 확률 표시")
    submitted = st.form_submit_button("던지기")

if submitted:
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    s = d1 + d2
    correct = (guess == s)
    st.session_state.rounds += 1
    if correct:
        st.session_state.score += 1
        st.success(f"정답! 주사위: {d1} {d2} → 합 {s} (예측 {guess})")
    else:
        st.error(f"틀렸습니다. 주사위: {d1} {d2} → 합 {s} (예측 {guess})")
    # 주사위 그림(유니코드)
    faces = ["⚀","⚁","⚂","⚃","⚄","⚅"]
    st.write(f"{faces[d1-1]}  {faces[d2-1]}")
    # 기록 저장
    st.session_state.history.insert(0, {"d1": d1, "d2": d2, "sum": s, "guess": guess, "correct": correct})
    if len(st.session_state.history) > 50:
        st.session_state.history = st.session_state.history[:50]

if show_hint:
    prob = sum_counts.get(guess, 0) / total_outcomes
    st.info(f"합 {guess}의 확률: {sum_counts.get(guess,0)}/{total_outcomes} = {prob:.2%}")

# 사이드바: 점수판 및 초기화
st.sidebar.header("게임 정보")
st.sidebar.write(f"라운드: {st.session_state.rounds}")
st.sidebar.write(f"점수: {st.session_state.score}")
if st.sidebar.button("기록 초기화"):
    st.session_state.score = 0
    st.session_state.rounds = 0
    st.session_state.history = []
    st.sidebar.success("기록을 초기화했습니다.")

st.header("최근 기록 (최대 50회)")
if st.session_state.history:
    for i, h in enumerate(st.session_state.history, 1):
        mark = "✅" if h["correct"] else "❌"
        st.write(f"{i}. 주사위: {h['d1']}, {h['d2']} → 합 {h['sum']} | 예측: {h['guess']} {mark}")
else:
    st.write("아직 플레이한 기록이 없습니다. '던지기' 버튼을 눌러 시작하세요.")

st.write("---")
st.write("확률 분포 (두 주사위의 합)")
df = pd.DataFrame({"합": list(sum_counts.keys()), "경우의 수": list(sum_counts.values())}).set_index("합")
st.bar_chart(df)

st.write("팁: 확률을 확인하려면 '힌트 보기'를 체크한 후 '던지기'를 누르세요.")
