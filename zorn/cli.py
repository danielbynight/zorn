import getpass
import importlib
import os
import shutil
import jinja2
import json

import sys

import zorn.elements


def process_request(args):
    try:
        # Register commands here
        if len(args) < 2 or args[1] == 'help':
            args.append('help')
            return Help(args)
        elif args[1] == 'generate':
            return Generate(args)
        elif args[1] == 'create':
            return Create(args)
        else:
            return NotFound(args)
    except Exception as e:
        sys.exit(CliColors.ERROR + str(e) + CliColors.RESET)


class UnrecognizedFlagError(Exception):
    pass


class CliColors:
    HEADER = '\033[32m'
    ERROR = '\033[1;31m'
    SUCESS = '\033[1;32m'
    RESET = '\033[0m'


class Command:
    _available_flags = []

    def __init__(self, args):
        self.name = args[1]
        self.flags = [flag for flag in args if flag[0] == '-']
        for flag in self.flags:
            if flag not in Command._available_flags:
                raise UnrecognizedFlagError(
                    "I'm afraid the flag {0} is not recognized." + flag
                )
        if len(args) > 2:
            self.args = [arg for arg in args[2:] if arg[0] != '-']

        print(
            CliColors.HEADER +
            '\nWelcome to zorn!\n' +
            CliColors.RESET
        )


class NotFound(Command):
    def __init__(self, args):
        super().__init__(args)
        print(
            CliColors.ERROR +
            "I'm afraid I don't recognize the command " +
            self.name +
            CliColors.RESET
        )


class Help(Command):
    def __init__(self, args):
        super().__init__(args)
        print(CliColors.RESET + 'Available commands:\n')
        print('help - list available commands')
        print('generate - generate the website (i.e. its html files)')
        print(CliColors.SUCESS + "\nAnd that's all\n")


class Generate(Command):
    @staticmethod
    def process_settings():

        module = importlib.import_module(os.environ['ZORN_SETTINGS'])
        settings = {}
        for setting in module.__dict__.keys():
            if setting.upper() == setting:
                settings[setting.lower()] = module.__dict__[setting]

        return settings

    def __init__(self, args):
        super().__init__(args)
        print(CliColors.RESET + 'Generating... \n')
        try:
            website = zorn.elements.Website(self.process_settings())
            website.generate_pages()
        except Exception as e:
            sys.exit(CliColors.ERROR + str(e) + CliColors.RESET)
        print(CliColors.SUCESS + 'Done!' + CliColors.RESET + '\n')


class Create(Command):
    def __init__(self, args):
        super().__init__(args)

        self.cwd = os.getcwd()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        # Get variables
        try:
            project_name = input('Give your project a name: ')
            while project_name == '' or \
                    ' ' in project_name or \
                    os.path.exists(os.path.join(self.cwd, project_name)):
                print('The project name cannot be empty or have spaces.')
                print('Also, a directory with that name cannot exist yet.')
                project_name = input('Give your project a name: ')

            self.project_name = project_name
            self.root_dir = os.path.join(self.cwd, project_name)

            temp_site_title = project_name.capitalize() \
                .replace('-', ' ') \
                .replace('_', ' ')
            site_title = input(
                'Give your site a title ({0}): '.format(temp_site_title)
            )
            if site_title.strip() == '':
                self.site_title = temp_site_title

            temp_author = getpass.getuser()
            author = input(
                'Who is the site author? ({0}) '.format(temp_author)
            )
            if author.strip() == '':
                self.author = temp_author
        except KeyboardInterrupt:
            sys.exit(
                '\n\n' +
                CliColors.ERROR +
                'You have interrupted the creation of a new zorn project.\n' +
                CliColors.SUCESS +
                'No worries, it\'s ok to change your mind. Bye!\n' +
                CliColors.RESET
            )

        print('\nStarting...\n')

        print("- creating project's directory")
        self.create_dir('')

        print('- adding settings file')
        self.add_file_from_template('settings.py')

        print('- adding admin file')
        self.add_file_from_template('admin.py')

        print('- creating the markdown directory')
        self.create_dir('md')

        print('- adding index content')
        md_content = '#Hello, world\n' \
                     'you have successfully created the zorn project "{0}"!'\
            .format(project_name)
        self.add_file_with_content(os.path.join('md', 'index.md'), md_content)

        print('- adding npm package file')
        package_content = json.dumps({
            'name': project_name,
            'version': '0.0.1',
            'description': '',
            'main': 'index.html',
            'author': author,
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

        print('- adding gulpfile')
        self.copy_file(
            os.path.join('defaults', 'gulpfile.js'),
            'gulpfile.js'
        )

        print('- adding style')
        self.copy_dir(
            os.path.join('styles', 'basic'),
            'scss'
        )

        print(CliColors.SUCESS + 'Done!' + CliColors.RESET + '\n')
        print('Now you can run "npm install" to generate the website!\n')
        print(CliColors.SUCESS + 'Good luck!' + CliColors.RESET + '\n')

    # Tasks

    def create_dir(self, dir_name):
        os.mkdir(os.path.join(self.root_dir, dir_name))

    def add_file_from_template(self, file_name):
        with open(os.path.join(self.script_dir, 'defaults', file_name)) \
                as f:
            raw_settings_content = f.read()
        template = jinja2.Template(raw_settings_content)
        settings_content = template.render({
            'project_name': self.project_name,
            'site_title': self.site_title,
            'author': self.author,
        })
        with open(os.path.join(self.root_dir, file_name), 'w') as f:
            f.write(settings_content)

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
