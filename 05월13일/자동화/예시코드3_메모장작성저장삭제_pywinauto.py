from os import remove

from pywinauto.application import Application # 윈도우 gui 자동화
import subprocess # 외부 파이썬 파일 실행
import time # 대기 시간 설정
import os # 파일 경로 및 삭제

# 저장할 파이썬 스크립트 경로
file_path = r"C:\Users\user\PycharmProjects\security\자동화\samplecode.py"

# 메모장 실행
app = Application().start("notepad.exe")
time.sleep(0.5) # 메모장 창이 뜰 시간을 잠깐 줌

# 메모장 편집창에 파이썬 코드 입력
app.UntitledNotepad.Edit.type_keys("print('메모장 자동입력 후 삭제')", with_spaces=True)

# 파일-> 저장 메뉴 클릭
app.UntitledNotepad.menu_select("파일(&F)->저장(&S)")
time.sleep(0.1) # 저장창이 뜰 시간을 줌

# 저장 창 조작( 창 제목은 언어에 따라 다를 수 있으므로 정규식 사용
save_dialog = app.window(title_re=".*저장")

# 파일경로 입력
save_dialog.Edit1.set_edit_text(file_path)

# 콤보막스의 항목을 출력할때
print(save_dialog.ComboBox2.item_texts())

# 파일 형식: 모든 파일 형식으로 설정
save_dialog.ComboBox2.select("모든 파일 (*.*)")

# 인코딩 방식 : utf-8로 설정
save_dialog.ComboBox3.select("UTF-8")

# 저장 버튼 클릭
save_dialog.Button1.click()
time.sleep(1.0) # 저장완료 대기

# 메모장 종료 시도
try:
    # 종료 메뉴 선택
    app.UntitledNotepad.menu_select("파일(&F)->끝내기(X)")
except:
    # 만약 종료가 실패하면 강제로 종료해 주세요
    app.kill()

# 저장한 .py파일을 실행
cmd = subprocess.run(["python",file_path], capture_output=True) # 실행결과를 캡쳐
print(cmd.stdout.decode()) # 표준 출력 결과 보여주기

# # 실행이 끝난 py파일 삭제
# remove(file_path)







