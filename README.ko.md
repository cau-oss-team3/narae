# 나래

Languages: \[한국어\] | [\[English\]](README.md)

## 기능

*Narae*는 백엔드 및 프론트엔드 개발과 같은 소프트웨어 개발 분야에서 사용자의 학습을 향상시키기 위해 LLM(대규모 언어 모델) 기반 멘토링 서비스를 제공합니다.  

주요 기능은 다음과 같습니다:  

- **개인 맞춤형 학습 정보 설정:** 사용자가 자신의 개발 목표를 설정하고, 개인의 필요, 목표 및 상황에 맞춘 학습 계획을 받습니다.
- **AI 기반 학습 가이드:** AI가 행동을 제안하고 어려운 주제에 대한 심층적인 설명과 연습 문제를 제공합니다.
- **진행 추적 및 평가:** AI가 상호작용을 요약하여 진행 상황을 추적하고, 학습 강화를 위한 일일 퀴즈를 생성합니다.
- **고급 지식 멘토링:** OpenAI의 임베딩 기술을 활용하여 깊고 전문화된 지식을 제공합니다.
- **피드백 기반 개선:** 사용자 피드백을 지속적으로 수집하여 서비스를 개선하고 강화합니다.
- **인터랙티브 학습:** 음성 상호작용 기능이 향후 추가될 가능성이 있으며, 이를 통해 사용자는 언제 어디서나 AI 멘토와 음성과 텍스트로 상호작용할 수 있습니다.

이러한 기능들로 우선 개발을 배우고 분들에게 효과적인 학습 환경을 제공해보고자 합니다.

## 사전 준비 사항

Narae를 실행하기 위해서는 다음과 같은 프로그램이 필요합니다:

- Docker
- Python 3.11

또한, Narae는 Postgres 데이터베이스가 필요합니다.

빠르게 개발을 시작하려면 다음 명령어를 사용하여 필요한 서비스를 시작하세요.

1. 먼저 사용할 external network를 생성합니다.

   ```sh
   docker network create narae-network
   ```

2. 임시로 사용할 데이터베이스 비밀번호를 설정합니다.

   ```sh
   mkdir secrets
   echo "my_user_password" > secrets/pg_user_password.txt
   ```

3. 도커 컴포즈로 실행합니다.

   ```sh
   docker compose up -d
   ```

데이터베이스를 간단하게 테스트할 수 있도록 Postgres 웹 클라이언트인 **pgamdin4**가 함께 실행됩니다. 필요한 경우 http://localhost:8080 에서 접속할 수 있습니다.

### 초기 설정

필요한 서비스를 모두 설정하고 나서는 환경 변수를 설정해야 합니다. 환경변수 파일을 지원하기 때문에 `app` 디렉토리에 `.env` 파일을 만들어도 됩니다.

필요한 환경 변수는 다음과 같습니다:

```dotenv
# Copy this file to app/.env and fill in the values
## FastAPI settings
### Required
CORS_ORIGINS="[\"http://a.com:3000\", \"http://www.b.com\"]"
ENV=dev # dev, prod, test (default: dev)
SECRET_KEY=supersecretkey # Secret key for FastAPI security
### Optional
BASE_URL=http://localhost:8000 # Base URL for the API
TIMEOUT=30 # Timeout for the API

## Database settings
### Required
DATABASE__USER=narae # Database user name
DATABASE__PASSWORD=1234 # Database password
DATABASE__HOST=postgres # ex) 127.0.0.1
DATABASE__PORT=5432 # default port for Postgres
DATABASE__DATABASE=narae # Database name
### Optional
DATABASE__PROVIDER=postgresql+psycopg_async # default provider for Postgres

## OPEN_AI_API settings (Required)
## Obtain your GPT API Key from https://beta.openai.com/account/api-keys
GPT_KEY=your_gpt_key # sk-xxxxxx
```

## 실행 방법

### 가상 환경에서 Narae 실행하기

1. 저장소 복제:

   ```sh
   git clone https://github.com/cau-oss-team3/narae.git
   cd narae
   ```

2. 가상 환경 설정:

   python3은 `3.11` 버전을 사용해야 합니다.

   ```sh
   # Make venv
   python3 -m venv .venv
   # If you use *nix environment
   source .venv/bin/activate
   # If you use windows environment
   .venv\Scripts\activate.bat
   ```

3. Dependency 설치:

   ```sh
   pip install -r requirements.txt
   ```

4. 애플리케이션 실행:

   ```sh
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

   만약 데이터베이스 연결이 실패한다면, 환경 변수를 확인하세요.

5. http://localhost:8000 에서 Narae에 접속하기

### Docker를 사용하여 Narae 실행하기

최신 도커 이미지는 매번 빌드하여 [Docker Hub](https://hub.docker.com/r/codinggroot/narae/tags)에 업로드됩니다. 해당 이미지를 사용하여 Narae를 바로 실행할 수 있습니다.

1. 필요한 환경 변수를 설정합니다.

   ```sh
   # .env 파일을 열어서 필요한 환경 변수를 설정하세요.
   touch .env # 새 .env 파일 생성
   ```

2. 최신 이미지를 가져오고 컨테이너 실행하기:

   ```sh
   # 도커가 아닌 외부 네트워크를 사용하는 경우, --network 옵션을 제거하세요.
   docker run --env-file .env --network=narae-network -p 80:8000 codinggroot/narae:latest
   ```

3. http://localhost:8000 에서 Narae에 접속하기

## 라이센스

Narae는 MIT 라이선스에 따라 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.

## 지원

문제가 발생하거나 질문이 있는 경우, GitHub 저장소에 이슈를 등록해 주시면 가능한 빨리 해결하도록 하겠습니다.
