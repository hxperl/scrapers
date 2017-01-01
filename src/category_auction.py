import requests
import re
from lxml import html

response = requests.get('http://script.auction.co.kr/common/HeaderCategoryInfo.js')

assert response.status_code == 200
print("****옥션 카테고리****")
#print(response.content)
pattern = "HeaderCategoryT\('\d{2}0{6}', '.*'"
#hash table 3번째 트리부터 탐색
r = re.compile(pattern)
#패턴 설정
match = r.findall(response.text)
#찾기
match = list(set(match))



for i in match:
   #print(i)

   hash_key = i.replace("HeaderCategoryT('", "")
   hash_key = hash_key[:2]
   category = i.replace("HeaderCategoryT('", "")
   category = category[12:]
   category = category.replace("', 'A'", "")
   #print(hash_key)
   print(category)

   pattern2 = "HeaderCategoryT\('"+hash_key+"\d{6}', '.*'"
   r2 = re.compile(pattern2)
   match2 = r2.findall(response.text)
   match2 = list(set(match2))
   for j in match2:
       hash_key2 = j.replace("HeaderCategoryT('", "")
       hash_key2 = hash_key2[:8]
       if hash_key2[2]=='0' and hash_key2[3]=='0':
           continue
       category2 = j.replace("HeaderCategoryT('", "")
       category2 = category2[12:]
       category2 = category2.replace("', 'A'", "")

       print("         "+category2)

       try:
           response2 = requests.get('http://listings.auction.co.kr/category/list.aspx?category='+hash_key2)
           assert response2.status_code==200
           tree = html.fromstring(response2.content)
           #print(response.status_code)
           for k in tree.xpath("//ul[@class='group_list']/li/a"):
               print("                      "+k.text)
       except:
           pass
