# -*- coding: utf-8 -*-

"""Top-level package for Hostinger Hevents Client."""

__author__ = """Edgaras Lukosevicius"""
__email__ = 'edgaras.lukosevicius@hostinger.com'
__version__ = '0.1.0'

import logging
from hostinger_hevents.event import Event
from hostinger_hevents.hevents_client import HeventsClient

__all__ = ('Event', 'HeventsClient')

logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format=('%(asctime)s %(levelname)-10s %(name)s.%(funcName)s() line %(lineno)d : %(message)s')
)
