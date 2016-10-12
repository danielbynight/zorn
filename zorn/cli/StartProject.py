import os


class NewProject:
    def __init__(self, project_name, project_dir):
        self.project_name = project_name
        self.project_dir = project_dir

    def create_dir(self):
        # Raises FileExistsError in case the directory already exists
        os.mkdir(self.project_dir)
