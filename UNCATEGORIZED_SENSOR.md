# Uncategorized Transactions Sensor - Detailed Example

## Sensor Overview

**Entity ID**: `sensor.pocketsmith_uncategorized_transactions`
**Friendly Name**: `PocketSmith Uncategorized Transactions`
**Icon**: `mdi:alert-circle-outline`

This sensor tracks all transactions across all your accounts that have not been assigned a category in PocketSmith.

## Example Output

### Scenario: Multiple Accounts with Uncategorized Transactions

```yaml
sensor.pocketsmith_uncategorized_transactions:
  state: 23
  icon: mdi:alert-circle-outline
  
  attributes:
    total_uncategorized: 23
    by_account:
      Chase_Checking:
        count: 12
        institution: Chase
        account_name: Checking
        transaction_ids:
          - 156789
          - 156790
          - 156791
          - 156792
          - 156793
          - 156794
          - 156795
          - 156796
          - 156797
          - 156798
      
      Bank_of_America_Savings:
        count: 5
        institution: Bank of America
        account_name: Savings
        transaction_ids:
          - 267890
          - 267891
          - 267892
          - 267893
          - 267894
      
      American_Express_Blue_Cash:
        count: 6
        institution: American Express
        account_name: Blue Cash
        transaction_ids:
          - 378901
          - 378902
          - 378903
          - 378904
          - 378905
          - 378906
```

### Scenario: All Transactions Categorized

```yaml
sensor.pocketsmith_uncategorized_transactions:
  state: 0
  icon: mdi:alert-circle-outline
  
  attributes:
    total_uncategorized: 0
    by_account: {}
```

### Scenario: Single Account with Uncategorized Transactions

```yaml
sensor.pocketsmith_uncategorized_transactions:
  state: 3
  icon: mdi:alert-circle-outline
  
  attributes:
    total_uncategorized: 3
    by_account:
      Chase_Checking:
        count: 3
        institution: Chase
        account_name: Checking
        transaction_ids:
          - 156789
          - 156790
          - 156791
```

## Transaction IDs in Regular Transaction Sensors

Transaction IDs are now also included in regular transaction sensors:

```yaml
sensor.pocketsmith_chase_checking_transactions:
  state: 20
  
  attributes:
    account_name: Checking
    institution_name: Chase
    currency: USD
    transaction_count: 20
    transactions:
      - id: 156798  # ← Transaction ID added
        amount: -45.67
        payee: Whole Foods Market
        date: "2025-01-09"
        memo: Weekly groceries
        category: Groceries
      
      - id: 156797
        amount: -12.99
        payee: Netflix
        date: "2025-01-08"
        memo: null
        category: null  # ← Uncategorized transaction
      
      - id: 156796
        amount: -85.00
        payee: Shell Gas Station
        date: "2025-01-08"
        memo: Fill up
        category: null  # ← Uncategorized transaction
      
      # ... more transactions
```

## Use Cases

### 1. Dashboard Card - Show Uncategorized Count

```yaml
type: entity
entity: sensor.pocketsmith_uncategorized_transactions
name: Transactions to Categorize
icon: mdi:tag-multiple
```

### 2. Dashboard Card - Detailed Breakdown

```yaml
type: markdown
title: Uncategorized Transactions
content: |
  **Total Uncategorized:** {{ states('sensor.pocketsmith_uncategorized_transactions') }}
  
  {% set accounts = state_attr('sensor.pocketsmith_uncategorized_transactions', 'by_account') %}
  {% if accounts %}
    {% for account_key, data in accounts.items() %}
  **{{ data.institution }} - {{ data.account_name }}:** {{ data.count }} transactions
    {% endfor %}
  {% else %}
  ✅ All transactions are categorized!
  {% endif %}
```

### 3. Conditional Card - Show Warning When Uncategorized > 10

```yaml
type: conditional
conditions:
  - entity: sensor.pocketsmith_uncategorized_transactions
    state_not: "0"
card:
  type: markdown
  title: ⚠️ Categorization Needed
  content: |
    You have **{{ states('sensor.pocketsmith_uncategorized_transactions') }}** uncategorized transactions.
    
    {% set accounts = state_attr('sensor.pocketsmith_uncategorized_transactions', 'by_account') %}
    {% for account_key, data in accounts.items() %}
    - **{{ data.account_name }}**: {{ data.count }} to categorize
    {% endfor %}
    
    [Go to PocketSmith](https://my.pocketsmith.com) to categorize them.
```

### 4. Gauge Card - Visual Indicator

```yaml
type: gauge
entity: sensor.pocketsmith_uncategorized_transactions
name: Uncategorized
min: 0
max: 50
severity:
  green: 0
  yellow: 5
  red: 15
```

### 5. Show Transaction IDs for Quick Access

```yaml
type: markdown
title: Uncategorized Transaction IDs
content: |
  {% set accounts = state_attr('sensor.pocketsmith_uncategorized_transactions', 'by_account') %}
  {% if accounts %}
    {% for account_key, data in accounts.items() %}
  ### {{ data.institution }} - {{ data.account_name }}
  Transaction IDs: {{ data.transaction_ids | join(', ') }}
    {% endfor %}
  {% else %}
  ✅ No uncategorized transactions
  {% endif %}
```

## Automation Examples

### 1. Daily Reminder if Uncategorized Transactions Exist

```yaml
automation:
  - alias: "Daily Uncategorized Transactions Reminder"
    trigger:
      - platform: time
        at: "09:00:00"
    condition:
      - condition: numeric_state
        entity_id: sensor.pocketsmith_uncategorized_transactions
        above: 0
    action:
      - service: notify.mobile_app
        data:
          title: "PocketSmith Reminder"
          message: >
            Good morning! You have {{ states('sensor.pocketsmith_uncategorized_transactions') }} 
            uncategorized transactions waiting for review.
```

