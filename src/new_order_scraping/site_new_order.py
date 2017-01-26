from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

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

    def listAppend(self, _list, _item, depth=0):    # 주문 목록 리스트를 저장 하는 method [[list1],[list2]......]
        if depth==0:
            _item = []
            _list.append(_item)
        elif depth==1:
            _list[-1].append(_item)
        else:
            print('depth error')
            return
        return _list

    def sendBackspace(self, element, i, act):               # element에 backspace 키를 여러번 설정하고 ActionChains에 저장
        for j in range(i):
            act.send_keys_to_element(element, Keys.BACK_SPACE)
        return act

    def postTo(self, url, site_name, num):                  #테스트용
        r = requests.post(url, json={site_name:num})
    def driverQuit(self):                                   # webdriver 해제
        self.driver.quit()

__all__ = ['SiteNewOrder']
