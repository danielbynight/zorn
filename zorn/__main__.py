"""
Used for creation of a new zorn project.
"""

import sys

# Register commands here
AVAILABLE_COMMANDS = {
    'test' : ['-t', '--test'],
    'help': [],
}


class ProjectStartCli:
    def __init__(self, flags):
        self.flags = flags

    def _validate_flags(self, available_flags):
        for flag in self.flags:
            if flag not in available_flags:
                sys.exit('You have inserted an unrecognized flag.')

    def test(self):
        """
        Used for testing purposes.
        """
        AVAILABLE_FLAGS = ['-t', '--test']
        self._validate_flags(AVAILABLE_FLAGS)

        sys.exit('You have successfully tested the zorn project start cli. Well done!')

    def help(self):
        """
        List the available commands
        """

if __name__ == '__main__':

    # Get input from command line
    input_from_cl = sys.argv

    # Remove base command
    input_from_cl.remove('zorn')

    # Separate input in command and flags
    command = [cmd for cmd in input_from_cl if cmd[0] != '-']
    flags = [flag for flag in input_from_cl if flag[0] == '-']

    # Validate command - there must be only one and it should be in AVAILABLE_COMMANDS
    if len(command) == 0:
        sys.exit('Welcome to zorn, your static website generator. Type "python zorn help" for a list of commands.')
    elif len(command) > 1:
        sys.exit('You inserted more than one command and now zorn is confused.')
    command = command.pop()
    if command not in AVAILABLE_COMMANDS:
        sys.exit('You have not inserted a known command. Type "python zorn help" for a list of commands')

    # Run task
    cli = ProjectStartCli(flags)
    getattr(cli, command)()
