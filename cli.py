from datetime import datetime
import auto_youtube as youtube
import time_tasks as time_tasks
import time

status = True
print("Youtube Music 자동화 프로그램 입니다")
print("현재 시간은", str(datetime.now())[:-7], "입니다.")

time_table = time_tasks.time_table()
time_table.show_task()


user_setting = youtube.is_setting_user()

if not user_setting.status:
    user_setting.login()

tasks = time_tasks.task(time_table)
query = ""
auto_song = youtube.auto_youtube()

while status:
    ## 새로운 task 있는 지 확인
    now_query = tasks.time_task()
    
    if now_query == "":
        now_query = query

    ## 특정 시간 시 자동 종료
    if datetime.now().hour > 18 or datetime.now().hour < 9:
        status = False
        break
    ## 점심 시간 자동 종료
    elif datetime.now().hour == 12 and datetime.now().minute >= 30:
        auto_song.quit()
        time.sleep(3600)
        continue
    
    ## 새로운 task가 있다면
    if query != now_query:
        query = now_query
        auto_song.quit()
        try :
            auto_song = youtube.auto_youtube()
            if "http" in query:
                auto_song.url_open(query)
            else :
                auto_song.query_open(query)
        except :
            continue
        
        # 10분 마다 확인
        time.sleep(600)
    else:
        # 10분 마다 확인
        time.sleep(600)