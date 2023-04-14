import logging
import traceback

import pkg_resources

from docdb_connector.plugins.base import plugins, register

logger = logging.getLogger(__name__)


def install_plugin_events(api):
    """Adds plugin endpoints to the event router."""
    for plugin in plugins.all():
        if plugin.events:
            api.include_router(plugin.events, prefix="/{organization}/events", tags=["events"])


def install_plugins():
    """
    Installs plugins associated with onpier
    :return:
    """

    for ep in pkg_resources.iter_entry_points("docdb_connector.plugins"):
        logger.info(f"Attempting to load plugin: {ep.name}")
        try:
            plugin = ep.load()
            register(plugin)
            logger.info(f"Successfully loaded plugin: {ep.name}")
        except KeyError as e:
            logger.info(f"Failed to load plugin {ep.name} due to missing configuration items. {e}")
        except Exception:
            logger.error(f"Failed to load plugin {ep.name}:{traceback.format_exc()}")
