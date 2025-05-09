import datetime
import random

import requests
import json
import streamlit as st
import pandas as pd
# サイドバーでページ選択
page = st.sidebar.selectbox('Choose your page', ['users', 'rooms', 'bookings'])

# ------------------ ユーザー ------------------ #
if page == 'users':
    st.title('ユーザー登録画面')

    with st.form(key='user_form'):
        username: str = st.text_input('ユーザー名', max_chars=12)
        
        data = {
            'username': username
        }
        submit_button = st.form_submit_button(label='リクエスト送信')
    if submit_button:
      st.write('## 送信データ')
      st.write('## レスポンス結果')
      url = 'http://127.0.0.1:8001/users'
        
      res = requests.post(
            url,
            data=json.dumps(data)
        )
        

      if res.status_code == 200:
            st.success('ユーザー登録完了')
      st.write(res.status_code)
      st.json(res.json())


# ------------------ 会議室 ------------------ #

           

# ------------------ 会議室 ------------------ #
elif page == 'rooms':
    st.title('会議室登録画面')

    with st.form(key='room'):
        room_id: int = random.randint(0, 10)
        room_name: str = st.text_input('会議室名', max_chars=12)
        capacity: int = st.number_input('定員', step =1)
        data = {
            'room_id': room_id,
            'room_name': room_name,
            'capacity': capacity
        }
        submit_button = st.form_submit_button(label='会議室登録')

        if submit_button:
            url = 'http://127.0.0.1:8001/rooms'
            res = requests.post(url, data=json.dumps(data))
            if res.status_code == 200:
                st.success('会議室登録完了')
            # st.write(res.status_code)
            st.json(res.json())



            # 会議室予約画面
elif page == 'bookings':
    st.title('会議室予約画面')
    url_users = 'http://127.0.0.1:8001/users'
    res = requests.get(url_users)
    users = res.json()
    
    users_name = {}
    for user in users:
        users_name[user['username']] = user['user_id']
   

    url_rooms = 'http://127.0.0.1:8001/rooms'
    res = requests.get(url_rooms)
    rooms = res.json()
   
    rooms_name = {}
    for room in rooms:
                rooms_name[room['room_name']] = {
                    'room_id': room['room_id'],
                    'capacity': room['capacity']
                }
    
    st.write('### 会議室一覧')
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ['会議室名', '定員', '会議室ID']
    st.table(df_rooms)

    url_bookings = 'http://127.0.0.1:8001/bookings'
    res = requests.get(url_bookings)
    bookings = res.json()
    df_booking = pd.DataFrame(bookings)

    users_id = {}
    for user in users:
        users_id[user['user_id']] = user['username']

    rooms_id = {}
    for room in rooms:
        rooms_id[room['room_id']] = {
            'room_name': room['room_name'],
            'capacity': room['capacity']
        }

        #idを名前に変換
    to_username = lambda x: users_id.get(x, f"不明ユーザー({x})")
    to_room_name = lambda x: rooms_id.get(x, {}).get('room_name', f"不明会議室({x})")
    to_datename = lambda x: datetime.datetime.fromisoformat(x).strftime('%Y/%m/%d %H:%M')


    #特定の列に適用適用
    df_booking['user_id']=df_booking['user_id'].map(to_username) 
    df_booking['room_id']=df_booking['room_id'].map(to_room_name) 
    df_booking['start_datetime']=df_booking['start_datetime'].map(to_datename) 
    df_booking['end_datetime']=df_booking['end_datetime'].map(to_datename) 

    df_booking.rename(columns={
        'user_id': '予約者名',
        'room_id': '会議室名',
        'booked_num': '予約人数',
        'start_datetime': '開始時刻',
        'end_datetime': '終了時刻',
        'booking_id': '予約番号'
    }, inplace=True)
    st.write('### 予約一覧')
    st.table(df_booking)


    with st.form(key='booking'):
      # booking_id: int = random.randint(0, 10)
       username: str = st.selectbox('予約者名', users_name.keys())
       room_name: str = st.selectbox('予約者名', rooms_name.keys())
       booked_num: int = st.number_input('予約人数', step =1, min_value=1)
       date = st.date_input('日付',min_value=datetime.date.today()) 
       start_time = st.time_input('開始時刻：', value=datetime.time(hour=9, minute=0))
       end_time = st.time_input('終了時刻：', value=datetime.time(hour=20, minute=0))
       submit_button = st.form_submit_button(label='予約登録')
      
      

    if submit_button:
            user_id: int = users_name[username]
            room_id: int = rooms_name[room_name]['room_id']
            capacity: int = rooms_name[room_name]['capacity']
            data = {
              
              'user_id': user_id,
              'room_id': room_id,
              'booked_num': booked_num,
              'start_datetime': datetime.datetime(
                 year=date.year,
                 month=date.month,
                 day=date.day,
                 hour=start_time.hour,
                 minute=start_time.minute
            ).isoformat(),
           'end_datetime': datetime.datetime(
               year=date.year,
              month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute
            ).isoformat(),
        }
        # 定員以下の予約人数
            if booked_num <= capacity:
             st.write('## レスポンス結果')
             url = 'http://127.0.0.1:8001/bookings'
             res = requests.post(url, data=json.dumps(data))
             if res.status_code == 200:
                st.success('予約登録完了')
             st.json(res.json())
            else:
                st.error(f'{room_name}の定員は{capacity}名です。{capacity}以下の予約人数のみ受け付けております。')
