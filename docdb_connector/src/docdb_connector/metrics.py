import logging

from docdb_connector.plugins.base import plugins
from .config import METRIC_PROVIDERS

log = logging.getLogger(__file__)


class Metrics(object):
    _providers = []

    def __init__(self):
        if not METRIC_PROVIDERS:
            log.info(
                "No metric providers defined via METRIC_PROVIDERS env var. Metrics will not be sent."
            )
        else:
            self._providers = METRIC_PROVIDERS

    def gauge(self, name, value, tags=None):
        for _provider in self._providers:
            log.debug(
                f"Sending gauge metric {name} to _provider {_provider}. Value: {value} Tags: {tags}"
            )
            p = plugins.get(_provider)
            p.gauge(name, value, tags=tags)

    def counter(self, name, value=None, tags=None):
        for _provider in self._providers:
            log.debug(
                f"Sending counter metric {name} to provider {_provider}. Value: {value} Tags: {tags}"
            )
            p = plugins.get(_provider)
            p.counter(name, value=value, tags=tags)

    def timer(self, name, value, tags=None):
        for _provider in self._providers:
            log.debug(
                f"Sending timer metric {name} to provider {_provider}. Value: {value} Tags: {tags}"
            )
            p = plugins.get(_provider)
            p.timer(name, value, tags=tags)


provider = Metrics()
