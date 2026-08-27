"""Select platform for Brink Flair."""

from dataclasses import dataclass
from enum import IntEnum

from brink_flair_modbus import BypassMode, ModbusControlMode, SwitchPosition

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import BrinkFlairConfigEntry, BrinkFlairCoordinator
from .entity import BrinkFlairEntity


def _enum_options(enum_type: type[IntEnum]) -> list[str]:
    """Return select options for an enum."""
    return [member.name.lower() for member in enum_type]


@dataclass(frozen=True, kw_only=True)
class BrinkFlairSelectDescription(SelectEntityDescription):
    """Describe a Brink Flair select entity."""

    component: str
    attribute: str
    enum_type: type[IntEnum]


SELECTS: tuple[BrinkFlairSelectDescription, ...] = (
    BrinkFlairSelectDescription(
        key="bypass_settings_mode",
        name="Bypass mode",
        component="bypass_settings",
        attribute="mode",
        enum_type=BypassMode,
        options=_enum_options(BypassMode),
        entity_category=EntityCategory.CONFIG,
    ),
    BrinkFlairSelectDescription(
        key="remote_control_control_mode",
        name="Remote control mode",
        component="remote_control",
        attribute="control_mode",
        enum_type=ModbusControlMode,
        options=_enum_options(ModbusControlMode),
        entity_category=EntityCategory.CONFIG,
    ),
    BrinkFlairSelectDescription(
        key="remote_control_requested_switch_position",
        name="Requested switch position",
        component="remote_control",
        attribute="requested_switch_position",
        enum_type=SwitchPosition,
        options=_enum_options(SwitchPosition),
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: BrinkFlairConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Brink Flair selects."""
    async_add_entities(
        BrinkFlairSelect(entry.runtime_data, description) for description in SELECTS
    )


class BrinkFlairSelect(BrinkFlairEntity, SelectEntity):
    """A writable Brink Flair select."""

    entity_description: BrinkFlairSelectDescription

    def __init__(
        self,
        coordinator: BrinkFlairCoordinator,
        description: BrinkFlairSelectDescription,
    ) -> None:
        """Initialize the select."""
        super().__init__(coordinator, description.key, description.component)
        self.entity_description = description

    @property
    def current_option(self) -> str | None:
        """Return the current option."""
        value = getattr(self._subsystem, self.entity_description.attribute)
        if value is None:
            return None
        return value.name.lower()

    async def async_select_option(self, option: str) -> None:
        """Set the selected option."""
        await self._subsystem.write(
            self.entity_description.attribute,
            self.entity_description.enum_type[option.upper()],
        )
        await self.coordinator.async_request_refresh()
