import os
from dotenv import load_dotenv

load_dotenv()

HF_HOME = os.getenv("HF_HOME", "./hf_cache")

DATABASE_URL = os.getenv("DATABASE_URL")
