""""
platform, socket,psutil은 포렌식에서 시스템 환경을 파악할때
자주 쓰이는 표준 라이브러리
"""
from dataclasses import dataclass,field,asdict
import platform # os 관련 정보를 가져오는 모듈
import socket   # 컴퓨터 이름 정보
import psutil   # 시스템 자원(cpu,ram,디스크..) 정보를 가져오는 모듈
import pprint   # 데이터를 보기좋게 출력해주는 모듈

from numpy.ma.core import identity


# 램 저장 정보 클래스
@dataclass
class Ram:
    total: str = "" # 총 램 용량
    free : str = "" # 사용 가능한 용량
# 디스크 저장 정보 클래스
@dataclass
class Disk:
    total: str = "" # 총 디사크 용량
    free : str = "" # 사용 가능한 디스크 용량

# 전체 시스템 정보 저장용 데이터 클래스
@dataclass
class SystemInfo:
    system: str = ""       # os 운영체제 이름(예:Windows,Linux)
    version: str = ""      # os 버전
    architecture: str = "" # 시스템 아키텍쳐(X64,X32)
    hostname: str = ""     # 호스트 이름
    processor: str = ""    # cpu 정보
    cpu_core: str = ""     # cpu 코어 수
    ram: Ram = field(default_factory=Ram) # 램 정보(Ram 클래스 객체)
    disk: Disk = field(default_factory=Disk) # 디스크 정보(Disk 크래스 객체)
    # ram: Ram -> ram 변수는 Ram 클래스 타입입니다
"""
Ram.free -> Ram 클래스에 이런 속성이 있어요
SystemInfo.ram.free -> 실제로 그 속성에 어떤 값이 있는지 확인하는것
"""
# 시스템 정보를  수집하는 함수
def get_system_info():
    # 램정보
    ram = psutil.virtual_memory()
    # 디스크 정보 (루트 디렉토리 기준)
    disk = psutil.disk_usage(path='/')

    # Byte -> GB
    # 1024를 세번곱한다(1024 ** 3)
    ram_total = str(round(ram.total/ (1024.0 ** 3))) + " GB"
    ram_free = str(round(ram.available/ (1024.0 ** 3))) + " GB"
    disk_total = str(round(disk.total/ (1024.0 ** 3))) + " GB"
    disk_free = str(round(disk.free/ (1024.0 ** 3))) + " GB"

    # 시스템 정보 클래스 생성 및 값 채우기
    system_info = SystemInfo()
    # 운영체제 이름 가져오기
    system_info.system = platform.system()
    # 운영체제 버전 가져오기
    system_info.version = platform.version()
    # 아키텍쳐 정보 x64,x32
    system_info.architecture = platform.machine()
    # 호스트 이름
    system_info.hostname = socket.gethostname()
    # cpu 모델명
    system_info.processor = platform.processor()
    # cpu 코어수
    system_info.cpu_core = psutil.cpu_count()
    # 전체 램 용량
    system_info.ram.total = ram_total
    # 사용 가능한 램 용량
    system_info.ram.free = ram_free
    # 전체 디스크 용량
    system_info.disk.total = disk_total
    # 사용 가능한 디스크 용량
    system_info.disk.free = disk_free

    return system_info

# 시스템 정보 수집 실행
system_infomation = get_system_info()

# 예쁘게 출력( 딕셔너리 형태로 변환 후 보기 좋게 출력)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(asdict(system_infomation))