from flask import Flask,request,render_template

app = Flask(__name__)
@app.route("/", methods=["GET","POST"])

def ajax_unsafe():
    reflected_xss_string = ""

    if request.method == "GET":
        if "inputText" in request.args:
            reflected_xss_string = request.args.get("inputText",
                                                    default="", type=str)
        return render_template("xss_ajax_unsafe.html",
                               reflected_xss_string=reflected_xss_string)

@app.route("/get_data", methods=["GET","POST"])
def get_data():
    your_id = request.args.get('id')
    return "Hi " + str(your_id) + "!!!"
    #  Hi tom !!! 값을 넘김

 # 이 파일이 직접 실행되었을때 웹서버 시작
if __name__ == "__main__":
# 디버그 모드로 127.0.0.1:5000에서 실행
      app.run(debug=True)