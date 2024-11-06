""" Módulo que representa as categorias de despesas"""

from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from core.services.database.models.base import Base


class Loans(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date(), nullable=False)

    category = relationship("Categories", back_populates="loans")
    user = relationship("Users", back_populates="loans")

    @staticmethod
    def migrate(engine):
        Base.metadata.create_all(engine)
