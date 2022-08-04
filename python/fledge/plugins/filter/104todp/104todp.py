# -*- coding: utf-8 -*-

# FLEDGE_BEGIN
# See: http://fledge-iot.readthedocs.io
# FLEDGE_END

""" Plugin module that can be used to convert IEC 104 asdu object to simple datapoint"""

import logging
import copy
import random

from fledge.common import logger
from fledge.plugins.common import utils
import filter_ingest

__author__ = "Akli Rahmoun"
__copyright__ = "Copyright (c) 2020, RTE (https://www.rte-france.com)"
__license__ = "Apache 2.0"

_LOGGER = logger.setup(__name__, level=logging.INFO)

PLUGIN_NAME = "104todp"

_DEFAULT_CONFIG = {
    'plugin': {
        'description': 'Filter used to convert IEC 104 asdu object to simple datapoint',
        'type': 'string',
        'default': PLUGIN_NAME,
        'readonly': 'true'
    },
    'enable': {
        'description': 'Enable/Disable filter plugin',
        'type': 'boolean',
        'default': 'false',
        'displayName': 'Enabled',
        'order': "2"
    }
}


def plugin_info():
    """ Returns information about the plugin
    Args:
    Returns:
        dict: plugin information
    Raises:
    """
    return {
        'name': PLUGIN_NAME,
        'version': '1.9.2',
        'mode': 'none',
        'type': 'filter',
        'interface': '1.0',
        'config': _DEFAULT_CONFIG
    }


def plugin_init(config, ingest_ref, callback):
    """ Initialise the plugin
    Args:
        config:     JSON configuration document for the Filter plugin configuration category
        ingest_ref: filter ingest reference
        callback:   filter callback
    Returns:
        data:       JSON object to be used in future calls to the plugin
    Raises:
    """
    data = copy.deepcopy(config)
    data['callback'] = callback
    data['ingestRef'] = ingest_ref
    return data


def plugin_reconfigure(handle, new_config):
    """ Reconfigures the plugin

    Args:
        handle:     handle returned by the plugin initialisation call
        new_config: JSON object representing the new configuration category for the category
    Returns:
        new_handle: new handle to be used in the future calls
    """
    _LOGGER.info("Old config {} \n new config {} for {} plugin ".format(handle, new_config, PLUGIN_NAME))
    new_handle = copy.deepcopy(new_config)
    new_handle['callback'] = handle['callback']
    new_handle['ingestRef'] = handle['ingestRef']
    return new_handle


def plugin_shutdown(handle):
    """ Shutdowns the plugin doing required cleanup.

    Args:
        handle: handle returned by the plugin initialisation call
    Returns:
    """
    handle['callback'] = None
    handle['ingestRef'] = None
    _LOGGER.info('{} filter plugin shutdown.'.format(PLUGIN_NAME))


def plugin_ingest(handle, data):
    """ Modify readings data and pass it onward

    Args:
        handle: handle returned by the plugin initialisation call
        data:   readings data
    """
    if handle['enable']['value'] == 'false':
        # Filter not enabled, just pass data onwards
        filter_ingest.filter_ingest_callback(handle['callback'],  handle['ingestRef'], data)
        return

    # Filter is enabled: compute for each reading
    processed_data = []
    for element in data:
        processed_data.append(convert_to_dp(handle, element))
    _LOGGER.debug("processed data {}".format(processed_data))
    # Pass data onwards
    filter_ingest.filter_ingest_callback(handle['callback'],  handle['ingestRef'], processed_data)

    _LOGGER.debug("{} filter ingest done".format(PLUGIN_NAME))


def convert_to_dp(handle, reading):
    """ convert iec 104 data object to a simple datapoint
    Args:
        reading:       A reading object
    Returns:
        new_dict:          A processed dictionary
    """
    _LOGGER.debug("reading {}".format(reading))

    '''new_dict = {
        'asset': reading['asset'],
        'timestamp': utils.local_timestamp(),
        'readings': {"asdu_io_val": reading['do_value']}
    }'''

    '''new_dict = {
        'asset': reading['asset'],
        'timestamp': utils.local_timestamp(),
        'readings': {"asdu_io_val": random.random()}
    }'''

    return new_dict
