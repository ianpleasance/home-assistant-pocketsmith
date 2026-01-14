# Contributing to PocketSmith Integration

Thank you for your interest in contributing to the PocketSmith Home Assistant integration!

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature/fix

## Development Setup

1. Install Home Assistant in development mode
2. Copy the `custom_components/pocketsmith` directory to your Home Assistant's `custom_components` directory
3. Restart Home Assistant
4. Enable debug logging in `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.pocketsmith: debug
```

## Testing

Before submitting a pull request:

1. Test the integration with a valid PocketSmith API key
2. Verify all sensors are created correctly
3. Check that updates work as expected
4. Review logs for any errors or warnings

## Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to functions and classes
- Keep functions focused and small

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the version number in `manifest.json`
3. Create a pull request with a clear description of changes
4. Wait for review and address any feedback

## Questions?

Open an issue if you have questions or need help!
