"""Fixtures for Brink Flair tests."""

import pytest

from homeassistant.components.brink_flair.const import (
    CONF_CONNECTION,
    CONF_UNIT_ID,
    DOMAIN,
)

from tests.common import MockConfigEntry

TEST_CONNECTION_ENTRY_ID = "modbus-connection-entry"
TEST_UNIT_ID = 20
TEST_UNIQUE_ID = f"{TEST_CONNECTION_ENTRY_ID}_{TEST_UNIT_ID}"


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return a Brink Flair config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_CONNECTION: TEST_CONNECTION_ENTRY_ID,
            CONF_UNIT_ID: TEST_UNIT_ID,
        },
        unique_id=TEST_UNIQUE_ID,
        title="Brink Flair",
    )
