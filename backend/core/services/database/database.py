from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.services.database.models.base import Base
from core.services.database.models.user import Users
from core.services.database.models.categories import Categories
from core.services.database.models.expenses import Expenses
from core.services.database.models.loans import Loans
from consts import DATABASE_URL

engine = create_engine(url=DATABASE_URL)


class DatabaseManager:
    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def initialize(self, database_url):
        engine = create_engine(database_url)
        self.Session.configure(bind=engine)

    def create_tables(self):
        Base.metadata.create_all(engine)

    def session_execute_query(self, query, one_row=False):
        with self.Session() as session:
            try:
                result = session.execute(query)
                return result.fetchone() if one_row else result.fetchall()
            except Exception as e:
                session.rollback()
                raise e

    def session_insert_data(self, entities: list):
        with self.Session() as session:
            try:
                session.add_all(entities)
                session.commit()
                session.expunge_all()
            except Exception as e:
                session.rollback()
                raise e

    def migrate(self):
        Users.migrate(engine)
        Categories.migrate(engine)
        Expenses.migrate(engine)
        Loans.migrate(engine)
