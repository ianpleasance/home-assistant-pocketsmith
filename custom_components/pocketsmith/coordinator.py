"""DataUpdateCoordinator for PocketSmith."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_BASE_URL, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class PocketSmithDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching PocketSmith data."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        api_key: str,
        update_interval: timedelta,
        entry_id: str,
    ) -> None:
        """Initialize coordinator."""
        self.session = session
        self.api_key = api_key
        self.entry_id = entry_id
        # PocketSmith uses X-Developer-Key header, not Bearer token
        self.headers = {"X-Developer-Key": api_key}

        super().__init__(
            hass,
            _LOGGER,
            name="PocketSmith",
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from PocketSmith API."""
        _LOGGER.debug("Starting PocketSmith data fetch")
        
        try:
            # Fetch user information
            _LOGGER.debug("Fetching user information from /me")
            user_data = await self._fetch_endpoint("me")
            user_id = user_data.get("id")
            _LOGGER.debug("Successfully fetched user data: %s (ID: %s)", user_data.get("login", "unknown"), user_id)

            # Fetch accounts using user ID
            _LOGGER.debug("Fetching accounts from /users/%s/accounts", user_id)
            accounts = await self._fetch_endpoint("users/{}/accounts".format(user_id))
            _LOGGER.debug("Successfully fetched %d accounts", len(accounts))

            # Fetch transaction accounts using user ID
            _LOGGER.debug("Fetching transaction accounts from /users/%s/transaction_accounts", user_id)
            transaction_accounts = await self._fetch_endpoint("users/{}/transaction_accounts".format(user_id))
            _LOGGER.debug("Successfully fetched %d transaction accounts", len(transaction_accounts))

            # Fetch transactions for each transaction account (last 20)
            transactions_by_account = {}
            for ta in transaction_accounts:
                ta_id = ta["id"]
                _LOGGER.debug("Fetching transactions for account %s", ta_id)
                try:
                    transactions = await self._fetch_endpoint(
                        "transaction_accounts/{}/transactions?per_page=20".format(ta_id)
                    )
                    transactions_by_account[ta_id] = transactions
                    _LOGGER.debug("Fetched %d transactions for account %s", len(transactions), ta_id)
                except Exception as err:
                    _LOGGER.warning(
                        "Failed to fetch transactions for account %s: %s", ta_id, err
                    )
                    transactions_by_account[ta_id] = []

            # Organize data
            data = {
                "user": user_data,
                "accounts": {account["id"]: account for account in accounts},
                "transaction_accounts": {
                    ta["id"]: ta for ta in transaction_accounts
                },
                "transactions": transactions_by_account,
            }

            _LOGGER.debug("Successfully completed PocketSmith data fetch")
            return data

        except UpdateFailed:
            # Re-raise UpdateFailed with original message
            raise
        except aiohttp.ClientError as err:
            _LOGGER.error("Network error communicating with PocketSmith API: %s", err, exc_info=True)
            raise UpdateFailed("Error communicating with API: {}".format(err)) from err
        except Exception as err:
            _LOGGER.error("Unexpected error during data fetch: %s", err, exc_info=True)
            raise UpdateFailed("Unexpected error: {}".format(err)) from err

    async def _fetch_endpoint(self, endpoint: str) -> Any:
        """Fetch data from a specific endpoint."""
        url = "{}/{}".format(API_BASE_URL, endpoint)
        
        _LOGGER.debug("Fetching endpoint: %s", url)

        try:
            async with self.session.get(
                url, headers=self.headers, timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                status = response.status
                _LOGGER.debug("Response status for %s: %s", endpoint, status)
                
                if status != 200:
                    response_text = await response.text()
                    _LOGGER.error(
                        "Error fetching %s: HTTP %s - %s", 
                        endpoint, 
                        status, 
                        response_text[:200]
                    )
                    raise UpdateFailed(
                        "Error fetching {}: HTTP {}".format(endpoint, status)
                    )
                
                data = await response.json()
                _LOGGER.debug("Successfully parsed JSON from %s", endpoint)
                return data
                
        except aiohttp.ClientError as err:
            _LOGGER.error("Network error fetching %s: %s", endpoint, err)
            raise
        except Exception as err:
            _LOGGER.error("Unexpected error fetching %s: %s", endpoint, err, exc_info=True)
            raise
