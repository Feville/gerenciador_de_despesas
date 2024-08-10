from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.services.database.models.user import User


class DatabaseManager:
    engine = None
    Session = None

    @classmethod
    def initialize(cls, database_url):
        cls.engine = create_engine(database_url)
        cls.Session = sessionmaker(bind=cls.engine)

    @classmethod
    def session_execute_query(cls, query, one_row=False):
        Session = sessionmaker(bind=cls.engine)
        with Session() as session:
            try:
                result = session.execute(query)
                return result.fetchone() if one_row else result.fetchall()
            except Exception as e:
                session.rollback()
                raise e

    @classmethod
    def session_insert_data(cls, entities: list):
        with cls.session as session:
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
        User.migrate(cls.engine)
