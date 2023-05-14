from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func

engine = create_engine("postgresql://app:1234@127.0.0.1:5431/app")
Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class Adv(Base):
    __tablename__ = "advertisement"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())


Base.metadata.create_all()
