import os
import re
from dotenv import load_dotenv, set_key, find_dotenv
from notion_client import Client
from notion_client.errors import APIResponseError, RequestTimeoutError
import httpx

load_dotenv()

#노션 토큰/ 부모페이지 ID 확인
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_PARENT_PAGE_ID = os.getenv("NOTION_PARENT_PAGE_ID")

if not NOTION_TOKEN or not NOTION_PARENT_PAGE_ID:
    raise RuntimeError(
        "NOTION_TOKEN 또는 NOTION_PARENT_PAGE_ID가 설정되어 있지 않습니다."
    )

#.env파일 존재 확인
DOTENV_PATH = find_dotenv()
if not DOTENV_PATH:
    raise RuntimeError(".env 파일을 찾을 수 없습니다.")

notion = Client(auth=NOTION_TOKEN)

def create_database():
    '''
    노션 DB에 첫 데이터베이스 생성
    처음에만 실행
    '''
    database = notion.databases.create(
        parent={
            "type": "page_id",
            "page_id": NOTION_PARENT_PAGE_ID
        },
        title=[
            {
                "type": "text",
                "text": {
                    "content": "서버 자산 대장"
                }
            }
        ],
        initial_data_source={
            "properties": {
                "호스트명": {
                    "title": {}
                },
                "IP주소": {
                    "rich_text": {}
                },
                "포트": {
                    "number": {}
                },
                "상태":{
                    "select":{
                        "options":[
                            {"name":"Active"},
                            {"name":"Maintenance"},
                            {"name":"Decommissioned"}
                        ]
                    }
                },
                "태그":{
                    "multi_select":{
                        "options":[
                            {"name":"Web", "color":"red"},
                            {"name":"DB", "color":"yellow"},
                            {"name":"WAS", "color":"green"},
                            {"name":"Cache", "color":"purple"}
                        ]        
                    }
                }
            }
        }
    )

    database_id = database["id"]
    database_info = notion.databases.retrieve(database_id)
    data_source_id = database_info["data_sources"][0]["id"]
    print("🟢첫 데이터베이스 생성완료")
    return data_source_id
    
def get_server_list(data_source_id: str):
    '''
    노션DB에서 전체 서버 목록 조회
    
    Args : data_source_id(str)
    return : page_id_list
    '''
    try :
        servers = []
        cursor = None

        #DB에 존재하는 전체 서버 목록을 가져옴
        while True:
            query_args = {"data_source_id": data_source_id}

            if cursor:
                query_args["start_cursor"] = cursor

            response = notion.data_sources.query(**query_args)
            servers.extend(response["results"])

            if not response.get("has_more"):
                break

            cursor = response["next_cursor"]

        #등록된 서버가 없으면 빈 list 리턴
        if not servers:
            print("등록된 서버가 없습니다.")
            return []

        print("\n ===== 전체 서버 목록 =====")

        #서버 목록에서 원하는 값만 추출및 출력
        page_id_list=[]
        for num,server in enumerate(servers, start=1):
            properties = server["properties"]

            host = properties["호스트명"]["title"][0]["plain_text"]
            ip = properties["IP주소"]["rich_text"][0]['text']['content']
            port = properties["포트"]["number"]
            status = properties["상태"]["select"]["name"]
            tags =[tag["name"] for tag in properties["태그"]["multi_select"]]

            print(f"{num}. 호스트명 : {host} | ip : {ip} | 포트 : {port} | 상태 : {status} | 태그 : {tags}")
            
            page_id_list.append(server["id"])

        return page_id_list
    except APIResponseError as e:
        print(f"🚨 서버 조회 API 오류{e}")
    except (RequestTimeoutError, httpx.RequestError):
        print(f"🚨 통신 오류 입니다.")
    finally:
        print("-"*40)

