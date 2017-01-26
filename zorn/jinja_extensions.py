from jinja2 import lexer, nodes
from jinja2.ext import Extension


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
        token = parser.stream.expect(lexer.TOKEN_STRING)
        path = nodes.Const(token.value)
        call = self.call_method('_get_url', [path], lineno=lineno)

        return nodes.Output([call], lineno=lineno)

    def _get_url(self, path):
        the_page = None
        for page in self.environment.zorn_settings.pages:
            if page.file_name == path:
                the_page = page
        url = the_page.get_relative_path(
            self.environment.zorn_page,
            self.environment.zorn_settings.url_style,
            self.environment.zorn_settings.debug,
        )
        return '/' + path + self.environment.zorn_settings.root_dir
