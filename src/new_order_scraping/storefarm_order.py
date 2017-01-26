from site_new_order import SiteNewOrder
import requests
import json

class StorefarmOrder(SiteNewOrder):
    def __init__(self, _id, _password):                         # requests Session설정
        self.s = requests.Session()
        SiteNewOrder.__init__(self, _id, _password)
        SiteNewOrder.driverQuit(self)                           # webdriver는 사용하지 않음
    def logOn(self):                                            # 로그인 성공시 True, 실패시 False 리턴
        SiteNewOrder.logOn(self)
        payload={   "from":"http://sell.storefarm.naver.com/s",       #로그인 data form
                    "username":self._id,                              # _id, _password 값을 각각 세팅
                    "password":self._password,
                    "connect_id":"on"}

        header={"Referer":"https://sell.storefarm.naver.com/l/login", "Origin":"https://sell.storefarm.naver.com/l"}

        r = self.s.post("https://sell.storefarm.naver.com/l/login", data=payload, headers=header) # 로그인 post 요청
        r = self.s.get("http://sell.storefarm.naver.com/s/home")       # 로그인 성공 여부를 위해 /s/home get요청
        lists = r.text.split('.')
        if lists[0]=="<script type='text/javascript'>window":           # 로그인 페이지로 redirectoion 스크립트일 경우 로그인 실패
            return False
        else:
            return True
    def getNewOrderNum(self):                               # 신규 주문 목록 개수 리턴
        payload2 = {    "summaryInfoType":"NEW_ORDERS",     # 주문 목록 post 요청을 위한 data form
                        "paging.current":"1",
                        "rowPerPageType":"ROW_CNT_100",
                        "sort.type":"RECENTLY_ORDER_YMDT",
                        "sort.direction":"DESC",
                        "onlyValidation":"true"
        }
        header2 = {"Referer":"https://sell.storefarm.naver.com/o/n/sale/delivery?summaryInfoTyoe=NEW_ORDERS"} # 주문 목록 post 요청에 추가할 헤더
        r = self.s.post("https://sell.storefarm.naver.com/o/n/sale/delivery/json", data=payload2, headers=header2) # 신규 주문목록 post 요청
        result = r.json()           # json파싱

        return (len(result['htReturnValue']['pagedResult']['content']))     # 신규 주문 목록 개수 리턴

    def postTo(self, url, site_name, num):
        SiteNewOrder.postTo(self, url, site_name, num)
