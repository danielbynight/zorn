import os
from jinja2 import nodes
from jinja2.ext import Extension
from markdown import markdown


class JinjaExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.extend(settings=None, page=None)


class ReplacementTag(JinjaExtension):
    tags = {'tag'}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        return nodes.Output([
            nodes.MarkSafeIfAutoescape(self.call_method('_get_replacement', args))
        ]).set_lineno(lineno)

    def _get_replacement(self, index):
        return index


class Static(ReplacementTag):
    tags = {'static'}

    def _get_replacement(self, filename):
        return './' + filename if self.environment.settings.DEVELOPMENT is True else '/' + filename


class Url(ReplacementTag):
    tags = {'url'}

    def _get_replacement(self, page_name):
        the_page = None
        for page in self.environment.settings.PAGES:
            if page.name == page_name:
                the_page = page
                break

        if the_page is None:
            return page_name

        if self.environment.settings.DEVELOPMENT is True:
            route_to_root = ''
            if self.environment.page.route != '':
                route_to_root = ''.join(['../' for _ in self.environment.page.route.split('/')])

            if route_to_root == '':
                route_to_root = './'

            partial_route = route_to_root + the_page.route

            if not partial_route.endswith('/'):
                partial_route += '/'

            return partial_route + the_page.file_name
        else:
            route = '/' + the_page.route
            if the_page.file_name != 'index.html':
                route += the_page.file_name

            if route.endswith('.html'):
                route = route[:-5]
            return route


class Markdown(ReplacementTag):
    tags = {'markdown'}

    def _get_replacement(self, filename):
        with open(os.path.join(self.environment.settings.TEMPLATES_DIR, filename)) as f:
            content = f.read()
        return markdown(content)
