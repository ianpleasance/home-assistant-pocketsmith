# PocketSmith Sensor Names and Attributes - Complete Examples

This document shows exactly what your sensors will look like in Home Assistant.

## 🎯 Entity ID Naming Strategy

**Why use account IDs instead of names?**

✅ **Stability**: Entity IDs never change, even if you rename accounts
✅ **Reliable Automations**: Your automations keep working forever
✅ **Consistent Dashboards**: No broken entity references

**Entity IDs**:
- Balance: `sensor.pocketsmith_account_{account_id}`
- Transactions: `sensor.pocketsmith_transactions_{transaction_account_id}`

**Friendly Names** (shown in UI):
- Automatically set to: "PocketSmith {Institution} {Account Name}"
- Updates automatically when you rename accounts in PocketSmith

### Example Scenario:
1. Initial setup: Entity `sensor.pocketsmith_account_123456`, Name "PocketSmith Chase Checking"
2. You rename to "Main Checking" in PocketSmith  
3. Entity stays: `sensor.pocketsmith_account_123456` ✅
4. Name updates to: "PocketSmith Chase Main Checking" ✅
5. All automations continue working ✅

---

## 💰 Account Balance Sensors

### Example 1: Chase Checking Account

**Entity ID**: `sensor.pocketsmith_account_123456`  
**Friendly Name**: `PocketSmith Chase Checking`

```yaml
State: 2,543.67
Unit: USD

Attributes:
  current_balance: 2543.67
  currency: USD
  institution_name: Chase
  account_name: Checking
  account_number: "****1234"
  account_type: bank
  current_balance_date: "2025-01-09T10:30:00Z"
  current_balance_exchange_rate: 1.0
  safe_balance: 2343.67
  safe_balance_in_base_currency: 2343.67
```

---

### Example 2: Bank of America Savings

**Entity ID**: `sensor.pocketsmith_account_789012`  
**Friendly Name**: `PocketSmith Bank of America Savings`

```yaml
State: 15,892.34
Unit: USD

Attributes:
  current_balance: 15892.34
  currency: USD
  institution_name: Bank of America
  account_name: Savings
  account_number: "****5678"
  account_type: savings
  current_balance_date: "2025-01-09T10:30:00Z"
  current_balance_exchange_rate: 1.0
  safe_balance: 15892.34
  safe_balance_in_base_currency: 15892.34
```

---

### Example 3: American Express Credit Card

**Entity ID**: `sensor.pocketsmith_account_345678`  
**Friendly Name**: `PocketSmith American Express Blue Cash`

```yaml
State: -1,234.56
Unit: USD

Attributes:
  current_balance: -1234.56
  currency: USD
  institution_name: American Express
  account_name: Blue Cash
  account_number: "****9012"
  account_type: credit_card
  current_balance_date: "2025-01-09T10:30:00Z"
  current_balance_exchange_rate: 1.0
  safe_balance: -1234.56
  safe_balance_in_base_currency: -1234.56
```

💡 **Note**: Credit cards show negative balances (what you owe)

---

### Example 4: Barclays UK Account (Foreign Currency)

**Entity ID**: `sensor.pocketsmith_account_901234`  
**Friendly Name**: `PocketSmith Barclays Current Account`

```yaml
State: 3,450.00
Unit: GBP

Attributes:
  current_balance: 3450.00
  currency: GBP
  institution_name: Barclays
  account_name: Current Account
  account_number: "12345678"
  account_type: bank
  current_balance_date: "2025-01-09T10:30:00Z"
  current_balance_exchange_rate: 1.27
  safe_balance: 3200.00
  safe_balance_in_base_currency: 4064.00
```

💡 **Note**: Exchange rate converts to your base currency

---

### Example 5: Investment Account (No Account Number)

**Entity ID**: `sensor.pocketsmith_account_567890`  
**Friendly Name**: `PocketSmith Fidelity 401k`

```yaml
State: 87,543.21
Unit: USD

Attributes:
  current_balance: 87543.21
  currency: USD
  institution_name: Fidelity
  account_name: 401k
  account_number: null
  account_type: investment
  current_balance_date: "2025-01-09T10:30:00Z"
  current_balance_exchange_rate: 1.0
  safe_balance: 87543.21
  safe_balance_in_base_currency: 87543.21
```

