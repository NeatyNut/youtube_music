import pandas as pd
from datetime import datetime

class time_table:
    ## 실행 시
    def __init__(self) -> None:
        self.time_table = pd.read_excel("C:/Users/user/Desktop/작업중/노래DB예시.xlsx")
        self.times = self.time_table['시간'].apply(lambda x:x.replace('"','')).to_list()
        self.tasks = self.time_table['요청사항'].array.tolist()

class task:
    def __init__(self, time_table) -> None:
        self.times = time_table.times
        self.tasks = time_table.tasks
        self.now_hour = datetime.now().hour
        self.now_minute = datetime.now().minute

    def _time_reload(self):
        self.now_hour = datetime.now().hour
        self.now_minute = datetime.now().minute

    def time_task(self, index=0):
        ## 시간 업데이트
        self._time_reload()
        
        ## 현재시간과 비교
        for idx, i in enumerate(self.times[index:]):
            time = i.split(":")
            time_hour = int(time[0])
            time_minute = int(time[1])

            ## 재귀 호출
            if self.now_hour > time_hour:
                return self.time_task(index+idx+1)

            if self.now_hour == time_hour:
                if self.now_minute >= time_minute:
                    return self.time_task(index+idx+1)
                else:
                    return self.tasks[index + idx - 1]
            else:
                return self.tasks[index + idx - 1]