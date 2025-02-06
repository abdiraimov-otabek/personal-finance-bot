from environs import Env
from urllib.parse import urlparse
import psycopg2

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
DATABASE_URL = env.str("DATABASE_URL")

parsed_url = urlparse(DATABASE_URL)

DB_USER = parsed_url.username
DB_PASS = parsed_url.password
DB_NAME = parsed_url.path[1:]
DB_HOST = parsed_url.hostname
DB_PORT = parsed_url.port

try:
    with psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    ) as conn:
        print("✅ Connected to PostgreSQL!")
except Exception as e:
    print("❌ Database connection failed:", e)
