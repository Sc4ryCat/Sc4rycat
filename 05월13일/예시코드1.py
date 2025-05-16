from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# 브라우저가 꺼지지 않게 옵션 설정
options = Options()
options.add_experimental_option("detach", True)

# chromdriver 연결
service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# 구글 열기
driver.get("https://google.com")

# 검색창에 검색어 입력
search_box = driver.find_element(By.NAME,"q")
search_box.send_keys("파이썬 셀레니움 자동 검색")
search_box.submit() # 엔터키

time.sleep(3) # 결과 잠깐 보기위해서 대기해 주세요
# driver.quit() # 창 닫고 싶을 때 사용




