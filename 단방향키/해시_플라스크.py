from flask import Flask,request,render_template
# hash함수 사용하기 위한 모듈
from Crypto.Hash import SHA256
import base64
app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def encoding():
    convert_text = ""
    convert_result = ""
    method_type = "encode" # 기본값을 encode

    if request.method == "POST":
        convert_text = request.form["inputText"]
        method_type = request.form["convert_select"]
    if convert_text: # 입력된 텍스트가 있으면
        if method_type == "encode":
            hash = SHA256.new()
            hash.update(convert_text.encode('utf-8'))
            convert_result = hash.hexdigest()

        elif method_type == "decode":
            convert_result = "복호화 할 수 없습니다."

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


