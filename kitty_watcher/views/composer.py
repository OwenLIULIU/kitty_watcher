# coding=utf-8
from __future__ import absolute_import
import json

from flask import Response


class JsonResponse(Response):
    default_mimetype = 'application/json'


def compose_ok(data=None):
    return JsonResponse(json.dumps(data or {'ok': True}, ensure_ascii=False))


def compose_error(error):
    return JsonResponse(json.dumps({'error': error}, ensure_ascii=False))
