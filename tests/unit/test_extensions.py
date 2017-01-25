import os

import jinja2

from zorn.jinja_extensions import Url


def test_url():
    env = jinja2.Environment(extensions=[Url])
    env.loader = jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
    )
    template = env.get_template('url.html')
    html = template.render()
    assert html == 'This is a url: /path'
