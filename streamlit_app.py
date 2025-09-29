import streamlit as st
import random
import time
import pandas as pd

# --- 1. 앱 설정 및 30개 중학교 1학년 수준 단어 목록 ---
st.set_page_config(layout="centered")
st.title("📚 중1 필수 국어 낱말 퀴즈 (버튼형)")
st.write("원하는 보기를 클릭하는 즉시 채점이 이루어집니다.")

# 중학교 1학년 수준에서 알아야 할 30개 단어 및 의미 (이전과 동일)
WORD_BANK = {
    "역설": "실제로는 모순되지만 그 속에 진리가 담겨 있는 표현 방식.",
    "은유": "원관념은 숨기고 보조관념만 드러내어 비유하는 표현 방식.",
    "직유": "‘~처럼, ~같이, ~듯’ 등의 연결어를 사용하여 직접 비유하는 표현 방식.",
    "풍자": "비판적인 시각으로 대상을 깎아내리거나 비웃는 표현 방식.",
    "해학": "익살스럽고 우스꽝스러우면서도 정감이 있는 말이나 행동.",
    "수사": "말이나 글을 아름답고 효과적으로 꾸미는 일 또는 그 방법.",
    "관습": "오랫동안 사회적으로 행해져 온 습관이나 방식.",
    "개요": "어떤 내용의 중요한 부분을 간추린 것.",
    "연대": "시간적으로 이어짐 또는 함께 행동함.",
    "정서": "사람의 마음속에 일어나는 여러 가지 감정.",
    "낭만": "현실에 얽매이지 않고 감정적, 이상적인 것을 추구하는 태도.",
    "감상": "아름다운 예술 작품을 감상하거나 자연의 경치를 봄.",
    "심미": "아름다움을 느끼고 깨달아 아는 일.",
    "성찰": "자신의 마음을 깊이 돌이켜 반성함.",
    "논리": "말이나 글에서 이치에 맞게 생각하고 표현하는 것.",
    "객관적": "개인의 의견을 떠나 사실이나 일반적 기준에 따른 것.",
    "주관적": "자신의 개인적인 생각이나 관점에 따른 것.",
    "추상적": "구체적이지 않고 막연하거나 개념적인 것.",
    "구체적": "직접 보고 만질 수 있거나 자세하게 드러난 것.",
    "선입견": "어떤 대상에 대해 미리 가지고 있는 고정된 생각.",
    "편견": "공정하지 못하고 한쪽으로 치우친 생각.",
    "지양": "더 높은 단계로 나아가기 위해 현재의 것을 부정하고 버림.",
    "지향": "특정한 목표나 방향으로 뜻이 쏠려 나아감.",
    "화자": "시에서 말하는 사람.",
    "청자": "듣는 사람.",
    "단정": "확신을 가지고 판단하여 결론을 내림.",
    "갈등": "서로 대립하여 충돌하는 상황.",
    "애환": "사랑과 기쁨, 그리고 슬픔과 한이 섞인 복잡한 감정.",
    "서술": "어떤 사실이나 생각을 자세히 풀어서 말하거나 적음.",
    "분석": "복잡한 것을 나누어 그 구성 요소를 자세히 살펴봄.",
}
ALL_MEANINGS = list(WORD_BANK.values())


# --- 2. 세션 상태 초기화 ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_attempts' not in st.session_state:
    st.session_state.total_attempts = 0
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = None
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'is_correct' not in st.session_state:
    st.session_state.is_correct = None


# --- 3. 핵심 함수: 새 퀴즈 생성 ---
def generate_new_quiz():
    word = random.choice(list(WORD_BANK.keys()))
    correct_meaning = WORD_BANK[word]
    
    # 정답 외의 오답 4개 선정
    incorrect_meanings = random.sample([m for m in ALL_MEANINGS if m != correct_meaning], 4)
    options = [correct_meaning] + incorrect_meanings
    random.shuffle(options)
    
    # 세션 상태 업데이트 (새 문제)
    st.session_state.current_quiz = {
        "word": word,
        "correct_meaning": correct_meaning,
        "options": options
    }
    st.session_state.answered = False
    st.session_state.is_correct = None
    st.session_state.total_attempts += 1


