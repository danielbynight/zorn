import os
from zorn import cli
from shutil import rmtree


def test_project_is_created():
    cli.process_request(['zorn', 'create', 'example'])
    assert os.path.exists(os.path.join(os.getcwd(), 'example', 'settings.py')) is True
    assert os.path.exists(os.path.join(os.getcwd(), 'example', 'admin.py')) is True
    assert os.path.exists(os.path.join(os.getcwd(), 'example', 'gulpfile.js')) is True
    assert os.path.exists(os.path.join(os.getcwd(), 'example', 'package.json')) is True
    assert os.path.exists(os.path.join(os.getcwd(), 'example', 'md', 'index.md')) is True
    assert os.path.exists(os.path.join(os.getcwd(), 'example', 'scss', 'main.scss')) is True
    rmtree(os.path.join(os.getcwd(), 'example'))
