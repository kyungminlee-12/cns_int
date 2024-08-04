import streamlit as st
from streamlit import connections
from local_components import card_container
import streamlit_shadcn_ui as ui
import pandas as pd
from streamlit_shadcn_ui import slider, input, textarea, radio_group, switch
from PIL import Image
import numpy as np

# 페이지 기본 설정
# st.set_page_config(
#     # page_icon = ""
#     page_title = "LOT state" ,
#     layout= "wide"
# )

im = Image.open("images\main_logo_green.png")

# 1752, 680
image_resize = im.resize((219, 85))

# 페이지 기본 설정
st.set_page_config(
    page_icon = image_resize ,
    page_title = "CNS INT" ,
    layout= "wide"
)

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

# st.write(select_com_port)
# st.write(new_location_id(select_com_port).iloc[0]["id"])

st.header('LOT STATE')
st.subheader('데이터 상태 표 입니다.')

conn = st.connection('mysql', type='sql')
# THEN concat(sub_str(A.data_value, 1, 2) , '.' sub_str(A.data_value, 3, 2) ) 

@st.experimental_fragment(run_every="3s")
def show_lot_state_table():
    select_data_query = """ SELECT A.ID AS "LOT_ID", 
                                max(CASE WHEN A.data_type = "RPD" 
                                        THEN concat(SUBSTRING(A.data_value, 1, 2) , '.', SUBSTRING(A.data_value, 3, 2) ) 
                                    END
                                    ) AS PH,
                                max(CASE WHEN A.data_type = "RTD"   
                                    THEN concat(SUBSTRING(A.data_value, 1, 2) , '.', SUBSTRING(A.data_value, 3, 2) ) 
                                    END
                                    ) AS TEMP,
                                max(CASE WHEN A.data_type = "SD" and A.data_value in ('55', 'A5') THEN 'OFF'
                                         WHEN A.data_type = "SD" and A.data_value in ('5A', 'AA') THEN 'ON'
                                  END
                                    ) AS "AIR 밸브",
                                max(CASE WHEN A.data_type = "SD" and A.data_value in ('55', '5A') THEN 'OFF'
                                         WHEN A.data_type = "SD" and A.data_value in ('A5', 'AA') THEN 'ON'
                                    END
                                    ) AS "CO2 밸브",
                                max(CASE WHEN A.data_type = "MD"  and A.data_value ='FF' THEN '오토'
                                         WHEN A.data_type = "MD"  and A.data_value ='00' THEN '매뉴얼'
                                    END
                                    ) AS "CO2 모드",
                                max(DATE(date_time)) "날짜", 
                                MIN(DATE_FORMAT(date_time, '%H:%i:%s')) as "시간" 
                            FROM  device_data.LOT_STATE A ,
                                (SELECT location_id, id, data_type, MAX(date_time) AS MAX_DATETIME
                                    FROM device_data.LOT_STATE 
                                    GROUP BY location_id, id, data_type
                                ) B
                            WHERE A.ID = B.ID
                                AND A.DATA_TYPE = B.DATA_TYPE
                                AND A.DATE_TIME = B.MAX_DATETIME
                                AND A.location_id = B.location_id
                                AND A.location_id = '{}'
                            GROUP BY A.ID
                            ORDER BY A.ID
                            ;""".format(new_location_id(select_com_port).iloc[0]["id"])

    # df.index = np.arange(1, len(df) + 1)
    df = conn.query(select_data_query, ttl=3)
    df.index = np.arange(1, len(df) + 1)
    # df.style.apply(lambda x: "background-color: red")
    # new_df = pd.DataFrame(df)

    # invoice_df = pd.DataFrame(df)

    # with card_container(key="table1"):
    #     ui.table(data=invoice_df, maxHeight=300)


    # pd.set_option('display.max_columns', 100)
    # st.dataframe(df, height=738)
    st.table(df)   # .set_index('column', inplace=True)
    # with card_container(key="table1"):
        # st.table(df)
        # .from_pandas(df).classes('max-h-40')
        # invoice_df = pd.DataFrame(df)
        # ui.table(data=invoice_df, maxHeight=300)

show_lot_state_table()


# Creating a DataFrame
# invoice_df = pd.DataFrame(data)
# ui.table(data=invoice_df, maxHeight=300)
# st.write(ui.table)

st.markdown("각 ID 별로 가장 최근 PH, 온도, AIR, C02 데이터를 보여줍니다.")
st.markdown("최근 1분간 들어온 데이터가 없을 경우 해당 값은 NULL로 표시됩니다.")


