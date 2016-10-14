import os

import jinja2

import markdown

import datetime


class PageError(Exception):
    def __init__(self, message):
        super().__init__(self, message)


class Page:
    def __init__(self, title, file_name, sub_pages=None):
        self.title = title
        self.file_name = file_name
        if sub_pages is None:
            sub_pages = []

        for sub_page in sub_pages:
            if type(sub_page) is not SubPage:
                raise PageError(
                    'All elements of submenu have to be of type '
                    'zorn.Elements.SubPage'
                )

        self.sub_pages = sub_pages

    def __str__(self):
        return self.title

    @staticmethod
    def render_html(context=None):
        if context is None:
            context = {}

        env = jinja2.Environment()
        env.loader = jinja2.FileSystemLoader(
            os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'templates'))
        template = env.get_template(
            os.path.join('structure.html'))
        return template.render(context)


class SubPage(Page):
    """A helper class to avoid attempts of creation of sub-sub pages"""

    def __init__(self, title, file_name):
        super().__init__(title, file_name, [])


class Website:
    def __init__(self, settings):
        self.root_dir = settings['root_dir']
        self.markdown_dir = settings['markdown_dir']
        self.description = settings['description']
        self.title = settings['site_title']
        self.subtitle = settings['site_subtitle']
        self.project_name = settings['project_name']
        self.author = settings['author']
        self.description = settings['description']
        self.keywords = settings['keywords']

        all_pages = []
        for page in settings['pages']:
            all_pages.append(page)
            if len(page.sub_pages) > 0:
                all_pages.extend(page.sub_pages)
        self.pages = all_pages

    def generate_pages(self):
        for page in self.pages:

            with open(os.path.join(self.markdown_dir,
                                   '{0}.md'.format(page.file_name))) as f:
                body_content = f.read()
                body_content = markdown.markdown(body_content)

            footer_content = '&copy; {0} {1}'.format(
                datetime.datetime.now().year, self.author)

            html = self.pages[0].render_html({
                'site_description': self.description,
                'site_author': self.author,
                'site_keywords': self.keywords,
                'site_title': self.title,
                'site_sub_title': self.subtitle,
                'page_title': page.title,
                'body_content': body_content,
                'footer_content' : footer_content,
            })
            with open(os.path.join(self.root_dir,
                                   '{0}.html'.format(page.file_name)),
                      'w') as f:
                f.write(html)
