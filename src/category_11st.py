import requests
import re
from lxml import html

response = requests.get('http://www.11st.co.kr/html/inc_footer_data.js')

assert response.status_code == 200

print("****11번가 카테고리****")
#print(response.content)
pattern = """("CtgrLv":3,"RefCtgrNo":\d+)"""
#카테고리 레벨 3인것만 골라내기
r = re.compile(pattern)
#패턴 설정

match = r.findall(response.text)
#찾기

match = list(set(match))
#중복제거

#print(match)

for i in match:
    i = i.replace("\"CtgrLv\":3,\"RefCtgrNo\":", "") #하위 카테고리 링크만 추출
    #print(i)
    #print(type(i))
    try:
        print('\t')
        response = requests.get('http://www.11st.co.kr/html/category/'+ i + '.html')
        #하위 링크 get요청
        assert response.status_code == 200
        #print(response.status_code)
        tree=html.fromstring(response.content)
        #하위 링크 카테고리 불러오기
        j = tree.xpath("//h3[@class='tit']")
        print(j[0].text + "\n")
        for k in tree.xpath("//h4[@class='s_tit']/a"):
            print("         "+k.text)
            #print("         "+k.get('href'))
            try:
                response = requests.get(k.get('href'))
                assert response.status_code==200
                tree=html.fromstring(response.content)
                c=1
                for l in tree.xpath("//span[@class='txt_cat']"):
                    if(c==1):
                        c+=1
                        continue
                    print("                     "+l.text)
            except:
                pass

    except:
        pass
