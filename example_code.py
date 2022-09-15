from module.Module import SearchClass

if __name__ == "__main__":
    # Class 생성
    S = SearchClass()

    S.set_user_agent("")
    # 검색될 페이지 상한 지정
    S.set_page_upper_bound(5)

    # 검색어 지정
    S.set_product("반팔")

    # 적용할 제한 조건 지정
    S.set_constrain("총장", 72, 74)
    S.set_constrain("가슴단면", 64, 100)

    # 검색 시작
    S.page_search("tee", reset_file=True)

