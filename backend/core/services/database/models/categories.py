from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.services.database.models.base import Base


class Categories(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120))
    user_id = Column(Integer, ForeignKey("users.id"))

    loans = relationship("Loans", back_populates="category")
    expenses = relationship("Expenses", back_populates="category")

    user = relationship("Users", back_populates="categories")

    @staticmethod
    def migrate(engine):
        Base.metadata.create_all(engine)
