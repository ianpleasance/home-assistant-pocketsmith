# Developer Documentation

## Architecture

The PocketSmith integration follows Home Assistant's modern integration patterns:

### Components

1. **Config Flow** (`config_flow.py`)
   - Handles UI-based configuration
   - Validates API keys against PocketSmith API
   - Creates config entries

2. **Coordinator** (`coordinator.py`)
   - Manages data fetching from PocketSmith API
   - Implements polling mechanism (5-minute interval)
   - Handles API errors and retries

3. **Sensor Platform** (`sensor.py`)
   - Creates sensors for accounts and transaction accounts
   - Updates from coordinator data
   - Provides rich attributes

### Data Flow

```
User enters API key
    ↓
Config Flow validates
    ↓
Integration setup creates Coordinator
    ↓
Coordinator fetches data every 5 minutes
    ↓
Sensors update from coordinator data
    ↓
Home Assistant displays sensor states
```

## PocketSmith API

### Base URL
`https://api.pocketsmith.com/v2`

### Authentication
Bearer token authentication via HTTP header:
```
Authorization: Bearer YOUR_API_KEY
```

### Endpoints Used

1. **GET /me**
   - Returns user information
   - Used for API key validation

2. **GET /accounts**
   - Returns all accounts
   - Includes balance, currency, institution details

3. **GET /transaction_accounts**
   - Returns transaction-level accounts
   - More granular than regular accounts

## Entity Naming

Entities follow this pattern:
- `sensor.pocketsmith_account_{account_id}` - for accounts
- `sensor.pocketsmith_transaction_account_{ta_id}` - for transaction accounts

## State Class

All balance sensors use `SensorStateClass.TOTAL` to indicate cumulative values.

## Adding New Features

### Adding New Sensor Types

1. Update `coordinator.py` to fetch required data
2. Add sensor description in `sensor.py`
3. Create entity class if needed
4. Update README with new sensor information

### Adding Configuration Options

1. Update `config_flow.py` schema
2. Add to `strings.json` for translations
3. Store in config entry data
4. Use in coordinator or sensors

## Testing Locally

1. Create a test Home Assistant instance
2. Copy integration to `custom_components/pocketsmith`
3. Configure with test API key
4. Monitor logs: `custom_components.pocketsmith: debug`

## API Rate Limiting

PocketSmith API has rate limits. The coordinator uses:
- 5-minute update interval (safe for most users)
- Timeout of 10 seconds per request
- Graceful error handling

## Error Handling

The integration handles:
- Network errors (cannot connect)
- Authentication errors (invalid API key)
- API response errors (unexpected status codes)
- Missing data (accounts not found)

All errors are logged and reported through Home Assistant's standard mechanisms.

## Future Enhancements

Potential features to add:
- Budget tracking sensors
- Category spending sensors
- Transaction history
- Net worth calculation
- Configurable update intervals
- Support for multiple currencies in dashboard
