# network = {
#     "router": {
#         "ip": "192.168.1.1",
#         "vendor": "Cisco",
#         "status": "UP"
#     },
#     "firewall": {
#         "ip": "192.168.1.254",
#         "vendor": "Fortinet",
#         "status": "UP"
#     }
# }

# print(network["firewall"].get("ip"))

# alerts = {
#     "10.10.10.15": {
#         "attack": "Port Scan",
#         "severity": "High"
#     },
#     "10.10.10.20": {
#         "attack": "Brute Force",
#         "severity": "Critical"
#     },
#     "10.10.10.30": {
#         "attack": "SQL Injection",
#         "severity": "High"
#     }
# }

# print(alerts['10.10.10.20'].get('attack'))
# print(alerts['10.10.10.20'].get('severity'))


# security_logs = {
#     "admin": "192.168.1.10",
#     "manager": "192.168.1.20",
#     "user01": "192.168.1.30"
# }

# username = "hacker"

# print(security_logs.get(username, "사용자 정보 없음"))

# servers = {
#     "web01": "192.168.10.10",
#     "web02": "192.168.10.20",
#     "db01": "192.168.10.30"
# }

# server_name = "web03"

# print(servers.get(server_name,"등록되지 않은 서버"))


# alerts = ['로그인 실패', '포트 스캔 탐지', '악성 파일 탐지', '비정상 접속', 'DDoS 공격 탐지'] 

# print(alerts)

# alerts.extend(['SQL Injection 탐지', 'Brute Force 공격 탐지'])
# alerts.pop()
# alerts.extend(['SQL Injection 탐지', 'Brute Force 공격 탐지'])
# alerts.remove('SQL Injection 탐지')
# alerts.insert(3, '랜섬웨어 탐지')
# print(alerts[3:6])
# print(alerts)
import random

name = input('분석가 이름을 입력하세요: ')
start_ip = '10.10.10.2'
fail = random.randint(5,51)

risk_score = random.uniform(1,101)
print(f'[브루트포스 탐지] 분석가: {name} / {start_ip} 실패 {fail}회 / 위험도 {risk_score:.1f}')