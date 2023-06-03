from dotenv import load_dotenv
import os

load_dotenv()


API_KEY = os.environ.get("API_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")