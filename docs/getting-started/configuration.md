# Configuration

Nebula Orion provides flexible configuration options to customize the library's behavior for your Notion workspace integration.

## Configuration Methods

There are several ways to configure Nebula Orion:

1. **YAML Configuration File** - The recommended approach for most projects
2. **Environment Variables** - Useful for sensitive information and deployment settings
3. **Programmatic Configuration** - For dynamic configuration needs
4. **Per-Instance Configuration** - For fine-grained control

## YAML Configuration

The simplest way to configure Nebula Orion is through a YAML configuration file. By default, Nebula Orion looks for a file named `orion_config.yaml` in your project root.

### Basic Configuration

Here's an example of a basic configuration file:

```yaml
# orion_config.yaml
notion:
  auth_token: "your_notion_api_token"  # For direct API token auth
  oauth:
    client_id: "your_client_id"        # For OAuth integration
    client_secret: "your_client_secret"
    redirect_uri: "your_redirect_uri"

storage:
  type: "local"  # Options: local, s3, azure
  path: "./data"  # For local storage

logging:
  level: "info"  # Options: debug, info, warning, error, critical
  file: "./logs/orion.log"
```

### Loading the Configuration

You can load the configuration file in your application:

```python
from nebula_orion import config

# Load default configuration (orion_config.yaml in current directory)
config.load()

# OR specify a custom configuration file path
config.load("/path/to/custom_config.yaml")
```

## Module-Specific Configuration

The Betelgeuse module can have its own configuration section:

```yaml
betelgeuse:
  # Notion API settings
  api_version: "2022-06-28"
  rate_limit_per_second: 3
  max_retries: 3
  retry_delay: 1.0

  # Cache settings
  cache_enabled: true
  cache_ttl: 300  # seconds
  cache_backend: "memory"  # Options: memory, redis

  # Sync settings
  sync_interval: 60  # seconds
  sync_chunk_size: 100

  # Template settings
  template_path: "./templates"
  default_locale: "en_US"
```

## Environment Variables

For sensitive information or deployment-specific settings, you can use environment variables:

```bash
# Core settings
export ORION_NOTION_TOKEN="your_notion_api_token"
export ORION_NOTION_CLIENT_ID="your_client_id"
export ORION_NOTION_CLIENT_SECRET="your_client_secret"

# Module-specific settings
export ORION_BETELGEUSE_API_VERSION="2022-06-28"
export ORION_BETELGEUSE_CACHE_ENABLED="true"
```

Environment variables take precedence over YAML configuration values.

## Programmatic Configuration

You can also configure Nebula Orion programmatically:

```python
from nebula_orion import config

# Set individual configuration values
config.set("notion.auth_token", "your_api_token")
config.set("betelgeuse.rate_limit_per_second", 5)

# Set multiple values at once
config.update({
    "notion": {
        "oauth": {
            "client_id": "your_client_id",
            "client_secret": "your_client_secret"
        }
    },
    "betelgeuse": {
        "cache_enabled": True,
        "cache_ttl": 600
    }
})

# Get configuration values
auth_token = config.get("notion.auth_token")
cache_enabled = config.get("betelgeuse.cache_enabled")
```

## Per-Instance Configuration

For fine-grained control, you can pass configuration options directly when initializing module instances:

```python
from nebula_orion.betelgeuse import NotionClient

# Configure the Notion client instance
client = NotionClient(
    auth_token="your_token",
    api_version="2022-06-28",
    rate_limit_per_second=5,
    cache_enabled=True,
    cache_ttl=300
)
```

## Configuration Precedence

Nebula Orion follows this order of precedence for configuration values (higher items override lower ones):

1. Direct instance configuration (e.g., passed to the constructor)
2. Programmatically set values (via `config.set()` or `config.update()`)
3. Environment variables
4. YAML configuration file
5. Default values

## Sensitive Information

For sensitive information like API tokens and OAuth credentials, we recommend using:

1. Environment variables (preferred for production)
2. A separate configuration file that is excluded from version control
3. Secret management services integrated with your deployment platform

Never store sensitive information directly in your code.

## Configuration Validation

Nebula Orion validates your configuration upon loading:

```python
try:
    config.load("orion_config.yaml")
except config.ValidationError as e:
    print(f"Configuration error: {e}")
    # Handle the error appropriately
```

## Advanced Configuration

### Multiple Environments

You can maintain multiple configuration files for different environments:

```python
# Development environment
if environment == "development":
    config.load("configs/dev_config.yaml")

# Production environment
elif environment == "production":
    config.load("configs/prod_config.yaml")
```

### Dynamic Configuration

For dynamic configuration that changes at runtime:

```python
# Update configuration based on user settings
def update_user_preferences(user_id, preferences):
    user_config = load_user_preferences(user_id)

    # Update Notion client configurations
    if "rate_limit" in preferences:
        config.set("betelgeuse.rate_limit_per_second", preferences["rate_limit"])

    if "cache_ttl" in preferences:
        config.set("betelgeuse.cache_ttl", preferences["cache_ttl"])
```

## Configuration Reference

For a complete list of configuration options, see the [Configuration API Reference](../api/config.md).

## Next Steps

Now that you understand how to configure Nebula Orion, check out:

- [Betelgeuse Module Overview](../modules/betelgeuse.md) - Learn about the Notion management features
- [Tutorials](../tutorials/basic-usage.md) - Step-by-step guides for common use cases
