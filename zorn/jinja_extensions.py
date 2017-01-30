from jinja2 import nodes
from jinja2.ext import Extension

from zorn.errors import PathNotFound


class ZornJinjaExtension(Extension):
    def __init__(self, environment):
        """A base extension for a zorn project

        Extend Jinja's Extension and extends the environment to acomodate the settings for the current Zorn project
        and the current page object (the page to be rendered).
        """
        super().__init__(environment)
        environment.extend(
            zorn_settings=None,
            zorn_page=None,
        )


class ZornReplacementTag(ZornJinjaExtension):
    tags = {'tag'}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        return nodes.Output([
            nodes.MarkSafeIfAutoescape(self.call_method('_get_replacement', args))
        ]).set_lineno(lineno)

    def _get_replacement(self, index):
        """Replaces the string index by the appropriate string

        :param index:
        :returns: the string to be printed to the page
        :rtype: str
        """
        return index


class Url(ZornReplacementTag):
    tags = {'url'}

    def _get_replacement(self, filename):
        """Take the filename of a page and return the path to that page

        :param filename:
        :returns: path to page
        :rtype: str
        """
        the_page = None
        for page in self.environment.zorn_settings.pages:
            if page.file_name == filename:
                the_page = page
        if the_page is None:
            raise PathNotFound('The page with file name "{0}" was not found for this website.'.format(filename))
        return the_page.get_relative_path(
            self.environment.zorn_page,
            self.environment.zorn_settings.url_style,
            self.environment.zorn_settings.debug,
        )


class Static(ZornReplacementTag):
    tags = {'static'}

    def _get_replacement(self, filename):
        """Take the filename of a static file and return the path to that file

        :param filename:
        :returns: path to page
        :rtype: str
        """
        return self.environment.zorn_page.get_path_to_root(
            self.environment.zorn_settings.debug,
            self.environment.zorn_settings.url_style
        ) + self.environment.zorn_settings.static_dir + '/' + filename
