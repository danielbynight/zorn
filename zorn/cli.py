import getpass
import importlib.util
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
            if args[0][-8:] == 'admin.py':
                return Generate(args)
            else:
                pass
        elif args[1] == 'importtemplates':
            if args[0][-8:] == 'admin.py':
                return ImportTemplates(args)
            else:
                pass
        elif args[1] == 'create':
            return Create(args)
        return NotFound(args)
    except Exception as e:
        sys.exit(CliColors.ERROR + str(e) + CliColors.RESET)


def process_settings():
    if os.environ['ZORN_SETTINGS'] is None:
        raise NotAZornProjectError('You are not inside a zorn project!')
    spec = importlib.util.spec_from_file_location(
        os.environ['ZORN_SETTINGS'],
        os.environ['ZORN_SETTINGS_PATH']
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    settings = {}
    for setting in module.__dict__.keys():
        if setting.upper() == setting:
            settings[setting.lower()] = module.__dict__[setting]

    return settings


class UnrecognizedFlagError(Exception):
    pass


class NotAZornProjectError(Exception):
    pass


class CliColors:
    HEADER = '\033[32m'
    ERROR = '\033[1;31m'
    SUCESS = '\033[1;32m'
    RESET = '\033[0m'


class Command:
    _available_flags = []

    def __init__(self, args):
        self.silent = False
        self.name = args[1]
        self.flags = [flag for flag in args if flag[0] == '-']
        for flag in self.flags:
            if flag not in self._available_flags:
                raise UnrecognizedFlagError('I\'m afraid the flag "{0}" is not recognized.'.format(flag))
        if len(args) > 2:
            self.args = [arg for arg in args[2:] if arg[0] != '-']

        print(CliColors.HEADER + '\nWelcome to zorn!\n' + CliColors.RESET)

    def communicate(self, message):
        if self.silent is False:
            print(message)


class NotFound(Command):
    def __init__(self, args):
        super().__init__(args)
        print(CliColors.ERROR + "I'm afraid I don't recognize the command " + self.name + CliColors.RESET)


class Help(Command):
    def __init__(self, args):
        super().__init__(args)
        print(CliColors.RESET + 'Available commands:\n')
        print('help - list available commands')
        print('create - start a new zorn project')
        print('generate - generate the website (i.e. its html files)- only avaialble through admin.py')
        print('importtemplates - imports the templates locally- only avaialble through admin.py')
        print(CliColors.SUCESS + "\nAnd that's all\n")


class Generate(Command):
    def __init__(self, args):
        super().__init__(args)
        print(CliColors.RESET + 'Generating... \n')
        try:
            website = zorn.elements.Website(process_settings())
            website.generate_pages()
        except Exception as e:
            sys.exit(CliColors.ERROR + str(e) + CliColors.RESET)
        print(CliColors.SUCESS + 'Done!' + CliColors.RESET + '\n')


class Create(Command):
    _styles = ['', 'basic', 'soprano']
    _available_flags = ['-s', '--silent']

    def __init__(self, args):
        super().__init__(args)

        self.cwd = os.getcwd()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        if '-s' in self.flags or '--silent' in self.flags:
            self.silent = True

        # Defaults
        self.author = getpass.getuser()
        self.style = 'basic'

        # If a project name was passed as an argument,
        # create the site based on it
        arguments = [arg for arg in args if arg[0] != '-']
        if len(arguments) > 2:
            self.project_name = arguments[2]
            self.root_dir = os.path.join(self.cwd, self.project_name)
            self.site_title = self.project_name.capitalize().replace('-', ' ').replace('_', ' ')
        else:
            # Get variables
            try:
                project_name = input('Give your project a name: ')
                while project_name == '' or ' ' in project_name or os.path.exists(
                        os.path.join(self.cwd, project_name)):
                    print('The project name cannot be empty or have spaces.')
                    print('Also, a directory with that name cannot exist yet.')
                    project_name = input('Give your project a name: ')

                self.project_name = project_name
                self.root_dir = os.path.join(self.cwd, project_name)

                self.site_title = project_name.capitalize().replace('-', ' ').replace('_', ' ')
                site_title = input('Give your site a title ({0}): '.format(self.site_title))
                if site_title.strip() != '':
                    self.site_title = site_title

                author = input('Who is the site author? ({0}) '.format(self.author))
                if author.strip() != '':
                    self.author = author

                style = input('Choose a style - basic or soprano (basic): ')
                while style not in Create._styles:
                    print('Unrecognized syle...')
                    self.communicate('Available styles:')
                    for style in Create._styles:
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
                    'No worries, it\'s ok to change your mind. Bye!\n' +
                    CliColors.RESET
                )

        print('\nStarting...\n')

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

        auto_generate = input('Would you like to generate now your site - yes or no? (yes) ')
        if auto_generate != 'no':
            os.system(
                'cd {0} && npm install --silent'.format(self.project_name))
        print(CliColors.SUCESS + 'Done!' + CliColors.RESET + '\n')
        if auto_generate == 'no':
            self.communicate('Now you can run "npm install" to generate the website!\n')
        print(CliColors.SUCESS + 'Good luck!' + CliColors.RESET + '\n')

    # Tasks

    def create_dir(self, dir_name):
        os.mkdir(os.path.join(self.root_dir, dir_name))

    def add_file_from_template(self, file_name):
        with open(os.path.join(self.script_dir, 'defaults', file_name)) as f:
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


class ImportTemplates(Command):
    _available_flags = ['-u', '--update']

    def __init__(self, args):
        super().__init__(args)
        print(CliColors.RESET + 'Importing templates...\n')
        settings = process_settings()
        if 'root_dir' not in settings.keys():
            raise zorn.elements.SettingNotFoundError('Root dir not found in settings.')
        shutil.copytree(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
            os.path.join(settings['root_dir'], 'templates')
        )

        if '-u' in self.flags or '--update' in self.flags:
            with open(os.path.join(settings['root_dir'], 'settings.py'), 'a') as f:
                f.write("\n\nTEMPLATES_DIR = os.path.join(ROOT_DIR, 'templates')")

        print(CliColors.SUCESS + 'Done!' + CliColors.RESET + '\n')
