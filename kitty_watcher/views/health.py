# coding=utf-8
from __future__ import absolute_import

from flask_classy import FlaskView, route

from kitty_watcher.views.composer import compose_ok


class HealthView(FlaskView):

    route_base = '/'

    @route('/health')
    def index(self):
        """Index endpoint is for monitoring service to make sure this application is online"""
        return compose_ok({'message': 'Gotcha!'})
