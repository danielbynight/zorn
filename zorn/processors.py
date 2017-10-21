import os
import json

import jinja2

from zorn import Processor
from zorn.jinja_extensions import Static, Markdown, Url


class JinjaProcessor(Processor):
    def render(self, page):
        env = jinja2.Environment(extensions=[Static, Markdown, Url])
        env.loader = jinja2.FileSystemLoader(self.settings.TEMPLATES_DIR)
        env.settings = self.settings
        env.page = page
        template = env.get_template(page.template_name)
        page.context.update({'development': self.settings.DEVELOPMENT})
        page.content = template.render(page.context).encode('utf-8')


class FileSystemProcessor(Processor):
    def render(self, page):
        output_dir = os.path.join(self.settings.OUTPUT_DIR, page.route)
        if not os.path.isdir(output_dir):
            # create sub directories if they don't exist
            os.makedirs(output_dir)

        with open(os.path.join(output_dir, page.file_name), 'wb') as file:
            file.write(page.content)


class JSONContextProcessor(Processor):
    def render(self, page):
        with open(os.path.join(self.settings.JSON_DIR, page.file_name)) as file:
            content = json.load(file.read())

        page.context.update(**content)
