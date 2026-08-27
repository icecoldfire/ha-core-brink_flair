"""Tests for Brink Flair sensors."""

from types import SimpleNamespace
from unittest.mock import Mock

from brink_flair_modbus import BypassStatus

from homeassistant.components.brink_flair.sensor import (
    BrinkFlairSensor,
    BrinkFlairSensorDescription,
)
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import UnitOfPressure


def test_sensor_maps_enum_to_lowercase_name() -> None:
    """Test enum sensors expose lowercase option names."""
    coordinator = Mock()
    coordinator.config_entry = SimpleNamespace(entry_id="entry-id")
    coordinator.device = SimpleNamespace(
        identity=SimpleNamespace(serial_number="123456789012"),
        bypass_status=SimpleNamespace(status=BypassStatus.OPEN),
    )

    entity = BrinkFlairSensor(
        coordinator,
        BrinkFlairSensorDescription(
            key="bypass_status_status",
            name="Bypass status",
            component="bypass_status",
            attribute="status",
            device_class=SensorDeviceClass.ENUM,
            options=["initialize", "opening", "open", "closing", "closed", "error"],
        ),
    )

    assert entity.native_value == "open"


def test_sensor_returns_numeric_value() -> None:
    """Test measurement sensors return their raw numeric state."""
    coordinator = Mock()
    coordinator.config_entry = SimpleNamespace(entry_id="entry-id")
    coordinator.device = SimpleNamespace(
        identity=SimpleNamespace(serial_number="123456789012"),
        supply_fan=SimpleNamespace(current_pressure=125.4),
    )

    entity = BrinkFlairSensor(
        coordinator,
        BrinkFlairSensorDescription(
            key="supply_fan_current_pressure",
            name="Supply fan pressure",
            component="supply_fan",
            attribute="current_pressure",
            device_class=SensorDeviceClass.PRESSURE,
            native_unit_of_measurement=UnitOfPressure.PA,
        ),
    )

    assert entity.native_value == 125.4
