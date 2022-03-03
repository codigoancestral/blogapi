from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

                 #'postgresql://<username>:<password>@<ip-address/hostnome>/<database_name>'
stringConexaoBD = 'postgresql://postgres:12345678@localhost/fastapi'
engine = create_engine(stringConexaoBD)
sessaoLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
  db = sessaoLocal()
  try:
    yield db
  finally:
    db.close()