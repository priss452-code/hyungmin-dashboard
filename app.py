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
selected_model = st.sidebar.selectbox("🔍 분석할 모델을 선택하세요", df['모델명'].unique())

filtered_df = df[df['모델명'] == selected_model]
sorted_df = filtered_df.sort_values(by='가격').reset_index(drop=True)

min_price = sorted_df.iloc[0]['가격']
min_store = sorted_df.iloc[0]['판매처']

st.subheader(f"[{selected_model}] 현재 최저가 현황")
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
