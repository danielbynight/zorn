import unittest
from zorn.cli import StartProject
import os


class TestStartProject(unittest.TestCase):
    def setUp(self):
        self.new_project = StartProject.NewProject(
            'test',
            (os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test'))
        )

    def test_create_dir(self):
        # Creates the directory
        self.new_project.create_dir()
        self.assertTrue(os.path.exists(self.new_project.project_dir))

    def test_raise_error_when_creating_existing_dir(self):
        with self.assertRaises(FileExistsError):
            self.new_project.create_dir()
            self.new_project.create_dir()


    def tearDown(self):
        if os.path.exists(self.new_project.project_dir):
            os.rmdir(self.new_project.project_dir)


if __name__ == '__main__':
    unittest.main()
