import os
import requests
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

# GitHub Secrets에서 Slack Webhook URL 읽어오기
# 저장소 Settings > Secrets and variables > Actions 에서 등록
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")


def send_line_alert(msg: str):
    """line_alert.py의 SendMessage와 동일한 역할 (GitHub Actions용)"""
    if not SLACK_WEBHOOK_URL:
        raise ValueError("SLACK_WEBHOOK_URL 환경변수가 설정되지 않았습니다.")

    try:
        requests.post(
            SLACK_WEBHOOK_URL,
            headers={"content-type": "application/json"},
            json={
                "text": "myAutobot",
                "blocks": [
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": msg},
                    }
                ],
            },
            timeout=10,
        )
        print(f"[알림 전송 완료] {msg}")
    except Exception as ex:
        print(f"[알림 전송 실패] {ex}")


def main():
    now = datetime.now(KST)
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")

    msg = f"*GitHub Actions 알림 테스트*\n실행 시각 (KST): {time_str}"
    send_line_alert(msg)


if __name__ == "__main__":
    main()
