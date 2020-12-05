from .. import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CONNECTION_STRING = "postgresql://{user}:{password}@{host}:{port}/{database}".format  # noqa: E501

_engine = None
_Session = None


def _get_engine():
    global _engine

    if _engine is None:
        _engine = create_engine(
            CONNECTION_STRING(
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                database=settings.DB_DATABASE
            ),
            echo=False  #(True if settings.TEST else False)
        )
    return _engine


def _create_session():
    global _Session

    if _Session is None:
        _Session = sessionmaker(bind=_get_engine())
    
    return _Session()
