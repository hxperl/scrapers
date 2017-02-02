from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import requests


class SiteNewOrder:

    def __init__(self, _id, _password):         # set ID, Password and Firefox webdriver
        self.driver = webdriver.Firefox()
        self._id = _id
        self._password = _password

    def getNewOrderNum(self):                   # pass
        pass

    def logOn(self):                            # pass
        pass

    def neverGiveUp(self, fn):                  # 성공할때까지 계속 시도
        while True:
            try:
                return fn()
            except Exception as e:
                pass

    # element에 backspace 키를 여러번 설정하고 ActionChains에 저장
    def sendBackspace(self, element, i, act):
        for j in range(i):
            act.send_keys_to_element(element, Keys.BACK_SPACE)
        return act

    def postTo(self, url, site_name, num):  # 테스트용
        r = requests.post(url, json={site_name: num})

    def driverQuit(self):                                   # webdriver 해제
        self.driver.quit()

__all__ = ['SiteNewOrder']
