"""Tests for the Brink Flair config flow."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from homeassistant.components.brink_flair.const import (
    CONF_CONNECTION,
    CONF_UNIT_ID,
    DOMAIN,
)
from homeassistant.config_entries import SOURCE_USER
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from .conftest import TEST_CONNECTION_ENTRY_ID, TEST_UNIT_ID, TEST_UNIQUE_ID
from tests.common import MockConfigEntry

USER_INPUT = {
    CONF_CONNECTION: TEST_CONNECTION_ENTRY_ID,
    CONF_UNIT_ID: TEST_UNIT_ID,
}


async def test_user_flow_creates_entry(hass: HomeAssistant) -> None:
    """Test a successful user flow."""
    with (
        patch(
            "homeassistant.components.brink_flair.config_flow.async_get_unit",
            return_value=MagicMock(),
        ),
        patch(
            "homeassistant.components.brink_flair.config_flow.BrinkFlair"
        ) as mock_device_cls,
    ):
        device = mock_device_cls.return_value
        device.identity.async_update = AsyncMock()
        device.identity.appliance_type_code = 1

        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_USER},
            data=USER_INPUT,
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Brink Flair"
    assert result["data"] == USER_INPUT


@pytest.mark.parametrize(
    ("side_effect", "appliance_type_code"),
    [
        pytest.param(OSError, None, id="os-error"),
        pytest.param(ValueError, None, id="value-error"),
        pytest.param(None, None, id="no-identity"),
    ],
)
async def test_user_flow_shows_error_on_failure(
    hass: HomeAssistant,
    side_effect: type[Exception] | None,
    appliance_type_code: int | None,
) -> None:
    """Test connection failures keep the flow on the user step."""
    with (
        patch(
            "homeassistant.components.brink_flair.config_flow.async_get_unit",
            return_value=MagicMock(),
        ),
        patch(
            "homeassistant.components.brink_flair.config_flow.BrinkFlair"
        ) as mock_device_cls,
    ):
        device = mock_device_cls.return_value
        device.identity.async_update = AsyncMock(side_effect=side_effect)
        device.identity.appliance_type_code = appliance_type_code

        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_USER},
            data=USER_INPUT,
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}


async def test_user_flow_aborts_if_already_configured(hass: HomeAssistant) -> None:
    """Test duplicate config entries are rejected."""
    existing_entry = MockConfigEntry(
        domain=DOMAIN,
        data=USER_INPUT,
        unique_id=TEST_UNIQUE_ID,
        title="Brink Flair",
    )
    existing_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
        data=USER_INPUT,
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
