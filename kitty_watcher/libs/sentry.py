# coding=utf-8
from __future__ import absolute_import
import inspect

from raven import Client
from raven.contrib.celery import register_signal
from raven.contrib.flask import Sentry
from raven.utils.stacks import iter_stack_frames

from kitty_watcher.libs.configs import configs


class DummySentry(object):

    def captureException(self, *args, **kwargs):  # noqa
        pass

    def captureMessage(self, *args, **kwargs):  # noqa
        pass

    def init_app(self, app):
        pass


_sentry = DummySentry()


def init_sentry(name):
    global _sentry
    if not configs.sentry.enabled:
        return
    if name == 'flask':
        _sentry = Sentry(dsn=configs.sentry.dsn)
        return
    if name == 'celery':
        _sentry = Client(dsn=configs.sentry.dsn)
        register_signal(_sentry, ignore_expected=True)


def sentry():
    return _sentry


def get_stacks():
    return inspect.stack()


def base_kwargs(extra=None):
    kwargs = {'stack': iter_stack_frames(get_stacks())}
    if extra is not None:
        kwargs['extra'] = extra
    return kwargs
