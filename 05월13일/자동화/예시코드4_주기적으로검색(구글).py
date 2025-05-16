from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# 검색어 목록을 정의(이 검색어들을 반복적으로 검색)
keywords = ["selenium python","chatgpt","보안 자동화"]

# 브라우저가 꺼지지 않게 옵션 설정
options = Options()
options.add_experimental_option("detach", True)
# 탐지 방지용 옵션(capcha)
# 자동화 도구 감지 기능 비활성화
options.add_argument("--disable-blink-features=AutomationControlled")
# chrome 자동화됨이라는 메시지 제거
options.add_experimental_option("excludeSwitches", ["enable-automation"])
# 자동화 확장 사용 안함
options.add_experimental_option('useAutomationExtension',False)
# chromdriver 연결
service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# 검색 자동화를 무한 반복 시작(ctrl + C 중단 가능)
# keywords = ["selenium python","chatgpt","보안 자동화"]
try:
    while True:
        # 각 키워드에 대해서 순차적으롤 검색
        for keyword in keywords:
            print(f" 검색어: {keyword}")
            # 구글페이지 열기
            driver.get("https://google.com")
            # 검색창 찾기
            search_box = driver.find_element(By.NAME,"q")
            # 검색 입력창 초기화
            search_box.clear()
            # 검색어 입력
            search_box.send_keys(keyword)
            # 검색 진행(enter)
            search_box.submit()
            # 결과 페이지 잠시 보여주기(사람처럼 행동)
            time.sleep(5)
        # 모든 키워드 검색 후 30초 대기
        print("10초 대기중...\n")
        time.sleep(10)

except KeyboardInterrupt:
    print("사용자 종료")
    driver.quit()





