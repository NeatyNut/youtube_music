import pandas as pd
from datetime import datetime
from tabulate import tabulate
import os

class time_table:
    ## 실행 시
    def __init__(self) -> None:
        try :
            self.time_table = pd.read_excel("Y:/youtube_db/노래Table.xlsx", sheet_name="TIME_TABLE")
            self.list_table = pd.read_excel("Y:/youtube_db/노래Table.xlsx", sheet_name="추천목록")
        except :
            self.time_table = pd.read_excel(os.path.join(os.getcwd(), "예비노래Table.xlsx"), sheet_name="TIME_TABLE")
            self.list_table = pd.read_excel(os.path.join(os.getcwd(), "예비노래Table.xlsx"), sheet_name="추천목록")

        ## 시간 또는 선택이 nan일 경우 삭제
        self.time_table = self.time_table.dropna(subset=self.time_table.columns[:2], how='any', axis=0)
        self.list_table = self.list_table.drop_duplicates(subset=self.list_table.columns[0], keep='first')

        self.times = self.time_table[self.time_table.columns[0]].apply(lambda x:x.replace('"','')).to_list()
        
        ## left join
        concat_list = pd.merge(self.time_table.iloc[:,1:], self.list_table, how='left', on=self.list_table.columns[0])
        self.tasks = []

        ## maping 처리
        for i in range(len(concat_list)):
            if concat_list.iloc[i,0] == self.list_table[self.list_table.columns[0]][0]:
                self.tasks.append(concat_list.iloc[i,1])
            else :
                self.tasks.append(concat_list.iloc[i,2])
    
    def show_task(self):
        tabulate.WIDE_CHARS_MODE = False
        print(tabulate(self.time_table.values, headers=self.time_table.columns, tablefmt='pretty'))

class task:
    def __init__(self, time_table) -> None:
        self.times = time_table.times
        self.tasks = time_table.tasks
        now = datetime.now()
        self.now_hour = now.hour
        self.now_minute = now.minute

    def _time_reload(self):
        now = datetime.now()
        self.now_hour = now.hour
        self.now_minute = now.minute

    def time_task(self, index=0):
        # 시간 업데이트
        self._time_reload()

        # 현재 시간 기준으로 테이블의 시간 확인
        for idx, time_str in enumerate(self.times):
            time_hour, time_minute = map(int, time_str.split(":"))

            # 현재 시간보다 시간이 크면 바로 이전 task 반환
            if self.now_hour < time_hour or (self.now_hour == time_hour and self.now_minute < time_minute):
                return self.tasks[max(idx - 1, 0)]  # idx가 0일 경우 처리

        # 모든 시간이 지나갔을 경우 마지막 task 반환
        return self.tasks[-1]