import os
import shutil


def test_create_and_generate_default():
    os.system('python zorn/bin/zorn -sn test_project')
    project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'test_project')
    assert os.path.exists(os.path.join(project_path, 'admin.py'))
    assert os.path.exists(os.path.join(project_path, 'settings.py'))
    assert os.path.exists(os.path.join(project_path, 'gulpfile.js'))
    assert os.path.exists(os.path.join(project_path, 'package.json'))
    assert os.path.exists(os.path.join(project_path, 'md', 'index.md'))
    assert os.path.exists(os.path.join(project_path, 'scss', 'main.scss'))
    assert os.path.exists(os.path.join(project_path, 'scss', '_settings.scss'))
    assert os.path.exists(os.path.join(project_path, 'scss', '_nav.scss'))
    os.system('cd test_project && python3 admin.py generate')
    assert os.path.exists(os.path.join(project_path, 'index.html'))
    shutil.rmtree(project_path)
