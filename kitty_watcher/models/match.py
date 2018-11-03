# coding=utf-8
from __future__ import absolute_import


class Match(object):

    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.subtype = kwargs.get('subtype')
        self.word = kwargs.get('word')
        self.start = kwargs.get('start')
        self.end = kwargs.get('end')
        self.data = kwargs.get('data')

    def to_dict(self):
        return {
            'type': self.type,
            'subtype': self.subtype,
            'word': self.word,
            'start': self.start,
            'end': self.end,
            'data': self.data,
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
