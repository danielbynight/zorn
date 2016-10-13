import os
import pytest
from zorn.cli.StartProject import NewProject

class TestStartProject:
    def test_create_dir(self):
        new_project = NewProject('test', 'testdir')
        new_project.create_dir()
        assert os.path.exists('testdir') == True

    def raise_error_if_dir_exists(self):
        new_project = NewProject('test', 'testdir')
        with pytest.raises(FileExistsError):
            new_project.create_dir()