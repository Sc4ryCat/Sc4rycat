# conn_str = (
#     "DRIVER={ODBC Driver 17 for SQL Server};"
#     "SERVER=localhost;"
#     "DATABASE=mytest;"
#     "UID=test;"
#     "PWD=test;"
#     "TrustServerCertificate=yes;"
#     # PORT=1433  1433은 SQL Server가 클라이언트 연결을 수신하는 기본 포트 번호 안써도 됨
# )

import pyodbc
import re # 정규표현식 패턴 검색을 위한 모듈
import pandas as pd
from dataclasses import dataclass,field
from typing import List

# 개인정보 정규표현식 패턴 정의하는 데이터 클래스
@dataclass
class Pattern:
    label: str # 항목 이름(email,phone 등) 필수 필드
    regex: str # 해당 항목의 정규표현식 필수필드 값(email,phone,ssn)

# 탐지 결과 저장용(각 행마다 어떤 개인정보가 탐지가 되었는지 저장)
@dataclass
class DetectionResult:
    table: str      # 탐지된 테이블 이름/ 필수 필드
    email: str = "" # 탐지된 이메일
    phone: str = "" # 탐지된 전화번호
    ssn : str = ""  # 탐지된 주민번호

# 검사 페이로드 구조(DB 접속 정보와 정규식 패턴 목록 포함)
@dataclass
class ScanPayload:
    connection_str : str # pyodbc용 mssql 연결 문자열
    patterns : List[Pattern] = field(default_factory=list) # 탐지할 패턴 리스트

# 개인정보 탐지 함수(DB연결 -> 모든 테이블 -> 개인정보 탐지)
def scan_personal_data(payload: ScanPayload) -> List[DetectionResult]:
    conn = pyodbc.connect(payload.connection_str) # mssql 연결
    cursor = conn.cursor()  # 커서 생성
    results = [] # 탐지 결과 저장 리스트

    # mssql의 모든 사용자 테이블 이름 가져오기
    cursor.execute("select table_name from information_schema.tables where table_type='base table'")
    tables = [row[0] for row in cursor.fetchall()] # 결과 테이블 목록으로 저장
    # row[0] : 여기서는 table_name만 선택했기 때문에 첫번째인 0
    # fetchall : 모든 행을 리스트로 변환
    # tables = ['','','','','']
    # 테이블 마다 반복
    for table in tables:
        try:
            cursor.execute(f"select * from [{table}]")
            columns = [desc[0] for desc in cursor.description] # 컬럼이름 추출
            rows = cursor.fetchall()

            # 각 행(row)마다 탐지 시도
            for row in rows:
                row_dict = dict(zip(columns, row)) # 컬럼이름과 값 맵핑
                result = DetectionResult(table = table) #결과 저장용 객체

                # 각 필드의 값(value)을 정규식으로 검사
                for value in row_dict.values():
                    # isinstance(value,str) : value가 문자연일지 확인
                    # continue 해당 반복문을 건너띄고 다음 값으로 넘김
                    if not isinstance(value,str): continue
                    for pattern in payload.patterns:
                        match = re.search(pattern.regex, value) # 정규표현식 매칭 시도
                        if match:
                            setattr(result,pattern.label, match.group()) # 결과 객체에 값을 채워주세요
                # 개인정보가 하나라도 탐지되면 결과에 추가
                if result.email or result.phone or result.ssn:
                    results.append(result)

        except Exception as e:
            print(f" {table} 테이블 오류 발생: {e}") # 예외발생시
            continue

    conn.close() # DB연결 종료
    return results # 결과 리스트 반환
# 페이로드 구성: DB연결 정보 + 탐지할 정규표현식 목록
payload = ScanPayload(
    connection_str=(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=mytest;"
    "UID=test;"
    "PWD=test;"
    "TrustServerCertificate=yes;"
    ),
    patterns=[
        # aaa@gamil.com
      Pattern("email", r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
      Pattern("phone", r"01[0-9]-\d{3,4}-\d{4}"),
      Pattern("ssn", r"\d{6}-\d{7}")
    ]
)

# 개인정보 탐지 실행
results = scan_personal_data(payload)

df = pd.DataFrame(r.__dict__ for r in results) # dataclass 객체를 딕셔너리로 변환
df.to_csv("mssql_detected_results.csv", index=False, encoding="utf-8-sig")
print("개인정보 탐지 완료. 결과는 : 'mssql_detected_results.csv'에 저장.")




