import os    # 파일 정보(경로,시간 등)
import time  # 시간 형식 변환을 위한 모듈

# 분석할 대상 파일 이름 설정
file = "./test.txt"

# 파일이 존재하는지 확인
if os.path.exists(file):
    # 파일 생성시간 가져오기 초단위로 타임스탬프
    created = os.path.getctime(file)
    # 사람이 읽을 수 있는 형식으로 변환(YYYY-MM-DD HH:MM:SS)
    created_time = time.strftime('%Y-%M-%D %H:%M:%S',time.localtime(created))
    print(" 생성 시간: " + created_time)
    # 파일 최종 수정 시간
    modified = os.path.getmtime(file)
    modified_time = time.strftime('%Y-%M-%D %H:%M:%S', time.localtime(modified))
    print(" 수정 시간: " + modified_time)
    # 파일 접근 시간
    accessed = os.path.getatime(file)
    accessed_time = time.strftime('%Y-%M-%D %H:%M:%S', time.localtime(accessed))
    print(" 접근 시간: " + accessed_time)

else:
    # 파일이 존재하지 않을 경우 안내 메시지 출력
    print(f"파일이 존재하지 않습니다: {file}")