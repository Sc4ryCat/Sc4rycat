from flask import Flask,request,render_template,make_response,redirect,jsonify

# 쿠키를 저장하는 함수
def save_cookie(response,customer_id):
    if customer_id in ["tom","jerry","aaaaaa"]:
        response.set_cookie("my_cookie",customer_id)
    return response

# 요청한 금액을 처리하는 함수
def precess_money(money):
    return money

app = Flask(__name__)
@app.route("/", methods=["GET","POST"])
def money():
    get_cookie = ""     # 서버가 받은 쿠키값
    customer_id = ""    # 사용자가 입력한 id
    withdraw_money = "" # 인출 요청 금액
    request_money = ""  # 사용자가 요청한 금액

    if request.method == "POST":
     # 사용자가 제출한 id와 요청금액 읽기
       customer_id =  request.form["myID"]
       request_money =  request.form["requestMoney"]
       # 클라이언트가 보낸 쿠키중 my_cookie값을 읽음
       get_cookie = request.cookies.get('my_cookie')
        # 요청 금액 처리
       withdraw_money =  precess_money(request_money)
       if not get_cookie:  # 쿠키값이 없으면
            get_cookie = "서버로 전송된 쿠키 없어요!"
    # html 렌더링
    response = make_response(
        render_template('client_code_practice.html',
                    customer_id = customer_id,
                    withdraw_money = withdraw_money,
                    get_cookie = get_cookie))
    # 조건에 따라서 쿠키 저장(tom,jerry,???)
    response = save_cookie(response,customer_id)

    return response

# 고객 잔액 조회 요청 처리(잔고보기 눌렀을때)
@app.route("/get_balance", methods=["GET","POST"])
def get_balance():
    # json 형식으로 전달된 데이터를 수신
    content = request.json
    customer_id = content["customer_id"]
    # 사용자 id에 따라 잔액 결정
    if customer_id =="tom":
        balance = "100000"
    elif customer_id =="jerry":
        balance = "200000"
    elif customer_id =="aaaaaa": # maxlength =  5
        balance = "limites"
    else:
        balance = "block_out"
    return jsonify({"balance":balance})
# jsonify -> 딕셔너리나 리스트를 json형태도 변환

 # 이 파일이 직접 실행되었을때 웹서버 시작
if __name__ == "__main__":
# 디버그 모드로 127.0.0.1:5000에서 실행
      app.run(debug=True)

"""
요약설명
쿠키저장(set_cookie): POST 요청으로 ID를 입력하면 특정 ID일 경우 쿠키로 저장
쿠키읽기(request.cookies.get):클라이언트가 다시 요청할때 저장된 쿠키를 서버가 읽음
잔액조회(get_balance): json으로 요청하고 json으로 응답
"""