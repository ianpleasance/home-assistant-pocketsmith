# PocketSmith Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

This custom integration allows you to integrate your PocketSmith accounts into Home Assistant.

## Features

- 💰 Track account balances in real-time
- 📊 Monitor transaction history (last 20 transactions per account)
- 🏷️ Semantic entity naming with institution and account details
- 📝 Detailed transaction information (ID, amount, payee, date, memo, category)
- 🔍 Track uncategorized transactions across all accounts
- 🎯 Per-account breakdown of uncategorized transactions with IDs
- ⏱️ **Configurable refresh interval** (1-1440 minutes, default: 5)
- 🔄 **Multi-instance support** - Add multiple PocketSmith accounts
- 💱 Multi-currency support with **currency symbols** (£, $, €, ¥, etc.)
- 🌍 **Translated UI** in 13 languages (EN, FR, IT, DE, NL, DA, SV, ES, PT, FI, JA, NO, PL)
- 🎨 Easy UI-based configuration
- 📱 Support for multiple accounts and institutions

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/ianpleasance/home-assistant-pocketsmith`
6. Select category: "Integration"
7. Click "Add"
8. Search for "PocketSmith" in HACS
9. Click "Download"
10. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/pocketsmith` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

### Getting Your API Key

1. Go to [PocketSmith Developer Portal](https://my.pocketsmith.com/developer)
2. Click "Generate New API Key"
3. Copy the generated API key

### Setting Up the Integration

1. Go to Settings → Devices & Services
2. Click "+ Add Integration"
3. Search for "PocketSmith"
4. Enter your API key
5. **Set refresh interval** (optional, 1-1440 minutes, default: 5)
6. Click "Submit"

The integration will automatically discover your accounts and create sensors for each one.

### Multiple Instances

You can add multiple PocketSmith accounts by repeating the setup process with different API keys. Each instance has entity IDs scoped to the PocketSmith username, so there are no clashes even if two accounts have identically named bank accounts.

## Sensors

The integration creates sensors for each account:

### Account Balance Sensors

**Entity ID Format**: `sensor.pocketsmith_{username}_{institution}_{account_name}`

The `username` is your PocketSmith login name, keeping entity IDs unique across multiple instances.

For example:
- `sensor.pocketsmith_ianpleasance_natwest_primary_account`
- `sensor.pocketsmith_ianpleasance_monzo_personal_account`

**Friendly Name**: Automatically set to `PocketSmith {username} {Institution} {Account Name}`
- Example: "PocketSmith ianpleasance NatWest Primary Account"
- Example: "PocketSmith ianpleasance Monzo Personal Account"

**State**: Current account balance (as a number)

**Attributes**:
- `current_balance`: Current balance amount
- `currency`: Currency code (e.g., GBP, USD, EUR)
- `currency_symbol`: Currency symbol (e.g., £, $, €)
- `institution_name`: Name of the financial institution
- `account_name`: Name of the account
- `account_number`: Account number (if available)
- `account_type`: Type of account (bank, credits, etc.)
- `current_balance_date`: Date of current balance
- `current_balance_exchange_rate`: Exchange rate for foreign currency accounts
- `safe_balance`: Safe balance amount (available to spend)
- `safe_balance_in_base_currency`: Safe balance in your base currency
- `starting_balance`: Starting balance
- `starting_balance_date`: Date of starting balance
- `last_updated`: Timestamp of last update

### Transaction History Sensors

**Entity ID Format**: `sensor.pocketsmith_{username}_{institution}_{account_name}_transactions`

For example:
- `sensor.pocketsmith_ianpleasance_natwest_primary_account_transactions`
- `sensor.pocketsmith_ianpleasance_monzo_personal_account_transactions`

**Friendly Name**: Automatically set to `PocketSmith {username} {Institution} {Account Name} Transactions`

**State**: Number of transactions stored (up to 20)

**Attributes**:
- `account_name`: Name of the account
- `institution_name`: Name of the financial institution
- `currency`: Currency code
- `currency_symbol`: Currency symbol (e.g., £, $, €)
- `transaction_count`: Total number of transactions
- `last_updated`: Timestamp of last update
- `transactions`: List of the last 20 transactions, each containing:
  - `id`: Unique transaction ID
  - `amount`: Transaction amount (positive for income, negative for expenses)
  - `payee`: Name of the payee/merchant
  - `date`: Transaction date (YYYY-MM-DD)
  - `memo`: Transaction memo (if available)
  - `category`: Transaction category (if available)

### Uncategorized Transactions Sensor

**Entity ID**: `sensor.pocketsmith_{username}_uncategorized_transactions`

For example: `sensor.pocketsmith_ianpleasance_uncategorized_transactions`

**State**: Total number of uncategorized transactions (from last 20 per account)

**Note**: This sensor counts uncategorized transactions from the most recent 20 transactions per account, not all transactions.

**Attributes**:
- `total_uncategorized`: Total count of uncategorized transactions
- `last_updated`: Timestamp of last update
- `by_account`: Dictionary of accounts with uncategorized transactions, containing:
  - `count`: Number of uncategorized transactions in this account
  - `institution`: Institution name
  - `account_name`: Account name
  - `transaction_ids`: List of up to 10 most recent uncategorized transaction IDs

Example:
```yaml
state: 15
attributes:
  total_uncategorized: 15
  last_updated: "2026-01-14 17:30:00+00:00"
  by_account:
    American Express_Amex Card:
      count: 8
      institution: American Express
      account_name: Amex Card
      transaction_ids: [12345, 12346, 12347, 12348, 12349, 12350, 12351, 12352]
    Natwest_MASTERCARD:
      count: 7
      institution: Natwest
      account_name: MASTERCARD
      transaction_ids: [23456, 23457, 23458, 23459, 23460, 23461, 23462]
```

### Feed Status Sensors

**Entity ID Format**: `sensor.pocketsmith_{username}_{institution}_{account_name}_feed_status`

For example:
- `sensor.pocketsmith_ianpleasance_natwest_primary_account_feed_status`
- `sensor.pocketsmith_ianpleasance_monzo_personal_account_feed_status`

**Note**: These sensors are only created for accounts connected via a live bank feed (`offline: false`). Offline or manually-managed accounts will not have a feed status sensor.

**Important**: The PocketSmith API does not expose a feed status field directly. Status is **inferred** from the account's `updated_at` timestamp:

| Value | Meaning |
|---|---|
| `active` | Account was updated within the last 24 hours — feed is healthy |
| `stale` | Account has not been updated in over 24 hours — feed may have a problem |
| `unknown` | Timestamp is missing or could not be parsed |

**Attributes**:
- `feed_name`: The feed account name as reported by the data provider (from `latest_feed_name`)
- `feed_status`: Derived status (mirrors the sensor state)
- `last_refreshed_at`: ISO 8601 timestamp of the last account update (from `updated_at`)
- `hours_since_refresh`: Hours elapsed since last refresh (float, pre-calculated for use in automations)
- `current_balance_date`: Date the balance was last updated from the feed
- `data_feeds_connection_id`: The PocketSmith data feeds connection ID (shared across accounts on the same bank login)
- `account_name`: Name of the account
- `institution_name`: Name of the financial institution
- `account_type`: Type of account (bank, credits, loans, etc.)
- `last_updated`: Timestamp of last HA update

### Feed Status on Balance Sensors

The `feed_name`, `feed_status`, and `last_refreshed_at` attributes are also available on the **Account Balance sensor** for convenience, so a single dashboard card can show both the balance and whether the feed is healthy. These attributes are only present on feed-connected accounts.

## Supported Currencies
- `feed_status`: Derived status (mirrors the sensor state)
- `last_refreshed_at`: ISO 8601 timestamp of the last account update (from `updated_at`)
- `hours_since_refresh`: Hours elapsed since last refresh (float, pre-calculated for use in automations)
- `current_balance_date`: Date the balance was last updated from the feed
- `data_feeds_connection_id`: The PocketSmith data feeds connection ID (shared across accounts on the same bank login)
- `account_name`: Name of the account
- `institution_name`: Name of the financial institution
- `account_type`: Type of account (bank, credits, loans, etc.)
- `last_updated`: Timestamp of last HA update

### Feed Status on Balance Sensors

The `feed_name`, `feed_status`, 
The integration UI is available in:

- 🇬🇧 English
- 🇫🇷 French (Français)
- 🇮🇹 Italian (Italiano)
- 🇩🇪 German (Deutsch)
- 🇳🇱 Dutch (Nederlands)
- 🇩🇰 Danish (Dansk)
- 🇸🇪 Swedish (Svenska)
- 🇪🇸 Spanish (Español)
- 🇵🇹 Portuguese (Português)
- 🇫🇮 Finnish (Suomi)
- 🇯🇵 Japanese (日本語)
- 🇳🇴 Norwegian (Norsk)
- 🇵🇱 Polish (Polski)

## Usage Examples

### Manual Refresh Service

You can manually refresh all PocketSmith data using the service:

```yaml
service: pocketsmith.refresh
```

This is useful when you want to immediately update account balances and transactions without waiting for the next automatic refresh.

**In automation:**
```yaml
automation:
  - alias: "Refresh PocketSmith before daily report"
    trigger:
      - platform: time
        at: "08:00:00"
    action:
      - service: pocketsmith.refresh
      - delay: "00:00:05"  # Wait for refresh to complete
      - service: notify.mobile_app
        data:
          message: "PocketSmith data refreshed!"
```

### Display Account Balance in Lovelace

```yaml
type: entity
entity: sensor.pocketsmith_ianpleasance_natwest_primary_account
```

### Create a Dashboard Card

```yaml
type: entities
title: PocketSmith Accounts
entities:
  - sensor.pocketsmith_ianpleasance_natwest_primary_account
  - sensor.pocketsmith_ianpleasance_monzo_personal_account
  - sensor.pocketsmith_ianpleasance_monzo_savings
```

### View Transaction History with Currency Symbols

```yaml
type: markdown
title: Recent Transactions
content: |
  {% set transactions = state_attr('sensor.pocketsmith_ianpleasance_natwest_primary_account_transactions', 'transactions') %}
  {% set symbol = state_attr('sensor.pocketsmith_ianpleasance_natwest_primary_account', 'currency_symbol') %}
  {% for transaction in transactions %}
  - **{{ transaction.date }}**: {{ transaction.payee }} - {{ symbol }}{{ "%.2f"|format(transaction.amount) }}
  {% endfor %}
```

### Low Balance Automation

```yaml
automation:
  - alias: "Low Balance Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.pocketsmith_ianpleasance_natwest_primary_account
        below: 100
    action:
      - service: notify.mobile_app
        data:
          message: "Your account balance is below {{ state_attr('sensor.pocketsmith_ianpleasance_natwest_primary_account', 'currency_symbol') }}100!"
```

### Uncategorized Transactions Alert

```yaml
automation:
  - alias: "Uncategorized Transactions Reminder"
    trigger:
      - platform: state
        entity_id: sensor.pocketsmith_ianpleasance_uncategorized_transactions
    condition:
      - condition: numeric_state
        entity_id: sensor.pocketsmith_ianpleasance_uncategorized_transactions
        above: 10
    action:
      - service: notify.mobile_app
        data:
          title: "PocketSmith Reminder"
          message: >
            You have {{ states('sensor.pocketsmith_ianpleasance_uncategorized_transactions') }}
            uncategorized transactions in your recent activity. Please review and categorize them.
```

### Feed Status Alert

```yaml
automation:
  - alias: "PocketSmith Feed Stale"
    trigger:
      - platform: state
        entity_id: sensor.pocketsmith_ianpleasance_natwest_primary_account_feed_status
        to: "stale"
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ PocketSmith Feed Stale"
          message: >
            {{ state_attr('sensor.pocketsmith_ianpleasance_natwest_primary_account_feed_status', 'institution_name') }}
            {{ state_attr('sensor.pocketsmith_ianpleasance_natwest_primary_account_feed_status', 'account_name') }}
            has not refreshed for
            {{ state_attr('sensor.pocketsmith_ianpleasance_natwest_primary_account_feed_status', 'hours_since_refresh') | round(0) | int }} hours.
            Check PocketSmith → Manage → Feeds.
```

**Note**: Feed status is derived from `updated_at` staleness — `active` means updated within 24 hours, `stale` means not updated for over 24 hours. The PocketSmith API does not expose a feed status field directly.

A more complete multi-account version of these automations is included in `pocketsmith_feed_alerts.yaml`.

## Troubleshooting

### API Connection Issues

If you experience connection issues:

1. Verify your API key is correct
2. Check that you have an active internet connection
3. Ensure PocketSmith API is accessible (check [status.pocketsmith.com](https://status.pocketsmith.com))

### Feed Status Shows 'stale'

A `stale` status means the account's `updated_at` timestamp is more than 24 hours old — the integration has not seen a fresh update from PocketSmith. This may mean:

1. The bank feed itself has an error or needs reauthorisation — log in to PocketSmith and go to **Manage → Feeds** to check
2. PocketSmith's data provider is experiencing a temporary outage — check the feed provider's status page
3. For Salt Edge (UK/EU) feeds, reauthorisation is required every 90 days by regulation — click "Authorise" in PocketSmith → Manage → Feeds

Once the feed syncs successfully in PocketSmith, the sensor will return to `active` on the next coordinator poll (within 5 minutes by default).

**Note**: The PocketSmith API does not expose a feed status field. The `stale`/`active` status is inferred from the account's last update timestamp. A feed that PocketSmith itself shows as errored will always appear as `stale` in HA since the account data stops being updated.

### Feed Status Sensor Not Created

Feed status sensors are only created for live feed accounts — those with `offline: false` and a `data_feeds_connection_id` in the API response. Accounts managed manually (loans, offline accounts) will not have a feed status sensor. This is expected.

### Sensors Not Updating

If sensors aren't updating:

1. Check the Home Assistant logs for errors
2. Try reloading the integration
3. Verify your API key hasn't expired
4. Check your configured refresh interval

### Entity ID Changes After Update

If you're upgrading from an older version, entity IDs now include your PocketSmith username for multi-instance support:

**Old format**: `sensor.pocketsmith_account_123456`
**Intermediate format**: `sensor.pocketsmith_01kez619_account_123456`
**Current format**: `sensor.pocketsmith_ianpleasance_natwest_primary_account`

You'll need to update your dashboards and automations with the new entity IDs. The current format uses human-readable names derived from your username, institution, and account name, making them much easier to identify.

## Support

For issues, feature requests, or contributions, please visit the [GitHub repository](https://github.com/ianpleasance/home-assistant-pocketsmith).

## License

This project is licensed under the Apache 2.0 License.

## Credits

Created by [@ianpleasance](https://github.com/ianpleasance)
