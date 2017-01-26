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
        SiteNewOrder.logOn(self)
        self.driver.get("https://www.esmplus.com/Member/SignIn/LogOn")      # 로그인 페이지
        options = self.driver.find_elements_by_id("rdoSiteSelect")          # 라디오 버튼으로 옥션, G마켓 선택 옵션이 있음
        for val in options:
            if val.get_attribute("value")=="IAC":                           # 옥션 버튼을 찾음
                val.click()                                                 # 옥션 버튼 선택
        siteId = self.driver.find_elements_by_id("SiteId")                  # 로그인 ID 입력 element
        password= self.driver.find_elements_by_id("SitePassword")           # 로그인 Password 입력 elemnet
        logOnBtn = self.driver.find_elements_by_id("btnSiteLogOn")          # 로그인 버튼 elemnet
        actions = ActionChains(self.driver)                                 # ActionChain 설정
        actions = self.sendBackspace(siteId[0], 3, actions)                 # ID 입력 element에 있는 default text를 지우는 명령을 체인에 저장
        actions.send_keys_to_element(siteId[0], self._id)                   # 실제 로그인 ID 입력하고 체인에 저장
        actions = self.sendBackspace(password[0], 4, actions)               # Password 입력 element에 있는 default text를 지움
        actions.send_keys_to_element(password[0], self._password)           # 실제 로그인 Password 입력하고 체인에 저장
        actions.perform()                                                   # ActionChain 수행
        logOnBtn[0].click()                                                 # 로그인 버튼 클릭

        try:
            title = WebDriverWait(self.driver, 5).until(EC.title_is('ESM Plus - Home'))     # 메인 타이틀이 로딩 될 때까지 기다림
            newOrder = self.neverGiveUp(lambda: self.driver.find_element_by_xpath("//p[@class='title1']/a"))    # '신규주문' 버튼을 찾음
            if newOrder.text=='신규주문':              # 텍스트값이 '신규주문'이 맞을 경우
                while self.driver.current_url!='http://www.esmplus.com/Home/Home#HTDM105':  # 신규 주문 페이지가 로딩 될 때까지
                        newOrder.click()    # '신규주문'클릭
                self.neverGiveUp(lambda: self.driver.switch_to_frame(self.driver.find_element_by_name("ifm_TDM105"))) # 신규주문 페이지가 로딩되면 프레임 전환을 성공할 때까지 시도
            return True         # 이상 없을 경우 True return
        except TimeoutException:
            return False        # 시간 초과시 False return
    def getNewOrderNum(self):               # 신규 주문 목록 개수 리턴
        SiteNewOrder.getNewOrderNum(self)
        try:
            search = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.ID, "btnSearch")))  # 검색 버튼이 위치할때까지 기다렸다가
            self.driver.execute_script("document.getElementById('btnSearch').click()")      #클릭

            pagging = WebDriverWait(self.driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='pagging']/a[@class='paggingnum']")))
            # 추가 페이지가 있는지 3초간 기다림. 없으면 exception
            for t in range(0, len(pagging)+1):
                try:
                    while True: # explicit 이 정확하게 작동하지 않을경우
                        try:
                            orderedList = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//tbody[@class='sb-grid-results']/tr")))
                            for i in orderedList:
                                #print('\n')
                                #new_order_list = self.listAppend(self.new_order_list, i)
                                for j in i.find_elements_by_xpath('./td'):
                                    pass
                                    #print(j.text, " ", end="")
                                    #new_order_list = self.listAppend(self.new_order_list, j.text, 1)
                            break
                        except:     # explicit wait 도 정확하게 불러오지 못할경우 Exception 발생
                            pass
                    self.driver.execute_script("document.getElementsByClassName('paggingnum')[%d].click()" % t)
                except WebDriverException: # 클릭할 다음 페이지가 없을 경우
                    break
        except (NoSuchElementException, TimeoutException): ## 추가 페이지가 없을 경우
                while True: # explicit 이 정확하게 작동하지 않을 수 있음
                    try:
                        orderedList = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//tbody[@class='sb-grid-results']/tr")))
                        # 주문 목록 리스트를 받아 orderedList에 저장
                        for i in orderedList:
                            #print('\n')
                            #self.new_order_list = self.listAppend(self.new_order_list, i)
                            for j in i.find_elements_by_xpath('./td'):
                                if j.text == '조회된 데이터가 없습니다.':      # 신규 주문목록이 0 이어도 텍스트값이 있어서 1이 리턴되므로 직접 0 리턴
                                    return 0
                                # else:
                                #     print(j.text, " ", end="")
                                #     self.new_order_list = self.listAppend(self.new_order_list, j.text, 1)
                        break
                    except:     # explicit wait 도 정확하게 불러오지 못할경우 Exception 발생
                        pass
        return len(orderedList)
    def postTo(self, url, site_name, num):
        SiteNewOrder.postTo(self, url, site_name, num)

    def driverQuit(self):
        SiteNewOrde.driverQuit(self)
