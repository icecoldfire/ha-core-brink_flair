"""Number platform for Brink Flair."""

from dataclasses import dataclass

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
)
from homeassistant.const import EntityCategory, PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import BrinkFlairConfigEntry, BrinkFlairCoordinator
from .entity import BrinkFlairEntity

MAX_REQUESTED_FLOW_RATE = 5 * 65


@dataclass(frozen=True, kw_only=True)
class BrinkFlairNumberDescription(NumberEntityDescription):
    """Describe a Brink Flair number."""

    component: str
    attribute: str


NUMBERS: tuple[BrinkFlairNumberDescription, ...] = (
    BrinkFlairNumberDescription(
        key="bypass_settings_temperature_from_dwelling",
        name="Bypass dwelling temperature",
        component="bypass_settings",
        attribute="temperature_from_dwelling",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=0,
        native_max_value=100,
        native_step=0.1,
        entity_category=EntityCategory.CONFIG,
    ),
    BrinkFlairNumberDescription(
        key="bypass_settings_temperature_from_outside",
        name="Bypass outside temperature",
        component="bypass_settings",
        attribute="temperature_from_outside",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=0,
        native_max_value=100,
        native_step=0.1,
        entity_category=EntityCategory.CONFIG,
    ),
    BrinkFlairNumberDescription(
        key="bypass_settings_temperature_hysteresis",
        name="Bypass temperature hysteresis",
        component="bypass_settings",
        attribute="temperature_hysteresis",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=0,
        native_max_value=100,
        native_step=0.1,
        entity_category=EntityCategory.CONFIG,
    ),
    BrinkFlairNumberDescription(
        key="geo_heat_exchanger_minimum_temperature",
        name="Geothermal minimum temperature",
        component="geo_heat_exchanger",
        attribute="minimum_temperature",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=0,
        native_max_value=10,
        native_step=0.1,
        entity_category=EntityCategory.CONFIG,
    ),
    BrinkFlairNumberDescription(
        key="geo_heat_exchanger_maximum_temperature",
        name="Geothermal maximum temperature",
        component="geo_heat_exchanger",
        attribute="maximum_temperature",
        device_class=NumberDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_min_value=15,
        native_max_value=40,
        native_step=0.1,
        entity_category=EntityCategory.CONFIG,
    ),
    BrinkFlairNumberDescription(
        key="imbalance_offset_supply",
        name="Supply imbalance offset",
        component="imbalance",
        attribute="offset_supply",
        native_unit_of_measurement=PERCENTAGE,
        native_min_value=-15,
        native_max_value=15,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
    ),
    BrinkFlairNumberDescription(
        key="imbalance_offset_exhaust",
        name="Exhaust imbalance offset",
        component="imbalance",
        attribute="offset_exhaust",
        native_unit_of_measurement=PERCENTAGE,
        native_min_value=-15,
        native_max_value=15,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
    ),
    BrinkFlairNumberDescription(
        key="remote_control_requested_flow_rate",
        name="Requested flow rate",
        component="remote_control",
        attribute="requested_flow_rate",
        native_unit_of_measurement="m³/h",
        native_min_value=0,
        native_max_value=MAX_REQUESTED_FLOW_RATE,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: BrinkFlairConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Brink Flair numbers."""
    async_add_entities(
        BrinkFlairNumber(entry.runtime_data, description) for description in NUMBERS
    )


class BrinkFlairNumber(BrinkFlairEntity, NumberEntity):
    """A writable Brink Flair number."""

    entity_description: BrinkFlairNumberDescription

    def __init__(
        self,
        coordinator: BrinkFlairCoordinator,
        description: BrinkFlairNumberDescription,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator, description.key, description.component)
        self.entity_description = description

    @property
    def native_value(self) -> float | int | None:
        """Return the current numeric value."""
        return getattr(self._subsystem, self.entity_description.attribute)

    async def async_set_native_value(self, value: float) -> None:
        """Set the numeric value."""
        # The unit accepts 0 or 50..maximum supported flow rate, but NumberEntity
        # ranges are continuous.
        await self._subsystem.write(self.entity_description.attribute, value)
        await self.coordinator.async_request_refresh()
