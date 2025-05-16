from flask import Flask,request,render_template
# RSA 키 생성을 위한 모듈을 import
from Crypto.PublicKey import RSA # RSA 키 생성 모듈
# RSA 암호화를 위한 OAEP 패닝 모듈 import
from Crypto.Cipher import PKCS1_OAEP
import base64

from base64_sample import decoded_bytes

app = Flask(__name__)

key_pair = RSA.generate(2048)
public_key = key_pair.public_key() # 공개키를 추출
private_key = key_pair # 개인키는 생성된 key_pair 자체

@app.route("/", methods=["GET","POST"])
def encoding():
    # 사용자로부터 입력받은 텍스트와 결과값을 초기화
    input_text = ""
    result = ""
    method = "encode" # 기본값을 encode

    if request.method == "POST":
        # inputText라는 이름의 폼 필드에서 텍스트를 가져옴
        input_text = request.form["inputText"]
        # select 박스 선택된 값(encode,decode)가져옴
        method = request.form["convert_select"]

        try:
            if method == "encode":
                # 공개키로 암호화 객체(도구) 생성
                cipher_encrypt = PKCS1_OAEP.new(public_key)
                # 평문을 공개키로 암호화 -> 암호문이 생성이 됨
                # 평문을 바이트로 변환후 암호화
                ciphertext = cipher_encrypt.encrypt(input_text.encode("utf-8"))
                # 암호문을 보기좋게 변환
                result = base64.b64encode(ciphertext).decode("utf-8")
            elif method == "decode":
                # 개인키로 복호화 도구를 생성
                cipher_decrypt = PKCS1_OAEP.new(private_key)
                # base64 문자열 -> 바이트로 디코딩
                decoded_bytes = base64.b64decode(input_text)
                # 복호화 실행
                decrypted = cipher_decrypt.decrypt(decoded_bytes)
                # 바이트를 문자열로 변환
                result = decrypted.decode("utf-8")
                
        except Exception as e:
                result = f"[Error] 복호화 실패: {str(e)}"

    # encode.html 템플릿에 변수들을 넘겨서 화면에 출력
    return render_template("rsa_form.html",
                           convert_text = input_text,
                           method_type = method,
                           convert_result = result
                           )

 # 이 파일이 직접 실행되었을때 웹서버 시작
if __name__ == "__main__":
# 디버그 모드로 127.0.0.1:5000에서 실행
    app.run(host='127.0.0.1', port=5000, debug=True)
#   app.run(debug=True)`
