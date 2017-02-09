from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# wait 사용 목적
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# exceptions
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from site_new_order import SiteNewOrder        # SiteNewOrder 클래스를 상속받음


class AuctionOrder(SiteNewOrder):

    def __init__(self, _id, _password):                 # ID, Password값을 받고 webdriver 로드
        SiteNewOrder.__init__(self, _id, _password)

    def logOn(self):                                    # 로그인 성공할시에 True 리턴 , 실패하면  False
        self.driver.get(
            "https://www.esmplus.com/Member/SignIn/LogOn")      # 로그인 페이지
        options = self.driver.find_elements_by_id(
            "rdoSiteSelect")          # 라디오 버튼으로 옥션, G마켓 선택 옵션이 있음
        for val in options:
            if val.get_attribute("value") == "IAC":                           # 옥션 버튼을 찾음
                val.click()                                                 # 옥션 버튼 선택
        siteId = self.driver.find_elements_by_id(
            "SiteId")                  # 로그인 ID 입력 element
        password = self.driver.find_elements_by_id(
            "SitePassword")           # 로그인 Password 입력 elemnet
        logOnBtn = self.driver.find_elements_by_id(
            "btnSiteLogOn")          # 로그인 버튼 elemnet
        # ActionChain 설정
        actions = ActionChains(self.driver)
        # ID 입력 element에 있는 default text를 지우는 명령을 체인에 저장
        actions = self.sendBackspace(siteId[0], 3, actions)
        # 실제 로그인 ID 입력하고 체인에 저장
        actions.send_keys_to_element(siteId[0], self._id)
        # Password 입력 element에 있는 default text를 지움
        actions = self.sendBackspace(password[0], 4, actions)
        # 실제 로그인 Password 입력하고 체인에 저장
        actions.send_keys_to_element(password[0], self._password)
        # ActionChain 수행
        actions.perform()
        # 로그인 버튼 클릭
        logOnBtn[0].click()

        try:
            title = WebDriverWait(self.driver, 5).until(
                EC.title_is('ESM Plus - Home'))     # 메인 타이틀이 로딩 될 때까지 기다림
            newOrder = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//p[@class='title1']/a")))
            if newOrder.text == '신규주문':              # 텍스트값이 '신규주문'이 맞을 경우
                while self.driver.current_url != 'http://www.esmplus.com/Home/Home#HTDM105':  # 신규 주문 페이지가 로딩 될 때까지
                    newOrder.click()    # '신규주문'클릭
                WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it(
                    (By.NAME, "ifm_TDM105")))  # switch frame
            return True         # 이상 없을 경우 return True (means login success)
        except TimeoutException:
            return False        # 시간 초과 or 'login fail' return False

    def getNewOrderNum(self):               # 신규 주문 목록 개수 리턴
        n = 0
        try:
            search = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.ID, "btnSearch")))  # 검색 버튼이 위치할때까지 기다렸다가
            self.driver.execute_script(
                "document.getElementById('btnSearch').click()")  # 클릭

            pagging = WebDriverWait(self.driver, 3).until(EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@class='pagging']/a[@class='paggingnum']")))
            # 추가 페이지가 있는지 3초간 기다림. 없으면 exception
            for t in range(0, len(pagging) + 1):
                try:
                    orderedList = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//tbody[@class='sb-grid-results']/tr")))
                    n += orderedList
                    self.driver.execute_script(
                        "document.getElementsByClassName('paggingnum')[%d].click()" % t)
                except TimeoutException:
                    print('TimeoutException while loading new ordered list')
                except WebDriverException:  # unless more page
                    break
            return n
        except (NoSuchElementException, TimeoutException):  # 추가 페이지가 없을 경우
            try:
                orderedList = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//tbody[@class='sb-grid-results']/tr")))
                # 주문 목록 리스트를 받아 orderedList에 저장
                for i in orderedList:
                    for j in i.find_elements_by_xpath('./td'):
                        if j.text == '조회된 데이터가 없습니다.':      # 신규 주문목록이 0 이어도 텍스트값이 있어서 1이 리턴되므로 직접 0 리턴
                            return 0

            except TimeoutException:
                print('TimeoutException while loading new ordered list')
        return len(orderedList)
