from datetime import datetime
import auto_youtube as youtube
import time_tasks as time_tasks

status = True
print("Youtube Music 자동화 프로그램 입니다")
print("현재 시간은", str(datetime.now())[:-7], "입니다.")

time_table = time_tasks.time_table()
print(time_table)

while status:
    user_setting = youtube.is_setting_user()
    
    if not user_setting.status:
        user_setting.login()
        break

    break


    
