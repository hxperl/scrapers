# Shopping sites scrapers

category scraping

##### www.coupang.com

> code : python3
>
> library: requests, lxml
>
> $ python3 coupang.py

print out categories and nested with taps



### New Order Scraping for seller

1. Availavle sites

   - [www.11st.co.kr](https://www.11st.co.kr)
   - [www.auction.co.kr](http://www.auction.co.kr)
   - [sell.storefarm.naver.com](https://sell.storefarm.naver.com)
   - [www.interpark.com](http://www.interpark.com)

2. defined Class

   - SiteNewOrder()	// super class
     - _11stOrder(SiteNewOrder)		
     - AuctionOrder(SiteNewOrder)
     - InterparkOrder(SiteNewOrder)
     - StorefarmOrder(SiteNewOrder)

3. Example

   ```python
   from storefarm_order import StorefarmOrder
   from pyvirtualdisplay import Display

   display = Display(visible=0, size=(800, 600))
   display.start()

   storefarm = StorefarmOrder('id', 'password')

   try:
       if storefarm.logOn():
           print('login success')
           print(storefarm.getNewOrderNum())
       else:
           print('login fail')
   finally:
       display.stop()

   ```



> code: python3
>
> library: check requirements.txt ,
>
> ​	and	also need [geckodriver](https://github.com/mozilla/geckodriver/releases) for selenimun webdriver Firefox.
>
> you can test with test.py

##### 