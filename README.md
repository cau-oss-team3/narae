# Narae

[![Containerize](https://github.com/cau-oss-team3/narae/actions/workflows/docker.yml/badge.svg)](https://github.com/cau-oss-team3/narae/actions/workflows/docker.yml)

Languages: \[English\] | [\[한국어\]](README.ko.md)

## Features

*Narae** is an llm-powered mentoring service designed to enhance user learning in software development fields such as backend and frontend development. Here are the key features:

- **Personalized Learning Paths:** Users set their development goals and receive tailored learning plans based on their individual needs, goals, and circumstances.
- **AI-Driven Guidance:** AI suggests actions and offers in-depth explanations and exercises on challenging topics.
- **Progress Tracking and Evaluation:** AI summarizes interactions for progress tracking and generates daily quizzes to reinforce learning.
- **Advanced Knowledge Mentoring:** Utilizes OpenAI's embedding technologies for deep, specialized knowledge delivery.
- **Feedback-Driven Improvements:** Continuous collection of user feedback to refine and enhance the service.
- **Interactive Learning:** Future potential for voice interactions allows users to engage with AI mentors anywhere, anytime, with responses in both voice and text. 

These features combine to create a dynamic and effective learning environment tailored to the needs of modern developers.

## Prerequisites

To run Narae, you will need the following software:

- Docker
- Python 3.11

Additionally, a Postgres database is required for Narae.

To quickly start development, use the following commands to launch the required services:

1. Create an external network to be used:

   ```sh
   docker network create narae-network
   ```

2. Set a database password to be used temporarily:

   ```sh
   mkdir secrets
   echo "my_user_password" > secrets/pg_user_password.txt
   ```

3. Launch with Docker Compose:

   ```sh
   docker compose up -d
   ```

**pgamdin4**, a web-based Postgres client, will run concurrently to facilitate database testing. You can access it at http://localhost:8080 if needed.

### Initial Setup

After all necessary services are configured, you must set up environment variables. You can create a `.env` file in the `app/` directory as dot files are supported. you can copy the `.env.example` file to `.env` and set the necessary environment variables.

Required environment variables are as follows:

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
## Obtain your GPT API Key  from https://beta.openai.com/account/api-keys
GPT_KEY=your_gpt_key # sk-xxxxxx
```

## How to Run

### Running Narae in a Virtual Environment

1. Clone the repository:

   ```sh
   git clone https://github.com/cau-oss-team3/narae.git
   cd narae
   ```

2. Set up a virtual environment using Python 3.11:

   ```sh
   # Make venv
   python3 -m venv .venv
   # If you use *nix environment
   source .venv/bin/activate
   # If you use windows environment
   .venv\Scripts\activate.bat
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Run the application:

   ```sh
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

   if database connection error occurs, check the database connection information in the `.env` file.

5. Access Narae at http://localhost:8000

### Running Narae Using Docker

The latest Docker images are built regularly and uploaded to [Docker Hub](https://hub.docker.com/r/codinggroot/narae/tags). You can directly run Narae using these images.

1. Set necessary environment variables:

   ```sh
   # Open the .env file and set the necessary environment variables.
   touch .env # Create a new .env file
   ```

2. Fetch the latest image and run the container:

   ```sh
   # If not using Docker's external network, remove the --network option.
   docker run --env-file .env --network=narae-network -p 80:8000 codinggroot/narae:latest
   ```

3. Access Narae at http://localhost:8000

## License

Narae is distributed under the MIT License. For more details, see the [LICENSE](LICENSE) file.

## Support

If you encounter any issues or have questions, please file an issue on the GitHub repository, and we will address it as soon as possible.
