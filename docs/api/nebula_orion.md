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

### \_\_version\_\_

```python
__version__ = "0.1.0"
```

The current version of the nebula_orion package.

### \_\_author\_\_

```python
__author__ = "Gishant Singh"
```

The author of the nebula_orion package.

### \_\_email\_\_

```python
__email__ = "khiladisngh@hotmail.com"
```

Contact email for the nebula_orion package.

### \_\_license\_\_

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

Nebula Orion follows a modular structure with the following key components:

```
nebula_orion/
├── __init__.py       # Core package initialization
├── main.py           # Main entry point
├── betelgeuse/       # Social Media Management module
├── bellatrix/        # AI Toolkit module
├── rigel/            # Video Production module
└── saiph/            # Automation System module
```

## See Also

- [betelgeuse API](betelgeuse.md) - Social Media Management API
- [bellatrix API](bellatrix.md) - AI Toolkit API
- [rigel API](rigel.md) - Video Production API
- [saiph API](saiph.md) - Automation System API
