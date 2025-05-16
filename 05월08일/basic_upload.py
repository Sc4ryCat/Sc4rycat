from flask import Flask,request,render_template
# 파일 이름을 안전하게 처리하기 위한 모듈
from werkzeug.utils import secure_filename
import os  # 파일 및 디렉터리 경로를 다루기 위한 모듈

app = Flask(__name__)

# 업로드 파일을 저장할 폴더
upload_folder = './uploads'
# 업로드 폴더가 없으면 자동으로 생성해 주세요
os.makedirs(upload_folder, exist_ok=True)
# flask 설정에 업로드 폴더 경로 저장
app.config['UPLOAD_FOLDER'] = upload_folder

@app.route("/upload", methods=["GET","POST"])
# @app.route("/upload")
def upload():
    return render_template('upload_form.html')

@app.route("/upload_process", methods=["POST"])
def upload_process():

        # name = "uploaded_file"
        file = request.files['uploaded_file']
        # 파일 이름을 안전하게 만든뒤 업로드 폴더에 저장
        # file.save(os.path.join)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        return 'file upload complete!!!'

if __name__ == "__main__":
# 디버그 모드로 127.0.0.1:5000에서 실행
      app.run(debug=True)