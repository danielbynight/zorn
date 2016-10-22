import argparse
import getpass
import importlib.util
import json
import os
import shutil
import sys

import jinja2

import zorn.elements

ADMIN_TASKS = {
    'generate': 'Generate',
    'importtemplates': 'ImportTemplates'
}


class NotAZornProjectError(Exception):
    pass


class UnknownStyleError(Exception):
    pass


def process_admin_request():
    parser = argparse.ArgumentParser(description='A tool for creation of zorn projects.')
    parser.add_argument('task', choices=ADMIN_TASKS.keys())
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-s', '--silent', action='store_true')
    parser.add_argument('-u', '--update', action='store_true')
    args = parser.parse_args()

    # import the correct task-class from within this module
    current_module = sys.modules[__name__]
    task_class = getattr(current_module, ADMIN_TASKS[args.task])

    # run the task
    task = task_class(
        verbosity=Task.parse_verbosity(args.verbose, args.silent),
        update=args.update
    )
    task.run()


class CliColors:
    HEADER = '\033[32m'
    ERROR = '\033[1;31m'
    SUCESS = '\033[1;32m'
    RESET = '\033[0m'


class Task:
    @staticmethod
    def parse_verbosity(verbose=False, silent=False):
        if silent is True:
            return 0
        elif verbose is True:
            return 2
        return 1

    def __init__(self, verbosity=1):
        self.verbosity = verbosity

    def communicate(self, message, standard_verbosity=True):
        if self.verbosity == 2 or (self.verbosity == 1 and standard_verbosity is True):
            print(message)


class AdminTask(Task):
    @staticmethod
    def process_settings():
        if 'ZORN_SETTINGS_PATH' not in os.environ.keys() or os.environ['ZORN_SETTINGS_PATH'] is None:
            raise NotAZornProjectError('You are not inside a zorn project!')
        spec = importlib.util.spec_from_file_location(
            'settings',
            os.environ['ZORN_SETTINGS_PATH']
        )
        settings_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(settings_module)
        settings = {}
        for setting in settings_module.__dict__.keys():
            if setting.upper() == setting:
                settings[setting.lower()] = settings_module.__dict__[setting]
        print(os.environ['ZORN_SETTINGS_PATH'])
        if 'root_dir' not in settings.keys():
            raise zorn.elements.SettingNotFoundError("The root dir setting wasn't found.")

        return settings

    def __init__(self, verbosity=1, update=False):
        super().__init__(verbosity)
        self.update = update


