from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import shutil
import os
import time

## 셀레니움 유저 데이터 저장 Path 클래스
class userfilepath:
    userfilepath = os.path.join(os.getcwd(), "user_data")

## 셀레니움 세팅 클래스
class chrome_driver_setting:
    def __init__(self, headless:bool=False) -> None:
        self.options = Options()
        
        ### headless 오픈을 원할 시
        if headless:
            self.options.add_argument("--headless")
        
        ### userfolder가 없다면 만들기
        try :
            self.options.add_argument("user-data-dir=" + userfilepath.userfilepath)
        except :
            os.mkdir(userfilepath.userfilepath)
            self.options.add_argument("user-data-dir=" + userfilepath.userfilepath)

        ### 크롬 드라이브 설치
        self.options.add_argument("disable-blink-features=AutomationControlled")
        self.options.add_argument('--log-level=1')
        self.options.add_experimental_option("detach", True)
        self.options.add_experimental_option("excludeSwitches", ['enable-logging'])
        self.address = ChromeDriverManager().install()
        print(self.address)

## 구글 계정 세팅 클래스
class is_setting_user:
    def __init__(self) -> None:
        ## (셀레니움 세팅 클래스 사용)
        self.chrome = chrome_driver_setting(True)
        self.driver = webdriver.Chrome(self.chrome.address, options=self.chrome.options)
        self.driver.implicitly_wait(3)
        
        ### "최유리 숲" 링크로 검색한 결과를 토대로 로그인 판단 => https://www.youtube.com/musicpremium 사이트 진입 확인(로그인X)
        self.driver.get(url='https://music.youtube.com/search?q=%EC%B5%9C%EC%9C%A0%EB%A6%AC%20%EC%88%B2/')
        self.status = True if self.driver.current_url.count("musicpremium") < 1 else False
        self.driver.quit()

    def login(self):
        ## (셀레니움 세팅 클래스 사용)
        self.chrome = chrome_driver_setting()
        self.driver = webdriver.Chrome(self.chrome.address, options=self.chrome.options)
        
        ### 로그인 화면 이동
        self.driver.get(url='https://accounts.google.com')
        
        print("로그인을 해주시기 바랍니다.")
        while True:
            
            ### 로그인 완료 시 뜨는 https://myaccount.google.com/ 링크 확인 시 셀레니움 종료
            if self.driver.current_url.count("myaccount") > 0:
                print("로그인을 완료하여 5초 후 자동으로 종료 됨")
                time.sleep(5)
                self.driver.quit()
                break
    
    ### 유저 데이터 삭제
    def auto_delete(self):
        shutil.rmtree(userfilepath.userfilepath)

## 유튜브 뮤직 조작 클래스
class auto_youtube:
    def __init__(self) -> None:
        ## (셀레니움 세팅 클래스 사용)
        self.chrome = chrome_driver_setting()
        self.driver = webdriver.Chrome(self.chrome.address, options=self.chrome.options)
        ### 창 최대화
        self.driver.maximize_window()
        
    ### url 기준 조작
    def url_open(self, song_url):
        self.driver.implicitly_wait(3)
        self.driver.get(url=song_url)
        self.driver.implicitly_wait(3)
        
        ### 유효 계정 아님 => https://www.youtube.com/musicpremium 사이트 진입 확인(로그인 새로 요청)
        if self.driver.current_url.count("musicpremium") > 0:
            self.driver.quit()
            print("올바른 계정으로 다시 로그인 해주세요.")
            
            #### 유저 데이터 삭제
            shutil.rmtree(userfilepath.userfilepath)
            #### 프로그램 종료
            return False

        ### 플레이 리스트 링크 vs 개별 음악 링크
        try :
            if 'playlist' in song_url:
                play_button = self.driver.find_element(By.CSS_SELECTOR, "#action-buttons > ytmusic-play-button-renderer")
            else : 
                play_button = self.driver.find_element(By.CSS_SELECTOR, "#icon")

            play_button.click()
        
        except Exception as e:
            #### 에러 메세지 띄움
            print(f"유튜브 조작 예외 발생: {e}")
            #### 프로그램 종료
            return False
        
        #### 프로그램 지속
        return True

    ## 쿼리 기준
    def query_open(self, song_query):
        self.driver.implicitly_wait(3)
        self.driver.get(url='https://music.youtube.com/search?q=' + song_query)
        self.driver.implicitly_wait(3)

        ### 유효 계정 아님 => https://www.youtube.com/musicpremium 사이트 진입 확인(로그인 새로 요청)
        if self.driver.current_url.count("musicpremium") > 0:
            self.driver.quit()
            print("올바른 계정으로 다시 로그인 해주세요.")
            
            #### 유저 데이터 삭제
            shutil.rmtree(userfilepath.userfilepath)
            #### 프로그램 종료
            return False

        ### url 접근 후 이동, 이 후 버튼 선택
        try :
            first_one = self.driver.find_element(By.CSS_SELECTOR, "#contents > ytmusic-responsive-list-item-renderer:nth-child(1) > div.flex-columns.style-scope.ytmusic-responsive-list-item-renderer > div.title-column.style-scope.ytmusic-responsive-list-item-renderer > yt-formatted-string > a")
            self.driver.get(url=first_one.get_attribute("href"))
            self.driver.implicitly_wait(3)
            self.driver.find_element(By.CSS_SELECTOR, "#icon").click()
        except Exception as e:
            #### 에러 메세지 띄움
            print(f"유튜브 조작 예외 발생: {e}")
            #### 프로그램 종료
            return False

        #### 프로그램 지속
        return True
    
    ## 셀레니움 종료
    def quit(self):    
        self.driver.quit()