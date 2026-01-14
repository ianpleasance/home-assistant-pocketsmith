# Example Lovelace Dashboard Configurations

This file contains example dashboard configurations for displaying your PocketSmith data in Home Assistant.

**Note**: Replace entity IDs like `sensor.pocketsmith_chase_checking` with your actual sensor names. Find them in **Settings** → **Devices & Services** → **Entities**.

## Account Balance Examples

### Simple Account Balance Card

```yaml
type: entity
entity: sensor.pocketsmith_chase_checking
name: Checking Account
icon: mdi:bank
```

### Multiple Accounts Grid

```yaml
type: grid
columns: 2
square: false
cards:
  - type: entity
    entity: sensor.pocketsmith_chase_checking
    name: Chase Checking
    icon: mdi:bank
  - type: entity
    entity: sensor.pocketsmith_chase_savings
    name: Chase Savings
    icon: mdi:piggy-bank
  - type: entity
    entity: sensor.pocketsmith_amex_credit_card
    name: Amex Credit Card
    icon: mdi:credit-card
  - type: entity
    entity: sensor.pocketsmith_fidelity_investment
    name: Fidelity Investment
    icon: mdi:chart-line
```

### Detailed Account Information

```yaml
type: entities
title: Account Details
entities:
  - entity: sensor.pocketsmith_chase_checking
    name: Balance
  - type: attribute
    entity: sensor.pocketsmith_chase_checking
    attribute: account_name
    name: Account Name
  - type: attribute
    entity: sensor.pocketsmith_chase_checking
    attribute: institution_name
    name: Bank
  - type: attribute
    entity: sensor.pocketsmith_chase_checking
    attribute: account_number
    name: Account Number
  - type: attribute
    entity: sensor.pocketsmith_chase_checking
    attribute: currency
    name: Currency
  - type: attribute
    entity: sensor.pocketsmith_chase_checking
    attribute: safe_balance
    name: Safe Balance
```

## Transaction History Examples

### Recent Transactions List

```yaml
type: markdown
title: Recent Transactions
content: |
  {% set transactions = state_attr('sensor.pocketsmith_chase_checking_transactions', 'transactions') %}
  {% if transactions %}
    {% for transaction in transactions[:10] %}
  **{{ transaction.date }}** - {{ transaction.payee }}
  Amount: ${{ transaction.amount }}
  {% if transaction.memo %}Memo: {{ transaction.memo }}{% endif %}
  ---
    {% endfor %}
  {% else %}
  No transactions available
  {% endif %}
```

### Transaction Summary Card

```yaml
type: entities
title: Transaction Summary
entities:
  - entity: sensor.pocketsmith_chase_checking_transactions
    name: Total Transactions
  - type: attribute
    entity: sensor.pocketsmith_chase_checking_transactions
    attribute: account_name
    name: Account
  - type: attribute
    entity: sensor.pocketsmith_chase_checking_transactions
    attribute: institution_name
    name: Bank
```

### Last 5 Transactions Table

```yaml
type: markdown
title: Last 5 Transactions
content: |
  | Date | Payee | Amount |
  |------|-------|--------|
  {% set transactions = state_attr('sensor.pocketsmith_chase_checking_transactions', 'transactions') %}
  {% if transactions %}
    {% for transaction in transactions[:5] %}
  | {{ transaction.date }} | {{ transaction.payee }} | ${{ transaction.amount }} |
    {% endfor %}
  {% else %}
  | - | No transactions | - |
  {% endif %}
```

## Financial Overview Card

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: |
      # Financial Overview
      Track all your PocketSmith accounts in one place
  
  - type: entities
    title: Bank Accounts
    entities:
      - sensor.pocketsmith_account_checking
      - sensor.pocketsmith_account_savings
    
  - type: entities
    title: Credit Cards
    entities:
      - sensor.pocketsmith_account_visa
      - sensor.pocketsmith_account_mastercard
    
  - type: entities
    title: Investments
    entities:
      - sensor.pocketsmith_account_stocks
      - sensor.pocketsmith_account_retirement
```

## Account with Gauge

```yaml
type: gauge
entity: sensor.pocketsmith_account_123456
name: Checking Account
min: 0
max: 10000
severity:
  green: 2000
  yellow: 1000
  red: 0
```

## Custom Button Card (requires custom:button-card)

```yaml
type: custom:button-card
entity: sensor.pocketsmith_account_123456
name: Checking Account
show_state: true
show_icon: true
icon: mdi:bank
styles:
  card:
    - background-color: |
        [[[
          if (entity.state < 100) return 'red';
          if (entity.state < 500) return 'orange';
          return 'green';
        ]]]
  state:
    - font-size: 24px
    - font-weight: bold
