"""Config flow for PocketSmith integration."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, API_BASE_URL, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): str,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=1440)
        ),
    }
)


async def validate_api_key(hass: HomeAssistant, api_key: str) -> dict[str, Any]:
    """Validate the API key by making a test request."""
    session = async_get_clientsession(hass)
    
    # Strip any whitespace from API key
    api_key = api_key.strip()
    
    # PocketSmith uses X-Developer-Key header, not Bearer token
    headers = {"X-Developer-Key": api_key}

    _LOGGER.debug("Validating PocketSmith API key")
    _LOGGER.debug("API URL: %s/me", API_BASE_URL)
    _LOGGER.debug("API key length: %s", len(api_key))

    try:
        async with session.get(
            "{}/me".format(API_BASE_URL), 
            headers=headers, 
            timeout=aiohttp.ClientTimeout(total=10),
            raise_for_status=False  # Don't raise on 4xx/5xx, handle manually
        ) as response:
            status = response.status
            _LOGGER.debug("Response status: %s", status)
            
            # Read response body for debugging
            try:
                response_text = await response.text()
                _LOGGER.debug("Response body: %s", response_text[:200])
            except Exception:
                response_text = ""
            
            # Handle different status codes
            if status == 401:
                _LOGGER.error("Invalid API key - 401 Unauthorized")
                raise InvalidAuth("API key is invalid or expired")
            
            if status == 403:
                _LOGGER.error("Forbidden - 403 response")
                raise InvalidAuth("API key does not have required permissions")
            
            if status >= 500:
                _LOGGER.error("PocketSmith API server error: %s", status)
                raise CannotConnect("PocketSmith API returned {}".format(status))
            
            if status >= 400:
                _LOGGER.error("Client error %s: %s", status, response_text[:200])
                raise InvalidAuth("API returned error {}".format(status))
            
            if status != 200:
                _LOGGER.error("Unexpected status code: %s", status)
                raise CannotConnect("Unexpected status {}".format(status))

            # Parse JSON response
            try:
                data = await response.json()
            except Exception as err:
                _LOGGER.error("Failed to parse JSON response: %s", err)
                raise CannotConnect("Invalid response from PocketSmith API")
            
            _LOGGER.debug("Successfully validated API key for user: %s", data.get("login", "unknown"))
            return {
                "title": data.get("login", "PocketSmith"),
                "user_id": str(data.get("id", "")),
            }

    except InvalidAuth:
        # Re-raise our custom auth errors
        raise
    except CannotConnect:
        # Re-raise our custom connection errors
        raise
    except asyncio.TimeoutError as err:
        _LOGGER.error("Timeout connecting to PocketSmith API: %s", err)
        raise CannotConnect("Timeout connecting to PocketSmith API") from err
    except aiohttp.ClientError as err:
        _LOGGER.error("Network error connecting to PocketSmith API: %s", err)
        raise CannotConnect("Network error: {}".format(err)) from err
    except Exception as err:
        _LOGGER.error("Unexpected error validating API key: %s", err, exc_info=True)
        raise CannotConnect("Unexpected error: {}".format(err)) from err


class PocketSmithConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for PocketSmith."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_api_key(self.hass, user_input[CONF_API_KEY])
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Use user email/login as unique_id for multi-instance support
                await self.async_set_unique_id(info["user_id"])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title="PocketSmith - {}".format(info["title"]), 
                    data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


class InvalidAuth(Exception):
    """Error to indicate there is invalid auth."""
