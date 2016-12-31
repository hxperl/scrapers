import requests
import re
from lxml import html

response = requests.get('http://category.gmarket.co.kr/listview/L100000103.aspx')
assert response.status_code==200
tree = html.fromstring(response.content)

for i in tree.xpath("//div[@class='mid-all-list']/div/h3/a"):
    print(i.text)
    href = i.get('href')
    ccp = href[:33]
    ccp = ccp[25:]
    pattern = "javascript:GoSNAChannel\('" + ccp + "_\d+"
    r = re.compile(pattern)
    match = r.findall(href)
    for j in match:
        j = j[25:]
#        print(j)
        pattern2 = "<li><a href=\"javascript:GoSNAChannel\('"+j+"_\d+"+".*"
        r2 = re.compile(pattern2)
        match2 = r2.findall(response.text)
        for k in match2:
            hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
            result = hangul.sub('', k)
            print("         "+result)

'''
    pattern2 = "<li><a href=\"javascript:GoSNAChannel\('"+ccp+"_\d"+".*"
    r2 = re.compile(pattern2)
    match2 = r.findall(response.text)
    for j in match2:
        j = j[167:]
        j = j.replace("</a></li>", "")
        print("            "+j)
'''
