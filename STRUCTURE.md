# Project Structure

This document describes the complete structure of the PocketSmith Home Assistant integration.

## Directory Layout

```
pocketsmith/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md           # Bug report template
│   │   └── feature_request.md      # Feature request template
│   └── workflows/
│       └── validate.yaml           # GitHub Actions validation workflow
├── custom_components/
│   └── pocketsmith/
│       ├── translations/
│       │   └── en.json            # English translations
│       ├── __init__.py            # Integration setup and entry point
│       ├── config_flow.py         # UI configuration flow
│       ├── const.py               # Constants and configuration
│       ├── coordinator.py         # Data update coordinator
│       ├── manifest.json          # Integration manifest
│       ├── sensor.py              # Sensor platform implementation
│       └── strings.json           # UI strings
├── .gitignore                     # Git ignore rules
├── CHANGELOG.md                   # Version history
├── CONTRIBUTING.md                # Contribution guidelines
├── DEVELOPER.md                   # Developer documentation
├── EXAMPLES.md                    # Lovelace configuration examples
├── INSTALLATION.md                # Detailed installation guide
├── LICENSE                        # MIT License
├── README.md                      # Main documentation
├── hacs.json                      # HACS integration metadata
└── info.md                        # HACS display information
```

## Core Files Description

### Integration Files

#### `__init__.py`
- Entry point for the integration
- Handles setup and teardown of config entries
- Manages coordinator lifecycle
- Forwards platform setups

#### `config_flow.py`
- Implements UI-based configuration
- Validates API keys against PocketSmith API
- Creates and manages config entries
- Handles errors and user feedback

#### `const.py`
- Defines constants used throughout the integration
- API URLs, domain name, default values
- Centralized configuration values

#### `coordinator.py`
- Manages data fetching from PocketSmith API
- Implements polling with configurable intervals
- Handles API errors and retries
- Caches data for sensors

#### `sensor.py`
- Implements sensor platform
- Creates sensors for accounts and transaction accounts
- Defines sensor attributes and state classes
- Updates from coordinator data

#### `manifest.json`
- Home Assistant integration manifest
- Defines integration metadata
- Lists dependencies and requirements
- Specifies integration type and capabilities

#### `strings.json` & `translations/en.json`
- UI strings for configuration flow
- Error messages and descriptions
- Localization support

### Documentation Files

#### `README.md`
- Primary documentation
- Installation instructions
- Feature overview
- Usage examples

#### `INSTALLATION.md`
- Detailed step-by-step installation guide
- Multiple installation methods (HACS and manual)
- API key acquisition instructions
- Troubleshooting guide

#### `EXAMPLES.md`
- Lovelace dashboard examples
- Card configurations
- Template examples
- Complete dashboard layouts

#### `DEVELOPER.md`
- Technical architecture documentation
- API endpoint descriptions
- Development guidelines
- Future enhancement ideas

#### `CONTRIBUTING.md`
- Contribution guidelines
- Development setup instructions
- Code style requirements
- Pull request process

#### `CHANGELOG.md`
- Version history
- Feature additions
- Bug fixes
- Breaking changes

### HACS Files

#### `hacs.json`
- HACS metadata
- Repository configuration
- Integration identification

#### `info.md`
- Brief description for HACS interface
- Quick feature overview
- Setup summary

### GitHub Files

#### `.github/workflows/validate.yaml`
- Automated validation workflow
- HACS validation
- Hassfest validation
- Runs on push, PR, and schedule

#### `.github/ISSUE_TEMPLATE/`
- Standardized issue templates
- Bug report format
- Feature request format

## File Size Guidelines

- Python files: Well-commented, following PEP 8
- JSON files: Properly formatted and validated
- Markdown files: Clear structure with examples
- Keep individual files focused and maintainable

## Code Organization Principles

1. **Separation of Concerns**
   - Configuration logic in config_flow
   - Data fetching in coordinator
   - Sensor logic in sensor platform

2. **Reusability**
   - Common functions in appropriate modules
   - Shared constants in const.py
   - Entity descriptions for sensor definitions

3. **Error Handling**
   - Graceful degradation
   - User-friendly error messages
   - Comprehensive logging

4. **Testing Friendly**
   - Modular design
   - Clear interfaces
   - Minimal coupling

## Adding New Files

When adding new files:

1. **Python modules** → `custom_components/pocketsmith/`
2. **Translations** → `custom_components/pocketsmith/translations/`
3. **Documentation** → Root directory
4. **Examples** → EXAMPLES.md or new dedicated file
5. **Tests** → `tests/` directory (to be created)

## File Naming Conventions

- Python files: lowercase with underscores (`config_flow.py`)
- Documentation: UPPERCASE for important files (`README.md`)
- JSON files: lowercase (`manifest.json`)
- GitHub files: `.github/` directory with descriptive names

## Import Structure

```python
# Standard library imports
from __future__ import annotations
import logging
from typing import Any

# Third-party imports
import aiohttp
import voluptuous as vol

# Home Assistant imports
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
# ... more specific imports

# Local imports
from .const import DOMAIN
from .coordinator import PocketSmithDataUpdateCoordinator
```

## Version Control

- `.gitignore` excludes Python cache files, IDE configs, and virtual environments
- All source files are tracked
- Binary files and secrets are excluded
- Clear commit messages following conventional commits

## Quality Assurance

Files include:
- Type hints for better IDE support
- Docstrings for functions and classes
- Comments for complex logic
- Error handling and logging
- Input validation
