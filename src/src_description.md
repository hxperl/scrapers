# 11번가 카테고리목록 로딩 소스내용

- main html에서 카테고리목록을 얻는데 한계가 있어서 inc_footer_data.js파일에서 카테고리목록을 얻음

- inc_footer_data.js파일안의 내용 `"CtgrLv":3,"RefCtgrNo":127680...CtgrLv":3,"RefCtgrNo":1454...CtgrLv":3,"RefCtgrNo":14617,"`

  CtgrLv :3 , RefCtgrNo: '하위 카테고리 링크 주소' 패턴으로 코딩 되어있음

- `pattern = """("CtgrLv":3,"RefCtgrNo":\d+)""" 해당 패턴을 정규식으로 추출 후 중복되는 내용은 제거

- 링크 주소목록만 다시 추출해서 loop문 안에서 해당 주소로 requests.

  하위 카테고리 주소는 'http://www.11st.co.kr/html/category/(추출한 링크주소).html'의 형식

  requests.get('http://www.11st.co.kr/html/category/'+ i + '.html')  //  loop문안에서 i값은 링크 주소

- requests.get으로 얻은 내용을 html폼으로 tree에 저장

- selector로 tree내에 카테고리 상위 품목을 출력해주고 하위 품목은 여러개 이므로 다시 loop문으로 구현

- loop문 안에 하위 카테고리 이름 출력과 해당 카테고리 주소로 가는 링크주소를 얻음(해당 카테고리가 포함하는 더 하위 카테고리들이 있기 때문)

  `response = requests.get(k.get('href'))`

- response내용을 tree에 저장하고 selector로 마지막 최하위 카테고리목록들을 찾아서 loop문으로 출력

  c=1

  ```python
              for l in tree.xpath("//span[@class='txt_cat']"):
                  if(c==1):
                      c+=1
                      continue
                  print("                     "+l.text)
  ```

변수 c용도 : selector로 얻은 리스트 첫번째 요소는 항상 '전체상품보기'가 있는데 해당 요소는 출력하지 않기 위해



# 옥션 카테고리 목록 로딩 소스 내용

- HeaderCategoryInfo.js파일에 카테고리 목록들이 해쉬테이블로 잘 정리되어있어서 해당 파일 requests.get

- HeaderCategoryInfo.js파일 내용 일부

  ```javascript
  cateGroupList[0] = new HeaderCategoryT('8', '브랜드 패션', 'A');
  ```

  ```javascript
  cateLcodeGroupByGroupIdHash['8'] = new Array(

  new HeaderCategoryT('80001', '브랜드 의류', 'A'),

  new HeaderCategoryT('80002', '브랜드 잡화', 'A')

  );
  ....

  categoryByLcodeGroupIdHash['80001'] = new Array(

  new HeaderCategoryT('66000000', '브랜드 여성의류', 'A'),

  new HeaderCategoryT('67000000', '브랜드 남성의류', 'A'),

  new HeaderCategoryT('68000000', '브랜드 캐주얼의류', 'A')

  );
  ```

  각 키값이 다음 하위 카테고리 품목으로 연결되는 특징이 있는데

  최상위 테이블부터 연결하고 싶었지만 3번째 테이블 값 ex) '80001'과 그 안의 값들 {'66000000', '67000000', '68000000'} 이 연관성이 없어서 정규식으로 추출하기에는 한계가 있었음//  정확한 패턴 범위 설정/ 일정하지 않은 목록 개수, newline문제 등등

- 그 다음 테이블부턴 키값이 해당 테이블내에 키값과 연관성이 있음

  ```javascript
  childCategoryHash['66000000'] = new Array(

  new HeaderCategoryT('66120000', '홈쇼핑브랜드', 'A'),

  new HeaderCategoryT('66010000', '티셔츠', 'A'),

  new HeaderCategoryT('66020000', '원피스', 'A'),

  new HeaderCategoryT('66110000', '블라우스/셔츠', 'A'),

  new HeaderCategoryT('66030000', '팬츠', 'A'),
  ```

  66000000 테이블 안에는 66XX0000의 키값을 가짐. 그리고 이 값은 해당 카테고리로 연결하는 링크 주소

- 시작 출력을 3번째 테이블 내용부터 하기로 해서 key값이 'XX000000' 패턴을 가지고 있으면 정규식으로 모두 추출

  `pattern = "HeaderCategoryT\('\d{2}0{6}', '.*'"`

  1. 문자열 자르기로 맨앞의 정수 2자리만 얻고 hash_key에 저장

  2. 문자열 자르기로 카테고리명만 얻어서 category에 저장

     ex) hash_key : 66, category : 브랜드 여성의류

     ​      hash_key : 67, category : 브랜드 남성의류

     ​      hash_key : 68, category : 브랜드 캐쥬얼의류

- 그 다음도 비슷한 과정으로 hash_key를 이용해 

  `pattern2 = "HeaderCategoryT\('"+hash_key+"\d{6}', '.*'"`

  HeaderCategoryT('(hash_key)XXXXXX')의 패턴(해쉬키2자리 + 아무 숫자 6자리)을 찾아냄

- 문자열 자르기로 다시 hash_key2 와 category2 에 각각 값을 저장한다.

  category2는 화면에 출력하고 hash_key2는 하위 카테고리 페이지로 연결하는 링크주소로 활용한다.

- EX) hash_key : 66 패턴 검색 결과로

  66000000

  66010000

  66020000

  66110000

  .... 결과 값을 얻을 수 있는데 66000000은 첫번째 내용과 중복되므로

  `if hash_key2[2]=='0' and hash_key2[3]=='0':`

  ​	`continue`

  코드로 제거해준다.

- hash_key2로 하위 카테고리 페이지 requests.get

  `response2 = requests.get('http://listings.auction.co.kr/category/list.aspx?category='+hash_key2)`

  response내용을 tree에 담고 마지막 최하위 카테고리가 위치한곳을 selector로 지정해서 loop문으로 출력해준다.

- > 잘 정리된 테이블을 정규식으로 추출하는데 한계가 있었는데 나중에 json을 활용해서 python위에서 javascript코드를 실행하는 방향으로 테이블값을 얻을 수 있으면 깔끔하게 구현 될수 있을것 같음.

  ​

  ​

  ​