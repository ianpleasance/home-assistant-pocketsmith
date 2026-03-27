# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.5] - 2026-03-27

### Added
- **Feed Status sensors** (`sensor.pocketsmith_{username}_{institution}_{account}_feed_status`) — one per live feed-connected account
  - Status is **derived** from `updated_at` staleness — the PocketSmith API does not expose a feed_status field directly
  - States: `active` (updated within 24 h), `stale` (no update in > 24 h), `unknown` (timestamp missing)
  - Dynamic icon: green check (active), amber alert (stale), grey (unknown)
  - Attributes: `feed_name` (from `latest_feed_name`), `feed_status`, `last_refreshed_at` (from `updated_at`), `hours_since_refresh`, `current_balance_date`, `data_feeds_connection_id`, `account_name`, `institution_name`, `account_type`
  - `hours_since_refresh` is pre-calculated so automations can use a simple numeric threshold without date arithmetic
  - Only created for live feed accounts (`offline: false` with a `data_feeds_connection_id`); offline/manual accounts are unaffected
- Feed health attributes on **Account Balance sensors**: `feed_name`, `feed_status`, and `last_refreshed_at` now also appear on the balance sensor for dashboard convenience (feed accounts only)
- New `pocketsmith_feed_alerts.yaml` automation file with two ready-to-use automations:
  - Alert immediately when any feed status changes to `stale`
  - Daily 9am summary of all stale feeds

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
