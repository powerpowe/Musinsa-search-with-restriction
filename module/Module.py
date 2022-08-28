import requests
from bs4 import BeautifulSoup
import os
import shutil

class SearchClass(object):
    """
    세팅한 제한 조건을 바탕으로 무신사에서 옷 정보 크롤링을 통해 검색된 옷을 디렉터리에 저장함.
    """
    
    def __init__(self):
        self.page = 100
        self.product = None
        self.headers = None
        self._constrain = {}

    def set_user_agent(self, headers):
        """
        크롤링에 필요한 User-Agent를 입력받는다.

        Args:
            headers(string) : User-Agent의 header를 입력받는다.
        """
        self.headers = {"User-Agent": headers}

    def set_page_upper_bound(self, page):
        """
        검색할 페이지의 상한을 설정함.

        Args:
            page (int) : 검색할 페이지의 상한을 설정함.
        """

        self.page = page
        
    def set_product(self, product):
        """
        검색할 검색어를 지정함.

        Args:
            product (string) : 검색어를 지정함.
        """
        self.product = product
    
    def set_constrain(self, constrain, low=0, high=10000):
        """
        제한 조건을 지정함.

        Args:
            constrain (string) : 제한 조건을 설정함.
            low (int) : 제한 조건의 하한을 설정함.
            high (int) : 제한 조건의 상한을 설정함.
        """
        self._constrain[constrain] = (low, high)
        
    def page_search(self, file_name, verbose=True, reset_file=False):
        """
        정한 검색어와 제한 조건을 바탕으로 검색을 시작함.

        Args:
            file_name (string) : 저장될 디렉터리명을 정함.
            verbose (bool) : 검색된 옷의 정보를 출력할지 결정
            reset_file (bool) : 이미 file_name 디렉터리가 존재하는 경우, 그 파일을 초기화시킬지 결정함.
        """

        if not self.product:
            raise Exception("Product is not defined. Please set product with set_product()")

        file_exist = os.path.exists(f"./{file_name}")
        
        if reset_file and file_exist:
            shutil.rmtree(f"./{file_name}")
            os.makedirs(f"./{file_name}")
        
        elif not file_exist:
            os.makedirs(f"./{file_name}")

        checked_name = []
        
        for p in range(1, self.page):
            url = f"https://www.musinsa.com/search/musinsa/goods?q={self.product}&list_kind=small&sortCode=pop&" \
                  f"page={p}&display_cnt=0&saleGoods=false&includeSoldOut=false&setupGoods=false&popular=false&" \
                  f"selectedFilters=%EA%B0%80%EC%8A%B4%EB%8B%A8%EB%A9%B4+64%7E68%3Ameasure_1%5E64%5E68%3Ameasure" \
                  f"%7C%EC%B4%9D%EC%9E%A5+72%7E74%3Ameasure_5%5E72%5E74%3Ameasure&originalYn=N&measure=measure_1%5E" \
                  f"64%5E68%2Cmeasure_5%5E72%5E74&openFilterLayout=N&groupSale=false"
            res = self._get_requests(url)
            soup = BeautifulSoup(res.text, "lxml")
            goods = soup.find_all('p', attrs = {"class": "list_info"})
            if not goods:
                print('모든 상품 탐색 완료')
                break
            for elem in goods:
                try:
                    brand = elem.find_previous_sibling().get_text()
                    a = elem.find('a')
                    name = a["title"]
                    link = a["href"]
                    price = elem.find_next_sibling().get_text().split()[-1]
                    link_res = self._get_requests(link)
                    link_soup = BeautifulSoup(link_res.text, "lxml")
            
                    thead = link_soup.find("thead")
                    tbody = link_soup.find("tbody")
                    tr_list = tbody.find_all("tr")
                    features = thead.get_text().split()

                    for tr in tr_list[2:]:  # 맨 앞 두 개는 사이즈 관련 아님
                        data = tr.get_text().split()
                        d = dict(zip(features, data))
                        if name in checked_name:
                            continue
                        c_low = [float(d[k]) - self._constrain[k][0] for k in self._constrain.keys()]
                        c_low = self._check_sign(c_low)
                        c_high = [self._constrain[k][1] - float(d[k]) for k in self._constrain.keys()]
                        c_high = self._check_sign(c_high)
                        
                        if all(c_low + c_high):
                            checked_name.append(name)
                            name = name.replace('/', '')
                            with open(f"./{file_name}/{name}.jpg", "wb") as f:
                                content_url = 'https:' + link_soup.find('div', attrs={'class': 'product-img'}).find('img')['src']
                                content_res = self._get_requests(content_url)
                                f.write(content_res.content)
                            if verbose:
                                print(f'브랜드: {brand}, 제품명: {name}, 가격대: {price}')
                                print(link)
                except:
                    pass

                
    def _get_requests(self, url):
        temp_res = requests.get(url, headers=self.headers)
        temp_res.raise_for_status()
        return temp_res

    def _check_sign(self, lst):
        sign = lambda x : False if x<0 else True
        return [sign(x) for x in lst]
    
