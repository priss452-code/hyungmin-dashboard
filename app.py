import streamlit as st
import pandas as pd

st.set_page_config(page_title="하이마트 MD 최저가 모니터링", layout="wide")
st.title("📊 모델별 최저가 모니터링 대시보드")

# 가데이터
data = {
    '모델명': ['냉장고-A100', '냉장고-A100', '냉장고-A100', 'TV-B200', 'TV-B200', 'TV-B200'],
    '판매처': ['하이마트', 'A사(경쟁사)', 'B사(경쟁사)', '하이마트', 'A사(경쟁사)', 'B사(경쟁사)'],
    '가격': [1500000, 1480000, 1520000, 2100000, 2150000, 2050000]
}
df = pd.DataFrame(data)

st.sidebar.header("검색 필터")
# selectbox를 text_input으로 변경하여 직접 입력받음
selected_model = st.sidebar.text_input("🔍 분석할 모델명을 입력하세요", placeholder="예: 냉장고-A100")

# 1. 입력값이 있을 때만 분석 로직 실행 (초기 빈 화면 에러 방지)
if selected_model:
    # 2. 대소문자 구분 없이 입력한 글자가 포함된 데이터 필터링 (부분 검색 가능)
    filtered_df = df[df['모델명'].str.contains(selected_model, case=False, na=False)]
    
    # 3. 검색 결과가 있는지 확인 (없는 모델명 검색 시 에러 방지)
    if not filtered_df.empty:
        sorted_df = filtered_df.sort_values(by='가격').reset_index(drop=True)

        min_price = sorted_df.iloc[0]['가격']
        min_store = sorted_df.iloc[0]['판매처']

        st.subheader(f"[{selected_model}] 검색 결과 최저가 현황")
        col1, col2, col3 = st.columns(3)

        col1.metric("최저가", f"{min_price:,} 원")
        col2.metric("최저가 판매처", min_store)

        with col3:
            if min_store == '하이마트':
                st.success("✨ 당사가 최저가입니다! (경쟁 우위)")
            else:
                st.error(f"⚠️ {min_store}가 더 저렴합니다! (가격 대응 필요)")

        st.markdown("---")
        st.write("📋 **전체 판매처 가격 비교 (낮은 가격순)**")
        st.dataframe(sorted_df, use_container_width=True, hide_index=True)
        
    else:
        # 검색 결과가 없을 때의 안내 메시지
        st.warning("⚠️ 검색하신 모델명과 일치하는 데이터가 없습니다. 다시 확인해 주세요.")
else:
    # 처음 앱을 열었을 때 검색을 유도하는 메시지
    st.info("👈 왼쪽 사이드바에서 검색할 모델명을 입력해 주세요.")
