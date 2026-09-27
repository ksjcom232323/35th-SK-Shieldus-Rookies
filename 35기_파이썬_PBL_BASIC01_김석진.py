import os 
import random

from dotenv import load_dotenv

# Scanner 설정
load_dotenv()
scanner = os.getenv("SCANNER_NAME", "LOCAL-Scanner")

# critical_hosts,vuln_assets 선언
critical_hosts = ("WEB-01", "DB-01")
vuln_assets = [
        {"cve": "CVE-2024-1001", "host":"WEB-01", "patched":False},
        {"cve": "CVE-2024-1002", "host":"DB-01", "patched":True}
]

# CVE_ID,호스트 사용자 입력
new_cve = input('추가할 CVE ID: ')
new_host = input('추가할 대상 호스트: ')
vuln_assets.append({"cve": new_cve, "host":new_host, "patched":False})

#첫번쨰 취약점 'patched'값 변경
vuln_assets[0].update({'patched': True})

#입력받은 cve,호스트에 위험도(cve_score) 추가
cve_score = random.uniform(0,10)
vuln_assets[2].update({"cve_score":cve_score})


#포멧팅 출력 시작
print(f'총 {len(vuln_assets)}건의 취약점에 대한 패치 점검을 수행합니다.')
print('--'*30)

#첫번째 취약점 출력
print(f"[스캐너: {scanner}] {vuln_assets[0].get('cve')} ({vuln_assets[0].get('host')}) 패치 상태: {vuln_assets[0].get('patched')}")
if vuln_assets[0].get("host") in critical_hosts:         #핵심 자산 포함여부 검사
    print('핵심 자산 여부: True')
else : 
    print('핵심 자산 여부: False')
print('--'*30)

#두번째 취약점 출력
print(f"[스캐너: {scanner}] {vuln_assets[1].get('cve')} ({vuln_assets[1].get('host')}) 패치 상태: {vuln_assets[1].get('patched')}")
if vuln_assets[1].get("host") in critical_hosts:         #핵심 자산 포함여부 검사
    print('핵심 자산 여부: True')
else : 
    print('핵심 자산 여부: False')
print('--'*30)

#세번째 취약점 출력
print(f"[스캐너: {scanner}] {vuln_assets[2].get('cve')} ({vuln_assets[2].get('host')}) 패치 상태: {vuln_assets[2].get('patched')}")
if vuln_assets[2].get("host") in critical_hosts:         #핵심 자산 포함여부 검사
    print(f"핵심 자산 여부: True / 현재 위험도 : {vuln_assets[2].get('cve_score'):.1f}")        #위험도(cve_score) 추가해서 출력
else : 
    print(f"핵심 자산 여부: False / 현재 위험도 : {vuln_assets[2].get('cve_score'):.1f}")       #위험도(cve_score) 추가해서 출력
print('--'*30)
