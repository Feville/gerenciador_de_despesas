""" Módulo que representa as categorias de despesas"""

from sqlalchemy import Column, String, Integer, LargeBinary
from sqlalchemy.orm import relationship
from core.services.database.models.base import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    secret_pass = Column(LargeBinary, nullable=False)

    expenses = relationship("Expenses", back_populates="user")
    categories = relationship("Categories", back_populates="user")
    loans = relationship("Loans", back_populates="user")

    @staticmethod
    def migrate(engine):
        Base.metadata.create_all(engine)
