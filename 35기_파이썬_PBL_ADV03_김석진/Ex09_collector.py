# collector.py — 주기적으로 실행할 수집 스크립트
import feedparser
from pymongo import MongoClient
from datetime import datetime

# mongodb 에 연결
# 여기
client = MongoClient('mongodb://localhost:27017/') # 로컬 PC에서 실행 중인 MongoDB에 연결
db = client['security_db']  # security_db라는 데이터베이스를 선택
col = db['security_news']

# rss 로 연결하여 데이타 수집
def collect_security_news():
    rss_url = "https://www.boannews.com/rss/allArticle.xml"
    new_count = 0

    # 20개의 정보를 가지고 와서 중복되지 않도록 디비에 저장
    # 여기
    feed = feedparser.parse(rss_url)
    news_list = feed.entries[:20]

    for news in news_list:
        news_doc = {
            "title": news.title,
            "link": news.link,
            "published" : news.published,
            "is_critical" : '취약점' in news.title or '유출' in news.title
        }
        col.insert_one(news_doc)
    
        new_count += 1

    print(f"신규 뉴스 {new_count}건 저장 완료")

# 아래 코드는 이 파일에서 확인할 때 필요
if __name__ == "__main__":
    collect_security_news()