# It isa abstraction layer of .env

from dotenv import load_dotenv
import os

load_dotenv()

class Config():
    db_host = os.getenv('DB_HOST')   # here db_host is a member varibale
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME') 

