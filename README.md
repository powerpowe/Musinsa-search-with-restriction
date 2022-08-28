# musinsa-clothes-search
무신사 홈페이지에서는 여러 가지의 조건으로 검색 시 L, XL에서 각각 그 조건들이 충족될 경우 그 제품이 노출되는 경우가 있었음.

예를 들어, 총장이 73~75, 가슴단면이 60 이상인 제품을 검색 시 

L : 총장 74, 가슴단면 57

XL : 총장 77, 가슴단면 63

위와 같은 제품 또한 검색 결과에 포함되어 검색되었다.

이를 해결하기 위해, 크롤링을 통해 무신사의 제품들을 크롤링하여 같은 사이즈에서 여러 제한 조건이 
충족된 경우에만 검색되고, 검색된 제품의 제품명과 사진을 디렉터리에 저장하도록 하였다.

# 사용 방법
1. SearchClass 인스턴스를 생성한다.
2. set_user_agent()를 통해 User-Agent를 지정해준다. 이는 https://www.whatismybrowser.com/detect/what-is-my-user-agent/ 에서 확인 가능하다.
3. set_product(product)를 통해 검색어를 지정해준다.
4. set_constrain(constrain, low, high)을 통해 제한 조건을 지정해준다.
5. set_page_upper_bound(high)를 통해 검색할 페이지의 상한을 지정해준다. 기본 high값은 100페이지이며, 
더 이상 상품이 검색이 되지 않는 페이지에 도달할 경우 자동으로 종료된다.
6. 마지막으로, page_search(file_name, verbose=True, reset_file=False)를 통해 검색을 시작한다.

example_code를 보면 쉽게 사용 방법을 이해할 수 있다.
