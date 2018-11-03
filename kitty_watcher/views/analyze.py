# coding=utf-8
from __future__ import absolute_import

from kitty_watcher.libs.exceptions import AppException
from kitty_watcher.models.message import Message
from kitty_watcher.services.analyze import AnalyzeService
from flask import request
from flask_classy import FlaskView, route

from kitty_watcher.views.composer import compose_error, compose_ok


class AnalyzeView(FlaskView):

    route_base = '/'

    @route('/analyze', methods=['POST'])
    def analyze(self):
        json = request.get_json() or {}

        message_json = json.get('message')
        if message_json is None:
            raise AppException('invalid_params.missing_message')
        message = Message(**message_json)
        if message.channel_uuid is None:
            raise AppException('invalid_params.missing_channel_uuid')
        if message.user_uuid is None:
            raise AppException('invalid_params.missing_user_uuid')
        if message.type is None:
            raise AppException('invalid_params.missing_type')
        if message.data is None:
            raise AppException('invalid_params.missing_data')
        if message.time is None:
            raise AppException('invalid_params.missing_time')
        analysis = json.get('analysis')
        if analysis is None:
            return compose_error('invalid_params.missing_analysis')

        matches = AnalyzeService.analyze(message, analysis)
        return compose_ok({u'matches': matches})
