import streamlit as st

from request_api import get_info

st.set_page_config(page_title="급식알리미", page_icon="🍱")
st.title("급식 알리미")

offices: dict = {
    "서울특별시교육청": "B10", "부산광역시교육청": "C10",
    "대구광역시교육청": "D10", "인천광역시교육청": "E10",
    "광주광역시교육청": "F10", "대전광역시교육청": "G10",
    "울산광역시교육청": "H10", "세종특별자치시교육청": "I10",
    "경기도교육청": "J10", "강원특별자치도교육청": "K10",
    "충청북도교육청": "M10", "충청남도교육청": "N10",
    "전북특별자치도교육청": "P10", "전라남도교육청": "Q10",
    "경상북도교육청": "R10", "경상남도교육청": "S10",
    "제주특별자치도교육청": "T10"
}
office_name = st.selectbox("교육청을 선택하세요", list(offices.keys()))

col1, col2 = st.columns(2)
with col1:
    school_name = st.text_input("학교 이름을 입력하세요")
with col2:
    date = st.date_input("날짜를 선택하세요")

st.write(f"입력한 학교: {school_name}")

if st.button("급식 조회하기"):

    with st.spinner("급식 정보를 불러오는 중..."):
        date_str: str = date.strftime("%Y%m%d")
        info: list[str] = get_info(date=date, school_name=school_name)

    if info:
        st.success(f"{school_name} 급식을 불러왔습니다.")

        st.write(f"### {school_name} {date.strftime("%m월 %d일")} 급식")
        for dish in info[0]:
            st.write(f"- {dish}")

        with st.expander("학교 정보 더보기"):
            st.write(f"교육청: {office_name} ({info[1]})")
            st.write(f"학교 코드: {info[2]}")
    else:
        st.error("급식 정보를 찾을 수 없습니다. 날짜나 학교 이름을 다시 확인해주세요.")