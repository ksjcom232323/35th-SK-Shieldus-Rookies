from pathlib import Path
import shutil
import csv
import json
# log_data = """Scan Time: 2026-09-07 02:00:11
# Target : 10.0.2.15
# port : 21 STATUS: OPEN
# port : 22 STATUS: OPEN
# port : 443 STATUS: OPEN
# port : 3389 STATUS: OPEN
# port : 80 STATUS: OPEN
# port : 8080 STATUS: OPEN"""

# Path("vuln_scan.log").write_text(log_data, encoding="utf-8")
# print("취약점 스캔 로그(vuln_scan.log) 생성 완료!")

port_list = []

def is_safe_port(port):
    ''' 안전한 포트 스캔'''
    safe_ports = (22,80,443)

    if port in safe_ports:
        return True
    else:
        return False

archive_dir = Path("archive_dir")

if Path("vuln_scan.log").exists():
    if not archive_dir.exists():
        archive_dir.mkdir(exist_ok=True)
    shutil.move("vuln_scan.log",archive_dir)


with open(f"{archive_dir}/vuln_scan.log", "r",encoding="utf-8") as f:
    for log in f:
        if "port : " in log:
            split_log = log.split()

            if len(split_log) < 2:
                print("포트번호가 누락되었습니다.")
                continue

            port_list.append(int(split_log[2]))


danger_port = list(filter(lambda port : not is_safe_port(port), port_list))

print(danger_port)




with open(f"{archive_dir}/vulnerable_ports.csv", "w",newline="", encoding= "utf-8-sig") as f:
    header = ["Detected_Port","Severity"]
    writer = csv.DictWriter(f,header)
    writer.writeheader()
    for port in danger_port:
        writer.writerow({'Detected_Port':port,'Severity':'Critical'})

with open(f"{archive_dir}/vulnerability_alert.json","w",encoding="utf-8") as f:
    json.dump()