# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.job import Job  # noqa
from app.models.job_log import JobLog  # noqa
from app.models.manifest import Manifest  # noqa
