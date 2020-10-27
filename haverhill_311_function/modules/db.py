"""The database module is the interface to PostgreSQL db with 311 request data.
"""
import os
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, Text, Float
from sqlalchemy.orm import sessionmaker
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
        shape=Point(latitude, longitude),
        srid=NAD_83
    )


class QAlertRequest(Base):
    """Sqlalchemy orm model for the qalert requests table"""
    __tablename__ = 'qalert_requests_geo'
    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    create_date = Column(DateTime)
    create_date_unix = Column(Integer)
    last_action = Column(DateTime)
    last_action_unix = Column(Integer)
    type_id = Column(Integer)
    type_name = Column(Text)
    comments = Column(Text)
    street_num = Column(Text)
    street_name = Column(Text)
    cross_name = Column(Text)
    city_name = Column(Text)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    point = Column(Geometry(geometry_type='POINT', srid=NAD_83), nullable=False, default=construct_point)


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

    def __init__(self, host=None, port=None, user=None, password=None, database=None):
        self.host: str = host or os.environ['db_host']
        self.port: int = port or os.environ['db_port']
        self.user: str = user or os.environ['db_user']
        self.database: str = database or os.environ['db_database']
        self.password: str = password or os.environ.get('db_password')

    def save(self, request: QAlertRequest, commit=True):
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
    
    def get(self, request_id: int, raise_exception=False):
        request = self.session.query(QAlertRequest).get(request_id)
        if request is None and raise_exception:
            raise Exception("QAlert request not found.")
        return request
    
    def find_by_props(self, prop_dict: dict) -> list:
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
        self.engine = create_engine(
            f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}', 
            echo=True
        )
        session_maker = sessionmaker(bind=self.engine)
        self.session = session_maker()

    def _disconnect(self):
        """Kill connection with psql db."""
        self.session.close()

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._disconnect()
