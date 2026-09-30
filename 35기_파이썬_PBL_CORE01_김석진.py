import random

#기초 데이터 준비
line_names = [f"LINE-{i:02d}" for i in range(1,13)]
raw_logs = [random.randint(1,100) for _ in range(10)] + [0, "Timeout", None, 99, "Error"]

#정상 log를 저장할 list
normal_logs = []

#raw_logs 섞음
random.shuffle(raw_logs)

#트래픽 점검 시작
print("--- 실시간 네트워크 트래픽 점검 시작 ---")
for log in raw_logs:        
    try:
        normal_log = float(log)  #flaot로 변환할 수 없는 비정상로그는 예외 처리로 넘김
    except (ValueError,TypeError):     #변환 실패 시 비정상로그를 출력하고 다음로그로 넘어감
        print(f"❌ [DATA ERROR] 읽을 수 없는 로그 형식입니다. (입력값 : {log})")
        continue
    else:
        normal_logs.append(normal_log)    #형변환에 성공한 정상로그 저장

        if normal_log >= 99:   #로그가 99% 이상일 경우 DDos 공격 의심으로 반복문 탈출
            print(f"🚨 [EMERGENCY] {normal_log:.1f}% 감지! 대규모 DDos 공격 의심으로 전체 점검 중단!")
            break
        elif normal_log >= 95: #로그가 95% 이상일 경우 회선 차단 및 우회 경로전환 메시지 출력
            print(f"🔴 [CRITICAL] 패킷 손실률 {normal_log:.1f}% 즉시 회선 차단 및 우회 경로 전환")
        elif normal_log >= 70: #로그가 70% 이상일 경우 네트워크 관리자 호출 및 회선 점검 메시지 출력
            print(f"🟡 [WARNING] 패킷 손실률 {normal_log:.1f}% 관리자 호출 및 회선 점검 필요")
        elif normal_log == 0 : #로그가 0% 일 경우 회선 다운 의심 메시지 출력
            print(f"🟣 [CHECK] 패킷 손실률 {normal_log:.1f}% 트래픽 없음 (회선 다운 의심)")
        else :  #위 외의 값일 경우 회선 정상 메시지 출력
            print(f"🟢 [NORMAL] 패킷 손실률 {normal_log:.1f}% 회선 정상")
    finally:    # 정상/예외 여부와 상관없이 구분선 출력
        print("-------------------- 점검 완료 --------------------")

print()
#정상 처리된 값들중 70%이상만 추출해 저장 및 출력
danger_log = [packet_loss_rate for packet_loss_rate in normal_logs if packet_loss_rate >= 70]
print(f"[요약] 위험(WARNING 이상) 손실률 목록: {danger_log}")