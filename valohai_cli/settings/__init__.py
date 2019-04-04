from valohai_cli.utils import walk_directory_parents
from .paths import get_settings_file_name
from .persistence import FilePersistence


class Settings:
    # Non-persistent settings and their defaults:
    table_format = 'human'

    def __init__(self, persistence=None):
        """

        :param persistence:
        """
        if not persistence:
            persistence = FilePersistence(get_filename=lambda: get_settings_file_name('config.json'))

        self.persistence = persistence
        self.overrides = {}

    def _get(self, key, default=None):
        if key in self.overrides:
            return self.overrides[key]
        return self.persistence.get(key, default)

    @property
    def user(self):
        """
        The logged in user (dictionary or None).
        :rtype: dict|None
        """
        return self._get('user')

    @property
    def host(self):
        """
        The host we're logged in to (string or None if not logged in).
        :return:
        """
        return self._get('host')

    @property
    def token(self):
        """
        The authentication token we have for the host we're logged in to.
        """
        return self._get('token')

    @property
    def links(self):
        """
        Dictionary of directory <-> project object dicts.
        """
        return self._get('links', {})

    def get_project(self, directory):
        """
        Get the Valohai project object for a directory context.

        The directory tree is walked upwards to find an actual linked directory.

        :param dir: Directory
        :return: Project object, or None.
        :rtype: valohai_cli.models.project.Project|None
        """
        links = self.links
        if not links:
            return None
        for directory in walk_directory_parents(directory):
            project_obj = links.get(directory)
            if project_obj:
                from valohai_cli.models.project import Project
                return Project(data=project_obj, directory=directory)

    def set_project_link(self, directory, project):
        links = self.links.copy()
        links[directory] = project
        self.persistence.set('links', links)
        assert self.get_project(directory).id == project['id']
        self.persistence.save()


settings = Settings()
