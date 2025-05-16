# 에러가 발생하면 인젝션이 성공이라고 판단하는 구조
# 실제로 sql 오류가 발생하지 않는 인제션은 탐지하지 못한다

from dataclasses import dataclass, field,asdict # 데이터클래스를 사용하기 위한 모듈
from typing import List        # 리스트 타입 지정
from bs4 import BeautifulSoup  # HTML 파싱을 위한 라이브러리
from urllib.parse import urljoin # 상대 URL을 절대 URL로 변환
import requests   # HTTP 요청을 보내기 위한 라이브러리

# 세션 객체 생성( 쿠키 유지 등에 사용)
s = requests.Session()

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

# 판단 문자열 생성함수

def get_judgement_strings():
    judgement_strings = JudgementString() # 객체 생성
    judgement_strings.string += {   # 에러판단을 위한 문자열
        "pyodbc.programmingerror"
    }
    return judgement_strings

def get_injection_strings():
    injection_strings = InjectionString() # 객체 생성
    injection_strings.string += { # sql 인젝션 시도용 문자열
        "'","tom","tom'","tom'''"
    }
    return injection_strings

# 웹 페이지에서 <form> 태그 영역만 추출하는 함수
def get_form_area(url):
    soup = BeautifulSoup(s.get(url).content,"html.parser")
    form_area = soup.find("form") # 첫번째 form 태그 찾기
    return form_area

# form 영역에서 action,method, input 태크 정보 추출하는 함수
def get_form_info(form_area):
    form_field = FormField()
    form_field.action = form_area.attrs.get("action").lower() # action 속성 추출
    form_field.method = form_area.attrs.get("method","get").lower() # method 속성추출 없으면 get


    # 모든 input 태그를 순회하며 정보를 수집
    for input_tag in form_area.find_all("input"):
        input_field = InputField() # 입력 필드 객체 생성
        input_field.type = input_tag.attrs.get("type", "text")
        input_field.name = input_tag.attrs.get("name")
        input_field.value = input_tag.attrs.get("value", "")

        form_field.input_fields.append(input_field)

    return form_field

def check_pandan(response, url, payload):
    judgment_strings = get_judgement_strings()

    # 응답 내용에 판단 문자열이 포함돼 있는지 확인
    for judgment_string in judgment_strings.string:
        if judgment_string in response.content.decode().lower():
            # 판단 문자열이 발견되면 취약점 가능성 출력
            print("인젝션 발견: ", url,
                  "\n테스트 데이터: ", str(payload),
                  "\n검출 문구: ", judgment_string,
                  "\n", "-"*10)

# 공격용 payload 생성 함수
def make_payload(form_info, injection_string):
    payload = {}                                             # 공격용 데이터 저장용 딕셔너리

    # input 필드 중 submit이 아닌 항목에만 공격 문자열 삽입
    for input_field in form_info.input_fields:
        if input_field.type != "submit":
            payload.update({input_field.name: injection_string})  # {name: 인젝션문자열}

    return payload                                           # 완성된 payload 반환

# 공격 데이터 전송 함수
def send_injection(url, form_info, payload):
    if form_info.method == "post":                           # POST 방식일 경우
        response = s.post(url, data=payload)                 # POST 요청 전송
    elif form_info.method == "get":                          # GET 방식일 경우
        response = s.get(url, params=payload)                # GET 요청 전송
    return response                                          # 응답 반환

# 전체 테스트 실행 함수
def page_scan(start_url):
    form_area = get_form_area(start_url)                     # 폼 영역 추출
    form_info = get_form_info(form_area)                     # 폼 필드 정보 추출
    injection_strings = get_injection_strings()              # 인젝션 문자열 목록 추출

    # 각 인젝션 문자열마다 테스트 수행
    for injection_string in injection_strings.string:
        payload = make_payload(form_info, injection_string)  # 공격용 입력값 생성
        url = urljoin(start_url, form_info.action)           # 상대경로를 절대 URL로 변환
        response = send_injection(url, form_info, payload)   # 공격 데이터 전송
        check_pandan(response, url, payload)          # 응답 분석 및 결과 출력

# 실행 시작점
if __name__ == "__main__":
    page_url = "http://127.0.0.1:5000/"           # 테스트 대상 URL
    page_scan(page_url)