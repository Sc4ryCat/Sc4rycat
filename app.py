"""
파일 구조
flask_app/
--app.py
--templates/ ->폴더
    -- index.html
"""
from flask import Flask,request,render_template
app = Flask(__name__)

# Flask 애플리케이션 객체 생성
@app.route("/", methods=["GET","POST"])
def index():
    result = "" # 결과 출력을 위한 변수 초기화
    # 사용자가 폼을 제출했을때 (POST 요청일 때)
    if request.method == 'POST':
        user_input = request.form["user_input"]
        result = f"당신이 입력한 값:{user_input}"

    # index.html 템플릿을 렌더링하면서 result값 전달
    return render_template("index.html", result=result)

 # 이 파일이 직접 실행되었을때 웹서버 시작
if __name__ == "__main__":
# 디버그 모드로 127.0.0.1:5000에서 실행
      app.run(debug=True)
