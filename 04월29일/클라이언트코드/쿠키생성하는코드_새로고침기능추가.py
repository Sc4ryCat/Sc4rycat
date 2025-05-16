from flask import Flask,request,render_template,make_response,redirect

"""
make_response: 응답객체를 직접 생성할수 있게 해주는 함수
쿠키설정,헤더 추가,상태코드 변경 등 추가작업을 하고 싶을때
"""
app = Flask(__name__)
@app.route("/", methods=["GET","POST"])
def set_cookie():
    cookie_text = "" # 사용자가 입력한 텍스트를 저장할 변수
    get_cookie = "" # 클라이언트로부터 전달받은 쿠키값을 저장할 변수

    if request.method == "POST":
        cookie_text = request.form["inputText"]
        # 이전에 저장할 쿠키중에서 my_cookie라는 이름의 쿠키값을 가져오세요
        get_cookie = request.cookies.get('my_cookie')

        if not get_cookie:  # 쿠키값이 없으면
            get_cookie = "서버로 전송된 쿠키 없어요!"

    response = make_response(render_template('client_code_cookie.html',
                    cookie_text = cookie_text,
                    get_cookie = get_cookie
                    ))

    # 사용자가 값을 입력했을 경우, 쿠키 my_cookie를 생성해서 response에 추가
    if cookie_text:
        response.set_cookie("my_cookie",cookie_text)
    return response

 # 이 파일이 직접 실행되었을때 웹서버 시작
if __name__ == "__main__":
# 디버그 모드로 127.0.0.1:5000에서 실행
      app.run(debug=True)
