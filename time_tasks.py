import pandas as pd
from datetime import datetime
from tabulate import tabulate
import os

class time_table:
    ## 실행 시
    def __init__(self) -> None:
        try :
            self.time_table = pd.read_excel("Y:/youtube_db/노래Table.xlsx", sheet_name="TIME_TABLE")
        except :
            self.time_table = pd.read_excel(os.path.join(os.getcwd(), "예비노래Table.xlsx"), sheet_name="TIME_TABLE")

        ## 시간 또는 요청사항이 nan일 경우
        self.time_table = self.time_table.dropna(subset=self.time_table.columns[:2], how='any', axis=0)

        self.times = self.time_table['시간'].apply(lambda x:x.replace('"','')).to_list()
        self.tasks = self.time_table['요청사항'].array.tolist()
    
    def show_task(self):
        tabulate.WIDE_CHARS_MODE = False
        print(tabulate(self.time_table.values[:,:3], headers=self.time_table.columns[:3], tablefmt='pretty'))

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
        
        ## 테이블에 해당할 시간 없을 시
        if int(self.times[0].split(":")[0]) > self.now_hour:
            return self.tasks[0]

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
        
        if int(self.times[-1].split(":")[0]) <= self.now_hour:
            return self.tasks[-1]