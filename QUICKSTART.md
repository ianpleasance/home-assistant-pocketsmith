# Quick Start Guide

Get your PocketSmith integration up and running in 5 minutes!

## 🚀 Prerequisites

- ✅ Home Assistant 2023.1.0 or newer
- ✅ HACS installed
- ✅ PocketSmith account

## 📝 Step 1: Get Your API Key (2 minutes)

1. Go to https://my.pocketsmith.com/developer
2. Click **"Generate New API Key"**
3. Name it "Home Assistant"
4. Click **"Generate"**
5. **Copy the key immediately** (you won't see it again!)

## 📦 Step 2: Install Integration (1 minute)

### Via HACS (Recommended)

1. Open HACS → Integrations
2. Click ⋮ → Custom repositories
3. Add: `https://github.com/cloudbr34k84/home-assistant-pocketsmith`
4. Category: Integration
5. Search "PocketSmith" and install

### Manual Install

Copy `custom_components/pocketsmith/` to your Home Assistant's `custom_components/` folder.

## ⚙️ Step 3: Configure (1 minute)

1. Restart Home Assistant
2. Go to Settings → Devices & Services
3. Click **+ Add Integration**
4. Search "PocketSmith"
5. Enter your API key
6. Click **Submit**

## ✨ Done!

Your PocketSmith accounts are now available as sensors in Home Assistant!

## 🎯 What's Next?

### View Your Sensors

Go to **Settings** → **Devices & Services** → **Entities** and search for "pocketsmith"

### Create a Dashboard

```yaml
type: entities
title: My Finances
entities:
  - sensor.pocketsmith_account_123456
  - sensor.pocketsmith_account_789012
```

### Set Up Alerts

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
        message: "Account balance is low!"
```

## 📚 Learn More

- [Full README](README.md) - Complete documentation
- [Examples](EXAMPLES.md) - Dashboard configurations
- [Installation Guide](INSTALLATION.md) - Detailed setup help
- [Developer Docs](DEVELOPER.md) - Technical details

## ❓ Need Help?

- Check the [Troubleshooting](#troubleshooting) section below
- [Open an issue](https://github.com/cloudbr34k84/home-assistant-pocketsmith/issues)
- Review [Home Assistant logs](https://my.home-assistant.io/redirect/logs/)

## 🔧 Troubleshooting

### Integration Not Found After Install

```bash
# 1. Clear browser cache (Ctrl+Shift+R)
# 2. Restart Home Assistant
# 3. Check files are in: config/custom_components/pocketsmith/
```

### Invalid API Key Error

```bash
# 1. Verify you copied the complete key
# 2. Check key is active at: https://my.pocketsmith.com/developer
# 3. Try generating a new key
```

### Sensors Not Updating

```yaml
# Enable debug logging in configuration.yaml:
logger:
  logs:
    custom_components.pocketsmith: debug

# Then restart and check logs
```

### Still Stuck?

Enable debug logging and [open an issue](https://github.com/cloudbr34k84/home-assistant-pocketsmith/issues) with:
- Your Home Assistant version
- Integration version
- Relevant logs
- Steps to reproduce

## 🎉 Success Checklist

- ✅ API key generated
- ✅ Integration installed
- ✅ Home Assistant restarted
- ✅ Integration configured
- ✅ Sensors visible in entities list
- ✅ Balance data showing correctly

**Congratulations! You're all set!** 🎊
