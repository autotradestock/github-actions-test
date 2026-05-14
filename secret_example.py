import os

def get_api_key():
    # 환경변수에서 토큰을 읽어옴 (GitHub Actions가 Secrets를 환경변수로 주입)
    api_key = os.environ.get("MY_API_KEY")

    if not api_key:
        raise ValueError("MY_API_KEY 환경변수가 설정되지 않았습니다.")

    return api_key

def main():
    api_key = get_api_key()
    # 실제로는 이 key로 API 호출 등을 함
    # 로그에 절대 출력하면 안 됨 - 아래처럼 길이만 확인
    print(f"API 키 로드 성공 (길이: {len(api_key)}자)")
    print("작업을 수행합니다...")

if __name__ == "__main__":
    main()
