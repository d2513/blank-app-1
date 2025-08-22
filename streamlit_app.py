import streamlit as st
import billboard

# --- 페이지 설정 ---
st.set_page_config(
    page_title="Billboard Hot 100",
    page_icon="🎵",
    layout="wide"
)

# --- 데이터 로딩 함수 ---
# @st.cache_data 데코레이터를 사용하여 API 응답을 캐싱합니다.
# 3600초(1시간) 동안 캐시가 유지됩니다.
@st.cache_data(ttl=3600)
def get_billboard_hot100():
    """Billboard Hot 100 차트 데이터를 가져옵니다."""
    try:
        chart = billboard.ChartData('hot-100')
        return chart
    except Exception as e:
        st.error(f"차트 데이터를 불러오는 데 실패했습니다: {e}")
        return None

# --- UI 그리기 ---

# 1. 빌보드 로고 표시
st.image(
    "https://media.discordapp.net/attachments/1337072239505445007/1408300733132046379/image.png?ex=68a93dc3&is=68a7ec43&hm=e2f7e7a0a62de5eaff419d4aeb31d7b134e8a3187ab72abd0da2a7794ccbdbac&=&format=webp&quality=lossless&width=1212&height=824",
    width=300
)
st.title("The Hot 100 Chart")
st.markdown("---")

# 2. 차트 데이터 불러오기 및 표시
chart_data = get_billboard_hot100()

if chart_data:
    st.write(f"**🗓️ 이번 주 차트 ({chart_data.date})**")

    # 헤더
    header_cols = st.columns([0.5, 1, 4, 3])
    header_cols[0].markdown("**순위**")
    header_cols[1].markdown("**앨범 커버**")
    header_cols[2].markdown("**제목**")
    header_cols[3].markdown("**아티스트**")
    st.markdown("---")

    # 3. 차트 목록을 순서대로 표시 (1위부터 100위까지)
    for song in chart_data:
        # 각 곡의 정보를 컬럼으로 나눔
        cols = st.columns([0.5, 1, 4, 3])

        # 순위 표시
        cols[0].markdown(f"## {song.rank}")

        # 앨범 커버 표시
        # 이미지 URL이 유효한지 확인
        try:
            # billboard.py 라이브러리는 때때로 이미지 URL을 가져오지 못할 수 있습니다.
            # 이 경우를 대비해 기본 이미지 URL을 준비합니다.
            image_url = song.image
            if not image_url:
                raise ValueError("No image URL")
        except (AttributeError, ValueError):
            image_url = "https://via.placeholder.com/150?text=No+Image" # 대체 이미지

        cols[1].image(image_url, width=100, caption=f"{song.title} Cover")

        # 곡 제목
        cols[2].markdown(f"### {song.title}")

        # 아티스트
        cols[3].markdown(f"#### {song.artist}")

        st.markdown("---") # 각 곡 사이에 구분선 추가

else:
    st.warning("빌보드 차트 정보를 가져올 수 없습니다. 잠시 후 다시 시도해주세요.")
