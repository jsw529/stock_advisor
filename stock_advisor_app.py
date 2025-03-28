
import streamlit as st
import yfinance as yf
import datetime

st.set_page_config(page_title="주식 분석 도우미", layout="centered")
st.title("📈 주식 분석 도우미")

symbol = st.text_input("종목 코드 또는 티커 (예: AAPL, TSLA, 005930.KS)")

if symbol:
    try:
        st.info(f"'{symbol}'에 대한 정보를 가져오는 중입니다...")
        stock = yf.Ticker(symbol)
        today = datetime.date.today()
        past = today - datetime.timedelta(days=180)
        hist = stock.history(start=past, end=today)

        if hist.empty:
            st.error("해당 종목의 데이터를 가져올 수 없습니다. 정확한 티커를 입력해주세요.")
        else:
            info = stock.info

            st.subheader("📊 주가 차트 (최근 6개월)")
            st.line_chart(hist['Close'])

            st.subheader("💬 종목 기본 정보")
            st.write(f"**현재가:** {info.get('currentPrice', '정보 없음')} 원")
            st.write(f"**PER:** {info.get('trailingPE', '정보 없음')}")
            st.write(f"**52주 최고가:** {info.get('fiftyTwoWeekHigh', '정보 없음')}")
            st.write(f"**추천 의견:** {info.get('recommendationKey', '정보 없음')}")

            st.subheader("📌 자동 판단 분석")
            current = info.get('currentPrice')
            high52 = info.get('fiftyTwoWeekHigh')

            if current and high52:
                ratio = current / high52
                if ratio < 0.7:
                    st.success("✅ 저평가된 종목입니다. 매수 타이밍일 수 있습니다.")
                elif ratio > 0.95:
                    st.warning("⚠️ 고점에 가까운 가격입니다. 매도 유의!")
                else:
                    st.info("📌 중립 구간입니다. 추세 확인이 필요합니다.")

            st.subheader("📰 관련 뉴스 (참고용)")
            st.markdown("※ 뉴스 데이터는 외부 API 또는 크롤링 기능 추가 필요")
            st.markdown("- 예시: 삼성전자, 새로운 반도체 라인 가동 예정")
            st.markdown("- 예시: 외국인 투자자 순매수 증가")

    except Exception as e:
        st.error(f"❌ 오류 발생: {str(e)}")
