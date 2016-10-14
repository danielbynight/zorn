import os

import jinja2

import markdown

import datetime


class PageError(Exception):
    pass


class SettingNotFoundError(Exception):
    pass


class Page:
    type = 'main'

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
    type = 'sub_page'

    def __init__(self, title, file_name):
        super().__init__(title, file_name, [])


class Website:
    def __init__(self, settings):

        settings_keys = settings.keys()

        # Non-optional settings
        if 'root_dir' not in settings_keys:
            module_name = os.environ['ZORN_SETTINGS']
            raise SettingNotFoundError(
                'ROOT_DIR has to be set in the settings module ({0}).'.
                format(module_name)
            )
        self.root_dir = settings['root_dir']

        if 'project_name' not in settings_keys:
            module_name = os.environ['ZORN_SETTINGS']
            raise SettingNotFoundError(
                'PROJECT_NAME has to be set in the settings module ({0}).'.
                format(module_name)
            )
        self.project_name = settings['project_name']

        # Optional settings
        self.debug = settings['debug'] if 'debug' in settings_keys else False

        self.markdown_dir = settings['markdown_dir'] \
            if 'markdown_dir' in settings_keys \
            else os.path.join(self.root_dir, 'md')

        self.title = settings['site_title'] \
            if 'site_title' in settings_keys \
            else self.project_name

        self.subtitle = settings['site_subtitle'] \
            if 'site.subtitle' in settings_keys \
            else ''

        self.description = settings['description'] \
            if 'description' in settings_keys \
            else ''

        self.author = settings['author'] \
            if 'author' in settings_keys \
            else ''

        self.keywords = settings['keywords'] \
            if 'keywords' in settings_keys \
            else ''

        all_pages = []
        if 'pages' in settings_keys:
            for page in settings['pages']:
                all_pages.append(page)
                if len(page.sub_pages) > 0:
                    all_pages.extend(page.sub_pages)
        self.pages = all_pages

    def generate_pages(self):
        for page in self.pages:

            if os.path.isfile(os.path.join(self.markdown_dir,
                                           '{0}.md'.format(page.file_name))):
                with open(os.path.join(self.markdown_dir,
                                       '{0}.md'.format(page.file_name))) as f:
                    body_content = f.read()
                    body_content = markdown.markdown(body_content)
            else:
                body_content = ''

            footer_content = '&copy; {0} {1}'.format(
                datetime.datetime.now().year, self.author)

            # list of links which should have class "active" in nav bar
            active_nav_links = [page.title]
            if type(page) is SubPage:
                # if the page in question is a subpage then activate parent too
                active_nav_links.extend(
                    [parent_page.title for parent_page in self.pages if
                     page in parent_page.sub_pages]
                )

            html = self.pages[0].render_html({
                'debug': self.debug,
                'site_description': self.description,
                'site_author': self.author,
                'site_keywords': self.keywords,
                'site_title': self.title,
                'site_sub_title': self.subtitle,
                'page_title': page.title,
                'body_content': body_content,
                'footer_content': footer_content,
                'pages': [page for page in self.pages if page.type == 'main'],
                'active_nav_links': active_nav_links,
            })
            with open(os.path.join(self.root_dir,
                                   '{0}.html'.format(page.file_name)),
                      'w') as f:
                f.write(html)
