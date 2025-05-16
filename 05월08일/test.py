# 응답에 판단 문자열이 있는지 확인 (취약 여부 판별)
def check_vulnerability(response, url, payload):
    judgment_strings = get_judgment_strings()               # 판단 기준 문자열 가져오기

    # 응답 내용에 판단 문자열이 포함돼 있는지 확인
    for judgment_string in judgment_strings.strings:
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
    for injection_string in injection_strings.strings:
        payload = make_payload(form_info, injection_string)  # 공격용 입력값 생성
        url = urljoin(start_url, form_info.action)           # 상대경로를 절대 URL로 변환
        response = send_injection(url, form_info, payload)   # 공격 데이터 전송
        check_vulnerability(response, url, payload)          # 응답 분석 및 결과 출력

# 실행 시작점
if __name__ == "__main__":
    page_url = "http://127.0.0.1:5000/"           # 테스트 대상 URL
    page_scan(page_url)                                      # 취약점 스캔 함수 실행