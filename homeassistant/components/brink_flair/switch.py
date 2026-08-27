"""Switch platform for Brink Flair."""

from dataclasses import dataclass

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import BrinkFlairConfigEntry, BrinkFlairCoordinator
from .entity import BrinkFlairEntity


@dataclass(frozen=True, kw_only=True)
class BrinkFlairSwitchDescription(SwitchEntityDescription):
    """Describe a Brink Flair switch."""

    component: str
    attribute: str


SWITCHES: tuple[BrinkFlairSwitchDescription, ...] = (
    BrinkFlairSwitchDescription(
        key="co2_settings_enabled",
        name="CO2 control",
        component="co2_settings",
        attribute="enabled",
        entity_category=EntityCategory.CONFIG,
    ),
    # Only meaningful on units fitted with the optional Plus PCB.
    BrinkFlairSwitchDescription(
        key="geo_heat_exchanger_enabled",
        name="Geothermal heat exchanger",
        component="geo_heat_exchanger",
        attribute="enabled",
        entity_category=EntityCategory.CONFIG,
    ),
    BrinkFlairSwitchDescription(
        key="imbalance_permitted",
        name="Imbalance permitted",
        component="imbalance",
        attribute="permitted",
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: BrinkFlairConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Brink Flair switches."""
    async_add_entities(
        BrinkFlairSwitch(entry.runtime_data, description) for description in SWITCHES
    )


class BrinkFlairSwitch(BrinkFlairEntity, SwitchEntity):
    """A writable Brink Flair switch."""

    entity_description: BrinkFlairSwitchDescription

    def __init__(
        self,
        coordinator: BrinkFlairCoordinator,
        description: BrinkFlairSwitchDescription,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, description.key, description.component)
        self.entity_description = description

    @property
    def is_on(self) -> bool | None:
        """Return whether the switch is enabled."""
        return getattr(self._subsystem, self.entity_description.attribute)

    async def async_turn_on(self, **kwargs: object) -> None:
        """Enable the setting."""
        await self._subsystem.write(self.entity_description.attribute, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: object) -> None:
        """Disable the setting."""
        await self._subsystem.write(self.entity_description.attribute, False)
        await self.coordinator.async_request_refresh()
