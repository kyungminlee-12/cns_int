import streamlit as st
import sqlalchemy
import pandas as pd
import streamlit_shadcn_ui as ui
from streamlit_extras.colored_header import colored_header 
from PIL import Image

# https://docs.streamlit.io/develop/tutorials/databases/mysql

# from time import sleep
# from streamlit_option_menu import option_menu
# from streamlit_shadcn_ui import slider, input, textarea, radio_group, switch
# from streamlit_extras.stylable_container import stylable_container


im = Image.open("images/main_logo_green.png")

# 1752, 680
image_resize = im.resize((219, 85))

# 페이지 기본 설정
st.set_page_config(
    page_icon = image_resize ,
    page_title = "CNS INT" ,
    layout= "wide"
)

st.image(image_resize)  # caption='CNS INT'


st.header('Carbon Negative Solution', divider='green')
# st.subheader('CNS INT는 미세조류를 활용하여 이상화탄소를 제거하는 B-CCRT 플랫폼을 개발하고 운영하는 기업입니다.')
# st.header('_Streamlit_ is :blue[cool] :sunglasses:')

# st.markdown('''CNS INT는 :green[**미세조류**]를 활용하여 **이산화탄소**를 제거하는 B-CCRT 플랫폼을 개발하고 운영하는 기업입니다.''')
st.markdown(' ')

def example():
    colored_header(
        label="우리는 미세조류로 [ 이산화탄소 ] 문제에 대한 해결책을 제시합니다.",
        description="CNS INT는 미세조류를 활용하여 이상화탄소를 제거하는 B-CCRT 플랫폼을 개발하고 운영하는 기업입니다.",
        color_name="green-70",
        # color_name="violet-70",
    )
# example()

# st.write("DB username:", st.secrets["db_username"])
# st.write("DB password:", st.secrets["db_password"])
# st.write(st.secrets)

conn = st.connection('dbx', type='sql')
table_name="co2_discharged_res"  

@st.experimental_fragment(run_every="2s")
def show_amt_c02_discharged_test():
    select_data_query = """SELECT * FROM device_data.{} ;""".format(table_name)
    cur_c02_discharged = conn.query(select_data_query, ttl=3)
    df_co2 = pd.DataFrame(cur_c02_discharged)

    all_res = df_co2.iloc[0]["res_value"]
    hour_res = df_co2.iloc[1]["res_value"]
    min_res = df_co2.iloc[2]["res_value"]

    if all_res is None:
        all_res = 0
    if hour_res is None:
        hour_res = 0
    if min_res is None:
        min_res = 0
    
    cur_all_res  = float(all_res)  
    cur_hour_res = float(hour_res)   
    cur_min_res  = float(min_res)   

    cols = st.columns(3)
    with cols[0]:
        ui.card(title="TOTAL", content=cur_all_res, description= "total CO2 reduction" , key="card1").render()
    with cols[1]:
        ui.card(title="CURRENT HOUR", content=cur_hour_res, description="CO2 reduction within 1 hour", key="card2").render()
    with cols[2]:
        ui.card(title="CURRENT MIN", content=cur_min_res, description="CO2 reduction within 1 minute", key="card3").render()

    st.write("date time: ", df_co2.loc[df_co2['id']=='MIN']["date_time"])

show_amt_c02_discharged_test()



# @st.experimental_fragment(run_every="2s")
# def show_amt_c02_discharged_per_min():
#     table_name="co2_discharged_min"  
#     select_data_query = """SELECT removed_amount, updated_date_time 
#                             FROM device_data.{}  
#                             order by updated_date_time desc
#                             LIMIT 20
#                             ;""".format(table_name)
#     datas_per_min = conn.query(select_data_query, ttl=3)
#     df_per_min = pd.DataFrame(datas_per_min)
#     st.dataframe(datas_per_min)
#     st.line_chart(df_per_min, y=['removed_amount'])

# show_amt_c02_discharged_per_min()


# cols = st.columns((1, 1, 2))

# cols[0].metric("Temperature", "70 °F", "1.2 °F")
# cols[0].metric("Humidity", "86%", "4%")
# cols[0].metric("Wind", "9 mph", "-8%")