# --- 4. 정답 체크 함수 (버튼 클릭 시 실행) ---
def check_answer(user_choice):
    # 이미 답한 상태라면 추가 클릭 방지
    if st.session_state.answered:
        return

    is_correct = (user_choice == st.session_state.current_quiz["correct_meaning"])
    
    # 세션 상태 업데이트 (정답/오답 및 점수)
    st.session_state.answered = True
    st.session_state.is_correct = is_correct
    st.session_state.selected_choice = user_choice # 사용자가 선택한 보기를 저장
    if is_correct:
        st.session_state.score += 1
            
    # 정답 체크 후 화면을 다시 로드하여 피드백을 보여줍니다.
    st.rerun() 


# --- 5. 메인 UI ---

# 퀴즈가 없으면 자동으로 첫 문제 생성
if st.session_state.current_quiz is None:
    generate_new_quiz()
    
st.sidebar.subheader("📊 학습 현황")
# 첫 시도는 0으로 보이기 위해 total_attempts가 0일 경우 0으로 표시
st.sidebar.metric("점수", f"{st.session_state.score}점", delta=f"총 {st.session_state.total_attempts if st.session_state.total_attempts==0 else st.session_state.total_attempts-1}문제 중")


st.header(f"Q. 다음 **'{st.session_state.current_quiz['word']}'**의 의미로 가장 알맞은 것은 무엇인가요?")
st.markdown("---")

# 5지 선다 버튼 출력
options = st.session_state.current_quiz["options"]

# 각 보기를 개별 버튼으로 생성
for i, option in enumerate(options):
    # 이미 답했을 경우 버튼의 색상과 상태를 변경하여 피드백 제공
    if st.session_state.answered:
        # 정답일 경우 (사용자가 선택했는지와 상관없이)
        if option == st.session_state.current_quiz["correct_meaning"]:
            button_type = "primary" # 정답 버튼은 파란색으로 표시
            icon = "✔️"
        # 오답이지만 사용자가 선택한 경우
        elif option == st.session_state.selected_choice:
            button_type = "secondary"
            icon = "❌"
        # 그 외 오답 보기
        else:
            button_type = "secondary"
            icon = " "
    # 아직 답하지 않은 경우
    else:
        button_type = "secondary"
        icon = " "
        
    
    # 버튼 생성. 버튼 텍스트는 옵션 내용으로 하고, 클릭 시 check_answer 실행
    if st.button(f"{icon} {i+1}. {option}", key=f"option_{i}", 
                 on_click=check_answer, args=(option,), 
                 use_container_width=True, type=button_type,
                 disabled=st.session_state.answered # 이미 답했으면 비활성화
                 ):
        pass # on_click으로 함수가 이미 실행되었으므로 이 블록은 비워둡니다.

# 5-1. 결과 피드백 표시
if st.session_state.answered:
    if st.session_state.is_correct:
        st.success("🎉 정답입니다! 다음 문제로 넘어가세요.")
    else:
        st.error("❌ 오답입니다. 다시 한번 확인해 보세요.")
        # 정답은 이미 버튼에 파란색으로 표시되어 있으므로 별도 표시는 생략

    st.markdown("---")
    
    # 다음 문제 버튼 (누르면 새로운 퀴즈 생성 및 화면 다시 로드)
    if st.button("➡️ 다음 문제 풀기", type="primary", use_container_width=True):
        generate_new_quiz()
        st.rerun()

st.markdown("---")
st.subheader("📋 전체 학습 단어 목록 (총 30개)")
df = pd.DataFrame(WORD_BANK.items(), columns=["단어", "의미"])
st.dataframe(df, use_container_width=True, hide_index=True)