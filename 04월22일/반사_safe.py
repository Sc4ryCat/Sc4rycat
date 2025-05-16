from flask import Flask,request,render_template

app = Flask(__name__)

# Flask 애플리케이션 객체 생성
@app.route("/", methods=["GET","POST"])
def xss():
     # 사용자 입력값 초기화
    reflected_xss_string = ""
    # get 요청일 때만 동작(url에 입력값을 넣었을 경우)
    if request.method == 'GET':
        # 쿼드스트링에 inpuText 라는 파라미터가 있을 경우
        if "inputText" in request.args:
            # 사용자가 입력한 값을 가져와서 변수에저장해 주세요
            reflected_xss_string = request.args.get("inputText", default="", type=str)
    # html 템플릿에 값을 전달해서 화면에 보여주세요
    return render_template("reflected_xss_safe.html",
                           reflected_xss_string=reflected_xss_string)

 # 이 파일이 직접 실행되었을때 웹서버 시작
if __name__ == "__main__":
# 디버그 모드로 127.0.0.1:5000에서 실행
      app.run(debug=True)
