# app.py — 저장된 뉴스를 웹으로 보여주는 Flask 서버
from flask import Flask, render_template
from pymongo import MongoClient

# flask 웹 애플리케이션 객체를 생성하고 app 변수에 저장
# 여기
app = Flask(__name__)

# mongodb 연동
# 여기
client = MongoClient('mongodb://localhost:27017/') # 로컬 PC에서 실행 중인 MongoDB에 연결
db = client['security_db']  # security_db라는 데이터베이스를 선택
col = db['security_news']

# 웹 브라우저가 / 주소로 접속했을 때 index() 함수를 실행하도록 설정
# 여기
@app.route('/')
def index():
    news_list = col.find().sort('published',-1)
    return render_template('index9.html',news_list=news_list)

# 개발시 python 실행가능하도록
if __name__ == "__main__":
    app.run(debug=True)