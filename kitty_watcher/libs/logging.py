# coding=utf-8
from __future__ import absolute_import

from logging.config import dictConfig

from kitty_watcher.libs.configs import configs


logging_configs = configs.logging.to_dict()

loggers = logging_configs.get('loggers')

for key, logger in loggers.iteritems():
    name = key if len(key) > 0 else 'default'
    handler_name = '{}_kafka'.format(name)
    topic_name = '{}_{}'.format(configs.application_identifier, name)
    if 'kafka' in logger.get('handlers'):
        logger.get('handlers').remove('kafka')
        logger.get('handlers').append(handler_name)
        kafka_handler = {
            'class': '{}.libs.handlers.KafkaLoggingHandler'.format(configs.application_identifier),
            'formatter': 'default',
            'hosts_list': ', '.join(configs.kafka),
            'topic': topic_name,
            'timeout_secs': 0.5,
            'retry': 6,
            'async': False,
            'async_retry': 10
        }
        if logger.get('level') is not None:
            kafka_handler['level'] = logger.get('level')
        logging_configs.get('handlers')[handler_name] = kafka_handler

dictConfig(logging_configs)
