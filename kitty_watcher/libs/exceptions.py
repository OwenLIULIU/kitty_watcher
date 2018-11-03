from __future__ import absolute_import


class AppException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
