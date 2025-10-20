import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    # SQLAlchemy database URL: mysql+pymysql://USER:PASSWORD@HOST:PORT/DBNAME
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root@127.0.0.1:3306/fairlift_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
