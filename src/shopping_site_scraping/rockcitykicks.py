import requests
from lxml import html
from lxml import etree


class Rockcitykicks():

    def keep_search(self, i, _dict, full_url=False):
        # 상품관련없는 페이지는 return
        if i.get('href') in ['/blogs/news', '/pages/about-us', '#mega-search']:
            return
        cate_name = i.text.strip()                          # 카테고리 이름
        url = 'https://rockcitykicks.com' + i.get('href')   # 카테고리 url
        if full_url:                                        # url 주소가 fullpath인 경우
            url = i.get('href')                             # href값 만 넣어줌
        _dict.update(                                       # _dict정보 업데이트
            {cate_name: {'url': url}})
        # li class가 'is-sub-nested'인 경우
        if i.xpath("../ul/li[@class='is-sub-nested']"):
            full_url = True                                 # href값이 full path
        elif i.xpath("../ul/li"):
            full_url = False
        # brands, size페이지는 따로 찾음
        elif i.get('href') in ['/pages/brands', '/pages/size']:
            _dict[cate_name] = dict(_dict[cate_name], **{'children': {}})
            r = requests.get('https://rockcitykicks.com' + i.get('href'))
            assert r.status_code == 200
            tree = html.fromstring(r.content)
            lists = [i.get('href') for i in tree.xpath(
                "//section[@class='inner rte']/center/a | //section[@class='inner rte']/center/span/a")]        # href값을 모두 저장
            cate_names = [
                i.replace('http://rockcitykicks.com/collections/', '').replace('https://rockcitykicks.com/collections/', '') for i in lists]    # href에서 뒷부분을 카테고리 이름으로 설정
            _dict[cate_name]['children'].update(
                dict(zip(cate_names, lists)))       # {'카테고리 이름':'카테고리 주소'}딕셔너리 업데이트
            return
        else:                       # 하위 카테고리가 없을 경우
            return
        _dict[cate_name] = dict(_dict[cate_name], **{'children': {}})
        for j in i.xpath("../ul/li/a"):     # 하위 카테고리 탐색
            keep_search(j, _dict[cate_name]['children'], full_url)

    def get_categories(self):       # 카테고리 목록을 dictionary 타입으로 리턴
        _dict = {}
        r = requests.get('https://rockcitykicks.com')
        assert r.status_code == 200
        tree = html.fromstring(r.content)
        for i in tree.xpath("//nav[@class='header-nav header-desktop-nav']/ul/li/a"):
            keep_search(i, _dict)

        return _dict

    def get_product_list(self, url):                  # 상품 목록 출력

        num = 1               # 1페이지 부터
        while True:
            r = requests.get(url + '?page=' + str(num))     # 페이지번호를 넘겨주면서 get
            assert r.status_code == 200
            tree = html.fromstring(r.content)
            # 페이지에 상품 정보가 있으면
            if tree.xpath("//section[@class='product-item-info']"):
                for i in tree.xpath("//section[@class='product-item-info']/a"):
                    yield(i.text, 'https://rockcitykicks.com' + i.get('href'))
                num += 1    # 다음 페이지 번호
            else:           # 상품 정보가 없으면 더이상 페이지를 탐색하지 않고 break
                break

    def get_product_detail(self, url):            # 상품 상세 정보 출력
        r = requests.get(url)
        assert r.status_code == 200
        tree = html.fromstring(r.content)
        _dict = {'name': tree.xpath("//h1[@class='product-title']")[0].text,
                 'img_url': ['https:' + i.get('href')
                             for i in tree.xpath("//ul[@class='featured-image-list']/li/a")],   # 기본 정보 상품 이름, 이미지 주소
                 'soldout': False,
                 'description': [etree.tostring(i) for i in tree.xpath("//div[@class='tabs-content']")],
                 'brand': [i.get('content') for i in tree.xpath("//meta[@name='twitter:data2']")],
                 'currency': 'dollar'}
        _dict.update(dict(zip(['price', 'sale_price'], [
            float(i.text[1:]) for i in tree.xpath("//div[@class='product-prices']/span")])))               # 가격 정보. 품절상태이면 dictionary에 추가 되지 않음
        _dict.update({'option': dict(map(lambda x: x.split(
                      '-'), [i.text.replace(' ', '') for i in tree.xpath("//select[@id='product-select']/option")]))})  # 옵션. 품절상태이면 옵션이 비어있음
        if 'Sold Out' in [i.text for i in tree.xpath(
                "//div[@class='product-labels']/span") if not i.get('style')]:      # 품절 여부 검사
            _dict.update({'soldout': True})  # 품절이면 True
        return _dict            # dictionary 리턴

__all__ = ['get_categories', 'get_product_list', 'get_product_detail']
