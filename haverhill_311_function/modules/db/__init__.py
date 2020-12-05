from .exceptions import DBException
from .models import QAlertAudit, QAlertRequest
from .repository import Repository


def create_repo(entity_model, connect=False) -> Repository:
    return Repository(entity_model, connect=connect)
