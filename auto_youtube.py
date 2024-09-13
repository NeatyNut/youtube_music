from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import shutil
import os

class chrome_driver_setting:
    def __init__(self, headless:bool=False) -> None:
        self.options = Options()
        
        # headless 오픈을 원할 시
        if headless:
            self.options.add_argument("--headless")
        
        try :
            self.options.add_argument("user-data-dir=C:\\user_data\\youtube")
        except :
            os.mkdir("C:\\user_data")
            self.options.add_argument("user-data-dir=C:\\user_data\\youtube")

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
                break

    def auto_delete(self):
        shutil.rmtree("C:\\user_data\\youtube")

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
        play_button = self.driver.find_element(By.CSS_SELECTOR, "#icon")
        play_button.click()

    ## 쿼리 기준
    def query_open(self, song_query):
        self.driver.implicitly_wait(3)
        self.driver.get(url='https://music.youtube.com/search?q=' + song_query)
        self.driver.implicitly_wait(3)

        first_one = self.driver.find_element(By.CSS_SELECTOR, "#contents > ytmusic-responsive-list-item-renderer:nth-child(1) > div.flex-columns.style-scope.ytmusic-responsive-list-item-renderer > div.title-column.style-scope.ytmusic-responsive-list-item-renderer > yt-formatted-string > a")
        self.driver.get(url=first_one.get_attribute("href"))
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.CSS_SELECTOR, "#icon").click()

    def quit(self):
        self.driver.quit()

## 클래스화
check = is_setting_user()
if not check.status:
    print("계정 정보를 삭제합니다.")
    check.auto_delete()
    login_status = check.login()

else:
    start = auto_youtube()
    time.sleep(10)
    start.query_open("최유리 숲")
    time.sleep(10)
    start.url_open("https://music.youtube.com/watch?v=-pUpgeZPUCI&list=RDAMVM-pUpgeZPUCI")
    time.sleep(10)