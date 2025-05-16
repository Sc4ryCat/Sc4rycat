from flask import Flask,request,render_template
# RSA 키 생성을 위한 모듈을 import
from Crypto.PublicKey import RSA # RSA 키 생성 모듈
from Crypto.Signature import pkcs1_15 # 전자서명(v1.5방식) 모듈
from Crypto.Hash import SHA256 # 해시 알고리즘

# 암호문을 사람이 읽을수 있도록 인코딩하기 위한 모듈
import base64
# RSA 키 생성(개인키/공개키)
key = RSA.generate(2048) # 2048비트 rsa키쌍 생성
private_key = key # 개인키 추출
public_key = key.public_key() # 공개키 추출


app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def encoding():
    message = "" # 사용자 입력 메시지
    signature = "" # 전자서명
    result = "" # 결과 메시지(성공/실패)

    if request.method == "POST":
        message = request.form.get("message","") # 입력된 값 가져오기
        action = request.form.get("action") # sign/verify

        try:
            if action == "sign":
                # 전자서명 생성
                # SHA256 해시 생성
                hash_val = SHA256.new(message.encode("utf-8"))
                # 개인키로 해시값에 서명 생성
                sign = pkcs1_15.new(private_key).sign(hash_val)
                # 서명을 base64로 인코딩하여 문자열로 저장
                signature = base64.b64encode(sign).decode("utf-8")
                result = "전자서명 생성 완료"

            elif action == "verify":
                # 전자서명 검증
                # 입력된 서명을 base64디코딩
                sign = base64.b64decode(request.form.get("signature",""))
                # 메시지를 다시 해시
                hash_val = SHA256.new(message.encode("utf-8"))
                # 공개키로 서명 검증 수행
                pkcs1_15.new(public_key).verify(hash_val, sign)
                result = " 전자서명 검증 성공:메시지가 위조되지 않았습니다"

        except Exception as e:
            # 서명 검증 실패시 예외 처리
            result = f"전자서명 검증 실패:{str(e)}"


    # encode.html 템플릿에 변수들을 넘겨서 화면에 출력
    return render_template("sign.html",
                           message = message,
                           signature = signature,
                           result = result
                           )

 # 이 파일이 직접 실행되었을때 웹서버 시작
if __name__ == "__main__":
# 디버그 모드로 127.0.0.1:5000에서 실행
    app.run(host='127.0.0.1', port=5000, debug=True)
#   app.run(debug=True)`