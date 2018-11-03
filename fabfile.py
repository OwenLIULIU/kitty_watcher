from __future__ import absolute_import
from functools import wraps

import os
from fabric.api import task, local
from fabric.colors import green, red


DEV_ENV = 'development'
TEST_ENV = 'test'
PROD_ENV = 'production'
DEFAULT_ENV = DEV_ENV

DB_DEFAULT_CHARSET = '/*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */'


def enforce_virtualenv(func):
    """Make sure the task is run in virtualenv (decorator)."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        virtual_env = os.environ.get("VIRTUAL_ENV")
        if virtual_env is not None:
            # Already in virtualenv, no need to wrap the function
            return func(*args, **kwargs)

        print red('Unable to find a python virtualenv for tickets! '
                  'Did you forget to activate one? Run following command:')
        print red('\nsource env/bin/activate')
    return wrapper


@task
def clean():
    """Remove all .pyc files."""
    print green('Clean up .pyc files')
    local("find . -name '*.py[co]' -exec rm -f '{}' ';'")


@task
@enforce_virtualenv
def lint():
    """Check for lints"""
    print green('Checking for lints')
    local("flake8")


@task(alias='s')
@enforce_virtualenv
def serve(env=DEFAULT_ENV):
    """Start the server."""
    os.environ['APP_ENV'] = './configs/%s.yaml' % env
    local("python kitty_watcher/main.py")


@task
@enforce_virtualenv
def shell(env=DEFAULT_ENV):
    """Run the shell in the environment."""
    os.environ['APP_ENV'] = './configs/%s.yaml' % env
    # local("ipython --ipython-dir ./settings/")  # useful if ipython is installed
    local("python")
