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

        cwd = os.getcwd()
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Get variables
        try:
            project_name = input('Give your project a name: ')
            while project_name == '' or \
                            ' ' in project_name or \
                    os.path.exists(os.path.join(cwd, project_name)):
                print('The project name cannot be empty or have spaces.')
                print('Also, a directory with that name cannot exist yet.')
                project_name = input('Give your project a name: ')

            temp_site_title = project_name.capitalize() \
                .replace('-', ' ') \
                .replace('_', ' ')
            site_title = input(
                'Give your site a title ({0}): '.format(temp_site_title)
            )
            if site_title.strip() == '':
                site_title = temp_site_title

            temp_author = getpass.getuser()
            author = input(
                'Who is the site author? ({0}) '.format(temp_author)
            )
            if author.strip() == '':
                author = temp_author
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
        root_dir = os.path.join(cwd, project_name)
        os.mkdir(root_dir)

        print('- adding settings file')
        with open(os.path.join(script_dir, 'defaults', 'settings.py')) as f:
            raw_settings_content = f.read()
        template = jinja2.Template(raw_settings_content)
        settings_content = template.render({
            'project_name': project_name,
            'site_title': site_title,
            'author': author,
        })
        with open(os.path.join(root_dir, 'settings.py'), 'w') as f:
            f.write(settings_content)

        print('- adding admin file')
        with open(os.path.join(script_dir, 'defaults', 'admin.py')) as f:
            raw_admin_content = f.read()
        template = jinja2.Template(raw_admin_content)
        admin_content = template.render({
            'project_name': project_name,
        })
        with open(os.path.join(root_dir, 'admin.py'), 'w') as f:
            f.write(admin_content)

        print('- creating the markdown directory')
        os.mkdir(os.path.join(root_dir, 'md'))

        print('- adding index content')
        with open(os.path.join(root_dir, 'md', 'index.md'), 'w') as f:
            f.write(
                '#Hello, world\n'
                'you have successfully created the zorn project {0}!'
                    .format(project_name)
            )

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
        with open(os.path.join(root_dir, 'package.json'), 'w') as f:
            f.write(package_content)

        print('- adding gulpfile')
        shutil.copy(
            os.path.join(script_dir, 'defaults', 'gulpfile.js'),
            os.path.join(root_dir, 'gulpfile.js')
        )

        print('- adding style')
        shutil.copytree(
            os.path.join(script_dir, 'styles', 'basic'),
            os.path.join(root_dir, 'scss')
        )

        print(CliColors.SUCESS + 'Done!' + CliColors.RESET + '\n')
        print('Now you can run "npm install" to generate the style')
        print(
            'and "python admin.py generate" (or "gulp") to generate ' +
            project_name + '.\n'
        )
        print(CliColors.SUCESS + 'Good luck!' + CliColors.RESET + '\n')
