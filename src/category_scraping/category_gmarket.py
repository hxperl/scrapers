import requests
import re
from lxml import html

response = requests.get('http://www.gmarket.co.kr/')    # main 페이지 get
assert response.status_code==200
tree = html.fromstring(response.content)            # main 페이지 tree 생성
print("****G마켓 카테고리****")
for i in tree.xpath("//div[@id='main_gnb']/ul/li/a"):
    print(i.text)                                   # 상위 카테고리부터 출력
    for j in i.xpath("../div/div/dl/dt"):
        print("         "+j.text)                   # 해당 카테고리 아래 포함된 하위 카테고리 리스트 출력
        for k in j.xpath("../dd/a"):
            print("                 "+k.text)       # 해당 카테고리 아래 포함된 하위 카테고리 리스트 출력
            try:
                response2 = requests.get(k.get('href'))     # 하위 카테고리 링크 get
                assert response2.status_code==200
                tree2 = html.fromstring(response2.content)  # 하위 카테고리 DOM tree 생성
                for l in tree2.xpath("//div[@class='mid-all-list']/div/h3/a"):
                    print("                         "+l.text)
                    href = l.get('href')
                    ccp = href[:33]
                    ccp = ccp[25:]          # ccp 값 추출
                    pattern = "javascript:GoSNAChannel\('" + ccp + "_\d+"   # ccp 값으로 정규식 패턴 설정
                    r = re.compile(pattern)
                    match = r.findall(href)
                    for m in match:
                        m = m[25:]
                        pattern2 = "<li><a href=\"javascript:GoSNAChannel\('"+m+"_\d+"+".*" # 최하위 카테고리를 찾는 패턴
                        r2 = re.compile(pattern2)
                        match2 = r2.findall(response2.text)
                        for n in match2:
                            hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')      # 결과 값 중 한글 패턴 찾기
                            result = hangul.sub('', n)
                            print("                                 "+result) # 최하위 카테고리 출력
            except:
                pass
