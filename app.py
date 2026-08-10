import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="하이마트 MD 실시간 최저가 모니터링", layout="wide")
st.title("📊 모델별 실시간 최저가 모니터링 대시보드 (구글 쇼핑)")

# 💡 여기에 발급받은 SerpApi 키를 입력하세요
SERPAPI_KEY = "863c36bdbb9d32848efb272f13e2f06d24bbd201e362ab4d7371e8de0ea58a80"

def get_google_shopping_data(query):
    url = "https://serpapi.com/search.json"
    # 구글 쇼핑 엔진, 한국어(hl), 한국 지역(gl) 설정
    params = {
        "engine": "google_shopping",
        "q": query,
        "hl": "ko",
        "gl": "kr",
        "api_key": SERPAPI_KEY
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        # SerpApi는 'shopping_results' 안에 상품 정보를 담아줍니다.
        return response.json().get('shopping_results', [])
    else:
        st.error(f"API 연결 에러가 발생했습니다. (에러 코드: {response.status_code})")
        return []

st.sidebar.header("검색 필터")
selected_model = st.sidebar.text_input("🔍 분석할 모델명을 입력하세요", placeholder="예: 믹서기 C300")

if selected_model:
    if SERPAPI_KEY == "여기에_SerpApi_Key_입력" or SERPAPI_KEY == "":
        st.warning("⚠️ 코드 9번째 줄에 SerpApi 키를 먼저 입력해 주세요.")
    else:
        with st.spinner('실시간 구글 쇼핑 최저가 데이터를 불러오는 중입니다...'):
            items = get_google_shopping_data(selected_model)
            
        if items:
            data = []
            for item in items:
                # 추출된 가격(extracted_price)이 있는 경우에만 데이터 수집
                if 'extracted_price' in item:
                    data.append({
                        '상품명': item.get('title', '이름 없음'),
                        '판매처': item.get('source', '판매처 미상'),
                        '가격': int(item.get('extracted_price')),
                        '링크': item.get('link', '')
                    })
            
            if not data:
                st.warning("⚠️ 가격 정보가 명확히 확인되는 상품이 없습니다.")
            else:
                df = pd.DataFrame(data)
                
                # 구글 쇼핑 데이터를 가격순으로 오름차순 정렬
                df = df.sort_values(by='가격').reset_index(drop=True)
                
                # '하이마트', '롯데하이마트' 등 당사 데이터 필터링
                himart_df = df[df['판매처'].str.contains('하이마트', case=False, na=False)]
                
                min_price = df.iloc[0]['가격']
                min_store = df.iloc[0]['판매처']
                
                st.subheader(f"[{selected_model}] 실시간 구글 쇼핑 최저가 현황")
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
                            st.warning("⚠️ 구글 쇼핑 검색 결과에 당사 상품이 노출되지 않고 있습니다.")

                st.markdown("---")
                st.write("📋 **전체 판매처 가격 비교 (낮은 가격순)**")
                
                st.dataframe(
                    df, 
                    width='stretch', 
                    hide_index=True,
                    column_config={
                        "링크": st.column_config.LinkColumn("해당 쇼핑몰로 이동")
                    }
                )
        else:
            st.warning("⚠️ 검색 결과가 없습니다. 구글 쇼핑에 등록되지 않은 모델일 수 있습니다.")
else:
    st.info("👈 왼쪽 사이드바에서 검색할 모델명을 입력해 주세요.")