### 2. Alert When Uncategorized Count Exceeds Threshold

```yaml
automation:
  - alias: "Too Many Uncategorized Transactions"
    trigger:
      - platform: numeric_state
        entity_id: sensor.pocketsmith_uncategorized_transactions
        above: 20
    action:
      - service: notify.mobile_app
        data:
          title: "⚠️ PocketSmith Alert"
          message: >
            You have {{ states('sensor.pocketsmith_uncategorized_transactions') }} 
            uncategorized transactions! Time to catch up on categorization.
          data:
            url: https://my.pocketsmith.com/transactions
```

### 3. Weekly Summary with Account Breakdown

```yaml
automation:
  - alias: "Weekly Uncategorized Summary"
    trigger:
      - platform: time
        at: "18:00:00"
    condition:
      - condition: time
        weekday:
          - fri
      - condition: numeric_state
        entity_id: sensor.pocketsmith_uncategorized_transactions
        above: 0
    action:
      - service: notify.mobile_app
        data:
          title: "Weekly Finance Summary"
          message: >
            {% set accounts = state_attr('sensor.pocketsmith_uncategorized_transactions', 'by_account') %}
            You have {{ states('sensor.pocketsmith_uncategorized_transactions') }} uncategorized transactions:
            {% for account_key, data in accounts.items() %}
            - {{ data.account_name }}: {{ data.count }}
            {% endfor %}
```

### 4. Celebrate When All Categorized

```yaml
automation:
  - alias: "All Transactions Categorized"
    trigger:
      - platform: state
        entity_id: sensor.pocketsmith_uncategorized_transactions
        to: "0"
    condition:
      - condition: template
        value_template: "{{ trigger.from_state.state | int > 0 }}"
    action:
      - service: notify.mobile_app
        data:
          title: "🎉 Great Job!"
          message: "All your transactions are now categorized!"
```

### 5. Persistent Notification in Home Assistant

```yaml
automation:
  - alias: "Create Uncategorized Notification"
    trigger:
      - platform: numeric_state
        entity_id: sensor.pocketsmith_uncategorized_transactions
        above: 10
    action:
      - service: persistent_notification.create
        data:
          title: "PocketSmith Categorization Needed"
          message: >
            You have {{ states('sensor.pocketsmith_uncategorized_transactions') }} 
            uncategorized transactions across your accounts.
          notification_id: pocketsmith_uncategorized

  - alias: "Dismiss Uncategorized Notification"
    trigger:
      - platform: numeric_state
        entity_id: sensor.pocketsmith_uncategorized_transactions
        below: 10
    action:
      - service: persistent_notification.dismiss
        data:
          notification_id: pocketsmith_uncategorized
```

## Template Examples

### Get Total Uncategorized Count

```yaml
{{ states('sensor.pocketsmith_uncategorized_transactions') }}
```

### Get Count for Specific Account

```yaml
{% set accounts = state_attr('sensor.pocketsmith_uncategorized_transactions', 'by_account') %}
{{ accounts['Chase_Checking'].count if 'Chase_Checking' in accounts else 0 }}
```

### List All Accounts with Uncategorized Transactions

```yaml
{% set accounts = state_attr('sensor.pocketsmith_uncategorized_transactions', 'by_account') %}
{% for account_key, data in accounts.items() %}
{{ data.institution }} - {{ data.account_name }}: {{ data.count }}
{% endfor %}
```

### Get Transaction IDs for Specific Account

```yaml
{% set accounts = state_attr('sensor.pocketsmith_uncategorized_transactions', 'by_account') %}
{{ accounts['Chase_Checking'].transaction_ids if 'Chase_Checking' in accounts else [] }}
```

### Check if Any Account Has Uncategorized Transactions

```yaml
{{ states('sensor.pocketsmith_uncategorized_transactions') | int > 0 }}
```

## How the Sensor Works

1. **Data Collection**: Every 5 minutes, the integration fetches the last 20 transactions from each account
2. **Category Detection**: For each transaction, it checks if a category exists
3. **Counting**: Transactions without a category (or with null/empty category) are counted
4. **Aggregation**: Counts are grouped by account and summed for the total
5. **ID Tracking**: The last 10 uncategorized transaction IDs per account are stored

## Notes

- **Update Frequency**: Updates every 5 minutes with other sensors
- **Transaction Limit**: Only checks the last 20 transactions per account (same as transaction history sensors)
- **ID Limit**: Stores up to 10 transaction IDs per account in attributes
- **Account Filtering**: Only accounts with uncategorized transactions appear in `by_account`
- **Zero State**: When all transactions are categorized, `by_account` is an empty dictionary

## Benefits

1. **Quick Overview**: See at a glance how many transactions need categorization
2. **Account Breakdown**: Know which accounts need attention
3. **Transaction IDs**: Direct access to transaction IDs for API or manual lookup
4. **Automation Ready**: Easy to create alerts and reminders
5. **Dashboard Integration**: Simple to display in your financial dashboard

## Troubleshooting

**Q: Sensor shows 0 but I know I have uncategorized transactions**
A: The sensor only checks the last 20 transactions per account. Older uncategorized transactions won't be counted.

**Q: Transaction IDs not showing**
A: The API may not return transaction IDs in some cases. This is dependent on PocketSmith's API response.

**Q: by_account is empty but state is > 0**
A: This shouldn't happen. Try reloading the integration or checking logs for errors.

**Q: Can I change the 10 transaction ID limit?**
A: Yes, modify the `transaction_ids[:10]` line in sensor.py to your preferred limit.
