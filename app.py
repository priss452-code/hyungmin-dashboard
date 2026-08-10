import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="하이마트 MD 실시간 최저가 모니터링", layout="wide")
st.title("📊 모델별 실시간 최저가 모니터링 대시보드 (네이버 API)")

# 💡 여기에 발급받은 네이버 API 키를 입력하세요
NAVER_CLIENT_ID = "lvrp66pn2x"
NAVER_CLIENT_SECRET = "RCanlHnDDfu8N6GXKuv4Vd8afp2zKL4nhprbmKLL"

def get_naver_shopping_data(query):
    url = "https://openapi.naver.com/v1/search/shop.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    # sort='asc'로 최저가순 정렬, display=20으로 상위 20개 판매처 데이터 가져오기
    params = {
        "query": query,
        "display": 20,
        "sort": "asc"
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()['items']
    else:
        st.error(f"API 연결 에러가 발생했습니다. (에러 코드: {response.status_code})")
        return []

st.sidebar.header("검색 필터")
selected_model = st.sidebar.text_input("🔍 분석할 모델명을 입력하세요", placeholder="예: 믹서기 C300")

if selected_model:
    if NAVER_CLIENT_ID == "여기에_Client_ID_입력":
        st.warning("⚠️ 코드 상단에 네이버 API 키(Client ID, Secret)를 먼저 입력해 주세요.")
    else:
        with st.spinner('실시간 네이버 쇼핑 최저가 데이터를 불러오는 중입니다...'):
            items = get_naver_shopping_data(selected_model)
            
        if items:
            # 가져온 JSON 데이터를 데이터프레임으로 변환
            data = []
            for item in items:
                # 네이버 API는 상품명에 <b> 태그를 포함하므로 텍스트 정제
                clean_title = item['title'].replace('<b>', '').replace('</b>', '')
                data.append({
                    '상품명': clean_title,
                    '판매처': item['mallName'],
                    '가격': int(item['lprice']),
                    '링크': item['link']
                })
            
            df = pd.DataFrame(data)
            
            # '하이마트', '롯데하이마트' 등 당사 데이터 필터링
            himart_df = df[df['판매처'].str.contains('하이마트', case=False, na=False)]
            
            min_price = df.iloc[0]['가격']
            min_store = df.iloc[0]['판매처']
            
            st.subheader(f"[{selected_model}] 실시간 검색 결과 최저가 현황")
            col1, col2, col3 = st.columns(3)
            
            col1.metric("종합 최저가", f"{min_price:,} 원")
            col2.metric("최저가 판매처", min_store)
            
            with col3:
                if '하이마트' in min_store:
                    st.success("✨ 당사가 종합 최저가입니다! (경쟁 우위)")
                else:
                    if not himart_df.empty:
                        himart_min_price = himart_df.iloc[0]['가격']
                        price_diff = himart_min_price - min_price
                        st.error(f"⚠️ 타사가 {price_diff:,}원 더 저렴합니다! (가격 대응 필요)")
                    else:
                        st.warning("⚠️ 상위 20개 검색 결과에 당사 상품이 노출되지 않고 있습니다.")

            st.markdown("---")
            st.write("📋 **전체 판매처 가격 비교 (최저가순)**")
            
            # 표에 상품 링크를 클릭할 수 있도록 컬럼 설정
            st.dataframe(
                df, 
                width='stretch',
                hide_index=True,
                column_config={
                    "링크": st.column_config.LinkColumn("해당 쇼핑몰로 이동")
                }
            )
        else:
            st.warning("⚠️ 검색 결과가 없습니다. 모델명을 다시 확인해 주세요.")
else:
    st.info("👈 왼쪽 사이드바에서 검색할 모델명을 입력해 주세요.")
