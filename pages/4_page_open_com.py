import streamlit as st
import serial
from sqlalchemy import text

# 페이지 기본 설정
st.set_page_config(
    # page_icon = ""
    page_title = "insert data" ,
    layout= "wide"
)

st.header('DB 저장 화면')
st.subheader('선택한 Device에서 들어오는 데이터 저장')


# 사이드바에 select box를 활용하여 종을 선택한 다음 그에 해당하는 행만 추출하여 데이터프레임을 만들고자합니다.
st.sidebar.title('Device 설정 화면')
select_device = st.sidebar.selectbox(
    'Device: ',
    ['COM3', 'COM4', 'COM5']
)
select_bit_sec = st.sidebar.selectbox(
    '비트/초(b): ',
    ['9600','19200']
)
select_location = st.sidebar.selectbox(
    '위치 데이터: ',
    ['화성','위치2', '위치3']
)

print("select_device:", select_device)
print("select_bit_sec:", select_bit_sec)
print("select_bit_sec:", select_bit_sec)

# serial 상태 값
ser = serial.Serial()     # 시리얼 연결
ser.timeout = 0.5  
ser.port = select_device  # 연결 port
ser.baudrate = 9600

if 'com_on_clicked' not in st.session_state:
    st.session_state.com_on_clicked = False

if 'com_off_clicked' not in st.session_state:
    st.session_state.com_off_clicked = False

def click_com_on_button():
    st.session_state.com_on_clicked = True
    st.session_state.com_off_clicked = False
def click_com_off_button():
    st.session_state.com_off_clicked = True
    st.session_state.com_on_clicked = False

st.button('Click ON' , on_click=click_com_on_button)
st.button('Click OFF', on_click=click_com_off_button)

if st.session_state.com_on_clicked:
    conn = st.connection('mysql', type='sql')
    ser.open()
    count = 1
    data_type_bytes = 1
    table_name=""

    while not st.session_state.com_off_clicked: 
        id = ''
        data_type = ''
        data_value = ''

        id_tf = False
        data_type_tf = False

        oneByte = ser.read(1)    # X 값
        new_val = oneByte.decode()
        if (new_val == "X"): 
            pass
        else: continue
        
        oneByte = ser.read(1)    # id 값
        id = oneByte.decode()

        # CO2 농도 데이터 혹은 SD 데이터
        if (id=="1" or id == "2"):  
            data_type_bytes = 3  
            bytes = ser.read(3)     # data_type 값
            data_type = bytes.decode()

        # LOT state 데이터
        else:                       
            data_type_bytes = 2
            table_name = "lot_state"
            bytes = ser.read(1)         # data_type 값
            new_val = bytes.decode()
            data_type +=new_val
            if new_val == "R":          # 데이터 타입 R+2byte
                oneByte = ser.read(2)
                data_type += oneByte.decode()
            else:                       # 데이터 타입 2byte
                oneByte = ser.read(1)
                data_type += oneByte.decode()

        if data_type in ("CDI", "CDO"):     # CO2 데이터
            bytes = ser.read(5)    # data_value 값
            data_value = bytes.decode()
            table_name = "co2_concentration"
        elif data_type in ("FDI", "FDO"):   # SD 데이터
            bytes = ser.read(4)    # data_value 값
            data_value = bytes.decode()
            table_name = "sd_data"
        elif data_type in ("RPD", "RTD"):   # LOT PH / 온도
            bytes = ser.read(4)    # data_value 값
            data_value = bytes.decode()
        elif data_type in ("SD", "MD"):     # LOT state
            bytes = ser.read(2)    # data_value 값
            data_value = bytes.decode()
        else: 
            # 알맞은 데이터 아님
            print("wrong data")
            print("id: %s, data_type: %s, data_value: %s" % (id, data_value, data_value) )
            continue


        with conn.session as session:
            insert_lot_state_data_query=text("INSERT INTO %s (id, data_type, data_value) VALUES(:id, :data_type, :data_value);" % (table_name))
            session.execute(insert_lot_state_data_query , params = dict(id = id, data_type=data_type, data_value=data_value))
            session.commit()

        print("count: %s, id: %s, data_type: %s, data_value: %s" % (count, id, data_type, data_value))

        count += 1
        if count > 50:
            break

    ser.close()
