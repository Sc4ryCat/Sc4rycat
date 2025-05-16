from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

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

# Javascript로 자동화 정보 제거
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{
    "source": """
        Object.defineProperty(navigator, 'webdriver',{
            get: () =?> undefined
        });
        """
})


# 구글 열기
driver.get("https://www.naver.com")

# 검색창에 검색어 입력
# 네이버 검색창은 name=query가 아닌 id=query이다
search_box = driver.find_element(By.ID,"query")
search_box.send_keys("파이썬 셀레니움 자동 검색")
search_box.submit() # 엔터키

time.sleep(3) # 결과 잠깐 보기위해서 대기해 주세요
# driver.quit() # 창 닫고 싶을 때 사용




