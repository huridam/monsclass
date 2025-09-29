import streamlit as st
import random

# --- 1. 앱 설정 및 데이터 뱅크 ---
st.set_page_config(layout="centered")
st.title("💡 창작 영감 생성기 (시/글쓰기 보조)")
st.write("버튼을 누를 때마다 무작위로 조합된 창작 아이디어를 얻을 수 있습니다.")

# 창작에 사용할 요소 목록
SUBJECTS = ["고요한 강물", "오래된 골목길", "바람이 멈춘 정원", "어둠 속의 별 하나", "잊혀진 약속"]
OBJECTS = ["낡은 시계 소리", "숨겨진 일기장", "마지막 잎새", "희미한 노랫소리", "차가운 돌멩이"]
ACTIONS = ["천천히 흘러간다", "반짝이며 떨어진다", "깊이 잠들어 있다", "소리 없이 사라진다", "다시 피어난다"]
EMOTIONS = ["그리움", "쓸쓸함", "환희", "망설임", "기억"]
ADVERBS = ["가끔씩", "문득", "조용히", "왠지 모르게", "아주 희미하게"]


# --- 2. 핵심 함수: 영감 생성 ---
def generate_inspiration():
    # 각 목록에서 무작위로 하나의 요소를 선택하여 조합
    prompt = {
        "주제 구절": random.choice(SUBJECㄹTS),
        "핵심 대상": random.choice(OBJECTS),
        "느낌": random.choice(EMOTIONS),
        "움직임": random.choice(ADVERBS) + " " + random.choice(ACTIONS),
    }
    st.session_state.prompt = prompt
    st.session_state.result_text = f"**{prompt['주제 구절']}**에서 시작하여, **{prompt['핵심 대상']}**이 **{prompt['움직임']}**을 묘사하고, 그 속에 **'{prompt['느낌']}'**의 감정을 담아보세요."


# --- 3. 세션 상태 초기화 ---
if 'prompt' not in st.session_state:
    st.session_state.prompt = None
    st.session_state.result_text = "아래 버튼을 눌러 첫 번째 영감을 얻어보세요."


# --- 4. 메인 UI ---

# 영감 생성 버튼
if st.button("✨ 새로운 영감 얻기", type="primary", use_container_width=True):
    generate_inspiration()

st.markdown("---")

# 결과 표시 섹션
st.subheader("📝 오늘 당신의 영감 (Creative Prompt)")
st.markdown(st.session_state.result_text)

if st.session_state.prompt:
    st.markdown("---")
    st.subheader("🔑 구성 요소")
    
    # 생성된 구성 요소를 표 형태로 보여줍니다.
    df = pd.DataFrame(st.session_state.prompt.items(), columns=["요소", "내용"])
    st.dataframe(df, use_container_width=True, hide_index=True)


# --- 5. 사이드바: 참고 목록 (Codespaces 환경에서 pandas 에러 방지용으로 import 필요)
import pandas as pd # <- 이 구문이 있어야 DataFrame 오류를 막을 수 있습니다.

with st.sidebar:
    st.header("참고: 모든 단어 목록")
    
    st.markdown("##### 주제 목록")
    st.dataframe(pd.DataFrame(SUBJECTS), hide_index=True)
    
    st.markdown("##### 행동/움직임 목록")
    st.dataframe(pd.DataFrame(ACTIONS), hide_index=True)