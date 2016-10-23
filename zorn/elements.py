import datetime
import os

import jinja2
import markdown

from zorn import errors


class Page:
    def __init__(self, title, file_name, sub_pages=None):
        self.title = title
        self.file_name = file_name
        if sub_pages is None:
            sub_pages = []

        for sub_page in sub_pages:
            if type(sub_page) is not SubPage:
                raise errors.PageError('All elements of submenu have to be of type zorn.Elements.SubPage')

        self.sub_pages = sub_pages
        self.body_content = None

    def generate_content_menu(self, url_style):
        content = '#' + self.title + '\n'
        for sub_page in self.sub_pages:
            url = './{0}/{1}.html'.format(self.file_name, sub_page.file_name) \
                if url_style == 'nested' \
                else './{0}.html'.format(sub_page.file_name)
            content += '- [{0}]({1})\n'.format(sub_page.title, url)
        return content

    def __str__(self):
        return self.title

    def set_content_from_md(self, markdown_dir, markdown_extensions=None, url_style='flat'):
        markdown_extensions = [] if markdown_extensions == None else markdown_extensions
        if os.path.isfile(os.path.join(markdown_dir, '{0}.md'.format(self.file_name))):
            with open(os.path.join(markdown_dir, '{0}.md'.format(self.file_name))) as f:
                body_content = f.read()
                body_content = markdown.markdown(
                    body_content,
                    extensions=markdown_extensions
                )
        elif type(self) is Page and self.sub_pages != []:
            # Create menu-page in case no content was set for this page
            body_content = markdown.markdown(
                self.generate_content_menu(url_style),
                extensions=markdown_extensions
            )
        else:
            body_content = ''
        self.body_content = body_content

    @staticmethod
    def render_html(context, templates_dir):
        env = jinja2.Environment()
        env.loader = jinja2.FileSystemLoader(templates_dir)
        template = env.get_template(os.path.join('structure.html'))
        return template.render(context)


class SubPage(Page):
    """A helper class to avoid attempts of creation of sub-sub pages"""

    def __init__(self, title, file_name):
        super().__init__(title, file_name, [])


class UnlinkedPage(Page):
    def __init__(self, title, file_name, path=None):
        super().__init__(title, file_name, [])
        if path is None:
            path = []
        elif type(path) == str:
            path = path.split('/')
        self.path = path


class Website:
    def __init__(self, settings):

        settings_keys = settings.keys()

        # Non-optional settings
        if 'root_dir' not in settings_keys:
            raise errors.SettingNotFoundError('ROOT_DIR has to be set in the settings module.')
        self.root_dir = settings['root_dir']

        if 'project_name' not in settings_keys:
            raise errors.SettingNotFoundError('PROJECT_NAME has to be set in the settings module.')
        self.project_name = settings['project_name']

        # Optional settings
        self.debug = settings['debug'] if 'debug' in settings_keys else False

        self.url_style = settings['url_style'] if 'url_style' in settings_keys else 'flat'

        self.templates_dir = settings['templates_dir'] if 'templates_dir' in settings_keys \
            else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

        self.markdown_dir = settings['markdown_dir'] if 'markdown_dir' in settings_keys \
            else os.path.join(self.root_dir, 'md')

        self.markdown_extensions = settings['markdown_extensions'] if 'markdown_extensions' in settings_keys \
            else []

        self.site_dir = settings['site_dir'] if 'site_dir' in settings \
            else self.root_dir

        self.title = settings['site_title'] if 'site_title' in settings_keys \
            else self.project_name

        self.subtitle = settings['site_subtitle'] if 'site_subtitle' in settings_keys \
            else ''

        self.description = settings['description'] if 'description' in settings_keys \
            else ''

        self.author = settings['author'] if 'author' in settings_keys \
            else ''

        self.keywords = settings['keywords'] if 'keywords' in settings_keys \
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

            # get parent page in case of sub page
            parent_page = ''
            if type(page) is SubPage:
                parent_page = [parent_page for parent_page in self.pages if page in parent_page.sub_pages].pop()

            page.set_content_from_md(self.markdown_dir, self.markdown_extensions, self.url_style)
            body_content = page.body_content

            # list of links which should have class "active" in nav bar
            active_nav_links = [page.title]
            if type(page) is SubPage:
                # if the page in question is a subpage then activate parent too
                active_nav_links.append(parent_page.title)

            # generate css path

            css_file = 'main.css' if self.debug is True else 'main.min.css'
            css_path = './' + css_file
            if type(page) is SubPage and self.url_style == 'nested':
                css_path = '../' + css_file
            elif type(page) is UnlinkedPage:
                css_path = ''.join(['../' for _ in range(len(page.path))]) + css_file

            back_path = ''.join(['../' for _ in range(len(page.path))]) if type(page) is UnlinkedPage else '../'

            pages = [page for page in self.pages if type(page) is Page]

            html = self.pages[0].render_html({
                'debug': self.debug,
                'site_description': self.description,
                'site_author': self.author,
                'site_keywords': self.keywords,
                'site_title': self.title,
                'site_subtitle': self.subtitle.replace(' ', '&nbsp;'),
                'page_title': page.title,
                'back_path': back_path,
                'page_type': type(page).__name__,
                'body_content': body_content,
                'current_year': datetime.datetime.now().year,
                'pages': pages,
                'active_nav_links': active_nav_links,
                'url_style': self.url_style,
                'css_path': css_path,
            }, self.templates_dir)

            if type(page) is UnlinkedPage:
                final_dir = self.site_dir
                for partial in page.path:
                    if not os.path.exists(os.path.join(final_dir, partial)):
                        os.mkdir(os.path.join(final_dir, partial))
                    final_dir = os.path.join(final_dir, partial)
                page_path = os.path.join(final_dir, '{0}.html'.format(page.file_name))
                with open(page_path, 'w+') as f:
                    f.write(html)
            elif self.url_style == 'flat' or type(page) is Page:
                page_path = os.path.join(self.site_dir, '{0}.html'.format(page.file_name))
                with open(page_path, 'w+') as f:
                    f.write(html)
            elif type(page) is SubPage:
                page_dir_path = os.path.join(self.site_dir, parent_page.file_name)
                if not os.path.exists(page_dir_path):
                    os.mkdir(page_dir_path)
                page_path = os.path.join(page_dir_path, '{0}.html'.format(page.file_name))
                with open(page_path, 'w+') as f:
                    f.write(html)
