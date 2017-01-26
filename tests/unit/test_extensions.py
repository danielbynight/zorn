import os

import jinja2

from zorn.elements import Page, ZornSettings
from zorn.jinja_extensions import Url


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
