# PocketSmith Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

This custom integration allows you to integrate your PocketSmith accounts into Home Assistant.

## Features

- 💰 Track account balances in real-time
- 📊 Monitor transaction history (last 20 transactions per account)
- 🏷️ Semantic entity naming: `sensor.pocketsmith_{institution}_{account_name}`
- 📝 Detailed transaction information (ID, amount, payee, date, memo, category)
- 🔍 Track uncategorized transactions across all accounts
- 🎯 Per-account breakdown of uncategorized transactions with IDs
- 🔄 Automatic updates every 5 minutes
- 🎨 Easy UI-based configuration
- 📱 Support for multiple accounts and institutions
- 💱 Multi-currency support

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/cloudbr34k84/home-assistant-pocketsmith`
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
5. Click "Submit"

The integration will automatically discover your accounts and create sensors for each one.

## Sensors

The integration creates two types of sensors:

### Account Balance Sensors

**Entity ID Format**: `sensor.pocketsmith_account_{account_id}`

For example:
- `sensor.pocketsmith_account_123456`
- `sensor.pocketsmith_account_789012`
- `sensor.pocketsmith_account_345678`

**Friendly Name**: Automatically set to `PocketSmith {Institution} {Account Name}`
- Example: "PocketSmith Chase Checking"
- Example: "PocketSmith Bank of America Savings"
- Example: "PocketSmith American Express Credit Card"

**Note**: Entity IDs use account IDs for stability. If you rename an account in PocketSmith, the entity ID stays the same, but the friendly name updates automatically.

**State**: Current account balance (as a number)

**Attributes**:
- `current_balance`: Current balance amount
- `currency`: Currency code (e.g., USD, EUR, GBP)
- `institution_name`: Name of the financial institution
- `account_name`: Name of the account
- `account_number`: Account number (if available)
- `account_type`: Type of account (checking, savings, credit card, etc.)
- `current_balance_date`: Date of current balance
- `current_balance_exchange_rate`: Exchange rate for foreign currency accounts
- `safe_balance`: Safe balance amount (available to spend)
- `safe_balance_in_base_currency`: Safe balance in your base currency

### Transaction History Sensors

**Entity ID Format**: `sensor.pocketsmith_transactions_{transaction_account_id}`

For example:
- `sensor.pocketsmith_transactions_123456`
- `sensor.pocketsmith_transactions_789012`

**Friendly Name**: Automatically set to `PocketSmith {Institution} {Account Name} Transactions`
- Example: "PocketSmith Chase Checking Transactions"
- Example: "PocketSmith Bank of America Savings Transactions"

**State**: Number of transactions stored (up to 20)

**Attributes**:
- `current_balance`: Current balance amount
- `currency`: Currency code (e.g., USD, EUR, GBP)
- `institution_name`: Name of the financial institution
- `account_name`: Name of the account
- `account_number`: Account number (if available)
- `account_type`: Type of account (checking, savings, credit card, etc.)
- `current_balance_date`: Date of current balance
- `current_balance_exchange_rate`: Exchange rate for foreign currency accounts
- `safe_balance`: Safe balance amount (available to spend)
- `safe_balance_in_base_currency`: Safe balance in your base currency

### Transaction History Sensors

**Entity ID Format**: `sensor.pocketsmith_{institution}_{account_name}_transactions`

For example:
- `sensor.pocketsmith_chase_checking_transactions`
- `sensor.pocketsmith_bank_of_america_savings_transactions`

**State**: Number of transactions stored (up to 20)

**Attributes**:
- `account_name`: Name of the account
- `institution_name`: Name of the financial institution
- `currency`: Currency code
- `transaction_count`: Total number of transactions
- `transactions`: List of the last 20 transactions, each containing:
  - `id`: Unique transaction ID
  - `amount`: Transaction amount (positive for income, negative for expenses)
  - `payee`: Name of the payee/merchant
  - `date`: Transaction date
  - `memo`: Transaction memo (if available)
  - `category`: Transaction category (if available)

### Uncategorized Transactions Sensor

**Entity ID**: `sensor.pocketsmith_uncategorized_transactions`

**State**: Total number of uncategorized transactions across all accounts

**Attributes**:
- `total_uncategorized`: Total count of uncategorized transactions
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
  by_account:
    Chase_Checking:
      count: 8
      institution: Chase
      account_name: Checking
      transaction_ids: [12345, 12346, 12347, 12348, 12349, 12350, 12351, 12352]
    Bank_of_America_Savings:
      count: 7
      institution: Bank of America
      account_name: Savings
      transaction_ids: [23456, 23457, 23458, 23459, 23460, 23461, 23462]
```

## Usage Examples

### Display Account Balance in Lovelace

```yaml
type: entity
entity: sensor.pocketsmith_account_123456
```

### Create a Dashboard Card

```yaml
type: entities
title: PocketSmith Accounts
entities:
  - sensor.pocketsmith_account_123456
  - sensor.pocketsmith_account_789012
  - sensor.pocketsmith_account_345678
```

### View Transaction History

```yaml
type: markdown
title: Recent Transactions
content: |
  {% for transaction in state_attr('sensor.pocketsmith_transactions_123456', 'transactions') %}
  - **{{ transaction.date }}**: {{ transaction.payee }} - ${{ transaction.amount }}
  {% endfor %}
```

### Low Balance Automation

```yaml
automation:
  - alias: "Low Balance Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.pocketsmith_account_123456
        below: 100
    action:
      - service: notify.mobile_app
        data:
          message: "Your account balance is below $100!"
```

### Track Recent Spending

```yaml
automation:
  - alias: "Large Transaction Alert"
    trigger:
      - platform: state
        entity_id: sensor.pocketsmith_transactions_123456
    condition:
      - condition: template
        value_template: >
          {% set transactions = state_attr('sensor.pocketsmith_transactions_123456', 'transactions') %}
          {{ transactions[0].amount | float < -100 if transactions else false }}
    action:
      - service: notify.mobile_app
        data:
          message: "Large transaction detected: ${{ state_attr('sensor.pocketsmith_transactions_123456', 'transactions')[0].amount }}"
```

### Uncategorized Transactions Alert

```yaml
automation:
  - alias: "Uncategorized Transactions Reminder"
    trigger:
      - platform: state
        entity_id: sensor.pocketsmith_uncategorized_transactions
    condition:
      - condition: numeric_state
        entity_id: sensor.pocketsmith_uncategorized_transactions
        above: 10
    action:
      - service: notify.mobile_app
        data:
          title: "PocketSmith Reminder"
          message: >
            You have {{ states('sensor.pocketsmith_uncategorized_transactions') }} 
            uncategorized transactions. Please review and categorize them.
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

## Support

For issues, feature requests, or contributions, please visit the [GitHub repository](https://github.com/cloudbr34k84/home-assistant-pocketsmith).

## License

This project is licensed under the MIT License.

## Credits

Created by [@cloudbr34k84](https://github.com/cloudbr34k84)
