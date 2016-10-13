from zorn.Page import Page
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
    Page('Home', 'index'),
    Page('Documentation', 'doc', [
        Page('Getting Started', 'getting_started'),
        Page('CLI', 'cli'),
        Page('Templates', 'templates'),
    ]),
    Page('Contact', 'contact'),
]
