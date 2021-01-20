from app.model.constants import (
    THINGIVERSE_SERVICE,
    MYMINIFACTORY_SERVICE,
    WIKIFACTORY_SERVICE,
)
from app.model.constants import IMPORT_SERVICE, IMPORT_URL, IMPORT_TOKEN
from app.model.constants import GIT_SERVICE

from app.model.constants import GOOGLEDRIVE_SERVICE
from app.controller.importers.thingiverse_importer import ThingiverseImporter
from app.controller.importers.git_importer import GitImporter
from app.controller.importers.googledrive_importer import GoogleDriveImporter
from app.controller.importers.myminifactory_importer import MyMiniFactoryImporter
from app.controller.importers.wikifactory_importer import WikifactoryImporter


class ImporterProxy:
    def __init__(self, job_id):
        self.job_id = job_id

    def handle_request(self, json_request):

        try:

            if json_request[IMPORT_SERVICE].lower() == THINGIVERSE_SERVICE:

                return self.handle_thingiverse(
                    json_request[IMPORT_URL], json_request[IMPORT_TOKEN], self.job_id
                )

            elif json_request[IMPORT_SERVICE].lower() == GIT_SERVICE:
                return self.handle_git(
                    json_request[IMPORT_URL], json_request[IMPORT_TOKEN], self.job_id
                )

            elif json_request[IMPORT_SERVICE].lower() == MYMINIFACTORY_SERVICE:
                return self.handle_myminifactory(
                    json_request[IMPORT_URL], json_request[IMPORT_TOKEN], self.job_id
                )

            elif json_request[IMPORT_SERVICE].lower() == GOOGLEDRIVE_SERVICE:
                return self.handle_googledrive(
                    json_request[IMPORT_URL], json_request[IMPORT_TOKEN], self.job_id
                )
            elif json_request[IMPORT_SERVICE].lower() == WIKIFACTORY_SERVICE:
                return self.handle_wikifactory(
                    json_request[IMPORT_URL], json_request[IMPORT_TOKEN], self.job_id
                )
            else:
                raise NotImplementedError()
        except Exception as e:
            print(e)

    def handle_thingiverse(self, url, auth_token, job_id):
        imp = ThingiverseImporter(job_id)
        return imp.process_url(url, auth_token)

    def handle_git(self, url, auth_token, job_id):
        imp = GitImporter(job_id)
        return imp.process_url(url, auth_token)

    def handle_googledrive(self, url, auth_token, job_id):
        imp = GoogleDriveImporter(job_id)
        return imp.process_url(url, auth_token)

    def handle_myminifactory(self, url, auth_token, job_id):
        imp = MyMiniFactoryImporter(job_id)
        return imp.process_url(url, auth_token)

    def handle_wikifactory(self, url, auth_token, job_id):
        imp = WikifactoryImporter(job_id)
        return imp.process_url(url, auth_token)
