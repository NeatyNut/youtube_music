import pandas as pd
from datetime import datetime
from tabulate import tabulate
import tkinter as tk
from tkinter import filedialog
import os
import warnings

class time_table:
    ## 실행 시
    def __init__(self) -> None:
        config_name = os.path.join(os.getcwd(), "xlsx_config.ini")
        if not os.path.exists(config_name):
            with open(config_name, 'w', encoding='utf-8') as address:
                pass
        
        ## 경고 문구 지우기
        warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

        while True:
            with open(config_name, 'r', encoding='utf-8') as address:
                self.config_file = address.read()
            
            if self.config_file == "":
                root = tk.Tk()
                root.withdraw()  # 기본 창을 숨김

                # 파일 선택 대화 상자 열기
                self.config_file = filedialog.askopenfilename(title="노래Table을 선택하세요", 
                                            filetypes=[("xlsx 파일", "*.xlsx")])

                # 파일 미선택 시
                if self.config_file == "":
                    self.status = False
                    print("프로그램을 종료합니다.")
                    break
                else :
                    with open(config_name, 'w', encoding='utf-8') as address:
                        address.write(self.config_file)

            try :
                ## 파일 읽기
                self.onoff_table = pd.read_excel(self.config_file, sheet_name="ONOFF", dtype=str)
                self.time_table = pd.read_excel(self.config_file, sheet_name="TIME_TABLE", dtype=str)
                self.list_table = pd.read_excel(self.config_file, sheet_name="추천목록", dtype=str)
                
                ## 1. ONOFF
                self.on_hour, self.on_minute = self.onoff_table[self.onoff_table[self.onoff_table.columns[0]] == 'ON'].iloc[0, 1].replace('"','').split(":")
                self.on_hour = int(self.on_hour)
                self.on_minute = int(self.on_minute)
                
                self.off_hour, self.off_minute = self.onoff_table[self.onoff_table[self.onoff_table.columns[0]] == 'OFF'].iloc[0, 1].replace('"','').split(":")
                self.off_hour = int(self.off_hour)
                self.off_minute = int(self.off_minute)

                if self.onoff_table[self.onoff_table[self.onoff_table.columns[0]] == 'PAUSE'].iloc[0, 1] != "" and self.onoff_table[self.onoff_table[self.onoff_table.columns[0]] == 'PAUSE'].iloc[0, 2] != "":
                    self.pause_hour, self.pause_minute = self.onoff_table[self.onoff_table[self.onoff_table.columns[0]] == 'PAUSE'].iloc[0, 1].replace('"','').split(":")
                    self.pause_hour = int(self.pause_hour)
                    self.pause_minute = int(self.pause_minute)
                    self.pause_time = self.onoff_table[self.onoff_table[self.onoff_table.columns[0]] == 'PAUSE'].iloc[0, 2]
                else :
                    self.pause_hour = 0
                    self.pause_minute = 0
                    self.pause_time = 0

                ## 2. task 정의 / 시간 또는 선택이 nan일 경우 삭제
                self.time_table = self.time_table.dropna(subset=self.time_table.columns[:2], how='any', axis=0)
                self.list_table = self.list_table.drop_duplicates(subset=self.list_table.columns[0], keep='first')
                self.times = self.time_table[self.time_table.columns[0]].apply(lambda x:x.replace('"','')).to_list()

                ## 2. task 정의 / left join
                concat_list = pd.merge(self.time_table.iloc[:,1:], self.list_table, how='left', on=self.list_table.columns[0])
                self.tasks = []

                ## 2. task 정의 / maping 처리
                del_count = 0
                for i in range(len(concat_list)):
                    if concat_list.iloc[i,0] == self.list_table[self.list_table.columns[0]][0]:
                        if str(concat_list.iloc[i,1]) == "nan" or ('http' in str(concat_list.iloc[i,1]) and not "music.youtube" in str(concat_list.iloc[i,1])) :
                            self.time_table = self.time_table.drop(index=i)
                            del self.times[i - del_count]
                            del_count += 1
                        else :
                            self.tasks.append(concat_list.iloc[i,1])
                    else :
                        if str(concat_list.iloc[i,2]) == "nan" or 'http' in str(concat_list.iloc[i,2]) and not "music.youtube" in str(concat_list.iloc[i,2]):
                            self.time_table = self.time_table.drop(index=i)
                            del self.times[i - del_count]
                            del_count += 1
                        else :
                            self.tasks.append(concat_list.iloc[i,2])
                self.status = True
                
                ## 정지
                break
            except Exception as e:
                with open(config_name, 'w', encoding='utf-8') as address:
                    pass
                
                print(f"파일 처리 예외 발생: {e}")
                continue


    def show_task(self):
        tabulate.WIDE_CHARS_MODE = False
        print("ON TIME : " + str(self.on_hour).zfill(2) + ":" + str(self.on_minute).zfill(2))
        if not self.pause_hour == 0:
            print("PAUSE TIME : " + str(self.pause_hour).zfill(2) + ":" + str(self.pause_minute).zfill(2) + "부터 " + str(self.pause_time) + "시간 동안 멈춤")
        print("OFF TIME : " + str(self.off_hour).zfill(2) + ":" + str(self.off_minute).zfill(2))
        print()
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