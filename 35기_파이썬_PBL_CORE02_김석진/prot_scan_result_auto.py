from pathlib import Path
import shutil
import csv
import json
import glob

# log_data = """Scan Time: 2026-09-07 02:00:11
# Target : 10.0.2.15
# Port: 21 STATUS: OPEN
# Port: 22 STATUS: OPEN
# Port: 443 STATUS: OPEN
# Port: 3389 STATUS: OPEN
# Port: 80 STATUS: OPEN
# Port: 8080 STATUS: OPEN"""

# Path("vuln_scan.log").write_text(log_data, encoding="utf-8")
# print("취약점 스캔 로그(vuln_scan.log) 생성 완료!")



def is_safe_port(port):
    ''' 안전한 포트 목록과 비교합니다.

    args : 
        port : 검사할 포트번호
    return :
        bool : 안전포트이면 True, 아니면 False
    '''
    safe_ports = (22,80,443)
    return port in safe_ports


archive_dir = Path("archive")   #로그 보관 폴더 경로
vuln_scan = Path("vuln_scan.log")   #원본 로그 파일 경로
port_list = []  #로그 검사 후 port를 담기위한 list




try:
    #vuln_scan파일 존재 유무확인 및 archive디렉토리 유무확인 후 vuln_scan파일을 archive폴더로 이동
    if vuln_scan.is_file():     
        if not archive_dir.exists():
            archive_dir.mkdir(exist_ok=True)
        shutil.move("vuln_scan.log",archive_dir)
    else : 
        raise Exception(f"🚨로그파일이 없어 종료합니다.")
    
    #정상이동 확인 위해 archive내 log파일출력
    archive_dir_files = glob.glob(str(archive_dir/"*.log"))
    print("[파일확인] archive내 log파일")
    for num,file in enumerate(archive_dir_files, start=1):
        print(f"{num}. {file}")
    print("--"*40)
    
    
    print("[로그 검사 시작]")
    print("--"*40)
    #vuln_scan파일에서 port번호만 port_list에 저장
    with open(archive_dir/vuln_scan, "r",encoding="utf-8") as f:
        for line in f :
            if line.startswith("Port: "):
                split_log = line.split()

                if len(split_log) < 2:  #인덱싱 오류검사
                    print(f"❌[로그검사] 형식에 맞지 않습니다.{line}")
                    continue
                try:        #정수 변환시도
                    port_list.append(int(split_log[1]))
                except ValueError:
                    print(f"❌[로그검사] 정수가 아닙니다.{line}")
                    continue

    #port_list중 안전한 포트 목록에 없는 포트 구별
    danger_port = list(filter(lambda port : not is_safe_port(port), port_list))


    
    print('[파일 생성 시작]')
    print("--"*40)

    #danger_port로 vulnerable_ports.csv파일 생성 [header : 'Detected_Port','Severity']
    with open("vulnerable_ports.csv", "w",newline="", encoding= "utf-8-sig") as f:
        header = ["Detected_Port","Severity"]
        writer = csv.DictWriter(f,header)
        writer.writeheader()
        for port in danger_port:
            writer.writerow({'Detected_Port':port,'Severity':'Critical'})

        print(f"🟢[CSV 파일 생성 성공]")
    print("--"*40)

    #json파일생성을 위해 딕셔너리 생성
    vulnerability_alert_json ={
        "Detected_Port" : danger_port,
        "Severity" : "Critical",
        "Assigned_Engineer" : None
    }

    #vulnerability_alert_json로 json 파일 생성
    with open("vulnerability_alert.json","w",encoding="utf-8") as f:
        json.dump(vulnerability_alert_json,f,indent=4)
        print(f"🟢[json 파일 생성 성공]")

except Exception as e:
    print(f"🚨오류가 발생했습니다.{e}")