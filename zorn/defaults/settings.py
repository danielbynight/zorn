from zorn import elements
import os

DEBUG = True

# General

PROJECT_NAME = '{{ project_name }}'
SITE_TITLE = '{{ site_title }}'
AUTHOR = '{{ author }}'

# Directories

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Navigation

PAGES = [
    elements.Page('Home', 'index'),
]
