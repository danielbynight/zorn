from zorn import elements
import os

# General

PROJECT_NAME = 'example'
SITE_TITLE = 'Zorn'
SITE_SUBTITLE = 'Getting Started'
AUTHOR = 'Daniel Matias Ferrer'
DESCRIPTION = 'A static website generator'
KEYWORDS = 'static generator website'

# Directories

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MARKDOWN_DIR = os.path.join(ROOT_DIR, 'md')

# Navigation

PAGES = [
    elements.Page('Home', 'index', [
        elements.SubPage('Example', 'example')
    ]),
    elements.Page('Documentation', 'doc', [
        elements.SubPage('Getting Started', 'getting_started'),
        elements.SubPage('CLI', 'cli'),
        elements.SubPage('Templates', 'templates'),
    ]),
    elements.Page('Contact', 'contact'),
]
