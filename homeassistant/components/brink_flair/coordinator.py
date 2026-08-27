"""DataUpdateCoordinator for Brink Flair."""

import logging

from brink_flair_modbus import BrinkFlair
from modbus_connection import ModbusError

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

BrinkFlairConfigEntry = ConfigEntry["BrinkFlairCoordinator"]


class BrinkFlairCoordinator(DataUpdateCoordinator[BrinkFlair]):
    """Refresh Brink Flair data on a schedule."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: BrinkFlairConfigEntry,
        device: BrinkFlair,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            config_entry=entry,
            update_interval=SCAN_INTERVAL,
        )
        self.device = device

    async def _async_update_data(self) -> BrinkFlair:
        """Fetch data from the device."""
        try:
            await self.device.async_update()
        except ModbusError as err:
            raise UpdateFailed(f"Error communicating with Brink Flair: {err}") from err
        return self.device
