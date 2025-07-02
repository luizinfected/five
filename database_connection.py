from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from env import RDS_DATABASE, RDS_PASSWORD, RDS_HOST, RDS_PORT, RDS_USER, LOCAL_MYSQL_CONNECTION_STR, IS_DEV

AWS_DB_CONNECTION_STR = f"mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/{RDS_DATABASE}"

DB_CONNECTION_STR = LOCAL_MYSQL_CONNECTION_STR if IS_DEV else AWS_DB_CONNECTION_STR



engine = create_engine(DB_CONNECTION_STR)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
