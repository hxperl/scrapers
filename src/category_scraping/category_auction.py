import requests
import re
from lxml import html

response = requests.get('http://script.auction.co.kr/common/HeaderCategoryInfo.js') # 카테고리 목록이 정리된 파일 get요청

assert response.status_code == 200
print("****옥션 카테고리****")
pattern = "HeaderCategoryT\('\d{2}0{6}', '.*'"      #hash table 에서 키값을 얻는 정규식 패턴
r = re.compile(pattern)
match = r.findall(response.text)
match = list(set(match))                            # 중복 제거

for i in match:
   hash_key = i.replace("HeaderCategoryT('", "")    # 키값만 추출
   hash_key = hash_key[:2]
   category = i.replace("HeaderCategoryT('", "")
   category = category[12:]
   category = category.replace("', 'A'", "")        # 카테고리 이름 추출
   print(category)                                  # 카테고리 이름 출력

   pattern2 = "HeaderCategoryT\('"+hash_key+"\d{6}', '.*'"  # 하위카테고리 키값들의 패턴
   r2 = re.compile(pattern2)
   match2 = r2.findall(response.text)
   match2 = list(set(match2))           # 중복 제거
   for j in match2:
       hash_key2 = j.replace("HeaderCategoryT('", "")   # 두번째 키값 추출. 아래 카테고리 링크 주소로 사용
       hash_key2 = hash_key2[:8]
       if hash_key2[2]=='0' and hash_key2[3]=='0':      # 하위 카테고리 loop인데 상위카테고리도 패턴에 포함되므로 상위카테고리 검색은 제외 시킴
           continue
       category2 = j.replace("HeaderCategoryT('", "")
       category2 = category2[12:]
       category2 = category2.replace("', 'A'", "")      # 하위 카테고리 이름 출출

       print("         "+category2)             # 하위 카테고리 이름 출력

       try:
           response2 = requests.get('http://listings.auction.co.kr/category/list.aspx?category='+hash_key2)
           assert response2.status_code==200
           tree = html.fromstring(response2.content)
           for k in tree.xpath("//ul[@class='group_list']/li/a"):
               print("                      "+k.text)               # 최하위 카테고리 출력
       except:
           pass
