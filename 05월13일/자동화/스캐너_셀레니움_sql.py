# 에러가 발생하면 인젝션이 성공이라고 판단하는 구조
# 실제로 sql 오류가 발생하지 않는 인제션은 탐지하지 못한다
# 필요한 셀레니움 모듈 가져오기
from selenium import webdriver
from selenium.webdriver.common.by import By # 요소를 탐색
from selenium.webdriver.support.ui import WebDriverWait # 대기 기능
from selenium.webdriver.support import expected_conditions as ec # 요소가 특정 상태일까지 기다림
from selenium.common.exceptions import TimeoutException # 타임아웃 예외처리
from selenium.webdriver.chrome.service import Service # 크롬드라이버 실행관련
from selenium.webdriver.chrome.options import Options # 브라우저 옵션

from dataclasses import dataclass, field,asdict # 데이터클래스를 사용하기 위한 모듈
from typing import List        # 리스트 타입 지정
from urllib.parse import urljoin # 상대 URL을 절대 URL로 변환

# 입력 필드를 정의하는 데이터 클래스
@dataclass
class InputField:
    type: str = "" # input type (예, text,submit)
    name: str = "" # input name 속성
    value: str = "" # input의 기본값

@dataclass
class FormField:
    action: str = "" # 폼 전송 주소
    method: str = "" # GET or POST
    input_fields: List[InputField] = field(default_factory=list) # 포함된 input 목록

 # 판단 문자열(취약점 여부를 확인할 기준 문자열)을 담는 클래스
@dataclass
class JudgementString:
    # 판단할 문자열 리스트  List : 3.7~3.8 / list : 3.9 이상
    string: List[str] = field(default_factory=list) # 인제션에 사용할 문자열 리스트
    # string: list[str] = field(default_factory=list) # 인제션에 사용할 문자열 리스트

@dataclass
class InjectionString:
    string: List[str] = field(default_factory=list) # 인제션에 사용할 문자열 리스트

# sql 에퍼 판단 문자열 생성함수
def get_judgement_strings():
    return JudgementString(string=["pyodbc.programmingerror"])

def get_injection_strings():
    return InjectionString(string=["'","tom","tom'","tom'''"])

# 웹 페이지에서 <form> 태그 영역만 추출하는 함수
def get_form_area(url):
    browser.get(url) # 브라우저에서 페이지 열기
    try:
        element = WebDriverWait(browser,3).until(
            ec.presence_of_element_located((By.TAG_NAME,"form"))
        )
    except TimeoutException:
        print("form not found") # form이 없을 경우 메시지 출력
        return None # 실패시 None값 반환
    return element

# form 영역에서 action,method, input 태크 정보 추출하는 함수
def get_form_info(form_area):
    form_field = FormField()
    # form_field.action = form_area.attrs.get("action").lower() # action 속성 추출
    # form_field.method = form_area.attrs.get("method","get").lower() # method 속성추출 없으면 get
    form_field.action = form_area.get_attribute("action").lower()  # action 속성 추출
    form_field.method = form_area.get_attribute("method").lower()  # method 속성추출 없으면 get

    # form 내부의 모든 <input> 요소를 추출해 주세요
    input_tags = form_area.find_elements(By.TAG_NAME,"input")

    # 모든 input 태그를 순회하며 정보를 수집
    for input_tag in input_tags:
        if input_tag.get_attribute("type").lower() != "text":
            continue

        # 입력 필드 데이터 구성
        input_field = InputField(
            type= input_tag.get_attribute("type"),
            name= input_tag.get_attribute("name"),
            value= input_tag.get_attribute("value")
        )
        form_field.input_fields.append(input_field)

    return form_field

# 응답에서 sql 에러 문구가 포함 여부 확인
def check_pandan(response, url, injection_string):
    # 응답 내용에 판단 문자열이 포함돼 있는지 확인
    for judgment_string in get_injection_strings().string:
        if judgment_string in response.lower():
            # 판단 문자열이 발견되면 취약점 가능성 출력
            print("인젝션 발견: ", url,
                  "\n테스트 데이터: ", injection_string,
                  "\n검출 문구: ", judgment_string,
                  "\n", "-"*10)

# 공격 데이터 전송 함수
def send_injection(url, form_info, injection_string):
    browser.get(url) # 공격할 대상 페이지 열기

    # 각 input필드에 인젝션 문자열 입력
    for input_field in form_info.input_fields:
        input_element = browser.find_element(By.NAME, input_field.name)
        input_element.clear() # 기존값을 삭제해 주세요
        input_element.send_keys(injection_string) # 공격용 페이로드 삽입

    # form 제출 (submit 버튼 대신 자동 제출)
    form_element = browser.find_element(By.TAG_NAME, "form")
    form_element.submit()

    # 전송 후, 에러 메시지가 뜨는지 확인
    try:
        element = WebDriverWait(browser,10).until(
            ec.presence_of_element_located((By.CLASS_NAME,"errormsg"))
        )
        return element.text # 에러 텍스트 반환
    except TimeoutException:
        return "" # 에러 없을 경우 빈 문자열


# 전체 테스트 실행 함수
def page_scan(start_url):
    form_area = get_form_area(start_url)                     # 폼 영역 추출
    if not form_area:
        return # form 없으면 종료해 주세요

    form_info = get_form_info(form_area)                     # 폼 필드 정보 추출
    injection_strings = get_injection_strings()              # 인젝션 문자열 목록 추출

    # 각 인젝션 문자열마다 테스트 수행
    for injection_string in injection_strings.string:
        full_url = urljoin(start_url,form_info.action) # 상대경로-> 절대경로
        response = send_injection(full_url, form_info, injection_string) # 공격실행
        check_pandan(response, full_url, injection_string)          # 응답 분석 및 결과 출력

# 실행 시작점
if __name__ == "__main__":
    # 브라우저 옵션
    options = Options()
    options.add_experimental_option("detach", True)
    # 드라이버 서비스 경로 지정
    service = Service(executable_path="./chromedriver.exe")
    # Selinum 4 권장방식으로 브라우저 실행
    browser = webdriver.Chrome(service=service, options=options)
    try:
        # 테스트할 페이지 url
        page_url = "http://127.0.0.1:5000/"
        page_scan(page_url) # 스캔 실행
    finally:
        browser.quit()