```

## Mini Graph Card (requires custom:mini-graph-card)

```yaml
type: custom:mini-graph-card
entities:
  - sensor.pocketsmith_account_123456
name: Account Balance History
hours_to_show: 168
points_per_hour: 1
line_width: 2
font_size: 75
```

## Markdown Summary Card

```yaml
type: markdown
content: |
  ## Account Summary
  
  **Checking:** ${{ states('sensor.pocketsmith_account_checking') }}
  **Savings:** ${{ states('sensor.pocketsmith_account_savings') }}
  **Credit Card:** ${{ states('sensor.pocketsmith_account_visa') }}
  
  ---
  
  **Total Liquid Assets:** ${{ (states('sensor.pocketsmith_account_checking') | float + 
                                  states('sensor.pocketsmith_account_savings') | float) }}
```

## Conditional Card (show warning when balance is low)

```yaml
type: conditional
conditions:
  - entity: sensor.pocketsmith_account_123456
    state_not: unavailable
  - entity: sensor.pocketsmith_account_123456
    state_not: unknown
  - entity: sensor.pocketsmith_account_123456
    state_below: 500
card:
  type: markdown
  content: |
    ⚠️ **Warning:** Your checking account balance is low!
    Current balance: ${{ states('sensor.pocketsmith_account_123456') }}
```

## Glance Card

```yaml
type: glance
title: Quick Balance Overview
entities:
  - entity: sensor.pocketsmith_account_checking
    name: Checking
  - entity: sensor.pocketsmith_account_savings
    name: Savings
  - entity: sensor.pocketsmith_account_visa
    name: Credit Card
  - entity: sensor.pocketsmith_account_investment
    name: Investment
columns: 4
```

## Complete Dashboard Example

```yaml
title: Finances
views:
  - title: Overview
    path: overview
    cards:
      - type: markdown
        content: |
          # Financial Dashboard
          Updated: {{ now().strftime('%Y-%m-%d %H:%M') }}
      
      - type: horizontal-stack
        cards:
          - type: entity
            entity: sensor.pocketsmith_chase_checking
            name: Checking
            icon: mdi:bank
          - type: entity
            entity: sensor.pocketsmith_chase_savings
            name: Savings
            icon: mdi:piggy-bank
      
      - type: entities
        title: All Accounts
        entities:
          - sensor.pocketsmith_chase_checking
          - sensor.pocketsmith_chase_savings
          - sensor.pocketsmith_amex_credit_card
          - sensor.pocketsmith_discover_card
          - sensor.pocketsmith_fidelity_401k
      
      - type: markdown
        title: Recent Spending
        content: |
          {% set transactions = state_attr('sensor.pocketsmith_chase_checking_transactions', 'transactions') %}
          {% if transactions %}
          ### Last 3 Transactions:
            {% for transaction in transactions[:3] %}
          - **{{ transaction.date }}**: {{ transaction.payee }} - ${{ transaction.amount }}
            {% endfor %}
          {% endif %}

  - title: Transactions
    path: transactions
    cards:
      - type: markdown
        title: Checking Account Transactions
        content: |
          | Date | Payee | Amount | Category |
          |------|-------|--------|----------|
          {% set transactions = state_attr('sensor.pocketsmith_chase_checking_transactions', 'transactions') %}
          {% if transactions %}
            {% for transaction in transactions %}
          | {{ transaction.date }} | {{ transaction.payee }} | ${{ transaction.amount }} | {{ transaction.category if transaction.category else '-' }} |
            {% endfor %}
          {% endif %}
      
      - type: markdown
        title: Credit Card Transactions
        content: |
          | Date | Payee | Amount |
          |------|-------|--------|
          {% set transactions = state_attr('sensor.pocketsmith_amex_credit_card_transactions', 'transactions') %}
          {% if transactions %}
            {% for transaction in transactions %}
          | {{ transaction.date }} | {{ transaction.payee }} | ${{ transaction.amount }} |
            {% endfor %}
          {% endif %}
```

## Advanced Examples

### Calculate Monthly Spending

```yaml
type: markdown
title: Monthly Summary
content: |
  {% set transactions = state_attr('sensor.pocketsmith_chase_checking_transactions', 'transactions') %}
  {% set now = now() %}
  {% set current_month = now.month %}
  {% set current_year = now.year %}
  {% set spending = namespace(total=0) %}
  
  {% if transactions %}
    {% for transaction in transactions %}
      {% set trans_date = strptime(transaction.date, '%Y-%m-%d') %}
      {% if trans_date.month == current_month and trans_date.year == current_year %}
        {% if transaction.amount < 0 %}
          {% set spending.total = spending.total + (transaction.amount | float) %}
        {% endif %}
      {% endif %}
    {% endfor %}
  {% endif %}
  
  **Total Spending This Month**: ${{ spending.total | abs | round(2) }}
