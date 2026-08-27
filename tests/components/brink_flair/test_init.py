"""Tests for Brink Flair setup."""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.core import HomeAssistant

from homeassistant.components.brink_flair import async_setup_entry, async_unload_entry
from tests.common import MockConfigEntry


async def test_async_setup_entry(
    hass: HomeAssistant, mock_config_entry: MockConfigEntry
) -> None:
    """Test setting up the integration."""
    mock_config_entry.add_to_hass(hass)

    unit = MagicMock()
    unit.on_connection_lost.return_value = lambda: None
    mock_device = SimpleNamespace(identity=SimpleNamespace(serial_number="123456789012"))

    with (
        patch(
            "homeassistant.components.brink_flair.async_get_unit",
            return_value=unit,
        ),
        patch(
            "homeassistant.components.brink_flair.BrinkFlair",
            return_value=mock_device,
        ),
        patch(
            "homeassistant.components.brink_flair.BrinkFlairCoordinator.async_config_entry_first_refresh",
            new=AsyncMock(),
        ) as mock_first_refresh,
        patch.object(
            hass.config_entries,
            "async_forward_entry_setups",
            AsyncMock(),
        ) as mock_forward_entry_setups,
    ):
        assert await async_setup_entry(hass, mock_config_entry)

    assert mock_config_entry.runtime_data is not None
    unit.on_connection_lost.assert_called_once()
    mock_first_refresh.assert_awaited_once()
    mock_forward_entry_setups.assert_awaited_once()


async def test_async_unload_entry(
    hass: HomeAssistant, mock_config_entry: MockConfigEntry
) -> None:
    """Test unloading the integration."""
    with patch.object(
        hass.config_entries,
        "async_unload_platforms",
        AsyncMock(return_value=True),
    ) as mock_unload_platforms:
        assert await async_unload_entry(hass, mock_config_entry)

    mock_unload_platforms.assert_awaited_once()
