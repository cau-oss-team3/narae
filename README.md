# narae

English | [한국어](README.ko.md)

Personal AI coaching companion designed to guide you through daily growth and learning.

## Features

- (tbd)

## Prerequisites

Before you start, ensure you have the following installed on your system:

- Docker
- Python 3.11
- Git

Additionally, you need to set up MySQL database to run Narae.

For development, you can use the following command to start the required services. A web-based MySQL client, phpMyAdmin, is also started to help you test the database easily.

```sh
docker compose up -d
```

### Initial Setup

dot file is supported, so you can create a `.env` file in the `app` directory. The following environment variables are required:

```dotenv
DB_USER=db_user_name
DB_PASSWORD=db_password
DB_DATABASE=db_name
DB_HOST=db_host # e.g. 127.0.0.1
GPT_TOKEN=your_gpt_token # Get your GPT token from https://beta.openai.com/account/api-keys
```

## How to Run

### Running Narae in a Virtual Environment

1. Clone the Repository:

```sh
git clone https://github.com/cau-oss-team3/narae.git
cd narae
```

2. Set Up the Virtual Environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

3. Install Dependencies:

```sh
pip install -r requirements.txt
```

4. Launch the Application:

```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

5. Access Narae at http://localhost:8000

### Running Narae Using Docker

1. Clone the Repository:

```sh
git clone https://github.com/cau-oss-team3/narae.git
cd narae
```

2. Build the Docker Image and run the Container:

```sh
# Build the Docker Image
docker build -t narae .
# Run the Docker Container (this command assumes that you have a network called narae_db-network)
docker run --network=narae_db-network -p 80:8000 narae:latest
```

3. Access Narae at http://localhost:8000

## License

Narae is released under the MIT License. By contributing to Narae, you agree to abide by its terms. See [LICENSE](LICENSE) for more information.

## Support

If you encounter any issues or have questions, please file an issue on the GitHub repository, and we'll make sure to address it as soon as possible.
