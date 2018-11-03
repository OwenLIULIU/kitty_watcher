# coding=utf-8
from __future__ import absolute_import
import time

import arrow


def arrow_to_timestamp(arrow):
    if not arrow:
        return None
    return int(round(arrow.timestamp * 1000))


def timestamp_to_arrow(ts):
    if not ts:
        return None
    return arrow.get(int(ts / 1000))


def get_timestamp(offset=0):
    return int(time.time() * 1000) + offset
