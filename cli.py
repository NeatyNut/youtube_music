from datetime import datetime
import auto_youtube as youtube
import time_tasks as time_tasks
import time
import os

## 프로그램 시작
print("Youtube Music 자동화 프로그램 입니다")
print("현재 시간은", str(datetime.now())[:-7], "입니다.")

## (타임 테이블 클래스 생성)
time_table = time_tasks.time_table()

## 오류 발생 시, 창 띄워두기 위한 bool
pause_status = True

## (타임 테이블 클래스 생성) 후 제대로 테이블을 불러왔을 때
if time_table.status:
    ### 각종 시간 정보 출력
    time_table.show_task()

    ### (구글 계정 세팅 클래스 생성)
    user_setting = youtube.is_setting_user()

    ### 로그인 상태 확인
    if not user_setting.status:
        user_setting.login() #### 로그인 요청

    ### (태스크 뽑기 클래스 생성)
    tasks = time_tasks.task(time_table)
    query = ""

    ### (타임 테이블 클래스 프로그램 허용 Bool)
    while time_table.status:
        now_time = datetime.now() #### 현재시간 뽑기
        
        #### <ON TIME 확인>
        if now_time.hour < time_table.on_hour or (now_time.hour == time_table.on_hour and now_time.minute < time_table.on_minute):
            pause_time = (time_table.on_hour - now_time.hour)*3600 + (now_time.minute - now_time.minute)*60 ##### 시, 분 차를 계산
            print(f"{str(pause_time)}초 후 노래를 실행합니다.")
            time.sleep(pause_time)
            continue

        #### <크롬 드라이버 시작>
        if query == "":
            auto_song = youtube.auto_youtube()
            print("음악 플레이를 시작합니다.")

        #### <OFF TIME 확인>
        if now_time.hour > time_table.off_hour or (now_time.hour == time_table.off_hour and now_time.minute >= time_table.off_minute):
            auto_song.quit()
            query = ""
            time_table.status = False
            pause_status = False #### 창 끄기 위한 bool
            print("5초 후 프로그램을 종료합니다.")
            time.sleep(5)
            break
        
        #### <PAUSE TIME 확인>
        if now_time.hour == time_table.pause_hour and now_time.minute >= time_table.pause_minute:
            auto_song.quit()
            query = ""
            print(f"{str(time_table.pause_hour).zfill(2)}:{str(time_table.pause_minute).zfill(2)}부터 PAUSE 중")
            time.sleep(time_table.pause_time*3600 - (datetime.now().minute - time_table.pause_minute)*60) ##### 분 오차를 계산
            continue
        
        #### 시간대 task 요청
        now_query = tasks.time_task()

        #### task가 바뀐 것에 대한 처리
        if query != now_query and now_query != "":
            query = now_query
            
            ##### 셀레니움 에러에 대한 처리
            try :
                if "http" in query:
                    if not auto_song.url_open(query):
                        ##### 프로그램 종료
                        time_table.status = False
                        print("5초 후 파일이 종료됩니다.")
                        time.sleep(5)
                        break
                else :
                    if not auto_song.query_open(query):
                        ##### 프로그램 종료
                        time_table.status = False
                        print("5초 후 파일이 종료됩니다.")
                        time.sleep(5)
                        break
            except :
                continue
            
            #### 10분 뒤 확인
            time.sleep(600)
        else:
            #### 10분 뒤 확인
            time.sleep(600)

#### 에러로 인한 종료 시
if pause_status:
    os.system("pause")
else :
    ##### 컴퓨터 종료
    os.system("shutdown -l")
    os.system("shutdown -s -t 0")