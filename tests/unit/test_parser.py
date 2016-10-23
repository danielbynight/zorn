import os
import shutil
from zorn import parser


def test_process_creation_request():
    current_dir = os.getcwd()
    parser.process_creation_request(['--silent', '--name', 'test_create_project'])
    new_project_path = os.path.join(current_dir, 'test_create_project')
    assert os.path.exists(new_project_path)
    shutil.rmtree(new_project_path)


def test_process_admin_request():
    original_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'example_project')
    current_dir = os.getcwd()
    shutil.copy(os.path.join(original_file_path, 'admin.py'), os.path.join(current_dir, 'admin.py'))
    os.environ['ZORN_SETTINGS_PATH'] = os.path.join(original_file_path, 'settings.py')
    parser.process_admin_request(['generate'])
    assert os.path.exists(os.path.join(original_file_path, 'index.html'))
    os.remove(os.path.join(current_dir, 'admin.py'))
    os.remove(os.path.join(original_file_path, 'index.html'))

def test_parser_set_task_to_verbose():
    parser_ = parser.Parser(['--verbose'])
    parser_.add_arguments()
    parser_.parse_arguments()
    assert parser_.task_arguments['verbosity'] == 2
