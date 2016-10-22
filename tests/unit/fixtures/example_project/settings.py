import os

from zorn import elements

DEBUG = True

# General

PROJECT_NAME = 'example_project'
SITE_TITLE = 'Example project'
AUTHOR = 'Mrs. Test'

# Directories

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Navigation

PAGES = [
    elements.Page('Home', 'index'),
]
