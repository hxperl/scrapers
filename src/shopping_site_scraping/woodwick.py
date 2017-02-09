import requests
from lxml import html


class Woodwick():

    def keep_search(self, i, _dict):           # 카테고리 탐색 함수 args (html element, dictionary)
        cate_name = i.text              # 카테고리 이름 저장
        href = i.xpath("..")
        href = href[0].get('href')      # 카테고리 url 저장
        _dict.update({cate_name: {'url': href}})     # dict 에 추가
        if i.xpath("../../ul/li"):      # 하위 카테고리가 더 있을 때
            _dict[cate_name] = dict(
                _dict[cate_name], **{'children': {}})  # 'children' 키 추가
            for j in i.xpath("../../ul/li/a/span"):     # 하위 카테고리로 selector 설정
                self.keep_search(j, _dict[cate_name]['children'])

    def get_categories(self):           # 카테고리 목록을 찾아서 dictionary type으로 return
        response = requests.get('https://www.woodwick.com/shop.html')
        assert response.status_code == 200
        my_dict = {}      # 빈 dict생성
        tree = html.fromstring(response.content)
        for i in tree.xpath("//ul[@id='sidebar-nav-menu']/li/a/span"):
            self.keep_search(i, my_dict)      # 카테고리 목록 탐색 함수 호출

        return my_dict   # dict 리턴

    def get_product_list(self, url):
        # 추가 페이지에 대한 get요청을 하지 않기 위해 모두보기 옵션으로 get
        r = requests.get(url + "?limit=all")
        assert r.status_code == 200
        tree = html.fromstring(r.content)
        for i in tree.xpath("//div[@class='product-information']/p"):
            a = i.text.strip()
            url = i.xpath("../h5/a")
            yield (a, url[0].get('href'))

    # 상품 url 주소를 받아서 상세 정보를 dictionary 타입으로 리턴
    def get_product_detail(self, url):
        r = requests.get(url)
        tree = html.fromstring(r.content)

        return {'name': [i.text for i in tree.xpath("//div[@class='product-name']/h1")]        # 상품이름
                # 상품가격
                , 'price': float([i.text for i in tree.xpath("//div[@class='price-stock']/div/span/span")][0][1:]),
                'image_url': [i.get('src') for i in tree.xpath("//img[@id='main-image']")],
                'description': tree.xpath("//div[@id='ja-tab-description']/div/div/text()"),
                'currency': 'dollar'}


__all__ = ['get_categories', 'get_product_list', 'get_product_detail']
