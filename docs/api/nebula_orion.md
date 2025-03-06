# API Reference: nebula_orion

<div class="doc-contents">
  <p>Core API documentation for the nebula_orion package</p>
</div>

## Core Package

::: nebula_orion
    options:
      show_root_heading: false
      show_if_no_docstring: true

## Module Functions

### hello

::: nebula_orion.hello
    options:
      show_root_heading: false

## Constants

### __version__

```python
__version__ = "0.1.0"
```

The current version of the nebula_orion package.

### __author__

```python
__author__ = "Gishant Singh"
```

The author of the nebula_orion package.

### __email__

```python
__email__ = "khiladisngh@hotmail.com"
```

Contact email for the nebula_orion package.

### __license__

```python
__license__ = "MIT"
```

License information for the nebula_orion package.

## Usage Examples

```python
import nebula_orion

# Print welcome message
print(nebula_orion.hello())

# Print version information
print(f"Nebula Orion version: {nebula_orion.__version__}")
```

## Module Structure

Nebula Orion follows a focused structure with its core Notion management module:

```
nebula_orion/
├── __init__.py       # Core package initialization
├── main.py          # Main entry point
├── betelgeuse/      # Notion Management module
    ├── api/         # Notion API client implementations
    ├── blocks/      # Block type definitions
    ├── demo/        # Demo application
    ├── oauth/       # OAuth implementation
    ├── properties/  # Property type definitions
    ├── sync/        # Sync utilities
    └── templates/   # Template definitions
```

## See Also

- [betelgeuse API](betelgeuse.md) - Notion Management API
