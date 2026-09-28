import random

line_names = [f"LINE-{i:02d}" for i in range(1,13)]
raw_logs = [random.randint(1,100) for _ in range(10)] + [0, "Timeout", None, 99, "Error"]
normal_log = []
print(line_names)

random.shuffle(raw_logs)
print(raw_logs)

print("--- 실시간 네트워크 트래픽 점검 시작 ---")
for log in raw_logs:
    try:
        normal_log.append(float(log))
        print(normal_log)
        if log >= 99:
            print(f"🚨 [EMERGENCY] {float(log):.1f}% 감지! 대규모 DDos 공격 의심으로 전체 점검 중단!")
            break
        elif log >= 95:
            print(f"🔴 [CRITICAL] 패킷 손실률 {float(log):.1f}% 즉시 회선 차단 및 우회 경로 전환")
        elif log >= 70:
            print(f"🟡 [WARNING] 패킷 손실률 {float(log):.1f}% 관리자 호출 및 회선 점검 필요")
        elif log == 0 :
            print(f"🟣 [CHECK] 패킷 손실률 {float(log):.1f}% 트래픽 없음 (회선 다운 의심)")
        else :
            print(f"🟢 [NORMAL] 패킷 손실률 {float(log):.1f}% 회선 정상")

    except:
        print(f"❌ [DATA ERROR] 읽을 수 없는 로그 형식입니다. (입력값 : {log})")
        continue
    finally:
        print("-------------------- 점검 완료 --------------------")

print()
danger_log = [packet_loss_rate for packet_loss_rate in normal_log if packet_loss_rate >= 70]
print(f"[요약] 위험(WARNING 이상) 손실률 목록: {danger_log}")