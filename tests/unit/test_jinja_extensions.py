import os

import jinja2
import pytest

from zorn.elements import Page, ZornSettings
from zorn.errors import PageNotFound
from zorn.jinja_extensions import Url, Static


def test_url():
    env = jinja2.Environment(extensions=[Url])
    test_page_from = Page('test_page1', 'test_page1')
    test_page_to = Page('test_page2', 'test_page2')
    env.zorn_settings = ZornSettings({
        'root_dir': '',
        'project_name': 'test',
        'pages': [test_page_from, test_page_to],
    })
    env.zorn_page = test_page_from
    env.loader = jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
    )
    template = env.get_template('url.html')
    html = template.render()
    assert html == 'This is a url: /test_page2'


def test_page_not_found_with_unexistent_filename():
    with pytest.raises(PageNotFound):
        env = jinja2.Environment(extensions=[Url])
        test_page_from = Page('test_page1', 'test_page1')
        test_page_to = Page('test_page3', 'test_page3')
        env.zorn_settings = ZornSettings({
            'root_dir': '',
            'project_name': 'test',
            'pages': [test_page_from, test_page_to],
        })
        env.zorn_page = test_page_from
        env.loader = jinja2.FileSystemLoader(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
        )
        template = env.get_template('url.html')
        template.render()


def test_static():
    env = jinja2.Environment(extensions=[Static])
    test_page = Page('test_page1', 'test_page1')
    env.zorn_settings = ZornSettings({
        'root_dir': '',
        'project_name': 'test',
        'pages': [test_page],
    })
    env.zorn_page = test_page
    env.loader = jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
    )
    template = env.get_template('static.html')
    html = template.render()
    assert html == 'This is a static file: /something.html'
