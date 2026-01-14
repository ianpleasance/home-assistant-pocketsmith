# Installation Guide

## Prerequisites

- Home Assistant 2023.1.0 or newer
- A PocketSmith account with API access
- HACS installed (for HACS installation method)

## Method 1: HACS Installation (Recommended)

### Step 1: Add Custom Repository

1. Open HACS in your Home Assistant interface
2. Click on **Integrations**
3. Click the **⋮** (three dots) menu in the top right
4. Select **Custom repositories**
5. Add the following:
   - **Repository**: `https://github.com/cloudbr34k84/home-assistant-pocketsmith`
   - **Category**: Integration
6. Click **Add**

### Step 2: Install via HACS

1. Search for "PocketSmith" in HACS
2. Click on the PocketSmith integration
3. Click **Download**
4. Select the latest version
5. Click **Download** again

### Step 3: Restart Home Assistant

1. Go to **Settings** → **System**
2. Click **Restart**
3. Wait for Home Assistant to restart

### Step 4: Configure the Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "PocketSmith"
4. Click on PocketSmith when it appears
5. Enter your PocketSmith API key (see below for how to get it)
6. Click **Submit**

## Method 2: Manual Installation

### Step 1: Download Files

Download the latest release from GitHub or clone the repository:

```bash
git clone https://github.com/cloudbr34k84/home-assistant-pocketsmith.git
```

### Step 2: Copy Files

Copy the `custom_components/pocketsmith` folder to your Home Assistant's `custom_components` directory:

```
<config_dir>/
└── custom_components/
    └── pocketsmith/
        ├── __init__.py
        ├── config_flow.py
        ├── const.py
        ├── coordinator.py
        ├── manifest.json
        ├── sensor.py
        ├── strings.json
        └── translations/
            └── en.json
```

### Step 3: Restart and Configure

Follow steps 3 and 4 from the HACS installation method above.

## Getting Your PocketSmith API Key

### Step 1: Log into PocketSmith

1. Go to [https://my.pocketsmith.com](https://my.pocketsmith.com)
2. Log in with your credentials

### Step 2: Access Developer Settings

1. Click on your profile in the top right
2. Select **Settings**
3. Click on **Security** in the left menu
4. Scroll down to **Developer** section

### Step 3: Generate API Key

1. Click **Generate New API Key**
2. Give your key a name (e.g., "Home Assistant")
3. Click **Generate**
4. **Copy the API key immediately** - you won't be able to see it again!

### Step 4: Use API Key in Home Assistant

Paste the copied API key into the PocketSmith integration setup in Home Assistant.

## Verifying Installation

After configuration, you should see:

1. A new integration card for PocketSmith in **Settings** → **Devices & Services**
2. New sensor entities in **Settings** → **Devices & Services** → **Entities**
3. Sensors named like:
   - `sensor.pocketsmith_account_123456`
   - `sensor.pocketsmith_transaction_account_789012`

## Troubleshooting

### Integration Not Found

- Ensure you've restarted Home Assistant after installation
- Check that files are in the correct location
- Clear your browser cache

### Invalid API Key Error

- Verify you copied the complete API key
- Check that the API key hasn't been revoked in PocketSmith
- Try generating a new API key

### Sensors Not Updating

- Check Home Assistant logs for errors
- Verify your internet connection
- Ensure PocketSmith API is operational

### Still Having Issues?

1. Enable debug logging:

```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.pocketsmith: debug
```

2. Restart Home Assistant
3. Check the logs under **Settings** → **System** → **Logs**
4. [Open an issue](https://github.com/cloudbr34k84/home-assistant-pocketsmith/issues) with the logs

## Next Steps

Once installed, check out the [README](README.md) for:
- Usage examples
- Dashboard configuration
- Automation ideas
