# Module Overview

Nebula Orion is focused on providing a robust Notion management system through its core module, Betelgeuse.

## Architecture Philosophy

The Orion library follows a focused architecture where Betelgeuse provides comprehensive Notion integration and management capabilities.

<div class="module-card">
  <h2><span class="emoji-icon">🔴</span> Betelgeuse</h2>
  <p><strong>Focus:</strong> Notion Management</p>
  <p>Like its namesake red supergiant star, Betelgeuse is the core module of Orion, handling all your Notion workspace needs. It manages databases, pages, content organization, permissions, and integrations.</p>
  <p><a href="betelgeuse/" class="md-button">Betelgeuse Documentation</a></p>
</div>

## Getting Started with Betelgeuse

The module follows a consistent pattern for ease of use:

1. Import the module
2. Initialize the Notion client
3. Use the provided methods to manage your Notion workspace

Here's a basic example:

```python
from nebula_orion import betelgeuse

# Initialize the module
notion = betelgeuse.NotionClient(auth_token="your-token")

# Use the module's functionality
page = notion.pages.create(
    parent={"database_id": "your-database-id"},
    properties={
        "Name": {"title": [{"text": {"content": "New Page"}}]}
    }
)
```

## Next Steps

Explore Betelgeuse in detail:

- [Betelgeuse Documentation](betelgeuse.md)
