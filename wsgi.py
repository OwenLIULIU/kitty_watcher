import sys
from os import path as op
from kitty_watcher.main import create_app


APPROOT = op.abspath(op.join(op.dirname(__file__), 'kitty_watcher'))
if APPROOT not in sys.path:
    sys.path.insert(0, APPROOT)
application = create_app()