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
        self.driver.get(
            "https://login.soffice.11st.co.kr/login/Login.page?returnURL=http%3A%2F%2Fsoffice.11st.co.kr%2FIndex.tmall")
        siteId = self.driver.find_element_by_id(
            "loginName")    # find 11번가 로그인 ID 입력 element
        password = self.driver.find_element_by_id(
            "passWord")    # find 패스워드 입력 element
        logOnBtn = self.driver.find_element_by_class_name(
            "btn_login")  # 로그인 버튼 element
        # ActionChain 설정
        actions = ActionChains(self.driver)
        # ID 입력 element에 있는 default text를 지우는 명령을 체인에 저장
        actions = self.sendBackspace(siteId, 8, actions)
        # 실제 로그인 ID 입력하고 체인에 저장
        actions.send_keys_to_element(siteId, self._id)
        # 실제 로그인 Password 입력하고 체인에 저장
        actions.send_keys_to_element(password, self._password)
        # ActionChain 수행
        actions.perform()
        logOnBtn.click()                                                # 로그인 버튼 클릭
        try:
            find_list = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, "//ul[@class='quick_menu']/li/ul/li/a/span")))
            for i in find_list:
                if i.text == '결제완료':         # 로그인 후에 '결제 완료' 페이지 까지 로딩
                    i.click()
                    WebDriverWait(self.driver, 10).until(
                        EC.frame_to_be_available_and_switch_to_it((By.ID, "Content_ifrm_35930")))
                    break           # loop에서 나옴
            return True             # 이상이 없으면 True return
        except TimeoutException:
            return False            # 시간 초과시 False return

    def getNewOrderNum(self):               # 신규 주문 목록 개수 리턴
        try:
            search = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "submitCommit")))  # 검색버튼을 클릭 할 수 있을때 까지 기다림
            # 검색버튼을 클릭해야 신규 주문목록이 로드됨
            self.driver.execute_script(
                "document.getElementById('submitCommit').click()")
            number = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, "//ul[@id='subClmCount']/li/b")))  # 신규주문목록 건수를 찾음
            # 리스트 첫번째 요소 리턴 이 값에 신규 주문 목록 개수가 들어있음
            return int(number[0].text)
        except (TimeoutException, StaleElementReferenceException):
            print(
                'TimeoutException or StaleElementReferenceException while loading new ordered list')
