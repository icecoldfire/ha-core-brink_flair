"""Binary sensors for Brink Flair."""

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import BrinkFlairConfigEntry, BrinkFlairCoordinator
from .entity import BrinkFlairEntity


@dataclass(frozen=True, kw_only=True)
class BrinkFlairBinarySensorDescription(BinarySensorEntityDescription):
    """Describe a Brink Flair binary sensor."""

    component: str
    attribute: str


BINARY_SENSORS: tuple[BrinkFlairBinarySensorDescription, ...] = (
    BrinkFlairBinarySensorDescription(
        key="filter_is_dirty",
        name="Filter",
        component="filter",
        attribute="is_dirty",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: BrinkFlairConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Brink Flair binary sensors."""
    async_add_entities(
        BrinkFlairBinarySensor(entry.runtime_data, description)
        for description in BINARY_SENSORS
    )


class BrinkFlairBinarySensor(BrinkFlairEntity, BinarySensorEntity):
    """A Brink Flair binary sensor."""

    entity_description: BrinkFlairBinarySensorDescription

    def __init__(
        self,
        coordinator: BrinkFlairCoordinator,
        description: BrinkFlairBinarySensorDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator, description.key, description.component)
        self.entity_description = description

    @property
    def is_on(self) -> bool | None:
        """Return whether the sensor is on."""
        return getattr(self._subsystem, self.entity_description.attribute)
