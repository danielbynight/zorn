def process_request(args):
    args = args[1:]
    print(args)


class UnrecognizedFlagError(Exception):
    pass


class Command:
    _available_flags = []

    def __init__(self, args):
        self.name = args[1]
        self.flags = [flag for flag in args if flag[0] == '-']
        for flag in self.flags:
            if flag not in Command._available_flags:
                raise UnrecognizedFlagError(
                    "I'm afraid the flag {0} is not recognized.".format(flag)
                )
        if len(args) > 2:
            self.args = [arg for arg in args[2:] if arg[0] != '-']


class Generate(Command):
    pass
