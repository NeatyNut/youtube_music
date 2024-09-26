from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import shutil
import os
import time

class userfilepath:
    userfilepath = os.path.join(os.getcwd(), "user_data")

class chrome_driver_setting:
    def __init__(self, headless:bool=False) -> None:
        self.options = Options()
        
        # headless 오픈을 원할 시
        if headless:
            self.options.add_argument("--headless")
        
        try :
            self.options.add_argument("user-data-dir=" + userfilepath.userfilepath)
        except :
            os.mkdir(userfilepath.userfilepath)
            self.options.add_argument("user-data-dir=" + userfilepath.userfilepath)

        self.options.add_argument("disable-blink-features=AutomationControlled")
        self.options.add_argument('--log-level=1')
        self.options.add_experimental_option("detach", True)
        self.options.add_experimental_option("excludeSwitches", ['enable-logging'])
        self.address = ChromeDriverManager().install()

class is_setting_user:
    def __init__(self) -> None:
        self.chrome = chrome_driver_setting(True)
        self.driver = webdriver.Chrome(self.chrome.address, options=self.chrome.options)
        self.driver.implicitly_wait(3)
        ## 검색한 걸로 판단하느라 불완전할 수도 있음.
        self.driver.get(url='https://music.youtube.com/search?q=%EC%B5%9C%EC%9C%A0%EB%A6%AC%20%EC%88%B2/')
        self.status = True if self.driver.current_url.count("musicpremium") < 1 else False
        self.driver.quit()

    def login(self):
        self.chrome = chrome_driver_setting()
        self.driver = webdriver.Chrome(self.chrome.address, options=self.chrome.options)
        self.driver.get(url='https://accounts.google.com')
        
        print("로그인을 해주시기 바랍니다.")
        while True:
            if self.driver.current_url.count("myaccount") > 0:
                print("로그인을 완료하여 5초 후 자동으로 종료 됨")
                time.sleep(5)
                self.driver.quit()
                break

    def auto_delete(self):
        shutil.rmtree(userfilepath.userfilepath)

class auto_youtube:
    def __init__(self) -> None:
        self.chrome = chrome_driver_setting()
        self.driver = webdriver.Chrome(self.chrome.address, options=self.chrome.options)
        self.driver.maximize_window()
        
    ## url 기준
    def url_open(self, song_url):
        self.driver.implicitly_wait(3)
        self.driver.get(url=song_url)
        self.driver.implicitly_wait(3)
        
        ## 제대로 된 계정 아닐시
        if self.driver.current_url.count("musicpremium") > 0:
            self.driver.quit()
            print("올바른 계정으로 다시 로그인 해주세요.")
            shutil.rmtree(userfilepath.userfilepath)
            return False

        # 플레이 리스트 vs 개별 음악
        if 'playlist' in song_url:
            play_button = self.driver.find_element(By.CSS_SELECTOR, "#action-buttons > ytmusic-play-button-renderer")
        else : 
            play_button = self.driver.find_element(By.CSS_SELECTOR, "#icon")

        play_button.click()
        return True

    ## 쿼리 기준
    def query_open(self, song_query):
        self.driver.implicitly_wait(3)
        self.driver.get(url='https://music.youtube.com/search?q=' + song_query)
        self.driver.implicitly_wait(3)

        if self.driver.current_url.count("musicpremium") > 0:
            self.driver.quit()
            print("올바른 계정으로 다시 로그인 해주세요.")
            shutil.rmtree(userfilepath.userfilepath)
            return False

        first_one = self.driver.find_element(By.CSS_SELECTOR, "#contents > ytmusic-responsive-list-item-renderer:nth-child(1) > div.flex-columns.style-scope.ytmusic-responsive-list-item-renderer > div.title-column.style-scope.ytmusic-responsive-list-item-renderer > yt-formatted-string > a")
        self.driver.get(url=first_one.get_attribute("href"))
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.CSS_SELECTOR, "#icon").click()
        return True

    def quit(self):
        self.driver.quit()