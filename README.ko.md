# 나래

한국어 | [English](README.md)

## 기능

(tbd)

## 사전 준비 사항

실행하기 위해 시스템에 다음과 같은 것들이 설치돼야 합니다:

- Docker
- Python 3.11
- Git

또한, Narae를 실행하기 위해서는 MySQL 데이터베이스가 필요합니다.

빠르게 개발을 시작하려면 다음 명령어를 사용하여 필요한 서비스를 시작할 수 있습니다. 데이터베이스를 간단하게 테스트할 수 있도록 웹 기반 MySQL 클라이언트인 phpMyAdmin이 함께 실행됩니다.

```sh
docker compose up -d
```

### 초기 설정

필요한 서비스를 모두 설정하고 나서는 환경 변수를 설정해야 합니다.
dot file을 지원하기 때문에 `app` 디렉토리에 `.env` 파일을 만들어도 됩니다. 필요한 환경 변수는 다음과 같습니다:

```dotenv
DB_USER=db_user_name
DB_PASSWORD=db_password
DB_DATABASE=db_name
DB_HOST=db_host # e.g. 127.0.0.1
GPT_TOKEN=your_gpt_token # Get your GPT token from https://beta.openai.com/account/api-keys
```

## 실행 방법

### 가상 환경에서 Narae 실행하기

1. 저장소 복제:

```sh
git clone https://github.com/cau-oss-team3/narae.git
cd narae
```

2. 가상 환경 설정:

python3는 python3.11을 의미합니다.

```sh
python3 -m venv .venv
source .venv/bin/activate
```

3. 의존성 설치:

```sh
pip install -r requirements.txt
```

4. 애플리케이션 실행:

```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

5. http://localhost:8000 에서 Narae에 접속하기

### Docker를 사용하여 Narae 실행하기

1. 최신 이미지를 가져오고 컨테이너 실행하기:

최신 도커 이미지는 매번 빌드하여 [Docker Hub](https://hub.docker.com/r/codinggroot/narae/tags)에 업로드됩니다.

```sh
# Docker 컨테이너 실행 (이때, 이 저장소에서 테스트용으로 제공하는 docker-compose의 네트워크인 narae_db-network가 있다고 가정합니다.)
docker run --env-file ./app/.env --network=narae_db-network -p 80:8000 codinggroot/narae:latest
```

2. http://localhost:8000 에서 Narae에 접속하기

## 라이센스

Narae는 MIT 라이선스에 따라 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.

## 지원

문제가 발생하거나 질문이 있는 경우, GitHub 저장소에 이슈를 등록해 주시면 가능한 빨리 해결하도록 하겠습니다.