💡 **Note**: Account number may be `null` for investment accounts

---

## 📊 Transaction History Sensors

### Example 1: Chase Checking Transactions

**Entity ID**: `sensor.pocketsmith_transactions_123456`  
**Friendly Name**: `PocketSmith Chase Checking Transactions`

```yaml
State: 20
Unit: (none)

Attributes:
  account_name: Checking
  institution_name: Chase
  currency: USD
  transaction_count: 20
  transactions:
    - amount: -45.67
      payee: Whole Foods Market
      date: "2025-01-09"
      memo: Weekly groceries
      category: Groceries
    
    - amount: -12.99
      payee: Netflix
      date: "2025-01-08"
      memo: null
      category: Entertainment
    
    - amount: -85.00
      payee: Shell Gas Station
      date: "2025-01-08"
      memo: Fill up
      category: Transportation
    
    - amount: 2500.00
      payee: Acme Corp - Direct Deposit
      date: "2025-01-05"
      memo: Salary
      category: Income
    
    - amount: -150.00
      payee: Electric Company
      date: "2025-01-04"
      memo: December bill
      category: Bills
    
    - amount: -23.45
      payee: Starbucks
      date: "2025-01-03"
      memo: null
      category: Dining
    
    - amount: -67.89
      payee: Amazon.com
      date: "2025-01-03"
      memo: Office supplies
      category: Shopping
    
    - amount: -15.00
      payee: Spotify
      date: "2025-01-01"
      memo: Monthly subscription
      category: Entertainment
    
    # ... up to 20 total transactions
```

💡 **Transaction Notes**:
- Negative amounts = expenses/charges
- Positive amounts = income/deposits
- `memo` and `category` may be `null` if not set

---

### Example 2: Credit Card Transactions

**Entity ID**: `sensor.pocketsmith_transactions_789012`  
**Friendly Name**: `PocketSmith American Express Blue Cash Transactions`

```yaml
State: 15
Unit: (none)

Attributes:
  account_name: Blue Cash
  institution_name: American Express
  currency: USD
  transaction_count: 15
  transactions:
    - amount: -234.56
      payee: Apple Store
      date: "2025-01-08"
      memo: null
      category: null
    
    - amount: -45.00
      payee: Amazon Prime
      date: "2025-01-07"
      memo: null
      category: null
    
    # ... more transactions
```

---

## 🔍 Finding Your Sensors

### Method 1: Developer Tools
1. **Developer Tools** → **States**
2. Search: "pocketsmith"
3. See all entity IDs and current states

### Method 2: Entities Page
1. **Settings** → **Devices & Services** → **Entities**
2. Filter: "pocketsmith"
3. View entity IDs, friendly names, and states

### Method 3: Integration Page
1. **Settings** → **Devices & Services**
2. Find "PocketSmith" integration
3. Click to see all entities

---

## 📝 Using in Dashboards

### Simple Balance Card
```yaml
type: entity
entity: sensor.pocketsmith_account_123456
# Friendly name shows automatically
```

### Custom Name
```yaml
type: entity
entity: sensor.pocketsmith_account_123456
name: Main Checking  # Override display name
icon: mdi:bank
```

### Multiple Accounts
```yaml
type: entities
title: Financial Accounts
entities:
  - entity: sensor.pocketsmith_account_123456
    name: Chase Checking
  - entity: sensor.pocketsmith_account_789012
    name: BofA Savings
  - entity: sensor.pocketsmith_account_345678
    name: Amex Card
```

### Transaction List
```yaml
type: markdown
title: Recent Transactions
content: |
  {% set trans = state_attr('sensor.pocketsmith_transactions_123456', 'transactions') %}
  {% if trans %}
    {% for t in trans[:5] %}
  - **{{ t.date }}**: {{ t.payee }} - ${{ t.amount }}
    {% endfor %}
  {% endif %}
```

---

## 🔨 Template Examples

