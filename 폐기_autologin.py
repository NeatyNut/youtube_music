    def auto_login(self, id, pw):
        self.chrome = chrome_driver_setting()
        self.driver = webdriver.Chrome(self.chrome.address, options=self.chrome.options)
        timeout = 5
        self.driver.get(url='https://accounts.google.com')
        self.driver.implicitly_wait(3)

        if self.driver.current_url.count("myaccount") < 1:
            login_attempt_bool = True
            erase_button_bool = True

        while login_attempt_bool:
            try :
                email_input = self.driver.find_element(By.CSS_SELECTOR, "#identifierId")
                email_input.send_keys(id)
                self.driver.find_element(By.CSS_SELECTOR, "#identifierNext > div > button").click()
                
                start_time = time.time()
                print("ID 확인 중")
                while self.driver.current_url.count("v3/signin/identifier") > 0:
                    if time.time() - start_time > timeout:
                        print("ID를 확인해주십시오.")
                        return False

                pw_input = self.driver.find_element(By.CSS_SELECTOR, "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input")
                pw_input.send_keys(pw)
                self.driver.find_element(By.CSS_SELECTOR, "#passwordNext > div > button").click()

                start_time = time.time()
                print("pw 확인 중")
                while self.driver.current_url.count("v3/signin/challenge/pwd") > 0:
                    if time.time() - start_time > timeout:
                        print("pw를 확인해주십시오.")
                        return False
                login_attempt_bool = False
                erase_button_bool = False
            except :
                while erase_button_bool:
                    index += 1
                    try :
                        erase_button = self.driver.find_element(By.CSS_SELECTOR, "#yDmH0d > div.gfM9Zd > div.tTmh9.NQ5OL > div.SQNfcc.WbALBb > div > div > div.Anixxd > div > div > div > form > span > section > div > div > div > div > ul > li:nth-child(" + str(index) + ") > div")
                        if erase_button.text == "계정 삭제":
                            erase_button.click()
                            self.driver.implicitly_wait(3)
                            self.driver.find_element(By.CSS_SELECTOR, "#yDmH0d > div.gfM9Zd > div.tTmh9.NQ5OL > div.SQNfcc.WbALBb > div > div > div.Anixxd > div > div > div > form > span > section > div > div > div > div.r4WGQb > ul > li.aZvCDf.oqdnae.W7Aapd.zpCp3.SmR8 > div > div.AEtdoc > svg").click()
                            self.driver.find_element(By.CSS_SELECTOR, "#yDmH0d > div.VfPpkd-Sx9Kwc.cC1eCc.UDxLd.PzCPDd.dgtjld.VfPpkd-Sx9Kwc-OWXEXe-FNFY6c > div.VfPpkd-wzTsW > div > div.VfPpkd-T0kwCb > button:nth-child(3)").click()
                            index = 2
                    except :
                        erase_button_bool = False

        if self.driver.current_url.count("v3/signin/challenge/") > 0:
            print("로그인을 완료해주세요.")
            while True:
                if self.driver.current_url.count("v3/signin/challenge/") == 0 or self.driver.current_url=="google.com":
                    break

        if self.driver.current_url.count("myaccount") > 0:
            self.driver.quit()
            return True
    
        return False
