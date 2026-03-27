"""Support for PocketSmith sensors."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN, CURRENCY_SYMBOLS
from .coordinator import PocketSmithDataUpdateCoordinator

# Threshold in hours after which a feed is considered stale
FEED_STALE_HOURS = 24


def _is_feed_account(ta: dict) -> bool:
    """Return True if this transaction account is connected via a live data feed."""
    return (
        not ta.get("offline", True)
        and ta.get("data_feeds_connection_id") is not None
    )


def _parse_iso(ts: str | None) -> datetime | None:
    """Parse an ISO 8601 timestamp string to an aware datetime, or return None."""
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def _hours_since(ts: str | None) -> float | None:
    """Return decimal hours elapsed since an ISO 8601 timestamp, or None."""
    dt = _parse_iso(ts)
    if dt is None:
        return None
    delta = dt_util.now() - dt
    return round(delta.total_seconds() / 3600, 1)


def _derive_feed_status(ta: dict) -> str:
    """Derive a feed health status from the available API fields.

    The PocketSmith API does not expose a feed_status field directly.
    We infer status from:
      - offline: True  → not a feed account, should not be called
      - updated_at staleness → 'active' if recent, 'stale' if > FEED_STALE_HOURS
    """
    if not _is_feed_account(ta):
        return "offline"

    hours = _hours_since(ta.get("updated_at"))
    if hours is None:
        return "unknown"
    if hours > FEED_STALE_HOURS:
        return "stale"
    return "active"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up PocketSmith sensor based on a config entry."""
    coordinator: PocketSmithDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = []

    if coordinator.data and "transaction_accounts" in coordinator.data:
        for ta_id, ta in coordinator.data["transaction_accounts"].items():
            entities.append(
                PocketSmithAccountBalanceSensor(
                    coordinator=coordinator,
                    account_id=ta_id,
                )
            )

            entities.append(
                PocketSmithTransactionHistorySensor(
                    coordinator=coordinator,
                    ta_id=ta_id,
                )
            )

            # Only create a feed status sensor for live feed accounts
            if _is_feed_account(ta):
                entities.append(
                    PocketSmithFeedStatusSensor(
                        coordinator=coordinator,
                        ta_id=ta_id,
                    )
                )

    entities.append(PocketSmithUncategorizedSensor(coordinator=coordinator))

    async_add_entities(entities)


class PocketSmithAccountBalanceSensor(CoordinatorEntity, SensorEntity):
    """Sensor for PocketSmith account balance."""

    _attr_has_entity_name = False
    _attr_state_class = SensorStateClass.TOTAL

    def __init__(
        self,
        coordinator: PocketSmithDataUpdateCoordinator,
        account_id: str,
    ) -> None:
        """Initialize the account balance sensor."""
        super().__init__(coordinator)
        self.account_id = account_id

        account = coordinator.data.get("transaction_accounts", {}).get(account_id, {})

        institution_data = account.get("institution", {})
        if isinstance(institution_data, dict):
            institution = institution_data.get("title", "Unknown")
        else:
            institution = str(institution_data) if institution_data else "Unknown"

        account_name = account.get("name", "Account {}".format(account_id))

        self._attr_unique_id = "{}_{}_account_{}".format(DOMAIN, coordinator.username, account_id)
        self._attr_name = "PocketSmith {} {} {}".format(coordinator.username, institution, account_name)

        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, coordinator.entry_id)},
            name="PocketSmith",
            manufacturer="PocketSmith",
        )

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor (current balance)."""
        account = self.coordinator.data.get("transaction_accounts", {}).get(self.account_id)
        if account:
            return account.get("current_balance")
        return None

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement (currency)."""
        account = self.coordinator.data.get("transaction_accounts", {}).get(self.account_id)
        if account:
            return account.get("currency_code")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        account = self.coordinator.data.get("transaction_accounts", {}).get(self.account_id, {})

        institution_data = account.get("institution", {})
        if isinstance(institution_data, dict):
            institution_name = institution_data.get("title")
        else:
            institution_name = str(institution_data) if institution_data else None

        currency_code = account.get("currency_code")
        currency_symbol = None
        if currency_code:
            currency_symbol = CURRENCY_SYMBOLS.get(currency_code.upper())

        attributes = {
            "current_balance": account.get("current_balance"),
            "currency": currency_code,
            "currency_symbol": currency_symbol,
            "institution_name": institution_name,
            "account_name": account.get("name"),
            "last_updated": dt_util.now(),
        }

        account_number = account.get("number")
        if account_number:
            attributes["account_number"] = account_number

        attributes.update({
            "account_type": account.get("type"),
            "current_balance_date": account.get("current_balance_date"),
            "current_balance_exchange_rate": account.get("current_balance_exchange_rate"),
            "safe_balance": account.get("safe_balance"),
            "safe_balance_in_base_currency": account.get("safe_balance_in_base_currency"),
            "starting_balance": account.get("starting_balance"),
            "starting_balance_date": account.get("starting_balance_date"),
        })

        # Surface feed health on the balance sensor for dashboard convenience.
        # Only populated for live feed accounts; absent for offline accounts.
        if _is_feed_account(account):
            attributes["feed_name"] = account.get("latest_feed_name")
            attributes["last_refreshed_at"] = account.get("updated_at")
            attributes["feed_status"] = _derive_feed_status(account)

        return attributes


