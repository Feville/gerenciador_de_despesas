""" Módulo que representa as categorias de despesas"""

from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from core.services.database.models.base import Base


class Expenses(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date(), nullable=False)

    category = relationship("Categories", back_populates="expenses")
    user = relationship("Users", back_populates="expenses")

    @staticmethod
    def migrate(engine):
        Base.metadata.create_all(engine)
