from flask import Flask,request,render_template
# RSA 키 생성을 위한 모듈을 import
from Crypto.PublicKey import RSA
# RSA 암호화를 위한 OAEP 패닝 모듈 import
from Crypto.Cipher import PKCS1_OAEP
# 암호문을 사람이 읽을수 있도록 인코딩하기 위한 모듈
import base64
"""
1024 bit 보안수준 낮음 사용자제
2048 bit 표준 보안 수준  일반적인 웹사이트 인증서,ssl/tls통신
3072 bit 고보안 수준  정부기관,금융기관
4096 bit 매우 높은 보안  군사,고위험 중요 인프라
키 길이가 길수록 보안은 높아지지만 암호화/복호화 속도가 느려진다
"""
# RSA 키 생성(2048 bit)
key = RSA.generate(2048)

# 공개키를 사용한 암호화 객체 생성
cipher_ras_public = PKCS1_OAEP.new(key.public_key())

# 개인키를 사용한 복호화 객체 생성
cipher_ras_private = PKCS1_OAEP.new(key)

app = Flask(__name__)
@app.route("/", methods=["GET","POST"])
def encoding():
    # 사용자로부터 입력받은 텍스트와 결과값을 초기화
    convert_text = ""
    convert_result = ""
    method_type = "encode" # 기본값을 encode

    if request.method == "POST":
        # inputText라는 이름의 폼 필드에서 텍스트를 가져옴
        convert_text = request.form["inputText"]
        # select 박스 선택된 값(encode,decode)가져옴
        method_type = request.form["convert_select"]

    if convert_text:  # 입력된 텍스트가 있으면
        if method_type == "encode":
            # 입력 텍스트를 utf-8로 인코딩 후 공개키로 암호화
            convert_result =  cipher_ras_public.encrypt(
                convert_text.encode('utf-8')
            )
            # 암호문을 base64로 인코딩을해서 출력 가능하도록 변환
            convert_result = base64.b64encode(convert_result).decode('utf-8')

        elif method_type == "decode":
            # base64로 인코딩된 암호문을 다시 바이트로 디코딩
            encrpyted_data =  base64.b64decode(convert_text)
            # 개인키로 복호화 한 후 utf-8로 디코딩 해서 복원
            convert_result = cipher_ras_private.decrypt(encrpyted_data).decode('utf-8')

    # encode.html 템플릿에 변수들을 넘겨서 화면에 출력
    return render_template("encode.html",
                           convert_text=convert_text,
                           method_type=method_type,
                           convert_result=convert_result
                           )

 # 이 파일이 직접 실행되었을때 웹서버 시작
if __name__ == "__main__":
# 디버그 모드로 127.0.0.1:5000에서 실행
    app.run(host='127.0.0.1', port=5000, debug=True)
#   app.run(debug=True)




