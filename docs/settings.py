import os

from zorn import elements

DEBUG = True

# General

PROJECT_NAME = 'docs'
SITE_TITLE = 'Zorn'
AUTHOR = 'Daniel Matias Ferrer'

# Directories

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Navigation

PAGES = [
    elements.Page('Home', 'index'),
]
