from sqlalchemy import Column, Integer, REAL, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Table = declarative_base()


class Expenses(Table):
    __tablename__ = "expenses"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    amount = Column(REAL(), nullable=False)
    category_id = Column(Integer(), ForeignKey("categories.id"))
    user_id = Column(Integer(), ForeignKey("user.id"))
    date = Column(Date(), nullable=False)

    category = relationship("Category", back_populates="expenses")
    user = relationship("User", back_populates="expenses")

    @staticmethod
    def migrate(engine):
        Table.metadata.create_all(engine)
