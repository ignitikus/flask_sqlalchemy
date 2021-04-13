from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login_count = Column(Integer, default=0)
    username = Column(String(30), nullable=False)
    password = Column(String(40), nullable=False)


engine = create_engine('sqlite:///users_info.db')
Base.metadata.create_all(engine)
