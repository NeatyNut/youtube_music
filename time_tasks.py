import pandas as pd
from datetime import datetime
from tabulate import tabulate
import tkinter as tk
from tkinter import filedialog
import os
import warnings

## 타임 테이블 접근
class time_table:
    def __init__(self) -> None:
        ### xlsx_config.ini 경로
        self.config_name = os.path.join(os.getcwd(), "xlsx_config.ini")

        ### xlsx_config.ini 파일이 없다면 빈문서로 생성
        if not os.path.exists(self.config_name):
            with open(self.config_name, 'w', encoding='utf-8') as address:
                pass

        ### openpyxl의 경고 문구 지우기
        warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
        ## 테이블 확인
        self._get_table()

    def _get_table(self):
        while True:
            ### xlsx_config.ini을 접근하여 xlsx 경로 획득
            with open(self.config_name, 'r', encoding='utf-8') as address:
                self.config_file = address.read()

            ### xlsx 경로가 없을 시, UI창 열기
            if self.config_file == "":
                root = tk.Tk()
                root.withdraw()  #### 기본 창을 숨김

                #### 파일 선택 대화 상자
                self.config_file = filedialog.askopenfilename(title="노래Table을 선택하세요",
                                            filetypes=[("xlsx 파일", "*.xlsx")])

                #### 파일 미선택 시
                if self.config_file == "":
                    self.status = False
                    print("프로그램을 종료합니다.")
                    break
                else :
                    #### 파일 선택 시, xlsx_config.ini에 Path 기록
                    with open(self.config_name, 'w', encoding='utf-8') as address:
                        address.write(self.config_file)

            ### xlsx 접근 후 데이터 가공 작업
            try :
                #### 시트별 자료 읽기
                self.onoff_table = pd.read_excel(self.config_file, sheet_name="ONOFF", dtype=str)
                self.time_table = pd.read_excel(self.config_file, sheet_name="TIME_TABLE", dtype=str)
                self.list_table = pd.read_excel(self.config_file, sheet_name="추천목록", dtype=str)

                #### 1. ON/OFF/PAUSE의 hour, minute, (time) 가공
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
                    self.pause_time = int(self.pause_time)
                else :
                    self.pause_hour = 0
                    self.pause_minute = 0
                    self.pause_time = 0

                #### 타임 테이블에서 시간, 선택 컬럼 둘 중 하나라도 비면 삭제
                self.time_table = self.time_table.dropna(subset=self.time_table.columns[:2], how='any', axis=0)

                #### 리스트 테이블에서 이름 기준 중복 제거
                self.list_table = self.list_table.drop_duplicates(subset=self.list_table.columns[0], keep='first')

                #### 타임 LIST 출력
                self.times = self.time_table[self.time_table.columns[0]].apply(lambda x:x.replace('"','')).to_list()

                ### 타임 테이블과 추천 목록 Leftjoin하여 시간 / URL 엮기
                concat_list = pd.merge(self.time_table.iloc[:,1:], self.list_table, how='left', on=self.list_table.columns[0])
                self.tasks = []

                ### ★ MAPPING 처리
                #### 리스트 인덱스 조정용 숫자
                del_count = 0

                #### Leftjoin한 데이터 반복
                for i in range(len(concat_list)):

                    #### 만약 "사용자지정(==리스트 테이블에서 가장 첫 번째 목록)"
                    if concat_list.iloc[i,0] == self.list_table[self.list_table.columns[0]][0]:

                        #### task란이 "nan" 이거나 http를 포함했지만, music.youtube가 아니라면 목록에서 삭제
                        if str(concat_list.iloc[i,1]) == "nan" or ('http' in str(concat_list.iloc[i,1]) and not "music.youtube" in str(concat_list.iloc[i,1])) :
                            self.time_table = self.time_table.drop(index=i)
                            del self.times[i - del_count]
                            del_count += 1
                        else :
                            #### 문제 없으면 추가
                            self.tasks.append(concat_list.iloc[i,1])

                    #### 사용자지정 외의 것들
                    else :
                        #### task란이 "nan" 이거나 http를 포함했지만, music.youtube가 아니라면 목록에서 삭제
                        if str(concat_list.iloc[i,2]) == "nan" or 'http' in str(concat_list.iloc[i,2]) and not "music.youtube" in str(concat_list.iloc[i,2]):
                            self.time_table = self.time_table.drop(index=i)
                            del self.times[i - del_count]
                            del_count += 1
                        else :
                            #### 문제 없으면 추가
                            self.tasks.append(concat_list.iloc[i,2])

                ### 프로그램 허용 Bool
                self.status = True

                ### 정지
                break
            except Exception as e:
                #### 파일 열다 오류 발생
                print(f"파일 처리 예외 발생: {e}")

                # #### xlsx_config.ini에 파일 경로 삭제
                # with open(self.config_name, 'w', encoding='utf-8') as address:
                #     pass

                #### 반복 요청
                continue

    def check_time_table(self):
        ## 테이블 확인
        ex_time_table = self.time_table
        ex_onoff_table = self.onoff_table
        self._get_table()

        if not ex_time_table.equals(self.time_table) or not ex_onoff_table.equals(self.onoff_table):
            print()
            print("시간표가 변경되어 Task를 새로이 업데이트 합니다.")
            print()
            ## 테이블 출력
            self.show_task()

    ### time 정보 출력
    def show_task(self):
        #### 시작 시간 표시
        print("ON TIME : " + str(self.on_hour).zfill(2) + ":" + str(self.on_minute).zfill(2))

        #### 멈춤 시간 표시
        if not self.pause_hour == 0:
            print("PAUSE TIME : " + str(self.pause_hour).zfill(2) + ":" + str(self.pause_minute).zfill(2) + "부터 " + str(self.pause_time) + "시간 동안 멈춤")

        #### 끄는 시간 표시
        print("OFF TIME : " + str(self.off_hour).zfill(2) + ":" + str(self.off_minute).zfill(2))

        #### 타임 테이블 그리기
        print()
        tabulate.WIDE_CHARS_MODE = False
        print(tabulate(self.time_table.values, headers=self.time_table.columns, tablefmt='pretty'))

## 테스크 뽑기 클래스
class task:
    def __init__(self, time_table) -> None:
        self.time_table = time_table
        now = datetime.now()
        self.now_hour = now.hour
        self.now_minute = now.minute

    ### 현재시간 요청
    def _time_reload(self):
        now = datetime.now()
        self.now_hour = now.hour
        self.now_minute = now.minute
        self.time_table.check_time_table()

    def time_task(self, index=0):
        ### (현재시간 요청)
        self._time_reload()

        ### 현재 시간 기준으로 테이블의 시간 확인
        for idx, time_str in enumerate(self.time_table.times):
            time_hour, time_minute = map(int, time_str.split(":"))

            #### 현재 시간보다 시간이 크면 바로 이전 task 반환
            if self.now_hour < time_hour or (self.now_hour == time_hour and self.now_minute < time_minute):
                return self.time_table.tasks[max(idx - 1, 0)]  #### idx가 0일 경우 처리

        #### 모든 시간이 지나갔을 경우 마지막 task 반환
        return self.time_table.tasks[-1]