class Create(Task):
    STYLES = ['basic', 'soprano']

    def __init__(
            self,
            project_name=None,
            site_title=None,
            author=None,
            style=None,
            generate=False,
            verbosity=1
    ):
        super().__init__(verbosity)

        # Settings
        self.project_name = project_name
        self.site_title = site_title
        self.author = author
        self.style = style
        if self.style not in Create.STYLES and self.style is not None:
            raise UnknownStyleError('The style {0} is not recognized.'.format(style))
        self.generate = generate

        # Directories
        self.cwd = os.getcwd()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.root_dir = None

    def run(self):
        try:
            if self.project_name is None:
                project_name = input('Give your project a name: ')
                while project_name == '' or ' ' in project_name or os.path.exists(
                        os.path.join(self.cwd, project_name)):
                    print('The project name cannot be empty or have spaces.')
                    print('Also, a directory with that name cannot exist yet.')
                    project_name = input('Give your project a name: ')
                self.project_name = project_name
            self.root_dir = os.path.join(self.cwd, self.project_name)

            if self.site_title is None:
                self.site_title = self.project_name.capitalize().replace('-', ' ').replace('_', ' ')
                if self.verbosity != 0:
                    site_title = input('Give your site a title ({0}): '.format(self.site_title))
                    if site_title.strip() != '':
                        self.site_title = site_title

            if self.author is None:
                self.author = getpass.getuser()
                if self.verbosity != 0:
                    author = input('Who is the site author? ({0}) '.format(self.author))
                    if author.strip() != '':
                        self.author = author

            if self.style is None:
                self.style = 'basic'
                if self.verbosity != 0:
                    style = input('Choose a style - basic or soprano (basic): ')
                    while style not in Create.STYLES and style != '':
                        print('Unrecognized syle...')
                        self.communicate('Available styles:')
                        for style in Create.STYLES:
                            self.communicate('\t' + style)
                        style = input('Choose a style (basic): ')
                    if style != '':
                        self.style = style
        except KeyboardInterrupt:
            sys.exit(
                '\n\n' +
                CliColors.ERROR +
                'You have interrupted the creation of a new project.\n' +
                CliColors.SUCESS +
                "No worries, it's ok to change your mind. Bye!\n" +
                CliColors.RESET
            )

        self.communicate('\nStarting...\n')

        self.communicate("- creating project's directory")
        self.create_dir('')

        self.communicate('- adding settings file')
        self.add_file_from_template('settings.py')

        self.communicate('- adding admin file')
        self.add_file_from_template('admin.py')

        self.communicate('- creating the markdown directory')
        self.create_dir('md')

        self.communicate('- adding index content')
        md_content = '#Hello, world\nyou have successfully created the zorn project "{0}"!' \
            .format(self.project_name)
        self.add_file_with_content(os.path.join('md', 'index.md'), md_content)

        self.communicate('- adding npm package file')
        package_content = json.dumps({
            'name': self.project_name,
            'version': '0.0.1',
            'description': '',
            'main': 'index.html',
            'author': self.author,
            'devDependencies': {
                'gulp': '^3.9.1',
                'gulp-autoprefixer': '^3.1.1',
                'gulp-clean-css': '^2.0.13',
                'gulp-rename': '^1.2.2',
                'gulp-sass': '^2.3.2',
                'gulp-shell': '^0.5.2',
            },
            'scripts': {
                'postinstall': 'gulp'
            }
        }, sort_keys=True, indent=2)
        self.add_file_with_content('package.json', package_content)

        self.communicate('- adding gulpfile')
        self.copy_file(os.path.join('defaults', 'gulpfile.js'), 'gulpfile.js')

        self.communicate('- adding style')
        self.copy_dir(os.path.join('styles', self.style), 'scss')

        if self.generate is True:
            auto_generate = 'yes'
        else:
            if self.verbosity == 0:
                auto_generate = 'no'
            else:
                auto_generate = input('Would you like to generate now your site - yes or no? (yes) ')

        if auto_generate.lower() not in ['no', 'n', 'nope', 'nee', 'non']:
            os.system(
                'cd {0} && npm install --silent'.format(self.project_name))
        self.communicate(CliColors.SUCESS + 'Done!' + CliColors.RESET + '\n')
        if auto_generate == 'no':
            self.communicate('Now you can run "npm install" to generate the website!\n')
        self.communicate(CliColors.SUCESS + 'Good luck!' + CliColors.RESET + '\n')

    # Create tasks

    def create_dir(self, dir_name):
        os.mkdir(os.path.join(self.root_dir, dir_name))

    def add_file_from_template(self, file_name):
        with open(os.path.join(self.script_dir, 'defaults', file_name)) as f:
            raw_settings_content = f.read()
        template = jinja2.Template(raw_settings_content)
        file_content = template.render({
            'project_name': self.project_name,
            'site_title': self.site_title,
            'author': self.author,
        })
        file_content += '\n'
        with open(os.path.join(self.root_dir, file_name), 'w') as f:
            f.write(file_content)

    def add_file_with_content(self, path_to, content):
        with open(os.path.join(self.root_dir, path_to), 'w') as f:
            f.write(content)

    def copy_file(self, path_from, path_to):
        shutil.copy(
            os.path.join(self.script_dir, path_from),
            os.path.join(self.root_dir, path_to)
        )

    def copy_dir(self, path_from, path_to):
        shutil.copytree(
            os.path.join(self.script_dir, path_from),
            os.path.join(self.root_dir, path_to)
        )


class Generate(AdminTask):
    def run(self):
        self.communicate(CliColors.RESET + 'Generating... \n')
        try:
            website = zorn.elements.Website(AdminTask.process_settings())
            website.generate_pages()
        except Exception as e:
            sys.exit(CliColors.ERROR + str(e) + CliColors.RESET)
        self.communicate(CliColors.SUCESS + 'Done!' + CliColors.RESET + '\n')


class ImportTemplates(AdminTask):
    def run(self):
        self.communicate(CliColors.RESET + 'Importing templates...\n')
        settings = AdminTask.process_settings()
        shutil.copytree(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
            os.path.join(settings['root_dir'], 'templates')
        )

        if self.update is True:
            with open(os.path.join(settings['root_dir'], 'settings.py'), 'a') as f:
                f.write("\n\nTEMPLATES_DIR = os.path.join(ROOT_DIR, 'templates')")

        self.communicate(CliColors.SUCESS + 'Done!' + CliColors.RESET + '\n')
