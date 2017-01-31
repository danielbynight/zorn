import getpass
import importlib.util
import json
import os
import re
import shutil
import sys

import jinja2

from zorn import elements, errors


class CliColors:
    """Helper which holds the colors to color the output to the command line"""
    HEADER = '\033[32m'
    ERROR = '\033[1;31m'
    SUCESS = '\033[1;32m'
    RESET = '\033[0m'


class Task:
    def __init__(self, **kwargs):
        """Base zorn task with mixins for comunication and running the task

        By default the only accepted argument is `verbosity`, which sets the verbosity level for the task (0, 1 or 2
        from less to more verbose)

        :param kwargs: arguments for the specific task
        """
        self.verbosity = kwargs['verbosity'] if 'verbosity' in kwargs.keys() else 1

    def communicate(self, message, standard_verbosity=True):
        """Communicates message to the user or not, depending on verbosity level

        :param message: message to communicate
        :param standard_verbosity: If `False`, then message is always communicated, else the message is communicated
        only if standard verbosity is set (`verbosity = 1`)
        """
        if self.verbosity == 2 or (self.verbosity == 1 and standard_verbosity is True):
            print(message)

    def run(self):
        """Run the task

        By default it only greets the user. Has to be extended.
        """
        self.communicate('\n' + CliColors.HEADER + 'Welcome to zorn!' + CliColors.RESET)


class AdminTask(Task):
    def __init__(self, **kwargs):
        """A task to alter an already created Zorn project

        Extend Task.

        :param verbosity: the verbosity level
        :param update: if `True` the settings will be auto-updated
        :param task_args: the arguments for the specific task
        """
        super().__init__(**kwargs)
        self.update = kwargs['update'] if 'update' in kwargs.keys() else False
        self.settings = AdminTask.process_settings()
        self.task_args = kwargs['task_args'] if 'task_args' in kwargs.keys() else None

    def update_settings(self, setting, value):
        """Update the project's setting in case this was requested

        It can only update a one-line setting. That is sufficient for the kind of tasks we have

        :param setting: the setting to be updated
        :param value: the value for that setting
        """
        if self.update is True:
            setting_name = setting.upper()
            new_setting = '{0} = {1}\n'.format(setting_name, value)
            with open(os.path.join(self.settings['root_dir'], 'settings.py'), 'r') as f:
                current_settings = f.read()

            if setting_name in current_settings:
                new_settings = ''
                for line in current_settings.splitlines(True):
                    if re.match('^' + setting_name + ' = ', line) is not None:
                        new_settings += new_setting
                    else:
                        new_settings += line
                with open(os.path.join(self.settings['root_dir'], 'settings.py'), 'w') as f:
                    f.write(new_settings)
            else:
                with open(os.path.join(self.settings['root_dir'], 'settings.py'), 'a') as f:
                    f.write('\n' + new_setting)

    @staticmethod
    def process_settings():
        """Read project settings and return them neatly in a dictionary

        :returns: settings dictionary
        :rtype: dict
        """
        if 'ZORN_SETTINGS_PATH' not in os.environ.keys() or os.environ['ZORN_SETTINGS_PATH'] is None:
            raise errors.NotAZornProjectError('You are not inside a zorn project!')
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
        if 'root_dir' not in settings.keys():
            raise errors.SettingNotFoundError("The root dir setting wasn't found.")

        return settings


class Create(Task):
    STYLES = ['basic', 'soprano']

    def __init__(self, **kwargs):
        """Create a new zorn project

        Extend Task.

        :param verbosity: the verbosity level
        :param project_name: the project name
        :param site_title: the title of the site
        :param author: the author of the site
        :param style: the style (bundle of `scss` files) for the site
        :param generate: if `True`, generate the website after having created it
        """
        super().__init__(**kwargs)

        # Settings
        self.project_name = kwargs['project_name'] if 'project_name' in kwargs.keys() else None
        self.site_title = kwargs['site_title'] if 'site_title' in kwargs.keys() else None
        self.author = kwargs['author'] if 'author' in kwargs.keys() else None
        self.style = kwargs['style'] if 'style' in kwargs.keys() else None
        if self.style not in Create.STYLES and self.style is not None:
            raise errors.UnknownStyleError('The style {0} is not recognized.'.format(kwargs['style']))
        self.generate = kwargs['generate'] if 'generate' in kwargs.keys() else False

        # Directories
        self.cwd = os.getcwd()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.root_dir = None

    def run(self):
        super().run()
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

    # "Create" sub-tasks

    def create_dir(self, dir_name):
        """Helper to create a directory under the project root

        :param dir_name: the name of the directory to be created
        """
        os.mkdir(os.path.join(self.root_dir, dir_name))

    def add_file_from_template(self, file_name):
        """Adds a file to the root directory generated from a template file

        :param file_name: the name of the template file
        """
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
        """Writes content to a new file in the project

        :param path_to: path to the file relative to the project's root directory
        :param content: content to be written in the file
        """
        with open(os.path.join(self.root_dir, path_to), 'w') as f:
            f.write(content)

    def copy_file(self, path_from, path_to):
        """Copy a file from one location in the zorn package to a location in the project

        :param path_from: path of the original file, relative to the Zorn package (including file name)
        :param path_to: path of the final file, relative to the project's root directory (including file name)
        """
        shutil.copy(
            os.path.join(self.script_dir, path_from),
            os.path.join(self.root_dir, path_to)
        )

    def copy_dir(self, path_from, path_to):
        """Copy a directory and everything inside it from a location in the Zorn package to the project

        :param path_from: path of the directory, relative to the Zorn package
        :param path_to: final path, relative to the project's root directory
        """
        shutil.copytree(
            os.path.join(self.script_dir, path_from),
            os.path.join(self.root_dir, path_to)
        )


class Generate(AdminTask):
    def run(self):
        """Generate the html of the site"""
        super().run()
        self.communicate(CliColors.RESET + 'Generating... \n')
        website = elements.Website(self.settings)
        website.generate_pages()
        self.communicate(CliColors.SUCESS + 'Done!' + CliColors.RESET + '\n')


class ImportTemplates(AdminTask):
    def run(self):
        """Import the templates directory and everything inside it from the Zorn package to the project"""
        super().run()
        self.communicate(CliColors.RESET + 'Importing templates...\n')
        shutil.copytree(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
            os.path.join(self.settings['root_dir'], 'templates')
        )
        self.update_settings('templates_dir', "os.path.join(ROOT_DIR, 'templates')")
        self.communicate(CliColors.SUCESS + 'Done!' + CliColors.RESET + '\n')


class ImportStyle(AdminTask):
    def __init__(self, **kwargs):
        """Extend Admin task

        This task takes one parsed argument - the style to be imported.

        :param kwargs:
        """
        super().__init__(**kwargs)
        input_style = self.task_args[0]
        if input_style not in Create.STYLES:
            raise errors.UnknownStyleError(
                'The style {0} was not recognized. Available styles: {1}'.format(input_style, Create.STYLES)
            )
        self.style = input_style

    def run(self):
        """Import a the requested style from the Zorn package to the projects"""
        super().run()
        self.communicate(CliColors.RESET + 'Importing style "{0}"...\n'.format(self.style))
        shutil.copytree(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles', self.style),
            os.path.join(self.settings['root_dir'], self.style)
        )
        self.communicate(CliColors.SUCESS + 'Done!' + CliColors.RESET + '\n')
