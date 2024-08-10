from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.services.database.models.base import Base
from core.services.database.models.user import Users
from core.services.database.models.categories import Categories
from core.services.database.models.expenses import Expenses
from core.services.database.models.loans import Loans


class DatabaseManager:
    engine = None
    Session = None

    @classmethod
    def initialize(cls, database_url):
        cls.engine = create_engine(database_url)
        cls.Session = sessionmaker(bind=cls.engine)

    @classmethod
    def create_tables(cls):
        Base.metadata.create_all(cls.engine)

    @classmethod
    def session_execute_query(cls, query, one_row=False):
        Session = cls.Session
        with Session() as session:
            try:
                result = session.execute(query)
                return result.fetchone() if one_row else result.fetchall()
            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def session_insert_data(cls, entities: list):
        Session = cls.Session
        with Session as session:
            try:
                session.add_all(entities)
                session.commit()
                session.expunge_all()
                session.close()
            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def migrate(
        cls,
    ):
        Users.migrate(cls.engine)
        Categories.migrate(cls.engine)
        Expenses.migrate(cls.engine)
        Loans.migrate(cls.engine)
