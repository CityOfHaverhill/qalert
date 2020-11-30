"""The database module is the interface to PostgreSQL db with 311 request data.
"""
from typing import List, Optional

from . import settings

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, Float, VARCHAR, Text
from sqlalchemy.orm import sessionmaker, validates
from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape
from geoalchemy2.types import WKBElement
from shapely.geometry import Point

NAD_83 = 4269
Base = declarative_base()


def construct_point(context) -> WKBElement:
    latitude = context.get_current_parameters()['latitude']
    longitude = context.get_current_parameters()['longitude']
    return from_shape(
        shape=Point(longitude, latitude),
        srid=NAD_83
    )


class QAlertRequest(Base):
    """Sqlalchemy orm model for the qalert requests table"""
    __tablename__ = 'qalert_requests'
    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    create_date = Column(DateTime)
    create_date_unix = Column(Integer)
    last_action = Column(DateTime)
    last_action_unix = Column(Integer)
    type_id = Column(Integer)
    type_name = Column(VARCHAR(length=200))
    comments = Column(VARCHAR(length=5000))
    street_num = Column(VARCHAR(length=100))
    street_name = Column(VARCHAR(length=100))
    cross_name = Column(VARCHAR(length=100))
    city_name = Column(VARCHAR(length=100))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    point = Column(
        Geometry(
            geometry_type='POINT',
            srid=NAD_83
        ),
        nullable=False,
        default=construct_point
    )

    @validates('type_name', 'comments', 'street_num', 'street_name', 'cross_name', 'city_name')  # noqa: E501
    def validate_length(self, key, value):
        max_len = getattr(self.__class__, key).prop.columns[0].type.length
        if len(value) > max_len:
            return value[:max_len]
        return value


class QAlertAudit(Base):
    """Sqlalchemy orm model for the qalert audit table"""
    __tablename__ = 'qalert_audits'
    id = Column(Integer, primary_key=True)
    create_date = Column(Text)


class QAlertAuditDB:
    CONNECTION_STRING = "postgresql://{user}:{password}@{host}:{port}/{database}".format  # noqa: E501

    def __init__(self, **kwargs):
        self._load_params(**kwargs)
        self._prepare_connection()

    def _load_params(self, **kwargs):
        self.host: str = kwargs.get('host') or os.environ['db_host']
        self.port: int = kwargs.get('port') or os.environ['db_port']
        self.user: str = kwargs.get('user') or os.environ['db_user']
        self.database: str = (
            kwargs.get('database') or os.environ['db_database']
        )
        self.password: str = (
            kwargs.get('password') or os.environ.get('db_password')
        )

    def _prepare_connection(self):
        self.engine = create_engine(
            self.CONNECTION_STRING(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            ),
            echo=True
        )
        self.session_maker = sessionmaker(bind=self.engine)

    def save(self, request: QAlertAudit, commit=True):
        self.session.add(request)
        self.session.flush()
        if commit:
            self.commit()

    def commit(self):
        self.session.commit()

    def get(self, request_id: int, raise_exception=False) -> Optional[QAlertAudit]:  # noqa: E501
        request = self.session.query(QAlertAudit).get(request_id)
        if request is None and raise_exception:
            raise Exception("QAlert request not found.")
        return request

    def get_latest_request(self, raise_exception=False) -> QAlertAudit:
        request = self.session.query(QAlertAudit).order_by(
            QAlertAudit.id.desc()).first()
        if request is None and raise_exception:
            raise Exception("QAlert request not found.")
        return request

    def _connect(self):
        """Establish connection with psql db."""
        self.session = self.session_maker()

    def _disconnect(self):
        """Kill connection with psql db."""
        self.session.close()

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._disconnect()


class QAlertDB:
    """QAlertDB class handles all database related operations.

        Example:

        request_1 = QAlertRequest(id=1, latitude=1.1, longitude=1.1)
        request_2 = QAlertRequest(id=2, latitude=1.1, longitude=1.1)
        requests = [request_1, request_2]
        with QAlertDB() as db:
            # save individual request object
            db.save(request_1)

            # save a list of request objects
            db.save_many(requests, commit=True)

            # delete a request object
            db.delete(request_2)

            # modify and save a request object
            request_1.type_name = "trash pickup"
            db.save(request_1)
    """
    CONNECTION_STRING = "postgresql://{user}:{password}@{host}:{port}/{database}".format  # noqa: E501

    def __init__(self, **kwargs):
        self._load_params(**kwargs)
        self._prepare_connection()

    def _load_params(self, **kwargs):
        self.host: str = kwargs.get('host') or settings.DB_HOST
        self.port: int = kwargs.get('port') or settings.DB_PORT
        self.user: str = kwargs.get('user') or settings.DB_USER
        self.password: str = (
            kwargs.get('password') or settings.DB_PASSWORD
        )
        self.database: str = (
            kwargs.get('database') or settings.DB_DATABASE
        )

    def _prepare_connection(self):
        self.engine = create_engine(
            self.CONNECTION_STRING(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            ),
            echo=(True if settings.TEST else False)
        )
        self.session_maker = sessionmaker(bind=self.engine)

    def save(self, request: QAlertRequest, commit=True):
        if self.get(request_id=request.id):
            return
        self.session.add(request)
        self.session.flush()
        if commit:
            self.commit()

    def save_many(self, requests: List[QAlertRequest], commit=True):
        for request in requests:
            self.save(request, commit=False)
        if commit:
            self.commit()

    def commit(self):
        self.session.commit()

    def get(self, request_id: int, raise_exception=False) -> Optional[QAlertRequest]:  # noqa: E501
        request = self.session.query(QAlertRequest).get(request_id)
        if request is None and raise_exception:
            raise Exception("QAlert request not found.")
        return request

    def find_by_props(self, prop_dict: dict) -> List[QAlertRequest]:
        q = self.session.query(QAlertRequest)
        for attr, value in prop_dict.items():
            q = q.filter(getattr(QAlertRequest, attr) == value)
        return q.all()

    def delete(self, request: QAlertRequest, commit=True):
        self.session.delete(request)
        self.session.flush()
        if commit:
            self.commit()

    def _connect(self):
        """Establish connection with psql db."""
        self.session = self.session_maker()

    def _disconnect(self):
        """Kill connection with psql db."""
        self.session.close()

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._disconnect()
