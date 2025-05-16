"""
CREATE TABLE comments (
    id INT IDENTITY(1,1) PRIMARY KEY,        -- 자동 증가하는 기본 키
    content NVARCHAR(MAX) NULL               -- 댓글 내용 (NULL 허용)
);
"""
from flask import Flask, request, render_template
import pyodbc

app = Flask(__name__)

# MSSQL 연결 정보
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"  # 또는 서버 주소 / SQLEXPRESS 등
    "DATABASE=mytest;"
    "UID=test;"
    "PWD=test;"
    "TrustServerCertificate=yes;"
)

def get_connection():
    return pyodbc.connect(conn_str)

@app.route("/", methods=["GET","POST"])
def xss():

    if request.method == "POST":
        comment = request.form.get("comment","")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("insert into comments (content) values (?)", (comment,))
        conn.commit()
        conn.close()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select content from comments order by id DESC")
    rows = cursor.fetchall()
    # 리스트 내표
    comment = [row[0] for row in rows]
    """"
    comment = ["테스트입니다",
               "12121313",
               "test"]
    """
    conn.close()


    return render_template("stored_xss_unsafe_db.html",
                           comments=comment)

 # 이 파일이 직접 실행되었을때 웹서버 시작
if __name__ == "__main__":
# 디버그 모드로 127.0.0.1:5000에서 실행
      app.run(debug=True)