```

### Recent Large Transactions Alert

```yaml
type: conditional
conditions:
  - entity: sensor.pocketsmith_chase_checking_transactions
    state_not: "0"
card:
  type: markdown
  title: ⚠️ Large Transactions
  content: |
    {% set transactions = state_attr('sensor.pocketsmith_chase_checking_transactions', 'transactions') %}
    {% set large_transactions = [] %}
    {% if transactions %}
      {% for transaction in transactions %}
        {% if transaction.amount | float | abs > 200 %}
          {% set large_transactions = large_transactions + [transaction] %}
        {% endif %}
      {% endfor %}
    {% endif %}
    
    {% if large_transactions %}
      {% for transaction in large_transactions[:5] %}
    - **{{ transaction.date }}**: {{ transaction.payee }} - ${{ transaction.amount }}
      {% endfor %}
    {% else %}
    No large transactions (>$200) in recent history
    {% endif %}
```

### Spending by Category

```yaml
type: markdown
title: Spending by Category
content: |
  {% set transactions = state_attr('sensor.pocketsmith_chase_checking_transactions', 'transactions') %}
  {% set categories = {} %}
  
  {% if transactions %}
    {% for transaction in transactions %}
      {% if transaction.amount < 0 and transaction.category %}
        {% set cat = transaction.category %}
        {% if cat in categories %}
          {% set categories = dict(categories, **{cat: categories[cat] + (transaction.amount | float)}) %}
        {% else %}
          {% set categories = dict(categories, **{cat: transaction.amount | float}) %}
        {% endif %}
      {% endif %}
    {% endfor %}
  {% endif %}
  
  {% if categories %}
    {% for category, amount in categories.items() %}
  - **{{ category }}**: ${{ amount | abs | round(2) }}
    {% endfor %}
  {% else %}
  No categorized transactions available
  {% endif %}
```

## Automation Examples

### Low Balance Alert

```yaml
automation:
  - alias: "Low Balance Warning"
    trigger:
      - platform: numeric_state
        entity_id: sensor.pocketsmith_chase_checking
        below: 100
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "Low Balance Alert"
          message: "Your Chase checking account is below $100. Current balance: ${{ states('sensor.pocketsmith_chase_checking') }}"
```

### Large Transaction Notification

```yaml
automation:
  - alias: "Large Transaction Alert"
    trigger:
      - platform: state
        entity_id: sensor.pocketsmith_chase_checking_transactions
    condition:
      - condition: template
        value_template: >
          {% set transactions = state_attr('sensor.pocketsmith_chase_checking_transactions', 'transactions') %}
          {{ (transactions[0].amount | float | abs > 500) if transactions else false }}
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "Large Transaction Detected"
          message: >
            {% set transactions = state_attr('sensor.pocketsmith_chase_checking_transactions', 'transactions') %}
            {{ transactions[0].payee }}: ${{ transactions[0].amount }} on {{ transactions[0].date }}
```

### Weekly Spending Report

```yaml
automation:
  - alias: "Weekly Spending Report"
    trigger:
      - platform: time
        at: "09:00:00"
      - platform: state
        entity_id: binary_sensor.workday_sensor
        to: "on"
    condition:
      - condition: time
        weekday:
          - mon
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "Weekly Spending Report"
          message: >
            {% set transactions = state_attr('sensor.pocketsmith_chase_checking_transactions', 'transactions') %}
            {% set spending = namespace(total=0, count=0) %}
            {% set now = now() %}
            {% set week_ago = now - timedelta(days=7) %}
            
            {% if transactions %}
              {% for transaction in transactions %}
                {% set trans_date = strptime(transaction.date, '%Y-%m-%d') %}
                {% if trans_date >= week_ago and transaction.amount < 0 %}
                  {% set spending.total = spending.total + (transaction.amount | float | abs) %}
                  {% set spending.count = spending.count + 1 %}
                {% endif %}
              {% endfor %}
            {% endif %}
            
            You had {{ spending.count }} transactions totaling ${{ spending.total | round(2) }} this week.
```

## Tips

1. Replace entity IDs with your actual sensor names from Home Assistant
2. Find your entity IDs in **Settings** → **Devices & Services** → **Entities**
3. Search for "pocketsmith" to see all your sensors
4. Customize card styles, colors, and formatting to match your preferences
5. Use the Developer Tools → Template to test template code before adding to dashboards
6. Transaction amounts are negative for expenses and positive for income
7. Not all transactions may have categories or memos - use `if` checks in templates
