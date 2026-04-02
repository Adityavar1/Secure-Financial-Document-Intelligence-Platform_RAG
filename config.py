import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DOCUMENTS_DIR = "documents"
VECTOR_DB_DIR = "vector_db"
USERS_FILE = "users.json"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
NUM_RETRIEVED_DOCS = 5

TEMPERATURE = 0
MODEL_NAME = "gpt-4"
SECRET_KEY = "secret-token"   
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60