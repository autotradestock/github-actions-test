from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

def make_report():
    now = datetime.now(KST)

    print("=" * 40)
    print("  자동 실행 리포트")
    print("=" * 40)
    print(f"실행 시각 (KST): {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"요일: {['월','화','수','목','금','토','일'][now.weekday()]}요일")
    print()

    # 간단한 계산 예시 (나중에 실제 전략 로직으로 교체)
    prices = [100, 102, 101, 105, 108, 107, 110]
    ma5 = sum(prices[-5:]) / 5
    latest = prices[-1]

    print(f"최근 가격: {latest}")
    print(f"5일 이동평균: {ma5:.1f}")
    print(f"신호: {'매수 👍' if latest > ma5 else '관망 ✋'}")
    print("=" * 40)

if __name__ == "__main__":
    make_report()
