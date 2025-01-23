import streamlit as st
import json
import urllib.parse
import re  # 정규표현식 사용

# JSON 파일 읽기
with open("restaurants.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def normalize_price(price):
    """가격 문자열에서 숫자만 추출"""
    try:
        if isinstance(price, int):  # 이미 숫자인 경우 그대로 반환
            return price
        if not price:  # 가격이 비어 있는 경우 0 반환
            return 0
        return int(re.sub(r"[^\d]", "", price))  # 숫자 외의 모든 문자를 제거
    except (ValueError, TypeError):
        return 0  # 비정상적인 값은 0으로 처리

def search_by_keyword(data, keyword, field="식당명", price=None):
    """키워드와 가격으로 데이터 검색"""
    result = []

    for restaurant in data:
        if field == "식당명" and keyword in restaurant["식당명"]:
            result.append(restaurant)
        elif field == "주소" and keyword in urllib.parse.unquote(restaurant["주소"]):
            result.append(restaurant)
        elif field == "메뉴":
            matching_menus = []
            for menu in restaurant["메뉴"]:
                menu_price = normalize_price(menu["가격"])  # 가격을 숫자로 변환
                # 메뉴명과 가격 조건을 모두 만족하는 경우
                if keyword in menu["메뉴명"] and (price is None or menu_price == price):
                    matching_menus.append(menu)
            if matching_menus:  # 조건에 맞는 메뉴가 있다면
                result.append({
                    "식당명": restaurant["식당명"],
                    "주소": restaurant["주소"],
                    "메뉴": matching_menus,  # 조건에 맞는 메뉴만 포함
                })
        elif field == "가격":
            for menu in restaurant["메뉴"]:
                menu_price = normalize_price(menu["가격"])  # 가격을 숫자로 변환
                if menu_price == normalize_price(keyword):  # 가격이 일치하는 경우
                    result.append(restaurant)
                    break
    return result

def display_results(restaurants):
    """검색된 식당 정보 출력"""
    if restaurants:
        for restaurant in restaurants:
            st.write(f"**식당명**: {restaurant['식당명']}")
            st.write(f"**주소**: {urllib.parse.unquote(restaurant['주소'])}")  # 주소 디코딩
            for menu in restaurant["메뉴"]:
                st.write(f"- **메뉴명**: {menu['메뉴명']}, **가격**: {menu['가격']}")
            st.write("=" * 30)
    else:
        st.write("검색 결과가 없습니다.")

# Streamlit을 사용하여 인터페이스 만들기
st.title("노포식당 검색기")

# 필드 선택 (주소, 메뉴명, 가격)
field_choice = st.selectbox("검색 카테고리를 선택하세요", ["식당명", "주소", "메뉴", "가격"])

# 검색어 입력
keyword = st.text_input(f"{field_choice}(으)로 검색할 키워드를 입력하세요")

# 메뉴와 가격 조건 추가
price = None
if field_choice == "메뉴":
    price_input = st.text_input("희망 가격 (선택 사항, 숫자만 입력)")
    if price_input:
        try:
            price = int(price_input)
        except ValueError:
            st.error("가격은 숫자로 입력해야 합니다.")

# 검색 실행 버튼
if st.button("검색"):
    if keyword:
        filtered_results = search_by_keyword(data, keyword, field_choice, price if field_choice == "메뉴" else None)
        display_results(filtered_results)
    else:
        st.error("검색어를 입력해야 합니다.")
