from app.models import StatusEnum, Session, JobStatus
from app.models import set_job_status
import os
import shutil


class Importer:

    status = StatusEnum.importing.value

    hooks_for_status = {}

    job_id = ""

    def __init__(self, job_id):
        raise NotImplementedError()

    def process_url(self, url):
        self.set_status(StatusEnum.importing)

    def validate_url(url):
        raise NotImplementedError()

    def set_status(self, new_status):
        self.status = new_status

        set_job_status(self.job_id, new_status)

        # Callbacks for the change
        if self.status in self.hooks_for_status:
            hooks = self.hooks_for_status[self.status]

            if len(hooks) > 0:
                for h in hooks:
                    h()  # Call the method. QUESTION: PARAMS?

    def add_hook_for_status(self, status, action):
        # If this is the first time that we will register an action for that status
        if status not in self.hooks_for_status:
            self.hooks_for_status[status] = []

        self.hooks_for_status[status].append(action)

    def remove_hook_for_status(self, status, action):
        # Remove the hook for that status
        if action in self.hooks_for_status[status]:
            self.hooks_for_status[status].remove(action)

    def on_import_error_found(self, exception):

        session = Session()

        # First, check in the db if the job has the login_required status

        job_status = (
            session.query(JobStatus)
            .filter(JobStatus.job_id == self.job_id)
            .filter(
                JobStatus.status
                == StatusEnum.importing_error_authorization_required.value
            )
            .one_or_none()
        )

        status_enum = (
            StatusEnum.importing_error_data_unreachable
            if job_status
            else StatusEnum.importing_error_authorization_required
        )

        set_job_status(self.job_id, status_enum.value)

    def prepare_folder(self, temp_folder_path, job_folder_path):
        # Check if the tmp folder for this service already exists
        if os.path.exists(temp_folder_path) is False:
            # If we need to create it,

            if not os.path.exists(temp_folder_path):
                print("Creating tmp folder")
                os.makedirs(temp_folder_path)

        if os.path.exists(job_folder_path) is True:
            # If the folder for this job has already been created,
            # we need to remove it, so it can be later created
            try:
                shutil.rmtree(job_folder_path)
            except OSError as e:
                print("Error: %s : %s" % (job_folder_path, e.strerror))


class NotValidURLForImportException(ValueError):
    pass
