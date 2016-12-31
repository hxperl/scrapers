import requests
import re
from lxml import html

response = requests.get('http://www.gmarket.co.kr/')
assert response.status_code==200
tree = html.fromstring(response.content)
#print(response.content)
print("****G마켓 카테고리****")
for i in tree.xpath("//div[@id='main_gnb']/ul/li/a"):
    print(i.text)
    for j in i.xpath("../div/div/dl/dt"):
        print("         "+j.text)
        for k in j.xpath("../dd/a"):
            print("                 "+k.text)
            try:
                response2 = requests.get(k.get('href'))
                assert response2.status_code==200
                tree2 = html.fromstring(response2.content)
                for l in tree2.xpath("//div[@class='mid-all-list']/div/h3/a"):
                    print("                         "+l.text)
                    href = l.get('href')
                    ccp = href[:33]
                    ccp = ccp[25:]
                    pattern = "javascript:GoSNAChannel\('" + ccp + "_\d+"
                    r = re.compile(pattern)
                    match = r.findall(href)
                    for m in match:
                        m = m[25:]
                        pattern2 = "<li><a href=\"javascript:GoSNAChannel\('"+m+"_\d+"+".*"
                        r2 = re.compile(pattern2)
                        match2 = r2.findall(response2.text)
                        for n in match2:
                            hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
                            result = hangul.sub('', n)
                            print("                                 "+result)
            except:
                pass
