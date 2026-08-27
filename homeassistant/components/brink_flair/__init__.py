"""The Brink Flair integration."""

from brink_flair_modbus import BrinkFlair

from homeassistant.components.modbus_connection import async_get_unit
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_CONNECTION, CONF_UNIT_ID
from .coordinator import BrinkFlairConfigEntry, BrinkFlairCoordinator

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
]


async def async_setup_entry(
    hass: HomeAssistant, entry: BrinkFlairConfigEntry
) -> bool:
    """Set up Brink Flair from a config entry."""
    unit = async_get_unit(
        hass, entry.data[CONF_CONNECTION], int(entry.data[CONF_UNIT_ID])
    )
    device = BrinkFlair(unit)
    coordinator = BrinkFlairCoordinator(hass, entry, device)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    entry.async_on_unload(
        unit.on_connection_lost(
            lambda: hass.config_entries.async_schedule_reload(entry.entry_id)
        )
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: BrinkFlairConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