def add_new_server(data_source_id: str,host,ip,port,tags):
    '''
    신규 서버를 노션DB에 등록
    
    Args : data_source_id(str)
            host(호스트명)
            ip(ip)
            port(포트번호)
            tags(태그 list)
    '''
    try:
        notion.pages.create(
            parent={
                "type" : "data_source_id",
                "data_source_id":data_source_id
            },
            properties={
                "호스트명":{
                    "title":[
                        {
                            "text":{
                                "content":host
                            }
                        }
                    ]
                },
                "IP주소":{
                    "rich_text":[
                        {"text":{"content":ip}}
                        ]
                },
                "포트":{
                    "number": int(port)
                },
                "상태":{
                    "select":{
                        "name": 'Active'
                    }
                },
                "태그":{
                    "multi_select":[{"name":tag}for tag in tags]
                }
            }
        )
    except APIResponseError as e:
        print(f"🚨 서버 등록 API 오류{e}")
    except (RequestTimeoutError, httpx.RequestError):
            print(f"🚨 통신 오류 입니다.")
    else:
        print("🟢서버 등록 성공!")
    finally:
        print("-"*40)

def update_sever(page_id, status):
    '''
    서버의 status 변경 함수

    Args: page_id(선택한 서버)
          status(상태)
    '''
    try:
        notion.pages.update(
            page_id = page_id,
            properties={
                "상태":{
                    "select":{
                        "name":status
                    }
                }
            }
        )
    except APIResponseError as e:
        print(f"🚨 상태 변경 API 오류: {e}")
    except (RequestTimeoutError, httpx.RequestError):
        print(f"🚨 통신 오류 입니다.")
    else:
        print("🟢서버 상태 변경 성공!")
    finally:
        print("-"*40)

def delete_server(page_id):
    '''
    서버 폐기(휴지통으로 이동)

    Args: page_id(선택한 서버)
    '''
    try:
        notion.pages.update(
            page_id= page_id,
            archived = True
        )
    except APIResponseError as e:
        print(f"🚨 서버삭제 API 오류: {e}")
    except (RequestTimeoutError, httpx.RequestError):
        print(f"🚨 통신 오류 입니다.")
    else:
        print('🟢서버 삭제 성공!')
    finally:
        print("-"*40)

HOSTNAME_PATTERN = re.compile(r"^srv-(web|db|was|cache)-\d{2}$")
IP_PATTERN = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
PORT_PATTERN = re.compile(r"^\d{1,5}$")


def validate_hostname(value: str) -> bool:
    '''
    호스트명 패턴 검사
    "^srv-(web|db|was|cache)-\d{2}$"
    '''
    return bool(HOSTNAME_PATTERN.match(value))


def validate_ip(value: str) -> bool:
    '''
    ip 패턴검사 
    "^\d{1,3}(\.\d{1,3}){3}$"
    '''
    if not IP_PATTERN.match(value):
        return False
    return all(0 <= int(octet) <= 255 for octet in value.split("."))


def validate_port(value: str) -> bool:
    '''
    port 패턴 검사
    "^\d{1,5}$"
    '''
    if not PORT_PATTERN.match(value):
        return False
    return 1 <= int(value) <= 65535


