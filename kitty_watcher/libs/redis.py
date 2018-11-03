# coding=utf-8
from __future__ import absolute_import

import redis

from kitty_watcher.libs.configs import configs, get_dynamic_string


redis_configs = configs.redis
redis_client = redis.StrictRedis(
    host=redis_configs.host,
    port=redis_configs.port,
    db=redis_configs.db,
    password=get_dynamic_string(redis_configs.password)
)
