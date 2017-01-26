# 카테고리 목록 Scraping

## 11번가 카테고리목록 

- ```
  출력 내용 : 11번가 최하위 카테고리까지 목록 출력
  최하위 카테고리 : ex)11번가 브랜드 패션 -> 브랜드 여성의류 -> 코트 -> 최하위 카테고리 = {트렌치코트, 무스탕/가죽코트, 퍼/모피코트, 하프코트 ...등}
  구현 언어 : python
  사용된 library - REQUESTS, RE, HTML.lxml
  구현 방식 : xpath selector로 html내 태그를 찾아서 나열하는 방식과
  			정규식으로 카테고리목록 패턴을 찾아서 나열하는 방식
  실행방법 : python3 category_11st.py
  ```



## 옥션 카테고리 목록

- ```
  출력 내용 : 옥션 최하위 카테고리까지 목록 출력
  최하위 카테고리 : ex) 옥션 의류 -> 남성의류 -> 반팔티셔츠 -> 최하위 카테고리 = {라운드넥티셔츠, 카라넥티셔츠, 브이넥티셔츠 ....등}
  구현언어 : python
  사용된 library - REQUESTS, RE, HTML.lxml
  구현 방식 : xpath selector로 html내 태그를 찾아서 나열하는 방식과
  			정규식으로 카테고리목록 패턴을 찾아서 나열하는 방식
  실행방법 : python3 category_auction.py
  ```



## G마켓 카테고리 목록

- ```
  출력 내용 : G마켓 최하위 카테고리까지 목록 출력
  최하위 카테고리 : ex)G마켓 브랜드패션 -> 브랜드의류 -> 브랜드 여성의류 -> 티셔츠 -> 최하위 카테고리 = {무지티셔츠, 프린트패턴 티셔츠, 스트라이프 티셔츠 ...등}
  구현 언어 : python
  사용된 library - REQUESTS, RE, HTML.lxml
  구현 방식 : xpath selector로 html내 태그를 찾아서 나열하는 방식과
  			정규식으로 카테고리목록 패턴을 찾아서 나열하는 방식
  실행방법: python3 category_gmarket.py
  ```

## 인터파크 카테고리 목록

- ```
  출력 내용 : 인터파크 최하위 카테고리까지 목록 출력
  구현 언어 : python
  사용된 library - REQUESTS, RE, HTML.lxml
  구현 방식 : xpath selector로 html내 태그를 찾아서 나열하는 방식과
  			정규식으로 카테고리목록 패턴을 찾아서 나열하는 방식
  실행방법 : python3 category_interpark.py
  ```

# 판매자용 신규 주문 목록 scraping

## SiteNewOrder class

#### defined methods

##### \_\_init\_\_(self, _id, _password)

```init Firefox webdriverset ```

```login ID, Password```

##### logOn(self)

```pass```

##### getNewOrderNum(self)

```pass```

#####  driverQuit(self) 

```self.driver.quit()```

11번가, 옥션만 해당

- [x] 옥션 - webdriver 해제 
- [x] 11번가 - webdriver 해제
- [ ] 스토어팜 - webdriver 사용안함
- [ ] 인터파크 - webdriver 사용안함

## AuctoinOrder class()

> SiteNewOrder class를 상속 받음
>
> webdriver를 이용해 신규 주문 목록을 얻음

#### defined methods

##### def  \_\_init\_\_(self, _id, _password):

```SiteNewOrder.__init__(self, _id, _password) 호출```

##### def logOn(self):

```_id, _password 로 옥션 판매자 사이트 로그인 후 신규 주문 목록 페이지 까지 이동 ```

```로그인 성공시 True, 실패하면 False 리턴```

##### def getNewOrderNum(self):

```신규 주문 목록 개수를 리턴```

##### def driverQuit(self):

```SiteNewOrder.driverQuit(self)호출```



## \_11stOrder class()

> SiteNewOrder class를 상속 받음
>
> webdriver를 이용해 신규 주문 목록을 얻음

#### defined methods

##### def  \_\_init\_\_(self, _id, _password):

```SiteNewOrder.__init__(self, _id, _password) 호출```

##### def logOn(self):

```_id, _password 로 11번가 판매자 페이지 로그인 후 결제 완료 페이지까지 이동```

``` 로그인 성공시 True, 실패하면 False 리턴```

##### def getNewOrderNum(self):

```신규 주문 목록 개수를 리턴```

##### def driverQuit(self):

```SiteNewOrder.driverQuit(self)호출```



## StorefarmOrder class()

> SiteNewOrder class를 상속 받음
>
> requests 라이브러리를 이용해 신규 주문 목록을 얻음

#### defined methods

##### def \_\_init\_\_(self, _id, _password):

```python
self.s = requests.Session()			# session 설정
SiteNewOrder.__init__(self, _id, _password) # webdriver 설정 
SiteNewOrder.driverQuit(self)		# webdriver 해제
```

requests 라이브러리를 사용하기 때문에 webdriver는 해제

##### def logOn(self):

```_id, _password로 스토어팜 판매자 페이지에 로그인```

```로그인 성공시 True, 실패하면 False 리턴```

##### def getNewOrderNum(self):

```신규 주문 목록 개수 리턴```



## InterparkOrder class()

> SiteNewOrder class를 상속 받음
>
> requests 라이브러리를 이용해 신규 주문 목록을 얻음

#### defined methods



##### def \_\_init\_\_(self, _id, _password):

```python
self.s = requests.Session()			# session 설정
SiteNewOrder.__init__(self, _id, _password) # webdriver 설정 
SiteNewOrder.driverQuit(self)		# webdriver 해제
```

storefarm과 마찬가지로 webdriver를 사용하지 않음

##### def logOn(self):

```인터파크 판매자 페이지에 로그인```

```로그인 성공시 True, 실패하면 False 리턴```

##### def getNewOrderNum(self):

```신규 주문 목록 개수 리턴```

## example

1. ```python
   from _11st_order import _11stOrder

   obj = _11stOrder('id', 'password')
   if obj.logOn():
       number_of_new_order = obj.getNewOrderNum()
   else:
       print('login failed!')
   obj.driverQuit()
   ```

2. ```python
   from storefarm_order import StorefarmOrder

   obj = StorfarmOrder('id', 'password')
   if obj.logOn():
       number_of_new_order = obj.getNewOrderNum()
   else:
       print('login failed!')
   ```

