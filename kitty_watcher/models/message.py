# coding=utf-8
from __future__ import absolute_import


class Message(object):

    def __init__(self, **kwargs):
        self.channel_uuid = kwargs.get('channel_uuid')
        self.user_uuid = kwargs.get('user_uuid')

        self.service_uuid = kwargs.get('service_uuid')
        if self.service_uuid is not None and len(self.service_uuid) == 0:
            self.service_uuid = None

        self.type = kwargs.get('type')
        self.data = kwargs.get('data')
        self.time = kwargs.get('time')
        self.intent = kwargs.get('intent')
        self.variables = kwargs.get('variables')
        self.coordinate = kwargs.get('coordinate')

    def to_dict(self):
        return {
            'channel_uuid': self.channel_uuid,
            'user_uuid': self.user_uuid,
            'service_uuid': self.service_uuid,
            'type': self.type,
            'data': self.data,
            'time': self.time,
            'intent': self.intent,
            'variables': self.variables,
            'coordinate': self.coordinate,
        }

    @classmethod
    def instance_to_dict(cls, x):
        if x is None:
            return None
        return x.to_dict()

    @classmethod
    def dict_to_instance(cls, d):
        if d is None:
            return None
        return cls(**d)
