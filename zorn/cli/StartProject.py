import os


class DirectoryExistsError(Exception):
    pass


class NewProject:
    def __init__(self, project_name, project_dir):
        self.project_name = project_name
        self.project_dir = project_dir

    def create_dir(self):
        if os.path.exists(self.project_dir):
            raise DirectoryExistsError('A directory already exists with that name.')
        os.mkdir(self.project_dir)
