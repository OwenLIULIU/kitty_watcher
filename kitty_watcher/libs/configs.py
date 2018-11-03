# coding=utf-8
from __future__ import absolute_import

import os

import hiyapyco
from addict import Dict

configs_file = os.environ.get('APP_ENV', 'configs/development.yaml')
configs_dict = hiyapyco.load(configs_file, method=hiyapyco.METHOD_SIMPLE)
configs = Dict(configs_dict)


def get_dynamic_string(value):
    if value is None:
        return None
    if value.startswith('<'):
        value = value[1:].strip()
        try:
            with open(value, 'r') as f:
                value = f.read()
                return value
        except IOError, e:
            return None
    if value.startswith('@'):
        return os.environ[value[1:]]
    return value