### Get Balance
```yaml
{{ states('sensor.pocketsmith_account_123456') }}
```
Output: `2543.67`

### Get Institution
```yaml
{{ state_attr('sensor.pocketsmith_account_123456', 'institution_name') }}
```
Output: `Chase`

### Get Account Name
```yaml
{{ state_attr('sensor.pocketsmith_account_123456', 'account_name') }}
```
Output: `Checking`

### Get Last Transaction
```yaml
{% set trans = state_attr('sensor.pocketsmith_transactions_123456', 'transactions') %}
{{ trans[0].payee if trans else 'None' }}
```
Output: `Whole Foods Market`

### Calculate Weekly Spending
```yaml
{% set trans = state_attr('sensor.pocketsmith_transactions_123456', 'transactions') %}
{% set week_ago = now() - timedelta(days=7) %}
{% set total = namespace(value=0) %}
{% if trans %}
  {% for t in trans %}
    {% if strptime(t.date, '%Y-%m-%d') >= week_ago and t.amount < 0 %}
      {% set total.value = total.value + (t.amount | float | abs) %}
    {% endif %}
  {% endfor %}
{% endif %}
${{ total.value | round(2) }}
```

---

## 🤖 Automation Examples

### Low Balance Alert
```yaml
automation:
  - alias: "Low Balance Warning"
    trigger:
      platform: numeric_state
      entity_id: sensor.pocketsmith_account_123456
      below: 100
    action:
      service: notify.mobile_app
      data:
        title: "Low Balance"
        message: "Balance: ${{ states('sensor.pocketsmith_account_123456') }}"
```

### Large Transaction Alert
```yaml
automation:
  - alias: "Large Purchase Notification"
    trigger:
      platform: state
      entity_id: sensor.pocketsmith_transactions_123456
    condition:
      template: >
        {% set trans = state_attr('sensor.pocketsmith_transactions_123456', 'transactions') %}
        {{ (trans[0].amount | float | abs > 200) if trans else false }}
    action:
      service: notify.mobile_app
      data:
        title: "Large Transaction"
        message: >
          {% set trans = state_attr('sensor.pocketsmith_transactions_123456', 'transactions') %}
          {{ trans[0].payee }}: ${{ trans[0].amount }}
```

### Daily Spending Report
```yaml
automation:
  - alias: "Daily Spending Summary"
    trigger:
      platform: time
      at: "20:00:00"
    action:
      service: notify.mobile_app
      data:
        title: "Today's Spending"
        message: >
          {% set trans = state_attr('sensor.pocketsmith_transactions_123456', 'transactions') %}
          {% set today = now().date() | string %}
          {% set total = namespace(value=0) %}
          {% if trans %}
            {% for t in trans if t.date == today and t.amount < 0 %}
              {% set total.value = total.value + (t.amount | float | abs) %}
            {% endfor %}
          {% endif %}
          You spent ${{ total.value | round(2) }} today
```

---

## 💡 Key Points

1. **Entity IDs are stable** - Based on PocketSmith account IDs (never change)
2. **Friendly names update** - Reflect current names from PocketSmith
3. **All attributes included** - Balance, currency, institution, account name/number
4. **20 transactions max** - Most recent transactions per account
5. **Updates every 5 minutes** - Automatic refresh
6. **Multi-currency support** - Each account shows its native currency
7. **Automations stay stable** - No broken entity references when renaming accounts

---

## ❓ FAQs

**Q: Can I customize entity IDs?**  
A: No, entity IDs are automatically generated. You can customize friendly names in the UI.

**Q: What if I rename an account?**  
A: Entity ID stays the same, friendly name updates automatically. Your automations keep working!

**Q: How do I find my account IDs?**  
A: Check Developer Tools → States or Settings → Entities. Look at the entity_id.

**Q: Can I get more than 20 transactions?**  
A: Currently limited to 20. This keeps the API calls efficient and sensor size manageable.

**Q: Do credit card balances show positive or negative?**  
A: Negative (showing what you owe). Positive balances mean credit/overpayment.

**Q: What if account_number is missing?**  
A: Some account types (investments) don't have account numbers. It will show as `null`.
