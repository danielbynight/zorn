import os
import shutil
import sys
from io import StringIO

import pytest

from zorn import errors, tasks


def test_task():
    task = tasks.Task()
    assert task.verbosity == 1


def test_task_run():
    task = tasks.Task()
    with StringIO() as stream:
        sys.stdout = stream
        task.run()
        assert 'Welcome to zorn!' in stream.getvalue()


def test_comunicate_standard_verbosity():
    task = tasks.Task(verbosity=1)
    with StringIO() as stream:
        sys.stdout = stream
        task.communicate('standard')
        task.communicate('verbose', False)
        assert stream.getvalue() == 'standard\n'


def test_comunicate_silent():
    task = tasks.Task(verbosity=0)
    with StringIO() as stream:
        sys.stdout = stream
        task.communicate('standard')
        task.communicate('verbose', False)
        assert stream.getvalue() == ''


def test_comunicate_verbose():
    task = tasks.Task(verbosity=2)
    with StringIO() as stream:
        sys.stdout = stream
        task.communicate('standard')
        task.communicate('verbose', False)
        assert stream.getvalue() == 'standard\nverbose\n'


def test_admin_task():
    os.environ['ZORN_SETTINGS_PATH'] = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project', 'settings.py'
    )
    task = tasks.AdminTask(verbosity=1, update=True)
    assert task.verbosity == 1
    assert task.update is True
    assert task.settings == {'root_dir': 'test', 'other_setting': 'test test'}


def test_process_settings():
    os.environ['ZORN_SETTINGS_PATH'] = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project', 'settings.py'
    )
    assert tasks.AdminTask.process_settings() == {'root_dir': 'test', 'other_setting': 'test test'}


def test_update_new_setting():
    settings_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'example_project', 'settings.py'
    )
    os.environ['ZORN_SETTINGS_PATH'] = settings_file_path
    with open(settings_file_path, 'r') as f:
        original_settings = f.read()
    task = tasks.AdminTask(verbosity=1, update=True)
    task.update_settings('test_setting', "'a test value'")
    with open(settings_file_path, 'r') as f:
        modified_settings = f.read()
    with open(settings_file_path, 'w+') as f:
        f.write(original_settings)
    assert "TEST_SETTING = 'a test value'" in modified_settings


def test_update_existing_setting():
    settings_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'example_project', 'settings.py'
    )
    os.environ['ZORN_SETTINGS_PATH'] = settings_file_path
    with open(settings_file_path, 'r') as f:
        original_settings = f.read()
    task = tasks.AdminTask(verbosity=1, update=True)
    task.update_settings('project_name', "'a whole new project name'")
    with open(settings_file_path, 'r') as f:
        modified_settings = f.read()
    with open(settings_file_path, 'w+') as f:
        f.write(original_settings)
    print(modified_settings)
    assert "PROJECT_NAME = 'a whole new project name'" in modified_settings
    assert "PROJECT_NAME = 'example_project'" not in modified_settings


def test_raise_error_if_no_zorn_setting_path():
    del os.environ['ZORN_SETTINGS_PATH']
    with pytest.raises(errors.NotAZornProjectError):
        tasks.AdminTask.process_settings()


def test_raise_error_if_no_root_dir_setting():
    os.environ.setdefault(
        'ZORN_SETTINGS_PATH',
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project', 'wrong_settings.py')
    )
    with pytest.raises(errors.SettingNotFoundError):
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
    with pytest.raises(errors.UnknownStyleError):
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


def test_generate_with_wrong_settings():
    example_project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'test_project')
    os.environ['ZORN_SETTINGS_PATH'] = os.path.join(example_project_path, 'wrong_settings.py')
    with pytest.raises(errors.SettingNotFoundError):
        tasks.Generate().run()


def test_import_templates():
    example_project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'example_project')
    assert not os.path.exists(os.path.join(example_project_path, 'templates'))
    os.environ['ZORN_SETTINGS_PATH'] = os.path.join(example_project_path, 'settings.py')
    tasks.ImportTemplates().run()
    assert os.path.exists(os.path.join(example_project_path, 'templates'))
    shutil.rmtree(os.path.join(example_project_path, 'templates'))


def test_import_style():
    example_project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'example_project')
    assert not os.path.exists(os.path.join(example_project_path, 'soprano'))
    os.environ['ZORN_SETTINGS_PATH'] = os.path.join(example_project_path, 'settings.py')
    import_task = tasks.ImportStyle(task_args=['soprano'])
    assert import_task.style == 'soprano'
    import_task.run()
    assert os.path.exists(os.path.join(example_project_path, 'soprano'))
    shutil.rmtree(os.path.join(example_project_path, 'soprano'))


def test_import_wrong_style():
    with pytest.raises(errors.UnknownStyleError):
        tasks.ImportStyle(task_args=['basics'])
