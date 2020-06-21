"""Global variables, for access by all modules"""

import logging
from botutils import MasterState

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S'
)


def init_master_state():
    """Initialize master state. Must only be used by main.py"""
    global master_state
    master_state = MasterState()


def init_client():
    """Initialize client. Must only be used by main.py"""
    global client
    client = None
