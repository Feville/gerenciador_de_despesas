from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Table = declarative_base()


class Categories(Table):
    __tablename__ = "categories"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(120))

    @staticmethod
    def migrate(engine):
        Table.metadata.create_all(engine)
