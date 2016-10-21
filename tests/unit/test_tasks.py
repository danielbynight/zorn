import os
import sys

import pytest
from zorn import tasks, elements
from io import StringIO


def test_task():
    task = tasks.Task()
    assert task.verbosity == 1


def test_parse_verbosity_standard():
    silent = False
    verbose = False
    verbosity = tasks.Task.parse_verbosity(verbose, silent)
    assert verbosity == 1


def test_parse_verbosity_silent():
    silent = True
    verbose = False
    verbosity = tasks.Task.parse_verbosity(verbose, silent)
    assert verbosity == 0
    silent = True
    verbose = True
    verbosity = tasks.Task.parse_verbosity(verbose, silent)
    assert verbosity == 0


def test_parse_verbosity_verbose():
    silent = False
    verbose = True
    verbosity = tasks.Task.parse_verbosity(verbose, silent)
    assert verbosity == 2


def test_comunicate_standard_verbosity():
    task = tasks.Task(1)
    with StringIO() as stream:
        sys.stdout = stream
        task.communicate('standard')
        task.communicate('verbose', False)
        assert stream.getvalue() == 'standard\n'


def test_comunicate_silent():
    task = tasks.Task(0)
    with StringIO() as stream:
        sys.stdout = stream
        task.communicate('standard')
        task.communicate('verbose', False)
        assert stream.getvalue() == ''


def test_comunicate_verbose():
    task = tasks.Task(2)
    with StringIO() as stream:
        sys.stdout = stream
        task.communicate('standard')
        task.communicate('verbose', False)
        assert stream.getvalue() == 'standard\nverbose\n'


def test_admin_task():
    task = tasks.AdminTask(1, True)
    assert task.verbosity == 1
    assert task.update is True


def test_process_settings():
    os.environ.setdefault(
        'ZORN_SETTINGS_PATH',
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project', 'settings.py')
    )
    processed_settings = tasks.AdminTask.process_settings()
    assert processed_settings == {'root_dir': 'test', 'other_setting': 'test test'}


def test_raise_error_if_no_zorn_setting_path():
    del os.environ['ZORN_SETTINGS_PATH']
    with pytest.raises(tasks.NotAZornProjectError):
        tasks.AdminTask.process_settings()


def test_raise_error_if_no_root_dir_setting():
    os.environ.setdefault(
        'ZORN_SETTINGS_PATH',
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project', 'wrong_settings.py')
    )
    with pytest.raises(elements.SettingNotFoundError):
        tasks.AdminTask.process_settings()


