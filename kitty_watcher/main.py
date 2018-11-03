# coding=utf-8
from __future__ import absolute_import
import logging
import traceback

from flask import Flask

from kitty_watcher.libs.configs import configs  # noqa
import kitty_watcher.libs.logging  # noqa
from kitty_watcher.libs.exceptions import AppException
from kitty_watcher.libs.sentry import sentry, init_sentry
from kitty_watcher.views import register_views
from kitty_watcher.views.composer import compose_error


def error_handler(e):
    error = 'internal_error'
    if isinstance(e, AppException):
        if not e.message.startswith('internal_error'):
            return compose_error(e.message)
        error = e.message
    sentry().captureException()
    traceback_logger = logging.getLogger()
    traceback_logger.error(traceback.format_exc())
    return compose_error(error)


def create_app():
    app = Flask(__name__)
    init_sentry('flask')
    sentry().init_app(app)
    register_views(app)
    app.register_error_handler(Exception, error_handler)
    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=34023, host='0.0.0.0')
