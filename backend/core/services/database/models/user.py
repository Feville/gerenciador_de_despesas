from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Table = declarative_base()


class User(Table):
    __tablename__ = "user"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    @staticmethod
    def migrate(engine):
        Table.metadata.create_all(engine)
