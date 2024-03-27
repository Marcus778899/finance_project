from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pydantic import BaseModel
from secret import key

# initialization
class Base(DeclarativeBase):
    pass

engine = create_engine(
    f'mysql+mysqldb://{key.mysql_user}:{key.mysql_password}@{key.clickhouse_host}/{key.mysql_database}', 
    echo=True
    )

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_db_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
        pass
    pass

# model for get method
class StockPrice(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    stock_id: str

