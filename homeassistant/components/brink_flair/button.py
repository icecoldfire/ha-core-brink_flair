"""Button platform for Brink Flair."""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from homeassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import BrinkFlairConfigEntry, BrinkFlairCoordinator
from .entity import BrinkFlairEntity


@dataclass(frozen=True, kw_only=True)
class BrinkFlairButtonDescription(ButtonEntityDescription):
    """Describe a Brink Flair button."""

    component: str
    press_action: Callable[[object], Awaitable[None]]


BUTTONS: tuple[BrinkFlairButtonDescription, ...] = (
    BrinkFlairButtonDescription(
        key="remote_control_reset_filter_warning",
        name="Reset filter warning",
        component="remote_control",
        press_action=lambda subsystem: subsystem.async_reset_filter_warning(),
        entity_category=EntityCategory.CONFIG,
    ),
    BrinkFlairButtonDescription(
        key="remote_control_reset_appliance",
        name="Reset appliance controller",
        component="remote_control",
        press_action=lambda subsystem: subsystem.async_reset_appliance(),
        device_class=ButtonDeviceClass.RESTART,
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: BrinkFlairConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Brink Flair buttons."""
    async_add_entities(
        BrinkFlairButton(entry.runtime_data, description) for description in BUTTONS
    )


class BrinkFlairButton(BrinkFlairEntity, ButtonEntity):
    """A Brink Flair action button."""

    entity_description: BrinkFlairButtonDescription

    def __init__(
        self,
        coordinator: BrinkFlairCoordinator,
        description: BrinkFlairButtonDescription,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator, description.key, description.component)
        self.entity_description = description

    async def async_press(self) -> None:
        """Press the button."""
        await self.entity_description.press_action(self._subsystem)
        await self.coordinator.async_request_refresh()
