import sys
from zorn import tasks
from io import StringIO


def test_task():
    task = tasks.Task()
    assert task.verbosity == 1


def test_parse_verbosity_standard():
    silent = False
    verbose = False
    verbosity = tasks.Task.parse_verbosity(verbose, silent)
    assert verbosity == 1


def test_parse_verbosity_silent():
    silent = True
    verbose = False
    verbosity = tasks.Task.parse_verbosity(verbose, silent)
    assert verbosity == 0
    silent = True
    verbose = True
    verbosity = tasks.Task.parse_verbosity(verbose, silent)
    assert verbosity == 0


def test_parse_verbosity_verbose():
    silent = False
    verbose = True
    verbosity = tasks.Task.parse_verbosity(verbose, silent)
    assert verbosity == 2


def test_comunicate_standard_verbosity():
    task = tasks.Task(1)
    stdout_ = sys.stdout
    stream = StringIO()
    sys.stdout = stream
    task.communicate('standard')
    task.communicate('verbose', False)
    sys.stdout = stdout_
    assert stream.getvalue() == 'standard\n'


def test_comunicate_silent():
    task = tasks.Task(0)
    stdout_ = sys.stdout
    stream = StringIO()
    sys.stdout = stream
    task.communicate('standard')
    task.communicate('verbose', False)
    sys.stdout = stdout_
    assert stream.getvalue() == ''


def test_comunicate_verbose():
    task = tasks.Task(2)
    stdout_ = sys.stdout
    stream = StringIO()
    sys.stdout = stream
    task.communicate('standard')
    task.communicate('verbose', False)
    sys.stdout = stdout_
    assert stream.getvalue() == 'standard\nverbose\n'
