from environs import Env
from urllib.parse import urlparse


env = Env()
env.read_env()


BOT_TOKEN = env.str("BOT_TOKEN")  # Bot Token
ADMINS = env.list("ADMINS")  # Adminlar ro'yxati

DATABASE_URL = env.str("DATABASE_URL")


db_url = urlparse(DATABASE_URL)
DB_USER = db_url.username
DB_PASS = db_url.password
DB_NAME = db_url.path[1:]
DB_HOST = db_url.hostname
DB_PORT = db_url.port

DB_USER2 = env.str("DB_USER")
DB_PASS2 = env.str("DB_PASS")
DB_NAME2 = env.str("DB_NAME")
DB_HOST2 = env.str("DB_HOST")
