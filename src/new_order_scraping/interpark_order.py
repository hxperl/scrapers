from site_new_order import SiteNewOrder
import requests
import json
import datetime


class InterparkOrder(SiteNewOrder):

    def __init__(self, _id, _password):
        self.s = requests.Session()                     # requests Session설정
        SiteNewOrder.__init__(self, _id, _password)
        SiteNewOrder.driverQuit(self)                   # webdriver는 사용하지 않음

    def logOn(self):                                    # 로그인 성공시 True, 실패시 False 리턴
        SiteNewOrder.logOn(self)
        payload = {                                     # post 요청에 필요한 data form
            "sc.memId": self._id,
            "sc.pwd": self._password,
            "sc.enterEntr": "Y",
            "isAjax": "Y",
            "imfsUserPath": "null",
            "imfsUserQuery": "null",
            "GNBLogin": "Y"
        }
        payload2 = {"_method": "login",                     # 두번째 post 요청에 필요한 data form
                    "ipssUserPath": "/ipss/ipssmainscr.do",
                    "ipssUserQuery": "_method=initial&_style=ipssPro&wid1=wgnb&wid2=wel_login&wid3=seller",
                    "sc.useAppTp": "02",
                    "sc.isIpss": "E",
                    "sc.enterEntr": "Y",
                    "sc.memId": self._id,
                    "sc.pwd": self._password,
                    }

        header = {"Referer": "https://ipss.interpark.com/member/login.do",  # post 요청에 필요한 header 설정
                  "Origin": "https://ipss.interpark.com"}
        # 두번째 post 요청에 필요한 header
        header2 = dict(header, **{"Upgrade-Insecure-Requests": "1"})
        r = self.s.post("https://ipss.interpark.com/member/login.do?_method=login",
                        data=payload, headers=header)  # 로그인
        r = self.s.post("https://ipss.interpark.com/member/login.do",
                        data=payload2, headers=header2)  # 두번째 post까지 있어야 쿠키값을 제대로 받음

        if "http://www.interpark.com/member/login.do?null" in r.text:       # 두번째 포스트 요청이후 결과 텍스트값으로 로그인 성공 여부 결정
            return True
        else:
            return False

    def getNewOrderNum(self):                           # 신규 주문 목록 개수 리턴
        enday = datetime.date.today()                   # 오늘 날짜 계산
        stday = enday + datetime.timedelta(days=-14)    # 2주전 날짜 계산
        stdate = str(stday).replace('-', '')            # '-' 없는 str값으로 변환
        # '-' 없는 str값으로 변환, 날짜 값을 get 요청에 같이 넣어줌으로 오늘을 기점으로 2주전까지의 목록을 불러옴
        endate = str(enday).replace('-', '')
        r = self.s.get("https://ipss.interpark.com/delivery/ProOrderCheckList.do?_method=list&_style=grid&_search=false&nd=1485218711647&rows=50&page=1&sidx=&sord=asc&sc.dateTp=2&sc.strDt=" +
                       stdate + "&sc.strHour=00&sc.endDt=" + endate + "&sc.endHour=23&sc.searchTp=&sc.searchNm=&flag=ko&sc.page=1&sc.row=50")
        result = r.json()                               # json 파싱
        # bs 키값 안의 리스트 길이를 구하고 리턴
        return len(result['bs'])

    def postTo(self, url, site_name, num):
        SiteNewOrder.postTo(self, url, site_name, num)
