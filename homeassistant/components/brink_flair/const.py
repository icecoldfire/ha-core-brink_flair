"""Constants for the Brink Flair integration."""

from datetime import timedelta
from typing import Final

from brink_flair_modbus import DEFAULT_SLAVE_ADDRESS

DOMAIN: Final = "brink_flair"

CONF_CONNECTION: Final = "connection_entry_id"
CONF_UNIT_ID: Final = "unit_id"

SCAN_INTERVAL: Final = timedelta(seconds=30)
