import winreg # 윈도우 레지스트리 접근을 위한 모듈
# 오피스 버전별 레지스트리 경로 지정
office_versions = {
    "Office 2007": "12.0",
    "Office 2010": "14.0",
    "Office 2013": "15.0",
    "Office 2016/19/365": "16.0"
}

# 경로를 찾았는지 여부 확인
found = False

for version_name,version_num in office_versions.items():
    try:
        reg_path = fr"Software\Microsoft\Office\{version_num}\Excel\File MRU"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,reg_path) as hkey:
            print(f"\n {version_name} ({version_num}) 경로 발견")
            for i in range(winreg.QueryInfoKey(hkey)[1]):
                # 키의 이름(name), 값(value), 타입(type)을 튜플로 가져옴
                name, value, _ = winreg.EnumValue(hkey, i)
                # 이름이 Item 으로 시작하는 항목만 필터링
                if name.startswith("Item"):
                    print(f"{name}: {value}")
            found = True

    except FileNotFoundError:
        # 해당 버전이 설치 안되어 있거나 기록이 없는 경우
        continue

if not found: # false
    print("어떤 office 버전에서도 경로를 찾을수 없습니다.")
"""
버전 자동 순회
설치가 안 된 경우 무시
"""

"""
2007 12.0
2010 14.0
2013 15.0
2016 16.0
2019/365 16.0  
"""