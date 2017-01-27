from jinja2 import nodes
from jinja2.ext import Extension

from zorn.errors import PageNotFound


class ZornJinjaExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.extend(
            zorn_settings=None,
            zorn_page=None,
        )


class Url(ZornJinjaExtension):
    tags = {'url'}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        return nodes.Output([
            nodes.MarkSafeIfAutoescape(self.call_method('_get_url', args))
        ]).set_lineno(lineno)

    def _get_url(self, filename):
        the_page = None
        for page in self.environment.zorn_settings.pages:
            if page.file_name == filename:
                the_page = page
        if the_page is None:
            raise PageNotFound('The page with file name {0} was not found for this website.'.format(filename))
        return the_page.get_relative_path(
            self.environment.zorn_page,
            self.environment.zorn_settings.url_style,
            self.environment.zorn_settings.debug,
        )
