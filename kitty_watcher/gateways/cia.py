# coding=utf-8
from __future__ import absolute_import

import requests
import simplejson as json

from kitty_watcher.libs.configs import configs
from kitty_watcher.libs.sentry import sentry, base_kwargs

CIA_SERVICE = '{}://{}:{}'.format(configs.cia.protocol, configs.cia.host, configs.cia.port)


class CIAGateway(object):

    @staticmethod
    def entity_query(collection, query, offset, limit):
        url = '{}{}'.format(CIA_SERVICE, '/entity_query')
        headers = {'Content-Type': 'application/json'}
        body = {
            'collection': collection,
            'query': query,
            'offset': offset,
            'limit': limit,
        }

        try:
            response = requests.post(url, json=body, headers=headers)
        except requests.exceptions.ConnectionError, e:
            sentry().captureException()
            return [], 'internal_error.connection_error'

        if not response.status_code == 200:
            kwargs = base_kwargs(extra={'body': body})
            sentry().captureMessage('internal_error.request_failure', **kwargs)
            return [], 'internal_error.request_failure'

        try:
            resp = response.json()
        except json.JSONDecodeError:
            sentry().captureException()
            return [], 'internal_error.invalid_service_response'

        error = resp.get('error')
        if error is not None:
            return [], error

        return resp.get('results'), None
