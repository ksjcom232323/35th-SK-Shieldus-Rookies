import random

line_names = [f"LINE-{i:02d}" for i in range(1,13)]
raw_logs = [random.randint(1,100) for _ in range(10)] + [0, "Timeout", None, 99, "Error"]
print(line_names)
print(raw_logs)
random.shuffle(raw_logs)

for log in raw_logs:
    try:
        if log >= 99:
            print(f"🚨 [EMERGENCY] {float(log):.1f}% 감지! 대규모 DDos 공격 의심으로 전체 점검 중단!")
            break
        elif log >= 95:
            print(f"🔴 [CRITICAL] 즉시 회선 차단 및 우회 경로 전환")
        elif log >= 70:
            print()
        elif log == 0 :
            print()
        else :
            print()
    except:
        print()
    finally:
        print("-------------------- 점검 완료 --------------------")
