# Configuration

Nebula Orion provides flexible configuration options to customize the library's behavior for your specific needs.

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
api_keys:
  twitter: "your_twitter_api_key"
  openai: "your_openai_api_key"
  youtube: "your_youtube_api_key"

storage:
  type: "local"  # Options: local, s3, azure
  path: "./data"  # For local storage

processing:
  default_resolution: "1080p"
  threads: 4
  temp_directory: "./tmp"

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

Each module can have its own configuration section:

```yaml
# Module-specific configurations
betelgeuse:  # Social Media Management
  default_platforms: ["twitter", "instagram", "linkedin"]
  post_approval_required: true
  analytics_retention_days: 90

bellatrix:  # AI Toolkit
  default_model: "gpt-4"
  cache_responses: true
  max_tokens: 1000

rigel:  # Video Production
  default_format: "mp4"
  default_codec: "h264"
  render_quality: "high"

saiph:  # Automation
  notification_email: "admin@example.com"
  check_interval_minutes: 15
  max_concurrent_tasks: 5
```

## Environment Variables

For sensitive information or deployment-specific settings, you can use environment variables:

```bash
# Core settings
export ORION_API_KEY_TWITTER="your_twitter_api_key"
export ORION_API_KEY_OPENAI="your_openai_api_key"
export ORION_STORAGE_TYPE="s3"
export ORION_S3_BUCKET="my-bucket"

# Module-specific settings
export ORION_BETELGEUSE_DEFAULT_PLATFORMS="twitter,linkedin"
export ORION_BELLATRIX_DEFAULT_MODEL="gpt-4"
```

Environment variables take precedence over YAML configuration values.

## Programmatic Configuration

You can also configure Nebula Orion programmatically:

```python
from nebula_orion import config

# Set individual configuration values
config.set("api_keys.twitter", "your_api_key")
config.set("processing.threads", 8)

# Set multiple values at once
config.update({
    "storage": {
        "type": "s3",
        "bucket": "my-orion-data",
        "region": "us-west-2"
    },
    "betelgeuse": {
        "default_platforms": ["twitter", "instagram"]
    }
})

# Get configuration values
twitter_api_key = config.get("api_keys.twitter")
storage_type = config.get("storage.type")
```

## Per-Instance Configuration

For fine-grained control, you can pass configuration options directly when initializing module instances:

```python
from nebula_orion import betelgeuse, bellatrix

# Configure the social media manager instance
sm_manager = betelgeuse.SocialMediaManager(
    default_platforms=["twitter", "linkedin"],
    analytics_retention_days=60,
    post_approval_required=False
)

# Configure the AI toolkit instance
ai_toolkit = bellatrix.AIToolkit(
    default_model="gpt-4",
    cache_responses=True,
    max_tokens=1500
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

For sensitive information like API keys and passwords, we recommend using:

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

    # Update module configurations based on user preferences
    if "video_quality" in preferences:
        config.set("rigel.render_quality", preferences["video_quality"])

    if "ai_model" in preferences:
        config.set("bellatrix.default_model", preferences["ai_model"])
```

## Configuration Reference

For a complete list of configuration options, see the [Configuration API Reference](../api/config.md).

## Next Steps

Now that you understand how to configure Nebula Orion, check out:

- [Module Overview](../modules/overview.md) - Learn about the different modules
- [Tutorials](../tutorials/basic-usage.md) - Step-by-step guides for common use cases
