import requests
import re
from lxml import html

response = requests.get('http://www.11st.co.kr/html/inc_footer_data.js')

assert response.status_code == 200      # 응답 코드 확인

print("****11번가 카테고리****")
pattern = """("CtgrLv":3,"RefCtgrNo":\d+)"""        #카테고리 레벨 3인것만 골라내기
r = re.compile(pattern)         #패턴 설정
match = r.findall(response.text)

match = list(set(match))        #중복제거


for i in match:
    i = i.replace("\"CtgrLv\":3,\"RefCtgrNo\":", "") #하위 카테고리 링크만 추출
    try:
        print('\t')
        response = requests.get('http://www.11st.co.kr/html/category/'+ i + '.html')    #하위 링크 get요청
        assert response.status_code == 200
        tree=html.fromstring(response.content)      #하위 링크 카테고리 불러오기
        j = tree.xpath("//h3[@class='tit']")
        print(j[0].text + "\n")
        for k in tree.xpath("//h4[@class='s_tit']/a"):
            print("         "+k.text)
            try:
                response = requests.get(k.get('href'))
                assert response.status_code==200
                tree=html.fromstring(response.content)
                for c,l in enumerate(tree.xpath("//span[@class='txt_cat']")):
                    if(c==0):
                        continue
                    print("                     "+l.text)
            except:
                pass

    except:
        pass
