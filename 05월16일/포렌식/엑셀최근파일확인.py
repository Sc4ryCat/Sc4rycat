import winreg # 윈도우 레지스트리 접근을 위한 모듈

try:
    hkey = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Office\16.0\Excel\File MRU"
    )

    for i in range(winreg.QueryInfoKey(hkey)[1]):
        # 키의 이름(name), 값(value), 타입(type)을 튜플로 가져옴
        name,value,_ = winreg.EnumValue(hkey,i)
        # 이름이 Item 으로 시작하는 항목만 필터링
        if name.startswith("Item"):
            print(f"{name}: {value}")

except FileNotFoundError:
    print("Excel 2016 버전이 맞지 않거나 설치 되어 있지 않습니다.")

"""
2007 12.0
2010 14.0
2013 15.0
2016 16.0
2019/365 16.0  
"""