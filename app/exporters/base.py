from sqlalchemy.orm import Session


class BaseExporter:
    def __init__(self, db: Session, job_id: str):
        raise NotImplementedError()

    def process(self) -> None:
        raise NotImplementedError()


class AuthRequired(Exception):
    pass


class NotReachable(Exception):
    pass
