from zorn import Elements
import os

# General

SITE_TITLE = 'Zorn - Getting Started'
AUTHOR = 'Daniel Matias Ferrer'
DESCRIPTION = 'A static website generator'
KEYWORDS = 'static generator website'

# Directories

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(ROOT_DIR, 'templates')
MARKDOWN_DIR = os.path.join(ROOT_DIR, 'md')


# Navigation

PAGES = [
    Elements.Page('Home', 'index'),
    Elements.Page('Documentation', 'doc', [
        Elements.SubPage('Getting Started', 'getting_started'),
        Elements.SubPage('CLI', 'cli'),
        Elements.SubPage('Templates', 'templates'),
    ]),
    Elements.Page('Contact', 'contact'),
]
