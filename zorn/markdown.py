import re

import markdown

from zorn import errors


class MarkdownParser:
    def __init__(self, page, all_pages, url_style='flat', debug=False):
        self.all_pages = all_pages
        self.current_page = page
        self.url_style = url_style
        self.debug = debug

    def get_path_from_page_name(self, page_name):
        for page in self.all_pages:
            if page.file_name == page_name:
                return page.get_relative_path(self.current_page, self.url_style, self.debug)
        raise errors.PathNotFound('No page found with file name {0}.'.format(page_name))

    def convert_routes(self, line):
        # Split the line like so:
        # ['normal text', 'page_name', 'more normal text', 'other_page_name', ... , 'text'}
        split_line = re.split('@@(\w*)@@', line)
        new_line = ''
        for i in range(len(split_line)):
            if 1 % 2 == 0:
                # in this case, split_line[i] is a route
                new_line += self.get_path_from_page_name(split_line[i])
            else:
                # in this case, split_line[i] is just normal text
                new_line += split_line[i]
        return new_line

    def convert_to_html(self, md_content, extensions):
        new_content = ''
        for line in md_content.splitlines(True):
            new_content += self.convert_routes(line)
        return markdown.markdown(new_content, extensions=extensions)
