from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
# wait 사용 목적
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# exceptions
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from site_new_order import SiteNewOrder         # SiteNewOrder 클래스를 상속받음

class _11stOrder(SiteNewOrder):
    def __init__(self, _id, _password):                 # ID, Password값을 받고 webdriver 로드
        SiteNewOrder.__init__(self, _id, _password)
    def logOn(self):                # 로그인 성공할시에 True 리턴 , 실패하면  False
        SiteNewOrder.logOn(self)
        self.driver.get("https://login.soffice.11st.co.kr/login/Login.page?returnURL=http%3A%2F%2Fsoffice.11st.co.kr%2FIndex.tmall")
        siteId = self.driver.find_element_by_id("loginName")    # find 11번가 로그인 ID 입력 element
        password= self.driver.find_element_by_id("passWord")    # find 패스워드 입력 element
        logOnBtn = self.driver.find_element_by_class_name("btn_login") # 로그인 버튼 element
        actions = ActionChains(self.driver)                             # ActionChain 설정
        actions = self.sendBackspace(siteId, 8, actions)                # ID 입력 element에 있는 default text를 지우는 명령을 체인에 저장
        actions.send_keys_to_element(siteId, self._id)                  # 실제 로그인 ID 입력하고 체인에 저장
        actions.send_keys_to_element(password, self._password)          # 실제 로그인 Password 입력하고 체인에 저장
        actions.perform()                                               # ActionChain 수행
        logOnBtn.click()                                                # 로그인 버튼 클릭
        try:
            find_list = WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//ul[@class='quick_menu']/li/ul/li/a/span")))
            for i in find_list:
                if i.text=='결제완료':         # 로그인 후에 '결제 완료' 페이지 까지 로딩
                    i.click()
                    self.neverGiveUp(lambda: self.driver.switch_to_frame(self.driver.find_element_by_id("Content_ifrm_35930"))) # 프레임으로 스위칭 성공 할때까지 시도
                    break           # loop에서 나옴
            return True             # 이상이 없으면 True return
        except TimeoutException:
            return False            # 시간 초과시 False return


    def getNewOrderNum(self):               # 신규 주문 목록 개수 리턴
        SiteNewOrder.getNewOrderNum(self)
        try:
            search = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "submitCommit")))  # 검색버튼을 클릭 할 수 있을때 까지 기다림
            self.driver.execute_script("document.getElementById('submitCommit').click()")                       # 검색버튼을 클릭해야 신규 주문목록이 로드됨
            number = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@id='subClmCount']/li/b")))  #신규주문목록 건수를 찾음
            return int(number[0].text)      # 리스트 첫번째 요소 리턴 이 값에 신규 주문 목록 개수가 들어있음
        except (TimeoutException, StaleElementReferenceException):
            return False        # exception에 걸리면 다시 시도하지 않고 False 리턴 , 계속 시도하면 무한 루프에 걸릴수 있음
    def postTo(self, url, site_name, num):
        SiteNewOrder.postTo(self, url, site_name, num)

    def driverQuit(self):               # webdriver 해제
        SiteNewOrder.driverQuit(self)
