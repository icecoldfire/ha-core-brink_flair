"""Base entity for Brink Flair."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import BrinkFlairCoordinator


class BrinkFlairEntity(CoordinatorEntity[BrinkFlairCoordinator]):
    """Common identity and device info for Brink Flair entities."""

    _attr_has_entity_name = True

    def __init__(
        self, coordinator: BrinkFlairCoordinator, key: str, component: str
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._component = component
        entry = coordinator.config_entry
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            manufacturer="Brink",
            model="Flair",
            name="Brink Flair",
            serial_number=coordinator.device.identity.serial_number,
        )

    @property
    def _subsystem(self) -> object:
        """Return the library subsystem used by this entity."""
        return getattr(self.coordinator.device, self._component)
