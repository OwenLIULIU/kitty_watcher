# coding=utf-8
from __future__ import absolute_import

from kitty_watcher.views.health import HealthView
from kitty_watcher.views.analyze import AnalyzeView



def register_views(app):
    """Register all routes to the application

    :param app: The application
    :type app: flask.Flask
    """
    AnalyzeView.register(app)
    HealthView.register(app)
