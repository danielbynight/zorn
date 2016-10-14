import os

import sys

from zorn.cli import process_request

if __name__ == '__main__':
    os.environ.setdefault('ZORN_SETTINGS', 'example.settings')
    process_request(sys.argv)