if __name__=="__main__":
    try:
        data_source_id = os.getenv("DATA_SOURCE_ID_AUTO")

        #data_source_id가 생성되어있으면 새로운 데이터베이스를 만들지 않음
        #없으면 새로운 데이터베이스를 생성하고, data_source_id 저장
        if data_source_id is None:
            data_source_id = create_database()
            set_key(DOTENV_PATH,"DATA_SOURCE_ID_AUTO",data_source_id,quote_mode="never")
            
            os.environ["DATA_SOURCE_ID_AUTO"] = data_source_id

    except APIResponseError as e:
        print(f"🚨초기화 API 오류: {e}")
        raise SystemExit(1)
    except (RequestTimeoutError, httpx.RequestError):
        print("🚨초기화 통신 오류입니다. 재실행 전 DB 생성 여부를 확인하세요.")
        raise SystemExit(1)
    except OSError as e:
        print(f"🚨환경파일 저장 오류: {e}")
        raise SystemExit(1)

    #주요 기능 시작 
    while(True):
        # 메뉴 선택
        print("-"*40)
        print("1. 전체 서버 목록 조회")
        print("2. 신규 서버 등록")
        print("3. 서버 상태 변경 (Active / MainTenance / Decommissioned)")
        print("4. 서버 폐기")
        print("0. 프로그램 종료")
        print("-"*40)
        menu = input("원하는 숫자를 입력해주세요 : ")

        match menu:
            case '1':
                print("[목록 조회] 전체 서버 목록을 조회합니다.")
                server_list = get_server_list(data_source_id)

                if not server_list:
                    continue

            case '2':
                print("[서버 등록]")

               
                print("-"*40)
                print("[호스트명 형식]")
                print("\"srv-(web,db,was,cache)-숫자 2개\"")
                host=input("호스트명을 입력해주세요 :")
                vali_host = validate_hostname(host)
                if not vali_host :
                    print("잘못된 호스트명을 입력했습니다. 선택화면으로 돌아갑니다.")
                    continue
                    

                
                print("-"*40)
                ip = input("ip 주소를 입력해주세요 :")
                vali_ip = validate_ip(ip)
                if not vali_ip :
                    print("잘못된 ip 입니다. 선택화면으로 돌아갑니다.")
                    continue
                
                print("-"*40)
                port = input("포트번호를 입력해주세요 :")
                vali_port = validate_port(port)           
                if not vali_port:
                    print("잘못된 port 입니다. 선택화면으로 돌아갑니다.")
                    continue

                #태그 중복선택을 위해 값을 입력받고 태그 list를 만드는부분
                tag_map ={
                    "1":"Web",
                    "2":"DB",
                    "3":"WAS",
                    "4":"Cache"}
                print("-"*40)
                print("원하는 태그를 선택해주세요")
                print(" [ 1.Web , 2.DB , 3.WAS , 4.Cache ]")
                tag_input = input("원하는 태그의 숫자를 입력해주세요(중복가능 , 로 구별해 입력)")
                tag_numbers = [value.strip() for value in tag_input.split(",")]
                if any(number not in tag_map for number in tag_numbers):
                    print("잘못된 태그 입니다. 선택화면으로 돌아갑니다.")
                    continue
                else:
                    tags = list(dict.fromkeys(tag_map[number] for number in tag_numbers))

                #DB등록 함수 호출
                add_new_server(data_source_id, host,ip,port,tags)

            case '3':
                print("[서버 상태 변경]")
                page_id_list= get_server_list(data_source_id)

                #등록된 서버가 없으면 메뉴로 넘어감
                if not page_id_list:
                    continue

                
                try:
                    input_update_server = int(input("변경할 서버의 번호를 입력해주세요: "))
                except ValueError:
                    print("서버 번호는 정수로 입력해주세요")
                    continue

                if not 1 <= input_update_server <= len(page_id_list):
                    print("목록에 있는 번호를 입력해주세요")
                    continue

                page_id = page_id_list[input_update_server-1]

                #서버 상태를 입력받음
                status_map ={
                    "1":"Active",
                    "2":"Maintenance",
                    "3":"Decommissioned"
                }
                status =""
                while not status:
                    print("-"*40)
                    print("원하는 상태를 입력해주세요")
                    print("1. Active, 2. Maintenance, 3. Decommissioned")
                    status_input = input("원하는 상태의 숫자를 입력해주세요 :")
                    status = status_map.get(status_input,None)
                    if not status :
                        print('올바른 상태를 골라주세요')

                update_sever(page_id , status)
            case '4':
                print("[서버 삭제]")
                page_id_list= get_server_list(data_source_id)

                #조회된 서버가 없으면 메뉴로 돌아감
                if not page_id_list:
                    continue
                
                try:
                    input_delete_server = int(input("삭제할 서버의 번호를 입력해주세요: "))
                except ValueError:
                    print("서버 번호는 정수로 입력해주세요")
                    continue
                
                if not 1 <= input_delete_server <= len(page_id_list):
                    print("목록에 있는 번호를 입력해주세요")
                    continue

                page_id = page_id_list[input_delete_server-1]
                delete_server(page_id)
            case '0':
                break
            case _:
                print("\n메뉴에 알맞는 숫자를 입력해주세요")