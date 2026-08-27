"""Config flow for Brink Flair."""

from typing import Any

from brink_flair_modbus import BrinkFlair, DEFAULT_SLAVE_ADDRESS
from modbus_connection import ModbusError
import voluptuous as vol

from homeassistant.components.modbus_connection import (
    ConnectionNotReady,
    async_get_unit,
)
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.selector import (
    ConfigEntrySelector,
    ConfigEntrySelectorConfig,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)

from .const import CONF_CONNECTION, CONF_UNIT_ID, DOMAIN

STEP_USER = vol.Schema(
    {
        vol.Required(CONF_CONNECTION): ConfigEntrySelector(
            ConfigEntrySelectorConfig(integration="modbus_connection")
        ),
        vol.Required(CONF_UNIT_ID, default=DEFAULT_SLAVE_ADDRESS): NumberSelector(
            NumberSelectorConfig(min=1, max=247, step=1, mode=NumberSelectorMode.BOX)
        ),
    }
)


class BrinkFlairConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Brink Flair."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Pick the shared Modbus connection and unit address."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input[CONF_CONNECTION]}_{int(user_input[CONF_UNIT_ID])}"
            )
            self._abort_if_unique_id_configured()

            if not await self._async_can_connect(user_input):
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title="Brink Flair", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER,
            errors=errors,
        )

    async def _async_can_connect(self, data: dict[str, Any]) -> bool:
        """Probe the selected unit."""
        try:
            unit = async_get_unit(
                self.hass, data[CONF_CONNECTION], int(data[CONF_UNIT_ID])
            )
            device = BrinkFlair(unit)
            await device.identity.async_update()
        except (ConnectionNotReady, ModbusError, OSError, ValueError):
            return False
        return device.identity.appliance_type_code is not None
