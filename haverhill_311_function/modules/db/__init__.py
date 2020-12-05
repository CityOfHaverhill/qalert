from .exceptions import DBException  # noqa: F401
from .models import QAlertAudit, QAlertRequest  # noqa: F401
from .repository import Repository


def create_repo(entity_model, connect=False) -> Repository:
    return Repository(entity_model, connect=connect)
