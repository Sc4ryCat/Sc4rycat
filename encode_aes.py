# 대칭키 암호화 방식
# 사용자가 텍스트를 입력하고 encode,decode 선택하면
# 서버에서 AES(EAX모드)를 이용해서 변환결과를 화면에 보여주는 구조
from flask import Flask,request,render_template
# Pycryptodome 라이브러리에서 AES 암호화 기능 import
from Crypto.Cipher import AES
# 암호문을 텍스트 형태로 안전하게 표현하기 위해 BASE64 사용
import base64
# 16바이트 키 설정(128비트) AES 암호화키
key = b'sixteen byte key'
# EAX모드에서 사용하는 초기값 세팅 / 한번만 사용하는값
nonce = b'abcdefghijkl' # nonce -> number once

# 플라스크 객체 생성
app = Flask(__name__)
# get  데이터 요청  ex) url?name=??
# post 서버에 데이터 전송(등록,수정)

# Flask 애플리케이션 객체 생성
@app.route("/encoding", methods=["GET","POST"])
def encoding():
    # 사용자로부터 입력받은 텍스트와 결과값을 초기화
    convert_text = ""
    convert_result = ""
    method_type = "encode" # 기본값을 encode

    # 사용자가 폼을 제출했을때 (POST 요청일 때)
    # 폼에서 값이 전송된 경우
    if request.method == "POST":
        # inputText라는 이름의 폼 필드에서 텍스트를 가져옴
        convert_text = request.form["inputText"]
        # select 박스 선택된 값(encode,decode)가져옴
        method_type = request.form["convert_select"]
    # 입력된 텍스트가 존재할 경우 인코딩 또는 디코딩  수행
    if convert_text: # 입력된 텍스트가 있으면
        if method_type == "encode":
            # AES 암호화 객체 생성(EAX모드, nonce 포함)

            convert_result
        elif method_type == "decode":

            convert_result
    # encoding.html 템플릿에 변수들을 넘겨서 화면에 출력
    return render_template("encode.html",
                           convert_text = convert_text,
                           method_type = method_type,
                           convert_result = convert_result
                          )

 # 이 파일이 직접 실행되었을때 웹서버 시작
if __name__ == "__main__":
# 디버그 모드로 127.0.0.1:5000에서 실행
    app.run(host='127.0.0.1', port=5000, debug=True)
#   app.run(debug=True)


