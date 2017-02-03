import os

from zorn import elements

DEBUG = True

# General

PROJECT_NAME = 'docs'
SITE_TITLE = 'Zorn'
SITE_SUBTITLE = 'A static site generator'
AUTHOR = 'danielmatiasferrer'

# Directories

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Navigation

URL_STYLE = 'nested'

PAGES = [
    elements.Page('Home', 'index'),
    elements.Page('Documentation', 'documentation', [
        elements.SubPage('Command line', 'cli'),
        elements.SubPage('Routing', 'routing'),
        elements.SubPage('Project structure', 'structure'),
        elements.SubPage('Style', 'style'),
        elements.SubPage('Automation', 'automation')
    ])
]
