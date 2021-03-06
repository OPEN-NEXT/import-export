import uuid
from typing import Optional

from pydantic import AnyHttpUrl, BaseModel

from app.models.job import JobStatus


class BaseJob(BaseModel):
    import_url: AnyHttpUrl
    export_url: AnyHttpUrl
    import_service: str
    export_service: str
    import_token: Optional[str] = None
    export_token: Optional[str] = None


class JobUpdate(BaseModel):
    import_url: Optional[AnyHttpUrl] = None
    export_url: Optional[AnyHttpUrl] = None
    import_token: Optional[str] = None
    export_token: Optional[str] = None


class Job(BaseJob):
    id: uuid.UUID
    status: JobStatus
    general_progress: float
    status_progress: float

    class Config:
        orm_mode = True


class JobCreate(BaseJob):
    pass