class PocketSmithFeedStatusSensor(CoordinatorEntity, SensorEntity):
    """Dedicated sensor for the inferred feed health of a PocketSmith account.

    The PocketSmith API does not return a feed_status field. Status is derived
    from the account's updated_at timestamp:

      - 'active'  — updated_at is within the last 24 hours
      - 'stale'   — updated_at is older than 24 hours (feed may have a problem)
      - 'unknown' — updated_at is missing or unparseable

    Attributes include last_refreshed_at (the raw updated_at value) and
    hours_since_refresh (pre-calculated float) for use in automations.
    """

    _attr_has_entity_name = False

    def __init__(
        self,
        coordinator: PocketSmithDataUpdateCoordinator,
        ta_id: str,
    ) -> None:
        """Initialize the feed status sensor."""
        super().__init__(coordinator)
        self.ta_id = ta_id

        ta = coordinator.data.get("transaction_accounts", {}).get(ta_id, {})

        institution_data = ta.get("institution", {})
        if isinstance(institution_data, dict):
            institution = institution_data.get("title", "Unknown")
        else:
            institution = str(institution_data) if institution_data else "Unknown"

        account_name = ta.get("name", "Account {}".format(ta_id))

        self._attr_unique_id = "{}_{}_feed_status_{}".format(DOMAIN, coordinator.username, ta_id)
        self._attr_name = "PocketSmith {} {} {} Feed Status".format(
            coordinator.username, institution, account_name
        )

        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, coordinator.entry_id)},
            name="PocketSmith",
            manufacturer="PocketSmith",
        )

    @property
    def native_value(self) -> StateType:
        """Return the derived feed status: 'active', 'stale', or 'unknown'."""
        ta = self.coordinator.data.get("transaction_accounts", {}).get(self.ta_id, {})
        return _derive_feed_status(ta)

    @property
    def icon(self) -> str:
        """Return a contextual icon based on derived feed status."""
        status = self.native_value
        if status == "active":
            return "mdi:check-circle-outline"
        if status == "stale":
            return "mdi:alert-circle-outline"
        return "mdi:help-circle-outline"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return feed-related attributes useful for automations."""
        ta = self.coordinator.data.get("transaction_accounts", {}).get(self.ta_id, {})

        institution_data = ta.get("institution", {})
        if isinstance(institution_data, dict):
            institution_name = institution_data.get("title")
        else:
            institution_name = str(institution_data) if institution_data else None

        last_refreshed_at = ta.get("updated_at")

        return {
            "feed_name": ta.get("latest_feed_name"),
            "feed_status": _derive_feed_status(ta),
            "last_refreshed_at": last_refreshed_at,
            "hours_since_refresh": _hours_since(last_refreshed_at),
            "current_balance_date": ta.get("current_balance_date"),
            "data_feeds_connection_id": ta.get("data_feeds_connection_id"),
            "account_name": ta.get("name"),
            "institution_name": institution_name,
            "account_type": ta.get("type"),
            "last_updated": dt_util.now(),
        }


class PocketSmithTransactionHistorySensor(CoordinatorEntity, SensorEntity):
    """Sensor for PocketSmith transaction history."""

    _attr_has_entity_name = False
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: PocketSmithDataUpdateCoordinator,
        ta_id: str,
    ) -> None:
        """Initialize the transaction history sensor."""
        super().__init__(coordinator)
        self.ta_id = ta_id

        ta = coordinator.data.get("transaction_accounts", {}).get(ta_id, {})

        institution_data = ta.get("institution", {})
        if isinstance(institution_data, dict):
            institution = institution_data.get("title", "Unknown")
        else:
            institution = str(institution_data) if institution_data else "Unknown"

        account_name = ta.get("name", "Account {}".format(ta_id))

        self._attr_unique_id = "{}_{}_transactions_{}".format(DOMAIN, coordinator.username, ta_id)
        self._attr_name = "PocketSmith {} {} {} Transactions".format(coordinator.username, institution, account_name)

        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, coordinator.entry_id)},
            name="PocketSmith",
            manufacturer="PocketSmith",
        )

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor (number of transactions)."""
        transactions = self.coordinator.data.get("transactions", {}).get(self.ta_id, [])
        return len(transactions)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes with last 20 transactions."""
        transactions = self.coordinator.data.get("transactions", {}).get(self.ta_id, [])

        ta = self.coordinator.data.get("transaction_accounts", {}).get(self.ta_id, {})

        institution_data = ta.get("institution", {})
        if isinstance(institution_data, dict):
            institution_name = institution_data.get("title")
        else:
            institution_name = str(institution_data) if institution_data else None

        currency_code = ta.get("currency_code")
        currency_symbol = None
        if currency_code:
            currency_symbol = CURRENCY_SYMBOLS.get(currency_code.upper())

        attributes = {
            "account_name": ta.get("name"),
            "institution_name": institution_name,
            "currency": currency_code,
            "currency_symbol": currency_symbol,
            "transaction_count": len(transactions),
            "last_updated": dt_util.now(),
            "transactions": [],
        }

        for transaction in transactions[:20]:
            transaction_data = {
                "id": transaction.get("id"),
                "amount": transaction.get("amount"),
                "payee": transaction.get("payee"),
                "date": transaction.get("date"),
            }

            if transaction.get("memo"):
                transaction_data["memo"] = transaction.get("memo")

            category = transaction.get("category")
            if category and isinstance(category, dict) and category.get("title"):
                transaction_data["category"] = category.get("title")

            attributes["transactions"].append(transaction_data)

        return attributes


class PocketSmithUncategorizedSensor(CoordinatorEntity, SensorEntity):
    """Sensor for uncategorized transactions across all accounts."""

    _attr_has_entity_name = False
    _attr_icon = "mdi:alert-circle-outline"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: PocketSmithDataUpdateCoordinator,
    ) -> None:
        """Initialize the uncategorized transactions sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = "{}_{}_uncategorized_transactions".format(DOMAIN, coordinator.username)
        self._attr_name = "PocketSmith {} Uncategorized Transactions".format(coordinator.username)

        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, coordinator.entry_id)},
            name="PocketSmith",
            manufacturer="PocketSmith",
        )

    @property
    def native_value(self) -> StateType:
        """Return the total number of uncategorized transactions."""
        total_uncategorized = 0

        transactions_by_account = self.coordinator.data.get("transactions", {})
        for ta_id, transactions in transactions_by_account.items():
            for transaction in transactions:
                category = transaction.get("category")
                if not category or (isinstance(category, dict) and not category.get("title")):
                    total_uncategorized += 1

        return total_uncategorized

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return attributes with uncategorized count per account and transaction IDs."""
        attributes = {
            "total_uncategorized": 0,
            "last_updated": dt_util.now(),
            "by_account": {},
        }

        transactions_by_account = self.coordinator.data.get("transactions", {})
        transaction_accounts = self.coordinator.data.get("transaction_accounts", {})

        for ta_id, transactions in transactions_by_account.items():
            ta = transaction_accounts.get(ta_id, {})
            account_name = ta.get("name", "account_{}".format(ta_id))

            institution_data = ta.get("institution", {})
            if isinstance(institution_data, dict):
                institution = institution_data.get("title", "unknown")
            else:
                institution = str(institution_data) if institution_data else "unknown"

            account_key = "{}_{}".format(institution, account_name)

            uncategorized_count = 0
            uncategorized_ids = []

            for transaction in transactions:
                category = transaction.get("category")
                if not category or (isinstance(category, dict) and not category.get("title")):
                    uncategorized_count += 1
                    transaction_id = transaction.get("id")
                    if transaction_id:
                        uncategorized_ids.append(transaction_id)

            if uncategorized_count > 0:
                attributes["by_account"][account_key] = {
                    "count": uncategorized_count,
                    "institution": institution,
                    "account_name": account_name,
                    "transaction_ids": uncategorized_ids[:10],
                }
                attributes["total_uncategorized"] += uncategorized_count

        return attributes
