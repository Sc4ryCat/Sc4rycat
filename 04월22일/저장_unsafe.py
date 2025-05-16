from flask import Flask,request,render_template

app = Flask(__name__)

# 서버에 저장된 사용자 코멘트(DB대신 전역변수로 저장)
stored_comments = []
# Flask 애플리케이션 객체 생성
@app.route("/", methods=["GET","POST"])
def xss():
     # 사용자 입력값 초기화
    global stored_comments

    if request.method == "POST":
        comment = request.form.get("comment","")
        stored_comments.append(comment)

    return render_template("stored_xss_unsafe.html",
                           comments=stored_comments)

 # 이 파일이 직접 실행되었을때 웹서버 시작
if __name__ == "__main__":
# 디버그 모드로 127.0.0.1:5000에서 실행
      app.run(debug=True)
