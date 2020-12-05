from .db import _create_session
from .exceptions import DBException

from sqlalchemy.exc import SQLAlchemyError



class Repository():
    """Repository is interface to operate on a particular ORM model (table).

        Example:

        request_1 = QAlertRequest(id=1, latitude=1.1, longitude=1.1)
        request_2 = QAlertRequest(id=2, latitude=1.1, longitude=1.1)
        requests = [request_1, request_2]

        Option 1: Use as a context manager -- handles aquiring and releasing resources (db sessions) for you
        with Repository(QAlertRequest) as qalert_request_repo:
            # save individual request object
            qalert_request_repo.save(request_1)

            # save a list of request objects
            qalert_request_repo.save_many(requests, commit=True)

            # delete a request object
            qalert_request_repo.delete(request_2)

            # modify and save a request object
            request_1 = qalert_request_repo.get(1)
            request_1.type_name = "trash pickup"
            qalert_request_repo.save(request_1)

        Option 2: Manually decide when to aquire and release resources (db sessions)
        qalert_request_repo = Repository(QAlertRequest)
        qalert_request_repo.connect()
        ...
        do operations
        ...
        qalert_request_repo.disconnect()

        qalert_audit_repo = Repository(QAlertAudit, connect=True)  # auto connect
        ...
        do operations
        ...
        qalert_audit_repo.disconnect()

    """
    def __init__(self, entity_model, connect=False):
        self.model = entity_model
        self.session = None
        if connect:
            self.connect()
    
    def save(self, entity, commit=True):
        if self.get(entity_id=entity.id):
            return
        self.session.add(entity)
        if commit:
            self.commit()
    
    def save_many(self, entities, commit=True):
        for entity in entities:
            self.save(entity, commit=False)
        if commit:
            self.commit()

    def get(self, entity_id, raise_exception=False):
        entity = self.session.query(self.model).get(entity_id)
        if entity is None and raise_exception:
            raise DBException(f"{self.model.__name__} with id {entity_id} not found.")
        return entity
    
    def get_latest(self, raise_exception=False):
        entity = self.session.query(self.model).order_by(
            self.model.id.desc()).first()
        if entity is None and raise_exception:
            raise DBException(f"{self.model.__name__} not found.")
        return entity

    def find_by(self, prop_dict: dict = {}, filters: list = [], limit: int = None) -> list:  # noqa: E501
        q = self.session.query(self.model)
        for attr, value in prop_dict.items():
            q = q.filter(getattr(self.model, attr) == value)
        for filter_item in filters:
            q = q.filter(filter_item)
        if limit:
            q.limit(limit)
        return q.all()

    def delete(self, entity, commit=True):
        self.session.delete(entity)
        if commit:
            self.commit()

    def commit(self):
        try:
            self.session.flush()
            self.session.commit()
        except SQLAlchemyError as exc:
            self.session.rollback()
            raise DBException(exc)
    
    def connect(self):
        self.session = _create_session()
    
    def disconnect(self):
        if self.session is not None:
            self.session.close()
            self.session = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
