# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.5] - 2026-03-27

### Added
- **Feed Status sensors** (`sensor.pocketsmith_{username}_{institution}_{account}_feed_status`) — one per feed-connected account
  - State is the raw feed status from the PocketSmith API (`active`, `error`, `needs_reauthorization`, `disabled`, `unknown`)
  - Dynamic icon: green check (active), red alert (error/needs_reauthorization), grey minus (disabled)
  - Attributes: `feed_name`, `feed_status`, `last_refreshed_at`, `hours_since_refresh`, `account_name`, `institution_name`, `account_type`
  - `hours_since_refresh` is pre-calculated so automations can use a simple numeric threshold without date arithmetic
  - Only created for accounts that have an active feed connection; offline/manual accounts are unaffected
- Feed status attributes on **Account Balance sensors**: `feed_name`, `feed_status`, and `last_refreshed_at` are now also surfaced as attributes on the balance sensor for dashboard convenience
- New `pocketsmith_feed_alerts.yaml` automation file with two ready-to-use automations:
  - Alert when any feed status is not `active`
  - Alert when any feed has not refreshed in more than 24 hours

## [1.0.1] - 2026-03-08

### Added
- Icons
- More translations 
- last_updated attributes
- Various hardening fixes
- Various corrections to HASS standards

## [1.0.0] - 2025-01-09

### Added
- Initial release
- UI-based configuration via config flow
- Account balance sensors with custom naming: `sensor.pocketsmith_{institution}_{account_name}`
- Transaction history sensors: `sensor.pocketsmith_{institution}_{account_name}_transactions`
- Uncategorized transactions tracking sensor: `sensor.pocketsmith_uncategorized_transactions`
- Automatic data updates every 5 minutes
- HACS compatibility
- Account balance tracking with detailed attributes:
  - Current balance, currency, institution name, account name, account number
  - Account type, safe balance, exchange rates
- Transaction history tracking (last 20 transactions per account):
  - Transaction ID, amount, payee name, date for each transaction
  - Optional memo and category fields
  - Transaction count as sensor state
- Uncategorized transactions monitoring:
  - Total count across all accounts
  - Per-account breakdown with counts
  - Last 10 uncategorized transaction IDs per account
- Rich attributes for accounts and transactions
- Multi-currency support
- Error handling for API connection issues
- English translations

### Changed
- Complete rewrite from YAML configuration to UI configuration
- Domain changed to `pocketsmith` for consistency
- Modernized integration structure following Home Assistant best practices
- Updated to use DataUpdateCoordinator for efficient polling

### Security
- API key stored securely in config entry
- Bearer token authentication with PocketSmith API

## [Unreleased]

### Planned
- Budget tracking sensors
- Category spending analysis
- Transaction history
- Net worth calculation
- Configurable update intervals
- Support for forecast data
- Graphical dashboards
