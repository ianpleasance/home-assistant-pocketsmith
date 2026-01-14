# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
