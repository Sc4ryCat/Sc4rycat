from openpyxl.styles.builtins import title
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# 결과 저장용 모듈
import pandas as pd # pandas: 표 형태로 데이터를 저장/분석
from openpyxl import Workbook # 엑셀(xlsx) 저장을 위한 모듈

# 검색어 목록을 정의(이 검색어들을 반복적으로 검색)
keywords = ["selenium python","chatgpt","보안 자동화"]

# 크롬 브라우저가 꺼지지 않게 옵션 설정
options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension',False)
# chromdriver 연결
service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# 검색 결과 저장을 위한 초기화 작업
result_list = [] # pandas용 리스트(나중에 dataframe으로 변환)
wb = Workbook() # 새 액셀파일 생성
ws = wb.active # 첫번째 시트 선택
ws.title= "검색결과" # 시트 이름 지정
ws.append(["검색어","제목","링크"]) # 엑셀 첫 줄 헤더 작성

# 검색 자동화를 무한 반복 시작(ctrl + C 중단 가능)
# keywords = ["selenium python","chatgpt","보안 자동화"]
try:
    while True:
        # 각 키워드에 대해서 순차적으롤 검색
        for keyword in keywords:
            print(f" 검색어: {keyword}")
            # 구글페이지 열기
            driver.get("https://google.com")
            time.sleep(1) # 페이지 로딩 대기

            # 검색창 찾고 키워드 입력
            search_box = driver.find_element(By.NAME,"q")
            search_box.clear()
            search_box.send_keys(keyword)
            search_box.submit()
            time.sleep(2)

            # 검색 결과 제목 태그(h3) 찾기 상위3개만
            results = driver.find_elements(By.CSS_SELECTOR,"h3")[:3]

            for result in results:
                try:
                    title = result.text.strip() # 제목 텍스트 추출
                    link = result.find_element(By.XPATH,"..").get_attribute("href") # a 태그에서 링크 추출

                    # pandas용 리스트에 저장(딕셔너리)
                    result_list.append(
                        {
                            "검색어": keyword,
                            "제목" : title,
                            "링크" : link
                        }
                    )
                    # 엑셀 시트에도 같은 데이터 추가
                    ws.append([keyword, title, link])
                except:
                    continue #오류 발생시 해당 결과를 넘겨주세요

        # 엑셀 파일 저장
        wb.save("google_search_results.xlsx")
        print("엑셀 저장 완료 : google_search_results.xlsx")

        # pandas dataframe 생성 후 csv 파일로 저장
        df = pd.DataFrame(result_list)
        df.to_csv("google_search_results.csv", index=False,encoding="utf-8-sig")
        print("pandas csv 저장 완료 : google_search_results.csv")

        # 다음 검색 주기까지 대기(20초)
        print(" 20초 대기중...\n")
        time.sleep(20)

except KeyboardInterrupt:
    print("사용자 종료")
    driver.quit() # 브라우저 종료

    # 마지막 검색결과를 다시 저장
    wb.save("google_search_results.xlsx")
    pd.DataFrame(result_list).to_csv("google_search_results.csv", index=False, encoding="utf-8-sig")