import streamlit as st
from time import sleep
from streamlit_option_menu import option_menu

# 페이지 기본 설정
st.set_page_config(
    # page_icon = ""
    page_title = "" ,
    layout= "wide"
)

# import SessionState

#session_state = SessionState.get(button_1=False)

# with st.sidebar:
#         menu = option_menu('Menu',['Home','EDA','ML'], icons = ['house-door-fill','bar-chart-line-fill','gear-wide-connected'],menu_icon="caret-down-fill", default_index=0,
#                          styles={
#         "container": {"padding": "5!important", "background-color": "#fafafa"},
#         "icon": {"color": "#243746", "font-size": "25px"}, 
#         "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
#         "nav-link-selected": {"background-color": "#ef494c"},})

# 로딩바
# with st.spinner(text="페이지 로딩 중..."): sleep(1)
st.header('데이터')
st.subheader('데이터 상태 표 입니다.')


# 사이드바에 select box를 활용하여 종을 선택한 다음 그에 해당하는 행만 추출하여 데이터프레임을 만들고자합니다.
st.sidebar.title('data selection')

# 변수에 사용자가 선택한 값이 지정됩니다
select_com_port = st.sidebar.selectbox(
    '확인하고 싶은 데이터를을 선택하세요',
    ['LOT의 상태', 'CO2 농도 데이터', 'SD 데이터']
)
table_name=""
if select_com_port == 'LOT의 상태':
    table_name = "lot_state"
    # st.rerun()
elif select_com_port == 'SD 데이터':
    table_name = "sd_data"
    # st.rerun()
    # st.experimental_rerun()
elif select_com_port == 'CO2 농도 데이터':
    table_name = "co2_concentration"
    # st.rerun()
    # st.experimental_rerun()

conn = st.connection('mysql', type='sql')

table_selected=table_name

@st.cache_data
def table_show(table_selected):
    select_data_query = """SELECT id, data_type, data_value
                            FROM ({}) 
                            ORDER BY date_time DESC
                            LIMIT 20
                            ; """.format(table_selected)

    df = conn.query(select_data_query, ttl=600)
    return df

st.dataframe(table_show(table_name))

