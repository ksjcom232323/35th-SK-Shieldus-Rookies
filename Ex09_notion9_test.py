import os
from dotenv import load_dotenv, set_key, find_dotenv
from notion_client import Client


# .env 파일 로드
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
PARENT_PAGE_ID = os.getenv("NOTION_PARENT_PAGE_ID")

if NOTION_TOKEN is None or PARENT_PAGE_ID is None:
    raise RuntimeError(
        "NOTION_TOKEN 또는 NOTION_PARENT_PAGE_ID가 설정되어 있지 않습니다."
    )

# set_key로 값을 저장할 .env파일경오
DOTENV_PATH = find_dotenv()

# Notion 클라이언트
notion = Client(auth=NOTION_TOKEN)


def create_todo_database():

    # 데이터베이스 제목
    title = [
        {
            "type": "text",
            "text": {
                "content": "자동 생성 ToDo DB"
            }
        }
    ]

    # 컬럼 정의
    properties = {
        "이름": {
            "title": {}
        },

        "상태": {
            "select": {
                "options": [
                    {"name": "Todo", "color": "red"},
                    {"name": "Doing", "color": "yellow"},
                    {"name": "Done", "color": "green"},
                ]
            }
        },

        "마감일": {
            "date": {}
        },

        "태그": {
            "multi_select": {
                "options": [
                    {"name": "개발", "color": "blue"},
                    {"name": "문서화", "color": "purple"},
                    {"name": "리뷰", "color": "orange"},
                ]
            }
        },

        "우선순위": {
            "number": {
                "format": "number"
            }
        },
    }

    # DB 생성
    db = notion.databases.create(
        parent={
            "type": "page_id",
            "page_id": PARENT_PAGE_ID,
        },

        title=title,

        initial_data_source={
            "properties": properties
        },
    )

    database_id = db["id"]

    print("새 데이터베이스 생성 완료!")
    print("Database ID:", database_id)

    # 생성된 DB에서 Data Source ID 가져오기
    db_info = notion.databases.retrieve(database_id)

    data_source_id = db_info["data_sources"][0]["id"]

    print("Data Source ID:", data_source_id)

    # 실제 Property 확인
    ds_info = notion.data_sources.retrieve(data_source_id)

    print("\n실제 Property:")

    for name, prop in ds_info["properties"].items():
        print(name, "->", prop["type"])

    return data_source_id


def add_sample_todo(data_source_id: str):

    records = [
        {
            "이름": {
                "title": [
                    {"text": {"content": "API로 만든 할 일 1"}}
                ]
            },
            "상태": {
                "select": {"name": "Todo"}
            },
            "마감일": {
                "date": {"start": "2026-11-30"}
            },
            "태그": {
                "multi_select": [
                    {"name": "개발"},
                    {"name": "문서화"}
                ]
            },
            "우선순위": {
                "number": 1
            },
        },

        {
            "이름": {
                "title": [
                    {"text": {"content": "API로 만든 할 일 2"}}
                ]
            },
            "상태": {
                "select": {"name": "Doing"}
            },
            "마감일": {
                "date": {"start": "2026-12-05"}
            },
            "태그": {
                "multi_select": [
                    {"name": "개발"}
                ]
            },
            "우선순위": {
                "number": 2
            },
        },

        {
            "이름": {
                "title": [
                    {"text": {"content": "API로 만든 할 일 3"}}
                ]
            },
            "상태": {
                "select": {"name": "Done"}
            },
            "마감일": {
                "date": {"start": "2026-12-10"}
            },
            "태그": {
                "multi_select": [
                    {"name": "리뷰"}
                ]
            },
            "우선순위": {
                "number": 3
            },
        },
    ]

    # 3개의 레코드를 차례대로 추가
    for record in records:

        new_page = notion.pages.create(
            parent={
                "data_source_id": data_source_id
            },
            properties=record
        )

        print("새 Row 추가:", new_page["id"])


def get_sample_todo(data_source_id: str):

    response = notion.data_sources.query(
        data_source_id=data_source_id
    )

    print("\n===== ToDo 데이터 =====")

    for page in response["results"]:

        properties = page["properties"]

        # 이름
        name = properties["이름"]["title"][0]["plain_text"]

        # 상태
        status = properties["상태"]["select"]["name"]

        # 마감일
        due_date = properties["마감일"]["date"]["start"]

        # 태그
        tags = [
            tag["name"]
            for tag in properties["태그"]["multi_select"]
        ]

        # 우선순위
        priority = properties["우선순위"]["number"]

        print(f"이름      : {name}")
        print(f"상태      : {status}")
        print(f"마감일    : {due_date}")
        print(f"태그      : {tags}")
        print(f"우선순위  : {priority}")
        print("-" * 30)

if __name__ == "__main__":

    # data_source_id = os.getenv("DATA_SOURCE_ID_AUTO")
    # if data_source_id is None:
    #     data_source_id = create_todo_database()
    #     set_key(DOTENV_PATH,"DATA_SOURCE_ID_AUTO",data_source_id,quote_mode="never")

    #     os.environ["DATA_SOURCE_ID_AUTO"] = data_source_id

    DATA_SOURCE_ID_AUTO = os.getenv("DATA_SOURCE_ID_AUTO")
    if DATA_SOURCE_ID_AUTO is None:
        raise RuntimeError("DATA_SOURCE_ID_AUTO 키값이 .env에 없습니다.")

    #add_sample_todo(DATA_SOURCE_ID_AUTO)
    #get_sample_todo(DATA_SOURCE_ID_AUTO)

    # ======================================================================
    # 메뉴 선택
    # ======================================================================
    while True:
        print("\n===== Todo 메뉴 =====")
        print("1. 할 일 추가")
        print("2. 할 일 조회")
        print("9. 프로그램 종료")

        choice = input("\n메뉴 번호를 입력하세요: ")

        # 1번: 할 일 추가
        if choice == "1":
            add_sample_todo(DATA_SOURCE_ID_AUTO)

        # 2번: 할 일 조회
        elif choice == "2":
            get_sample_todo(DATA_SOURCE_ID_AUTO)

        # 9번: 프로그램 종료
        elif choice == "9":
            print("\n프로그램을 종료합니다.")
            break

        # 잘못된 입력
        else:
            print("\n⚠️ 1, 2, 9 중에서 선택하세요.")