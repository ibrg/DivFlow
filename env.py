import os
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("API_KEY_fmpsdk")
SQLITE_DB = os.getenv("SQLITE_DB_PATH")