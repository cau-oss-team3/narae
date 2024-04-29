# 나래

Languages: \[한국어\] | [\[English\]](README.md)

## 기능

(TBD)

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
DATABASE__PROVIDER=postgresql # default provider for Postgres

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
   python3 -m venv .venv
   source .venv/bin/activate
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
