import streamlit as st
from streamlit import connections
from local_components import card_container
import streamlit_shadcn_ui as ui
import pandas as pd

# 페이지 기본 설정
st.set_page_config(
    # page_icon = ""
    page_title = "SD In & Out" ,
    layout= "wide"
)

# 로딩바
# with st.spinner(text="페이지 로딩 중..."): sleep(1)

st.header('SD IN / OUT')
st.subheader('데이터 상태 표 입니다.')

conn = st.connection('mysql', type='sql')

@st.experimental_fragment(run_every="10s")
def location_table():
    select_data_query = """SELECT id, location_name, nation, location_name_eng
                            FROM device_data.location_table
                            ; """

    df = conn.query(select_data_query, ttl=600)
    return df

location_list = location_table().loc[:, ["location_name"] ]
# 사이드바에 select box를 활용하여 종을 선택한 다음 그에 해당하는 행만 추출하여 데이터프레임을 만들고자합니다.
st.sidebar.title('select location')

# 변수에 사용자가 선택한 값이 지정됩니다
select_com_port = st.sidebar.selectbox(
    '확인이 필요한 데이터의 위치를 선택해주세요',
    # ['LOT의 상태', 'CO2 농도 데이터', 'SD 데이터']
    location_list
)

@st.experimental_fragment(run_every="2s")
def new_location_id(loc_name):
    select_data_query = """SELECT id
                            FROM device_data.location_table
                            where location_name = '{}'
                            ; """.format(loc_name)

    location_id = conn.query(select_data_query, ttl=600)
    return location_id

table_name="sd_data"
split_second = "10"     # N초 단위로 끊기

# new_location_id(select_com_port).iloc[0]["id"]
@st.experimental_fragment(run_every="2s")
def show_SD_in_out_table():
    select_data_query = """SELECT 
                                avg(CASE WHEN data_type = "FDI" THEN data_value END) AS "IN",
                                avg(CASE WHEN data_type = "FDO" THEN data_value END) AS "OUT",
                                max(DATE(date_time)) "날짜", 
                                max(DATE_FORMAT(date_time, '%H:%i:%s')) as "시간"
                            FROM device_data.{}
                            WHERE location_id = '{}'
                            GROUP BY DATE(date_time), HOUR(date_time), minute(date_time), FLOOR(second(date_time)/{})
                            ORDER BY DATE(date_time) desc, HOUR(date_time) desc, minute(date_time) desc, FLOOR(second(date_time)/{}) desc
                            ;""".format(table_name, new_location_id(select_com_port).iloc[0]["id"], split_second, split_second)

    df = conn.query(select_data_query, ttl=3)
    st.dataframe(df, height=738)

    # st.line_chart(df)
    # res = pd.DataFrame(df)
    # with card_container(key="table1"):
    #     ui.table(data=res, maxHeight=300)

show_SD_in_out_table()


