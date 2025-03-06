# Installation

This guide will help you set up Nebula Orion in your environment with minimal effort.

## Prerequisites

Before installing Nebula Orion, make sure you have the following:

- Python 3.9 or higher
- pip (Python package installer)
- Virtual environment tool (recommended: venv, virtualenv, or conda)

## Installation Methods

### Method 1: Using pip

The simplest way to install Nebula Orion is using pip:

```bash
pip install nebula-orion
```

### Method 2: Using UV (Recommended)

For faster and more reliable dependency resolution, we recommend using UV:

```bash
uv pip install nebula-orion
```

### Method 3: From Source (For Development)

If you want to install the latest development version or contribute to Nebula Orion:

```bash
# Clone the repository
git clone https://github.com/yourusername/orion.git
cd orion

# Install using make
make install
```

## Verifying Installation

To verify that Nebula Orion has been installed correctly, run:

```python
import nebula_orion

# Should print the version
print(nebula_orion.__version__)

# Should print a welcome message
print(nebula_orion.hello())
```

If the above code runs without errors and displays the version number and welcome message, you've successfully installed Nebula Orion.

## Optional Dependencies

Depending on which modules you plan to use, you may need to install additional dependencies:

### Betelgeuse (Social Media Module)

```bash
pip install nebula-orion[betelgeuse]
```

### Bellatrix (AI Toolkit)

```bash
pip install nebula-orion[bellatrix]
```

### Rigel (Video Production)

```bash
pip install nebula-orion[rigel]
```

### Saiph (Automation System)

```bash
pip install nebula-orion[saiph]
```

### All Modules

To install all optional dependencies:

```bash
pip install nebula-orion[all]
```

## Troubleshooting

If you encounter any issues during installation, try the following:

1. Ensure you have the latest version of pip:
   ```bash
   python -m pip install --upgrade pip
   ```

2. If you're using Windows and encounter build errors, you might need to install Visual C++ Build Tools.

3. If you're having dependency conflicts, try using a virtual environment:
   ```bash
   python -m venv orion-env
   source orion-env/bin/activate  # On Windows: orion-env\Scripts\activate
   pip install nebula-orion
   ```

4. For further assistance, please [open an issue](https://github.com/yourusername/orion/issues) on our GitHub repository.

## Next Steps

Now that you have Nebula Orion installed, check out the [Quick Start Guide](quick-start.md) to begin using it in your projects.
