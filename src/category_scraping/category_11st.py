import requests
import re
from lxml import html

response = requests.get('http://www.11st.co.kr/html/inc_footer_data.js')        # 11번가 카테고리 목록이 저장된 파일 get요청

assert response.status_code == 200      # 응답 코드 확인

print("****11번가 카테고리****")
pattern = """("CtgrLv":3,"RefCtgrNo":\d+)"""        # 카테고리 레벨 3인것만 골라내기
r = re.compile(pattern)         # 패턴 설정
match = r.findall(response.text)

match = list(set(match))        # 중복제거


for i in match:
    i = i.replace("\"CtgrLv\":3,\"RefCtgrNo\":", "") #하위 카테고리 링크만 주소 추출 'RefCtgrNo' 뒤에 나오는 값만 얻음
    try:
        print('\t')
        response = requests.get('http://www.11st.co.kr/html/category/'+ i + '.html')    # 하위 카테고리링크 주소로 get요청
        assert response.status_code == 200
        tree=html.fromstring(response.content)
        j = tree.xpath("//h3[@class='tit']")            # tree생성
        print(j[0].text + "\n")
        for k in tree.xpath("//h4[@class='s_tit']/a"):
            print("         "+k.text)
            try:
                response = requests.get(k.get('href'))      # 'a' tag안의 'href' 값으로 get요청
                assert response.status_code==200
                tree=html.fromstring(response.content)
                for c,l in enumerate(tree.xpath("//span[@class='txt_cat']")):
                    if(c==0):                       # 첫번째 요소 '전체상품보기' 는 출력하지 않음
                        continue
                    print("                     "+l.text)
            except:
                pass

    except:
        pass
