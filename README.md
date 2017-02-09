# Shopping sites scrapers

### EZ category scraping example

##### www.coupang.com

> code : python3
>
> libraries: requests, lxml
>
> $ python3 coupang.py

print out categories and nested with taps

### Shopping site scraping

1. Available sites
   - [rockcitykicks.com](https://rockcitykicks.com)
   - [www.woodwick.com](www.woodwick.com)

2. Defined methods
   - get_categories()
     - returns dictionary type of all categories and URLs until leaf nodes
     - output ex) {'shoes' : {'url':'www.shopping.com/shoes', 'children': {'Men' : { 'url' : 'www.shopping.com/shoes/men'}, 'Women' : { 'url' : 'www.shopping.com/shoes/women' }}}}
     - you can extract values easily
   - get_product_list('url')
     - recieves 'url' address : category leaf node URL
     - generates tuples of product list
     - output ex) ('prudoct A', 'urlA'), ('productB', 'urlB')
   - get_product_detail('url')
     - revcieves 'url' address : product url
     - returns dictionary type of product detail
     - output ex) {'name': 'product-name', 'price' : 'prudoct-price', 'img_url' : [list of product urls], etc...}

3. Example

   ```python
   from woodwick import Woodwick

   ww = Woodwick()
   a = ww.get_categories()
   for k, v in a.itmes():
       print(k, v)
   ```

> code: python3
>
> libraries: requests, lxml

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

3. defined methods

   - \_\_init\_\_('ID', 'Password')
   - logOn()  // return True or False
   - getNewOrderNum()  // return the number of new ordered list
   - driverQuit()  // only for '11st' and 'Auction' used selenium webdriver

4. Example

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