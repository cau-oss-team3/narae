import logging
import logging.config
import yaml
from os.path import exists, join

from app.settings import settings


def set_logging(base_dir: str) -> None:
    """
    Sets logging configuration based on YAML files.
    """
    if settings.env == "prod":
        config_files = [".logging.yaml"]
    else:
        config_files = [".logging.dev.yaml", ".logging.yaml"]

    for config_file in config_files:
        full_path = join(base_dir, config_file)
        if exists(full_path):
            with open(full_path, "rt") as f:
                config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
            print(f"INFO:     Logging configured using `{config_file}`")
            return

    # Fallback basic configuration
    logging.basicConfig(level=logging.DEBUG)
    print("WARN:      Fallback to basic logging configuration.")

# logger = logging.getLogger("fastapi")