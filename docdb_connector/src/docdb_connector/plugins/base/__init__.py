from docdb_connector.plugins.base.manager import PluginManager
from docdb_connector.plugins.base.v1 import *  # noqa

plugins = PluginManager()
register = plugins.register
unregister = plugins.unregister
