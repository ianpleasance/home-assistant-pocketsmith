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
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, CURRENCY_SYMBOLS
from .coordinator import PocketSmithDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up PocketSmith sensor based on a config entry."""
    coordinator: PocketSmithDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = []

    # Create balance and transaction sensors for each transaction account
    # Transaction accounts have both balance info AND transaction details
    if coordinator.data and "transaction_accounts" in coordinator.data:
        for ta_id, ta in coordinator.data["transaction_accounts"].items():
            # Create balance sensor
            entities.append(
                PocketSmithAccountBalanceSensor(
                    coordinator=coordinator,
                    account_id=ta_id,
                )
            )
            
            # Create transaction history sensor
            entities.append(
                PocketSmithTransactionHistorySensor(
                    coordinator=coordinator,
                    ta_id=ta_id,
                )
            )
    
    # Create uncategorized transactions sensor
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
        
        # Get account details for friendly name from transaction_accounts
        account = coordinator.data.get("transaction_accounts", {}).get(account_id, {})
        
        # Institution is a dict, extract the title
        institution_data = account.get("institution", {})
        if isinstance(institution_data, dict):
            institution = institution_data.get("title", "Unknown")
        else:
            institution = str(institution_data) if institution_data else "Unknown"
            
        account_name = account.get("name", "Account {}".format(account_id))
        
        # Use entry_id in unique_id and entity_id for multi-instance support
        self._attr_unique_id = "{}_{}_account_{}".format(DOMAIN, coordinator.entry_id, account_id)
        self.entity_id = "sensor.{}_{}_account_{}".format(DOMAIN, coordinator.entry_id, account_id)
        
        # Friendly name uses institution and account name
        self._attr_name = "PocketSmith {} {}".format(institution, account_name)

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
        
        # Extract institution name from dict
        institution_data = account.get("institution", {})
        if isinstance(institution_data, dict):
            institution_name = institution_data.get("title")
        else:
            institution_name = str(institution_data) if institution_data else None
        
        # Get currency and symbol
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
            "last_updated": datetime.now().isoformat(),
        }
        
        # Add account number if available
        account_number = account.get("number")
        if account_number:
            attributes["account_number"] = account_number
            
        # Add other useful attributes
        attributes.update({
            "account_type": account.get("type"),
            "current_balance_date": account.get("current_balance_date"),
            "current_balance_exchange_rate": account.get("current_balance_exchange_rate"),
            "safe_balance": account.get("safe_balance"),
            "safe_balance_in_base_currency": account.get("safe_balance_in_base_currency"),
            "starting_balance": account.get("starting_balance"),
            "starting_balance_date": account.get("starting_balance_date"),
        })
        
        return attributes


class PocketSmithTransactionHistorySensor(CoordinatorEntity, SensorEntity):
    """Sensor for PocketSmith transaction history."""

    _attr_has_entity_name = False

    def __init__(
        self,
        coordinator: PocketSmithDataUpdateCoordinator,
        ta_id: str,
    ) -> None:
        """Initialize the transaction history sensor."""
        super().__init__(coordinator)
        self.ta_id = ta_id
        
        # Get transaction account details for friendly name
        ta = coordinator.data.get("transaction_accounts", {}).get(ta_id, {})
        
        # Institution is a dict, extract the title
        institution_data = ta.get("institution", {})
        if isinstance(institution_data, dict):
            institution = institution_data.get("title", "Unknown")
        else:
            institution = str(institution_data) if institution_data else "Unknown"
            
        account_name = ta.get("name", "Account {}".format(ta_id))
        
        # Use entry_id in unique_id and entity_id for multi-instance support
        self._attr_unique_id = "{}_{}_transactions_{}".format(DOMAIN, coordinator.entry_id, ta_id)
        self.entity_id = "sensor.{}_{}_transactions_{}".format(DOMAIN, coordinator.entry_id, ta_id)
        
        # Friendly name uses institution and account name
        self._attr_name = "PocketSmith {} {} Transactions".format(institution, account_name)

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor (number of transactions)."""
        transactions = self.coordinator.data.get("transactions", {}).get(self.ta_id, [])
        return len(transactions)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes with last 20 transactions."""
        transactions = self.coordinator.data.get("transactions", {}).get(self.ta_id, [])
        
        # Get transaction account details
        ta = self.coordinator.data.get("transaction_accounts", {}).get(self.ta_id, {})
        
        # Extract institution name from dict
        institution_data = ta.get("institution", {})
        if isinstance(institution_data, dict):
            institution_name = institution_data.get("title")
        else:
            institution_name = str(institution_data) if institution_data else None
        
        # Get currency and symbol
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
            "last_updated": datetime.now().isoformat(),
            "transactions": [],
        }
        
        # Add last 20 transactions with amount, payee, date, and ID
        for transaction in transactions[:20]:
            transaction_data = {
                "id": transaction.get("id"),
                "amount": transaction.get("amount"),
                "payee": transaction.get("payee"),
                "date": transaction.get("date"),
            }
            
            # Add optional fields if available
            if transaction.get("memo"):
                transaction_data["memo"] = transaction.get("memo")
            
            # Check category - it might be None instead of a dict
            category = transaction.get("category")
            if category and isinstance(category, dict) and category.get("title"):
                transaction_data["category"] = category.get("title")
                
            attributes["transactions"].append(transaction_data)
        
        return attributes


class PocketSmithUncategorizedSensor(CoordinatorEntity, SensorEntity):
    """Sensor for uncategorized transactions across all accounts."""

    _attr_has_entity_name = False
    _attr_icon = "mdi:alert-circle-outline"

    def __init__(
        self,
        coordinator: PocketSmithDataUpdateCoordinator,
    ) -> None:
        """Initialize the uncategorized transactions sensor."""
        super().__init__(coordinator)
        # Use entry_id for multi-instance support
        self._attr_unique_id = "{}_{}_uncategorized_transactions".format(DOMAIN, coordinator.entry_id)
        self.entity_id = "sensor.{}_{}_uncategorized_transactions".format(DOMAIN, coordinator.entry_id)
        self._attr_name = "PocketSmith Uncategorized Transactions"

    @property
    def native_value(self) -> StateType:
        """Return the total number of uncategorized transactions."""
        total_uncategorized = 0
        
        transactions_by_account = self.coordinator.data.get("transactions", {})
        for ta_id, transactions in transactions_by_account.items():
            for transaction in transactions:
                # Check if transaction has no category
                category = transaction.get("category")
                if not category or (isinstance(category, dict) and not category.get("title")):
                    total_uncategorized += 1
        
        return total_uncategorized

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return attributes with uncategorized count per account and transaction IDs."""
        attributes = {
            "total_uncategorized": 0,
            "last_updated": datetime.now().isoformat(),
            "by_account": {},
        }
        
        transactions_by_account = self.coordinator.data.get("transactions", {})
        transaction_accounts = self.coordinator.data.get("transaction_accounts", {})
        
        for ta_id, transactions in transactions_by_account.items():
            # Get account details
            ta = transaction_accounts.get(ta_id, {})
            account_name = ta.get("name", "account_{}".format(ta_id))
            
            # Extract institution name from dict
            institution_data = ta.get("institution", {})
            if isinstance(institution_data, dict):
                institution = institution_data.get("title", "unknown")
            else:
                institution = str(institution_data) if institution_data else "unknown"
            
            account_key = "{}_{}".format(institution, account_name)
            
            uncategorized_count = 0
            uncategorized_ids = []
            
            for transaction in transactions:
                # Check if transaction has no category
                category = transaction.get("category")
                if not category or (isinstance(category, dict) and not category.get("title")):
                    uncategorized_count += 1
                    transaction_id = transaction.get("id")
                    if transaction_id:
                        uncategorized_ids.append(transaction_id)
            
            # Only add to attributes if there are uncategorized transactions
            if uncategorized_count > 0:
                attributes["by_account"][account_key] = {
                    "count": uncategorized_count,
                    "institution": institution,
                    "account_name": account_name,
                    "transaction_ids": uncategorized_ids[:10],  # Last 10 uncategorized
                }
                attributes["total_uncategorized"] += uncategorized_count
        
        return attributes


