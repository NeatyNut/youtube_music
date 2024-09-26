from datetime import datetime
import auto_youtube as youtube
import time_tasks as time_tasks
import time


print("Youtube Music 자동화 프로그램 입니다")
print("현재 시간은", str(datetime.now())[:-7], "입니다.")

time_table = time_tasks.time_table()

if time_table.status:
    time_table.show_task()

    user_setting = youtube.is_setting_user()

    if not user_setting.status:
        user_setting.login()

    tasks = time_tasks.task(time_table)
    query = ""

    while time_table.status:
        now_time = datetime.now()
        
        ## 1. ON TIME
        if not now_time.hour > time_table.on_hour or (now_time.hour == time_table.on_hour and now_time.minute >= time_table.on_minute):
            pause_time = (time_table.on_hour - now_time.hour)*60 + (now_time.minute - now_time.minute)
            print(f"{str(pause_time)}초 후 노래를 실행합니다.")
            time.sleep(pause_time)
            continue

        ## 유튜브 시작
        if query == "":
            auto_song = youtube.auto_youtube()

        ## 2. OFF TIME
        if now_time.hour > time_table.off_hour or (now_time.hour == time_table.off_hour and now_time.minute >= time_table.off_minute):
            auto_song.quit()
            query = ""
            status = False
            print("5초 후 프로그램을 종료합니다.")
            time.sleep(5)
            break
        
        ## 3. PAUSE TIME
        if now_time.hour == time_table.pause_hour and now_time.minute >= time_table.pause_minute:
            auto_song.quit()
            query = ""
            print(f"{str(time_table.pause_hour).zfill(2)}:{str(time_table.pause_minute).zfill(2)}부터 PAUSE 중")
            time.sleep(time_table.pause_time*3600 - (datetime.now().minute - time_table.pause_minute)*60)
            continue
        
        ## 새로운 task 있는 지 확인
        now_query = tasks.time_task()

        ## 새로운 task가 있다면
        if query != now_query and now_query != "":
            query = now_query
            try :
                if "http" in query:
                    if not auto_song.url_open(query):
                        time_table.status = False
                        print("5초 후 파일이 종료됩니다.")
                        time.sleep(5)
                        break
                else :
                    if not auto_song.query_open(query):
                        time_table.status = False
                        print("5초 후 파일이 종료됩니다.")
                        time.sleep(5)
                        break
            except :
                continue
            
            # 10분 마다 확인
            time.sleep(600)
        else:
            # 10분 마다 확인
            time.sleep(600)