# GitHub Actions 입문 가이드

> 이 폴더는 GitHub Actions를 처음 배우기 위해 만든 샘플입니다.  
> 이 문서를 보면서 전체 흐름을 복기할 수 있습니다.

---

## 1. GitHub Actions가 뭔가?

**한 줄 요약**: 내 컴퓨터가 꺼져 있어도 GitHub 서버가 내 파이썬 코드를 대신 실행해준다.

### 비유

카페 알바생(GitHub 서버)을 고용한 것과 같다.

- **내가 한 일**: 알바생에게 지시서(`.yml` 파일)를 줬다
- **지시서 내용**: "5분마다 `auto_report.py` 실행해줘"
- **결과**: 내 컴퓨터가 꺼져 있어도 알바생이 알아서 실행

### 퀀트에 적용하면

```
매일 오전 9시 → GitHub 서버가 자동으로
  → 주식 데이터 받아오기
  → 전략 계산
  → 결과를 텔레그램으로 알림 발송
```

### 무료 한도

| 저장소 종류 | 한도 |
|------------|------|
| Public(공개) | 무제한 무료 |
| Private(비공개) | 월 2,000분 무료 |

---

## 2. 핵심 개념

### Git vs GitHub vs GitHub Actions

| 용어 | 설명 |
|------|------|
| **Git** | 내 컴퓨터에서 코드 버전을 관리하는 도구 |
| **GitHub** | Git 저장소를 인터넷에 올려두는 서비스 |
| **GitHub Actions** | GitHub에 올린 코드를 자동으로 실행해주는 서비스 |

### Git 3단계 흐름

```
1. 작업 폴더     →    2. 스테이징 영역    →    3. 저장소
  (파일 수정)         (git add로 선택)          (git commit으로 확정)
                                                      ↓
                                               4. GitHub 업로드
                                                (git push)
```

```powershell
git add .                    # 변경된 파일 전부 선택 (. = 현재 폴더 전체)
git commit -m "커밋 메시지"   # 선택한 것을 로컬에 확정
git push                     # GitHub에 업로드
```

---

## 3. 폴더 구조

```
깃허브액션샘플/
├── .github/
│   └── workflows/               ← 이 폴더 안에 .yml 파일을 넣으면 GitHub가 자동 인식
│       ├── hello.yml            ← push할 때 자동 실행 + 테스트
│       ├── auto-run.yml         ← 5분마다 자동 실행
│       ├── use-secrets.yml      ← Secret(API 키) 사용 예제
│       ├── schedule.yml         ← 매일 오전 9시 실행 예제
│       └── quant-daily.yml      ← 퀀트 전략 실전 활용 예시
├── main.py                      ← 기본 파이썬 예제
├── test_main.py                 ← pytest 테스트 예제
├── auto_report.py               ← 자동 실행용 리포트 스크립트
├── secret_example.py            ← Secret을 환경변수로 읽는 예제
├── requirements.txt             ← 필요한 패키지 목록
└── README.md                    ← 이 파일
```

---

## 4. 워크플로우 파일(.yml) 구조 이해

### 기본 구조

```yaml
name: 워크플로우 이름          # GitHub Actions 탭에서 보이는 이름

on:                           # 언제 실행할지
  push:
    branches: [ main ]        # main 브랜치에 push할 때
  schedule:
    - cron: '*/5 * * * *'    # 5분마다
  workflow_dispatch:          # GitHub 웹에서 수동 실행 가능

jobs:
  작업이름:
    runs-on: ubuntu-latest    # GitHub 서버 OS (리눅스)
    env:
      FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true  # Node.js 24 사용 (경고 방지)

    steps:
      - name: 코드 체크아웃
        uses: actions/checkout@v4          # 남이 만든 액션 사용

      - name: Python 설치
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: 스크립트 실행
        run: python auto_report.py         # 직접 명령어 실행
```

### cron 시간 설정 (UTC 기준, 한국은 UTC+9)

```
분  시  일  월  요일
*   *   *   *   *

*/5 * * * *      → 5분마다
0 * * * *        → 매 시간 정각
30 0 * * 1-5     → 평일 매일 09:30 KST (= UTC 00:30)
0 1 * * 1        → 매주 월요일 10:00 KST (= UTC 01:00)
0 0 * * *        → 매일 09:00 KST (= UTC 00:00)
```

> **주의**: GitHub 스케줄 실행은 서버 상황에 따라 최대 수십 분 지연될 수 있다.

---

## 5. GitHub Secrets (API 키 안전하게 보관)

### 왜 필요한가?

```python
# 절대 금지! 코드를 공개하면 API 키가 노출됨
app_key = "실제API키값"
```

