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
- 🌍 **Translated UI** in 9 languages (EN, FR, IT, DE, NL, DA, SV, ES, PT)
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

You can add multiple PocketSmith accounts by repeating the setup process with different API keys. Each instance will have unique entity IDs based on the account.

## Sensors

The integration creates sensors for each account:

### Account Balance Sensors

**Entity ID Format**: `sensor.pocketsmith_{entry_id}_account_{account_id}`

For example:
- `sensor.pocketsmith_abc123_account_4546611`
- `sensor.pocketsmith_abc123_account_4546653`

**Friendly Name**: Automatically set to `PocketSmith {Institution} {Account Name}`
- Example: "PocketSmith American Express British Airways Card"
- Example: "PocketSmith Natwest MASTERCARD"

**State**: Current account balance (as a number)

**Attributes**:
- `current_balance`: Current balance amount
- `currency`: Currency code (e.g., GBP, USD, EUR)
- `currency_symbol`: Currency symbol (e.g., £, $, €) **NEW!**
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
- `last_updated`: Timestamp of last update **NEW!**

### Transaction History Sensors

**Entity ID Format**: `sensor.pocketsmith_{entry_id}_transactions_{account_id}`

For example:
- `sensor.pocketsmith_abc123_transactions_4546611`
- `sensor.pocketsmith_abc123_transactions_4546653`

**Friendly Name**: Automatically set to `PocketSmith {Institution} {Account Name} Transactions`

**State**: Number of transactions stored (up to 20)

**Attributes**:
- `account_name`: Name of the account
- `institution_name`: Name of the financial institution
- `currency`: Currency code
- `currency_symbol`: Currency symbol (e.g., £, $, €) **NEW!**
- `transaction_count`: Total number of transactions
- `last_updated`: Timestamp of last update **NEW!**
- `transactions`: List of the last 20 transactions, each containing:
  - `id`: Unique transaction ID
  - `amount`: Transaction amount (positive for income, negative for expenses)
  - `payee`: Name of the payee/merchant
  - `date`: Transaction date (YYYY-MM-DD)
  - `memo`: Transaction memo (if available)
  - `category`: Transaction category (if available)

### Uncategorized Transactions Sensor

**Entity ID**: `sensor.pocketsmith_{entry_id}_uncategorized_transactions`

**State**: Total number of uncategorized transactions (from last 20 per account)

**Note**: This sensor counts uncategorized transactions from the most recent 20 transactions per account, not all transactions.

**Attributes**:
- `total_uncategorized`: Total count of uncategorized transactions
- `last_updated`: Timestamp of last update **NEW!**
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
  last_updated: "2026-01-14T17:30:00.000000"
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

## Supported Currencies

The integration includes currency symbols for 33 major currencies:

🇦🇪 AED (د.إ), 🇦🇺 AUD (A$), 🇧🇬 BGN (лв), 🇧🇷 BRL (R$), 🇨🇦 CAD (C$), 🇨🇭 CHF (Fr), 🇨🇳 CNY (¥), 🇨🇿 CZK (Kč), 🇩🇰 DKK (kr), 🇪🇺 EUR (€), 🇬🇧 GBP (£), 🇭🇰 HKD (HK$), 🇭🇺 HUF (Ft), 🇮🇩 IDR (Rp), 🇮🇱 ILS (₪), 🇮🇳 INR (₹), 🇯🇵 JPY (¥), 🇰🇷 KRW (₩), 🇲🇽 MXN (Mex$), 🇲🇾 MYR (RM), 🇳🇴 NOK (kr), 🇳🇿 NZD (NZ$), 🇵🇭 PHP (₱), 🇵🇱 PLN (zł), 🇷🇴 RON (lei), 🇷🇺 RUB (₽), 🇸🇪 SEK (kr), 🇸🇬 SGD (S$), 🇹🇭 THB (฿), 🇹🇷 TRY (₺), 🇺🇸 USD ($), 🇿🇦 ZAR (R)

## Supported Languages

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

## Usage Examples

### Display Account Balance in Lovelace

```yaml
type: entity
entity: sensor.pocketsmith_abc123_account_4546611
```

### Create a Dashboard Card

```yaml
type: entities
title: PocketSmith Accounts
entities:
  - sensor.pocketsmith_abc123_account_4546611
  - sensor.pocketsmith_abc123_account_4546653
  - sensor.pocketsmith_abc123_account_4546656
```

### View Transaction History with Currency Symbols

```yaml
type: markdown
title: Recent Transactions
content: |
  {% set transactions = state_attr('sensor.pocketsmith_abc123_transactions_4546611', 'transactions') %}
  {% set symbol = state_attr('sensor.pocketsmith_abc123_account_4546611', 'currency_symbol') %}
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
        entity_id: sensor.pocketsmith_abc123_account_4546611
        below: 100
    action:
      - service: notify.mobile_app
        data:
          message: "Your account balance is below {{ state_attr('sensor.pocketsmith_abc123_account_4546611', 'currency_symbol') }}100!"
```

### Uncategorized Transactions Alert

```yaml
automation:
  - alias: "Uncategorized Transactions Reminder"
    trigger:
      - platform: state
        entity_id: sensor.pocketsmith_abc123_uncategorized_transactions
    condition:
      - condition: numeric_state
        entity_id: sensor.pocketsmith_abc123_uncategorized_transactions
        above: 10
    action:
      - service: notify.mobile_app
        data:
          title: "PocketSmith Reminder"
          message: >
            You have {{ states('sensor.pocketsmith_abc123_uncategorized_transactions') }} 
            uncategorized transactions in your recent activity. Please review and categorize them.
```

## Troubleshooting

### API Connection Issues

If you experience connection issues:

1. Verify your API key is correct
2. Check that you have an active internet connection
3. Ensure PocketSmith API is accessible (check [status.pocketsmith.com](https://status.pocketsmith.com))

### Sensors Not Updating

If sensors aren't updating:

1. Check the Home Assistant logs for errors
2. Try reloading the integration
3. Verify your API key hasn't expired
4. Check your configured refresh interval

### Entity ID Changes After Update

If you're upgrading from an older version, entity IDs now include the entry_id for multi-instance support:

**Old format**: `sensor.pocketsmith_account_123456`  
**New format**: `sensor.pocketsmith_abc123_account_123456`

You'll need to update your dashboards and automations with the new entity IDs.

## Support

For issues, feature requests, or contributions, please visit the [GitHub repository](https://github.com/ianpleasance/home-assistant-pocketsmith).

## License

This project is licensed under the MIT License.

## Credits

Created by [@ianpleasance](https://github.com/ianpleasance)
