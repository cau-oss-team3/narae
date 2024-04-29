import os 

import pytest


TEST_MODE = ["test"]
#os.environ["ENV"] = TEST_MODE

if os.getenv("ENV") not in TEST_MODE:
    pytest.exit(f"ENV가 test 모드가 아닙니다. 현재 {os.getenv('ENV')} 모드입니다.")
