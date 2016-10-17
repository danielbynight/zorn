import os

import sys

from zorn.cli import process_request

if __name__ == '__main__':
    os.environ.setdefault('ZORN_SETTINGS', 'settings')
    os.environ.setdefault(
        'ZORN_SETTINGS_PATH',
        os.path.join(os.path.dirname(os.path.abspath(__file__)),'settings.py')
    )
    process_request(sys.argv)