코드는 GitHub에 공개되어 있어도, **API 키는 GitHub Secrets에 암호화해서 저장**하면 안전하다.

### 작동 원리

```
내 코드 (공개)              GitHub Secrets (암호화, 비공개)
     ↓                               ↓
  yml 파일     ←←← 실행 시 주입 ←←←   MY_API_KEY = "실제키값"
${{ secrets.MY_API_KEY }}
```

### Secret 등록 방법 (GitHub 웹사이트)

1. 저장소 → 상단 **Settings** 탭
2. 왼쪽 메뉴 **Secrets and variables** → **Actions**
3. **New repository secret** 클릭
4. **Name**: `MY_API_KEY` (yml 파일에서 쓸 이름)
5. **Secret**: 실제 키 값 입력
6. **Add secret** 클릭

> 등록 후 값을 다시 볼 수 없다. 수정/삭제만 가능.

### yml에서 사용하는 방법

```yaml
- name: 스크립트 실행
  env:
    MY_API_KEY: ${{ secrets.MY_API_KEY }}   # Secrets에서 읽어서 환경변수로 전달
  run: python secret_example.py
```

### 파이썬에서 읽는 방법

```python
import os
api_key = os.environ.get("MY_API_KEY")   # 환경변수로 읽기
print(f"키 로드 성공 (길이: {len(api_key)}자)")  # 값 자체는 절대 출력 금지
```

### 절대 하면 안 되는 것

```python
print(f"키: {api_key}")        # 로그에 키 값 노출됨
api_key = "ghp_abc123..."     # 코드에 직접 값 입력
```

---

## 6. GitHub Personal Access Token (PAT)

GitHub는 2021년부터 비밀번호로 push 불가. PAT를 써야 한다.

### 토큰 발급 방법

1. GitHub → 프로필 사진 → **Settings**
2. 왼쪽 맨 아래 **Developer settings**
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token (classic)**
5. **Note**: 이름 입력, **Expiration**: 기간 설정, **Scopes**: `repo` 체크
6. **Generate token** → 생성된 토큰 복사 (이 화면 벗어나면 다시 못 봄!)

### push할 때 토큰 사용

```powershell
# 방법 1: URL에 토큰 포함
git remote set-url origin https://토큰값@github.com/아이디/저장소명.git

# 방법 2: Windows 자격증명 저장 (한 번만 설정, 이후 자동)
git config --global credential.helper manager
git push   # 팝업에서 Username=깃허브아이디, Password=토큰 입력
```

---

## 7. 실행 결과 확인 방법

1. GitHub 저장소 → 상단 **Actions 탭**
2. 왼쪽에서 워크플로우 이름 클릭
3. 실행 목록에서 항목 클릭 → 상세 로그 확인

### 실행 상태 아이콘

| 아이콘 | 의미 |
|--------|------|
| 🟡 노란 원 | 실행 중 |
| ✅ 초록 체크 | 성공 |
| ❌ 빨간 X | 실패 |

### 수동 실행 방법

Actions 탭 → 워크플로우 선택 → 오른쪽 **"Run workflow"** 버튼 → **"Run workflow"** 클릭

---

## 8. 자주 보는 경고/에러

### LF will be replaced by CRLF

```
warning: in the working copy of 'auto_report.py', LF will be replaced by CRLF
```

**원인**: Windows(CRLF)와 Linux/Mac(LF)의 줄바꿈 방식 차이  
**해결**: 무시해도 됨. 없애려면:
```powershell
git config --global core.autocrlf true
```

### Node.js 20 deprecated 경고

```
Node.js 20 actions are deprecated...
```

**원인**: GitHub Actions 내부가 Node.js 20 → 24로 업그레이드 중  
**해결**: yml 파일의 job에 아래 추가 (이미 적용됨):
```yaml
env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true
```

---

## 9. 퀀트 전략 자동화 적용 예시

`auto_report.py`의 가짜 데이터 부분을 실제 API로 교체하면 된다.

```python
# 현재 (가짜 데이터)
prices = [100, 102, 101, 105, 108, 107, 110]

# 나중에 (실제 API)
import requests
prices = get_real_prices("005930")  # 삼성전자 실제 데이터
```

`quant-daily.yml` 참고:

```yaml
- name: 전략 실행
  env:
    KIS_APP_KEY: ${{ secrets.KIS_APP_KEY }}        # 한국투자증권 앱키
    KIS_APP_SECRET: ${{ secrets.KIS_APP_SECRET }}  # 한국투자증권 시크릿
    TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}  # 텔레그램 알림
  run: python main.py
```
