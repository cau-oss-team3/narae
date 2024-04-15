# Narae

Languages: \[한국어\] | \[[English](README.md)\]

## Features

(TBD).

## Prerequisites

To run Narae, you will need the following software:

- Docker
- Python 3.11

Additionally, a MySQL database is required for Narae.

To quickly start development, use the following commands to launch the required services:

1. Create an external network to be used:

   ```sh
   docker network create narae-network
   ```

2. Set a database password to be used temporarily:

   ```sh
   mkdir secrets
   echo "my_root_password" > secrets/mysql_root_password.txt
   echo "my_user_password" > secrets/mysql_user_password.txt
   ```

3. Launch with Docker Compose:

   ```sh
   docker compose up -d
   ```

**Adminer**, a web-based MySQL client, will run concurrently to facilitate database testing. You can access it at http://localhost:8080 if needed.

### Initial Setup

After all necessary services are configured, you must set up environment variables. You can create a `.env` file in the `app/` directory as dot files are supported. you can copy the `.env.example` file to `.env` and set the necessary environment variables.

Required environment variables are as follows:

```dotenv
DB_USER=db_user_name # e.g., narae
DB_PASSWORD=db_password # e.g., my_awesome_password
DB_DATABASE=db_name # e.g., narae
DB_HOST=db_host # e.g., 127.0.0.1
GPT_TOKEN=your_gpt_token # Obtain your GPT token from https://beta.openai.com/account/api-keys
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
   python3 -m venv .venv
   source .venv/bin/activate
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
