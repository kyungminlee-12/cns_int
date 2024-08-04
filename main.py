import streamlit as st
from time import sleep
from streamlit_option_menu import option_menu
import pandas as pd
import streamlit_shadcn_ui as ui
from streamlit_shadcn_ui import slider, input, textarea, radio_group, switch

import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.colored_header import colored_header 
from PIL import Image


im = Image.open("images\main_logo_green.png")

# 1752, 680
image_resize = im.resize((219, 85))

# 페이지 기본 설정
st.set_page_config(
    page_icon = image_resize ,
    page_title = "CNS INT" ,
    layout= "wide"
)

# 사이드바에 select box를 활용하여 종을 선택한 다음 그에 해당하는 행만 추출하여 데이터프레임을 만들고자합니다.
# st.sidebar.title('Location 설정')
# select_location = st.sidebar.selectbox(
#     '위치 데이터: ',
#     ['화성','위치2', '위치3']
# )

# print("select_location:", select_location)

# st.image('images\main_logo_green.png', caption='CNS INT')
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

conn = st.connection('mysql', type='sql')
table_name="co2_discharged_res"  

@st.experimental_fragment(run_every="2s")
def show_amt_c02_discharged_test():
    select_data_query = """SELECT * FROM device_data.{} ;""".format(table_name)
    cur_c02_discharged = conn.query(select_data_query, ttl=3)
    df_co2 = pd.DataFrame(cur_c02_discharged)

    cur_all_res  = float(df_co2.iloc[0]["res_value"])   # float(df_co2.loc[df_co2['id']=='ALL']["res_value"])
    cur_hour_res = float(df_co2.iloc[1]["res_value"])   # float(df_co2.loc[df_co2['id']=='HOUR']["res_value"])
    cur_min_res  = float(df_co2.iloc[2]["res_value"])   # float(df_co2.loc[df_co2['id']=='MIN']["res_value"])
    cols = st.columns(3)
    with cols[0]:
        ui.card(title="TOTAL", content=cur_all_res, description= "total CO2 reduction" , key="card1").render()
    with cols[1]:
        ui.card(title="CURRENT HOUR", content=cur_hour_res, description="CO2 reduction within 1 hour", key="card2").render()
    with cols[2]:
        ui.card(title="CURRENT MIN", content=cur_min_res, description="CO2 reduction within 1 minute", key="card3").render()

    st.write("date time: ", df_co2.loc[df_co2['id']=='MIN']["date_time"])

show_amt_c02_discharged_test()



@st.experimental_fragment(run_every="2s")
def show_amt_c02_discharged_per_min():
    table_name="co2_discharged_min"  
    select_data_query = """SELECT removed_amount, updated_date_time 
                            FROM device_data.{}  
                            order by updated_date_time desc
                            LIMIT 20
                            ;""".format(table_name)
    datas_per_min = conn.query(select_data_query, ttl=3)
    df_per_min = pd.DataFrame(datas_per_min)
    st.dataframe(datas_per_min)
    st.line_chart(df_per_min, y=['removed_amount'])

# show_amt_c02_discharged_per_min()


cols = st.columns((1, 1, 2))

cols[0].metric("Temperature", "70 °F", "1.2 °F")
cols[0].metric("Humidity", "86%", "4%")
cols[0].metric("Wind", "9 mph", "-8%")

# from streamlit_extras.altex import scatter_chart

# https://arnaudmiribel.github.io/streamlit-extras/extras/altex/
# @st.cache_data
# def example_line():
#     stocks = get_stocks_data()

#     scatter_chart(
#         data=stocks.query("symbol == 'GOOG'"),
#         x="date",
#         y="price",
#         title="A beautiful simple line chart",
#     )




# with cols:
# This column holds the data queried from the parts table.
# st.header("CO2 감소량 list:")


# st.write(df_co2["res_value"])
# st.write(df_co2.loc[df_co2['id']=='MIN'])
# st.write(df_co2.loc[df_co2['id']=='MIN']["res_value"])
# st.write(df_co2.iloc[3]["res_value"])


# 라인 그래프 데이터 생성 with Pandas
# chart_data = pd.DataFrame(
# 
#     columns= ["IN", "OUT"]
# )


