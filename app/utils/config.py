from dotenv import load_dotenv
import os

load_dotenv()

tz_name = os.getenv("TIME_ZONE", "Asia/Yekaterinburg")
secret_key = os.getenv("SECRET_KEY").encode()
