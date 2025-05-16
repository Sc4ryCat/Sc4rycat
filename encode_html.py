from flask import Flask,request,render_template
# 문자열을 조작하고 해석(parsing)하는데 사용되는 표준 라이브러리
# HTML 특수문자 인코딩/디코딩
from html import escape,unescape

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
            # encode면 HTML 인코딩
            convert_result = escape(convert_text)
        elif method_type == "decode":
            # decode면 HTML 디코딩
            convert_result = unescape(convert_text)
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


