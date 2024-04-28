import os
from dotenv import load_dotenv


class Config:
    def __init__(self) -> None:
        load_dotenv(dotenv_path=self.get_env_path())
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_DATABASE = os.getenv("DB_DATABASE")
        self.DB_HOST = os.getenv("DB_HOST")

    def get_database_url(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_DATABASE}"

    def get_env_path(self):
        """
        Finds the absolute path of the .env file.
        NOTE: 윈도우의 경우, load_dotenv 파일을 호출할 때 절대 경로를 인자로 줘야 정상 작동합니다.
        """
        current_dir = os.path.dirname(__file__)
        env_file = '.env'
        env_path = os.path.join(current_dir, env_file)
        return env_path


