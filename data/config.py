from environs import Env
from urllib.parse import urlparse

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
