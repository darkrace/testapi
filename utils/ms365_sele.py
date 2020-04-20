from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import random
import string
import time
from testapi.settings import BASE_DIR
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
from selenium.common.exceptions import TimeoutException

class MS365():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--disable-dev-shm-usage')
        uniq = self.gen_uid()
        self.email = "superman_" + str(uniq) + "@techmonkey.com"
        self.org = "theironman" + ''.join(random.sample('0123456789', 5))
        self.driver = webdriver.Chrome(
            executable_path=os.path.abspath(BASE_DIR+"/driver/chromedriver"),
            chrome_options=chrome_options)
        time.sleep(5)
    def ms_create(self, number,code):
        delay =10
        self.driver.get("https://signup.microsoft.com/create-account/signup?products=467EAB54-127B-42D3-B046-3844B860BEBF&country=GB")
        WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and contains(.,'Next')]")))
        self.driver.find_element_by_xpath("//input[contains(@class,'c-text-field')]").send_keys(self.email)
        self.driver.find_element_by_xpath("//button[@type='submit' and contains(.,'Next')]").click()
        WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and contains(@data-bi-name,'Set up account')]")))
        self.driver.find_element_by_xpath("//button[@type='submit' and contains(@data-bi-name,'Set up account')]").click()
        WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and contains(.,'Next')]")))
        self.driver.execute_script("return document.getElementById('regionDropdown').value = 'GB'")
        self.driver.find_element_by_xpath("//input[@name='given-name']").send_keys("dark")
        self.driver.find_element_by_xpath("//input[@name='family-name']").send_keys("race")
        self.driver.find_element_by_xpath("//input[@name='phonenumber']").send_keys(number)
        self.driver.find_element_by_xpath("//input[@name='organization']").send_keys(self.org)
        self.driver.find_element_by_xpath("//select[@formcontrolname='orgSize']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//option[@value='1']").click()
        self.driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, "//button[@id='verificationButton']")))
            self.driver.execute_script("return document.querySelector('.mwf-select').value = '" + code + "'")
        except:
            self.driver.execute_script("return document.querySelector('.mwf-select').value = '"+code+"'")
        self.driver.find_element_by_xpath("//button[@id='verificationButton']").click()
        print(self.email)
        try:
            WebDriverWait(self.driver, delay).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='hipVerificationCodeInput']")))
            return {"message": "ok enter verify code." , "color":"green","flag": True }
        except:
            # self.driver.close()
            return {"message": "Sorry, we need additional information to verify your identity. Please contact support.", "color":"red", "flag": True}

    def phone_verify(self, code):
        delay = 10
        self.driver.find_element_by_xpath("//input[@id='hipVerificationCodeInput']").send_keys(code)
        self.driver.find_element_by_xpath("//button[@data-bi-id='SignupNext']").click()
        time.sleep(4)
        self.driver.find_element_by_xpath("//input[@id='domain']").send_keys(self.org)
        time.sleep(4)
        self.driver.find_element_by_xpath("//button[@id='moeraNextButton']").click()
        time.sleep(6)
        self.driver.find_element_by_xpath("//input[@id='username']").send_keys("dark")
        self.driver.find_element_by_xpath("//input[@formcontrolname='password']").send_keys("C1sco1234!")
        self.driver.find_element_by_xpath("//input[@formcontrolname='confirmPassword']").send_keys("C1sco1234!")
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[@data-bi-id='SignupNext']").click()
        time.sleep(3)
        self.driver.close()
        print("ok")
        return {"email":self.email, "phone":"","org":self.org}
    def gen_uid(self):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(4))