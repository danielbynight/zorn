import os

from zorn.tasks import process_admin_request

if __name__ == '__main__':
    os.environ.setdefault(
        'ZORN_SETTINGS_PATH',
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.py')
    )
    process_admin_request()
