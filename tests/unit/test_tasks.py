import os
import shutil
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


def test_create_with_defaults():
    create_task = tasks.Create()
    assert create_task.project_name is None
    assert create_task.site_title is None
    assert create_task.author is None
    assert create_task.style is None
    assert create_task.generate is False
    assert create_task.cwd == os.getcwd()
    assert create_task.root_dir is None


def test_create_with_no_defaults():
    create_task = tasks.Create(
        project_name='test_project_name',
        site_title='test_site_title',
        author='Mrs. Test',
        style='basic',
        generate=True,
        verbosity=0,
    )
    assert create_task.project_name == 'test_project_name'
    assert create_task.site_title == 'test_site_title'
    assert create_task.author == 'Mrs. Test'
    assert create_task.style == 'basic'
    assert create_task.generate is True


def test_create_raise_error_if_style_is_not_recognized():
    with pytest.raises(tasks.UnknownStyleError):
        tasks.Create(style='blah')


def test_create_and_run_no_defaults():
    create_task = tasks.Create(
        project_name='test_project_name',
        site_title='test_site_title',
        author='Mrs. Test',
        style='basic',
        verbosity=0,
    )
    create_task.run()
    project_path = os.path.join(os.getcwd(), 'test_project_name')
    assert os.path.exists(project_path)
    assert os.path.exists(os.path.join(project_path, 'admin.py'))
    assert os.path.exists(os.path.join(project_path, 'settings.py'))
    assert os.path.exists(os.path.join(project_path, 'gulpfile.js'))
    assert os.path.exists(os.path.join(project_path, 'package.json'))
    assert os.path.exists(os.path.join(project_path, 'md', 'index.md'))
    assert os.path.exists(os.path.join(project_path, 'scss', 'main.scss'))
    assert os.path.exists(os.path.join(project_path, 'scss', '_settings.scss'))
    assert os.path.exists(os.path.join(project_path, 'scss', '_nav.scss'))
    shutil.rmtree(project_path)


def test_create_and_run_only_project_name():
    create_task = tasks.Create(
        project_name='test_project_name',
        verbosity=0,
    )
    create_task.run()
    project_path = os.path.join(os.getcwd(), 'test_project_name')
    assert os.path.exists(project_path)
    assert os.path.exists(os.path.join(project_path, 'admin.py'))
    assert os.path.exists(os.path.join(project_path, 'settings.py'))
    assert os.path.exists(os.path.join(project_path, 'gulpfile.js'))
    assert os.path.exists(os.path.join(project_path, 'package.json'))
    assert os.path.exists(os.path.join(project_path, 'md', 'index.md'))
    assert os.path.exists(os.path.join(project_path, 'scss', 'main.scss'))
    assert os.path.exists(os.path.join(project_path, 'scss', '_settings.scss'))
    assert os.path.exists(os.path.join(project_path, 'scss', '_nav.scss'))
    shutil.rmtree(project_path)


def test_generate():
    example_project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'example_project')
    assert not os.path.exists(os.path.join(example_project_path, 'index.html'))
    os.environ['ZORN_SETTINGS_PATH'] = os.path.join(example_project_path, 'settings.py')
    tasks.Generate().run()
    assert os.path.exists(os.path.join(example_project_path, 'index.html'))
    os.remove(os.path.join(example_project_path, 'index.html'))
