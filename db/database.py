from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
 
engine = create_engine("postgresql://<username>:<password>@localhost/<db_name>",
    echo= True)
 
Base = declarative_base()
 
Session = sessionmaker()