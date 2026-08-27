"""Sensor platform for Brink Flair."""

from dataclasses import dataclass
from enum import IntEnum

from brink_flair_modbus import BypassStatus, PreheaterStatus, ResetOutcome

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    CONCENTRATION_PARTS_PER_MILLION,
    EntityCategory,
    PERCENTAGE,
    UnitOfPressure,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import BrinkFlairConfigEntry, BrinkFlairCoordinator
from .entity import BrinkFlairEntity


def _enum_options(enum_type: type[IntEnum]) -> list[str]:
    """Return Home Assistant enum sensor options."""
    return [member.name.lower() for member in enum_type]


@dataclass(frozen=True, kw_only=True)
class BrinkFlairSensorDescription(SensorEntityDescription):
    """Describe a Brink Flair sensor."""

    component: str
    attribute: str


SENSORS: tuple[BrinkFlairSensorDescription, ...] = (
    BrinkFlairSensorDescription(
        key="identity_serial_number",
        name="Serial number",
        component="identity",
        attribute="serial_number",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    BrinkFlairSensorDescription(
        key="supply_fan_current_pressure",
        name="Supply fan pressure",
        component="supply_fan",
        attribute="current_pressure",
        device_class=SensorDeviceClass.PRESSURE,
        native_unit_of_measurement=UnitOfPressure.PA,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BrinkFlairSensorDescription(
        key="supply_fan_current_flow",
        name="Supply fan flow",
        component="supply_fan",
        attribute="current_flow",
        native_unit_of_measurement="m³/h",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BrinkFlairSensorDescription(
        key="supply_fan_mass_flow",
        name="Supply fan mass flow",
        component="supply_fan",
        attribute="mass_flow",
        native_unit_of_measurement="kg/h",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BrinkFlairSensorDescription(
        key="supply_fan_fan_speed",
        name="Supply fan speed",
        component="supply_fan",
        attribute="fan_speed",
        native_unit_of_measurement="RPM",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BrinkFlairSensorDescription(
        key="supply_fan_anemometer_speed",
        name="Supply fan anemometer speed",
        component="supply_fan",
        attribute="anemometer_speed",
        native_unit_of_measurement="RPM",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    BrinkFlairSensorDescription(
        key="supply_fan_temperature",
        name="Supply fan temperature",
        component="supply_fan",
        attribute="temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BrinkFlairSensorDescription(
        key="supply_fan_relative_humidity",
        name="Supply fan humidity",
        component="supply_fan",
        attribute="relative_humidity",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BrinkFlairSensorDescription(
        key="supply_fan_status",
        name="Supply fan status",
        component="supply_fan",
        attribute="status",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    BrinkFlairSensorDescription(
        key="exhaust_fan_current_pressure",
        name="Exhaust fan pressure",
        component="exhaust_fan",
        attribute="current_pressure",
        device_class=SensorDeviceClass.PRESSURE,
        native_unit_of_measurement=UnitOfPressure.PA,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BrinkFlairSensorDescription(
        key="exhaust_fan_current_flow",
        name="Exhaust fan flow",
        component="exhaust_fan",
        attribute="current_flow",
        native_unit_of_measurement="m³/h",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BrinkFlairSensorDescription(
        key="exhaust_fan_mass_flow",
        name="Exhaust fan mass flow",
        component="exhaust_fan",
        attribute="mass_flow",
        native_unit_of_measurement="kg/h",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BrinkFlairSensorDescription(
        key="exhaust_fan_fan_speed",
        name="Exhaust fan speed",
        component="exhaust_fan",
        attribute="fan_speed",
        native_unit_of_measurement="RPM",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BrinkFlairSensorDescription(
        key="exhaust_fan_anemometer_speed",
        name="Exhaust fan anemometer speed",
        component="exhaust_fan",
        attribute="anemometer_speed",
        native_unit_of_measurement="RPM",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    BrinkFlairSensorDescription(
        key="exhaust_fan_temperature",
        name="Exhaust fan temperature",
        component="exhaust_fan",
        attribute="temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BrinkFlairSensorDescription(
        key="exhaust_fan_relative_humidity",
        name="Exhaust fan humidity",
        component="exhaust_fan",
        attribute="relative_humidity",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BrinkFlairSensorDescription(
        key="exhaust_fan_status",
        name="Exhaust fan status",
        component="exhaust_fan",
        attribute="status",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    BrinkFlairSensorDescription(
        key="bypass_status_status",
        name="Bypass status",
        component="bypass_status",
        attribute="status",
        device_class=SensorDeviceClass.ENUM,
        options=_enum_options(BypassStatus),
    ),
    BrinkFlairSensorDescription(
        key="bypass_status_step_position",
        name="Bypass step position",
        component="bypass_status",
        attribute="step_position",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    BrinkFlairSensorDescription(
        key="preheater_status",
        name="Preheater status",
        component="preheater",
        attribute="status",
        device_class=SensorDeviceClass.ENUM,
        options=_enum_options(PreheaterStatus),
    ),
    BrinkFlairSensorDescription(
        key="preheater_capacity",
        name="Preheater capacity",
        component="preheater",
        attribute="capacity",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BrinkFlairSensorDescription(
        key="frost_protection_status",
        name="Frost protection status",
        component="frost_protection",
        attribute="status",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    BrinkFlairSensorDescription(
        key="frost_protection_heater_power",
        name="Frost protection heater power",
        component="frost_protection",
        attribute="heater_power",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    BrinkFlairSensorDescription(
        key="frost_protection_fan_reduction",
        name="Frost protection fan reduction",
        component="frost_protection",
        attribute="fan_reduction",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    BrinkFlairSensorDescription(
        key="sensors_ntc1_temperature",
        name="NTC1 temperature",
        component="sensors",
        attribute="ntc1_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BrinkFlairSensorDescription(
        key="sensors_ntc2_temperature",
        name="NTC2 temperature",
        component="sensors",
        attribute="ntc2_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BrinkFlairSensorDescription(
        key="sensors_rht_humidity",
        name="RHT humidity",
        component="sensors",
        attribute="rht_humidity",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BrinkFlairSensorDescription(
        key="sensors_flow_switch_position",
        name="Flow switch position",
        component="sensors",
        attribute="flow_switch_position",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    BrinkFlairSensorDescription(
        key="co2_sensors_sensor_1",
        name="CO2 sensor 1",
        component="co2_sensors",
        attribute="sensor_1",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BrinkFlairSensorDescription(
        key="co2_sensors_sensor_2",
        name="CO2 sensor 2",
        component="co2_sensors",
        attribute="sensor_2",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    BrinkFlairSensorDescription(
        key="co2_sensors_sensor_3",
        name="CO2 sensor 3",
        component="co2_sensors",
        attribute="sensor_3",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    BrinkFlairSensorDescription(
        key="co2_sensors_sensor_4",
        name="CO2 sensor 4",
        component="co2_sensors",
        attribute="sensor_4",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    BrinkFlairSensorDescription(
        key="ventilation_active_function",
        name="Active function",
        component="ventilation",
        attribute="active_function",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    BrinkFlairSensorDescription(
        key="ventilation_fan_control_type",
        name="Fan control type",
        component="ventilation",
        attribute="fan_control_type",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    BrinkFlairSensorDescription(
        key="ventilation_ventilation_mode",
        name="Ventilation mode",
        component="ventilation",
        attribute="ventilation_mode",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    BrinkFlairSensorDescription(
        key="remote_control_filter_warning_reset_outcome",
        name="Filter warning reset outcome",
        component="remote_control",
        attribute="filter_warning_reset_outcome",
        device_class=SensorDeviceClass.ENUM,
        options=_enum_options(ResetOutcome),
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    BrinkFlairSensorDescription(
        key="remote_control_appliance_reset_outcome",
        name="Appliance reset outcome",
        component="remote_control",
        attribute="appliance_reset_outcome",
        device_class=SensorDeviceClass.ENUM,
        options=_enum_options(ResetOutcome),
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: BrinkFlairConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Brink Flair sensors."""
    async_add_entities(
        BrinkFlairSensor(entry.runtime_data, description) for description in SENSORS
    )


class BrinkFlairSensor(BrinkFlairEntity, SensorEntity):
    """A single Brink Flair sensor."""

    entity_description: BrinkFlairSensorDescription

    def __init__(
        self,
        coordinator: BrinkFlairCoordinator,
        description: BrinkFlairSensorDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, description.key, description.component)
        self.entity_description = description

    @property
    def native_value(self) -> object:
        """Return the current value."""
        value = getattr(self._subsystem, self.entity_description.attribute)
        if isinstance(value, IntEnum):
            return value.name.lower()
        return value
