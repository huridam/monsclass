import streamlit as st
import random
import pandas as pd

st.title("Streamlit 룰렛 앱 🎡")
st.write("룰렛에 들어갈 항목들을 쉼표(,)로 구분하여 입력하세요.")

# 1. 룰렛 항목을 입력받는 텍스트 영역
options_text = st.text_area(
    "항목 입력 (예: 점심 메뉴, 저녁 메뉴, 휴가 계획)",
    "사과, 바나나, 딸기, 포도" # 기본값 설정
)

# 2. 룰렛 돌리기 버튼
if st.button("룰렛 돌리기!"):
    # 3. 입력된 텍스트를 파싱(쉼표로 분리)
    options = [item.strip() for item in options_text.split(',') if item.strip()]

    if options:
        # 4. 항목 중에서 무작위로 하나 선택
        result = random.choice(options)
        
        # 5. 결과를 사용자에게 표시
        st.balloons() # 풍선 효과로 재미 추가!
        st.success(f"**오늘의 선택은... 🎉 {result} 🎉 입니다!**")
    else:
        st.error("룰렛 항목을 하나 이상 입력해 주세요.")