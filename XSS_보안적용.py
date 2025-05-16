# 보안이 취약한 웹앱(XSS학습 테스트)
from flask import Flask,request
from html import escape
app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def safe():
    comment = ""
    if request.method == "POST":
        # 사용자 입력 그대로 출력해 주세요
        # comment = request.form.get("comment")
        # 입력값 HTML 인코딩
        comment = escape(request.form.get("comment"))
    return f"""
    
    <html>
    <body>
        <h2> XSS 테스트 입력</h2>
        <form method="POST">
            <input type="text" name="comment">
            <input type="submit" value="제출">
            
        </form>
        <h2>XSS 테스트 댓글</h2>
        <div>{comment}</div> <!-- 취약점 발생 지점
        
    </body>
    </html>   
    """

 # 이 파일이 직접 실행되었을때 웹서버 시작
if __name__ == "__main__":
# 디버그 모드로 127.0.0.1:5000에서 실행
    app.run(host='127.0.0.1', port=5000, debug=True)
#   app.run(debug=True)


