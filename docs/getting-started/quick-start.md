# Quick Start Guide

This guide will help you get up and running with Nebula Orion quickly. We'll explore the basics of Notion workspace management to give you a solid foundation.

## Basic Usage

After [installing Nebula Orion](installation.md) and setting up your Notion integration, you can start managing your workspace:

```python
from nebula_orion.betelgeuse import NotionClient

# Initialize the client
notion = NotionClient(auth_token="your-notion-api-token")

# Print version
print(notion.version)
```

## Essential Operations

### Working with Pages

```python
# Create a simple page
page = notion.pages.create(
    parent={"page_id": "your-parent-page-id"},
    properties={
        "title": [{"text": {"content": "My New Page"}}]
    },
    children=[
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"text": {"content": "Welcome!"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"text": {"content": "This is my first page created with Nebula Orion."}}]
            }
        }
    ]
)

# Update a page
notion.pages.update(
    page_id=page.id,
    properties={
        "title": [{"text": {"content": "Updated Title"}}]
    }
)

# Get page content
page_content = notion.blocks.children.list(page.id)
```

### Managing Databases

```python
# Create a database
database = notion.databases.create(
    parent={"page_id": "your-parent-page-id"},
    title=[{"text": {"content": "Project Tasks"}}],
    properties={
        "Name": {"title": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "Not Started", "color": "red"},
                    {"name": "In Progress", "color": "yellow"},
                    {"name": "Complete", "color": "green"}
                ]
            }
        },
        "Priority": {
            "select": {
                "options": [
                    {"name": "High", "color": "red"},
                    {"name": "Medium", "color": "yellow"},
                    {"name": "Low", "color": "blue"}
                ]
            }
        },
        "Due Date": {"date": {}}
    }
)

# Add entries to database
notion.pages.create(
    parent={"database_id": database.id},
    properties={
        "Name": {"title": [{"text": {"content": "Important Task"}}]},
        "Status": {"select": {"name": "Not Started"}},
        "Priority": {"select": {"name": "High"}},
        "Due Date": {"date": {"start": "2024-04-01"}}
    }
)

# Query database
results = notion.databases.query(
    database_id=database.id,
    filter={
        "and": [
            {
                "property": "Status",
                "select": {"equals": "Not Started"}
            },
            {
                "property": "Priority",
                "select": {"equals": "High"}
            }
        ]
    },
    sorts=[
        {
            "property": "Due Date",
            "direction": "ascending"
        }
    ]
)
```

### Using Blocks

```python
# Add blocks to a page
notion.blocks.children.append(
    page.id,
    children=[
        {
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"text": {"content": "Task to complete"}}],
                "checked": False
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"text": {"content": "Important note!"}}],
                "icon": {"emoji": "⚠️"}
            }
        }
    ]
)

# Update a block
notion.blocks.update(
    block_id="your-block-id",
    to_do={
        "rich_text": [{"text": {"content": "Updated task"}}],
        "checked": True
    }
)
```

### Using the Builder Pattern

```python
from nebula_orion.betelgeuse.page_builder import PageBuilder
from nebula_orion.betelgeuse.blocks import (
    Heading1, Paragraph, TodoBlock, Callout
)

# Create a structured page
builder = PageBuilder(parent={"database_id": database.id})

# Add properties
builder.add_property("Name", "Weekly Review")
builder.add_property("Status", "Not Started")
builder.add_property("Priority", "High")

# Add content blocks
builder.add_block(Heading1("Weekly Objectives"))
builder.add_block(Paragraph("Key items to review this week:"))
builder.add_block(TodoBlock("Review project status", checked=False))
builder.add_block(TodoBlock("Update documentation", checked=False))
builder.add_block(Callout("Remember to update metrics!", icon="📊"))

# Create the page
page = notion.pages.create_from_builder(builder)
```

## Error Handling

```python
from nebula_orion.betelgeuse.errors import NotionError

try:
    page = notion.pages.retrieve("invalid-page-id")
except NotionError as e:
    print(f"Error: {e.message}")
    print(f"Status: {e.status}")
    print(f"Code: {e.code}")
```

## Configuration

```python
# Configure with options
notion = NotionClient(
    auth_token="your-token",
    api_version="2022-06-28",
    rate_limit_per_second=3,
    cache_enabled=True,
    cache_ttl=300
)

# Or use configuration file
from nebula_orion import config

config.load("orion_config.yaml")
notion = NotionClient()  # Will use config file settings
```

## Next Steps

Now that you understand the basics, explore these resources:

- [Betelgeuse Module Documentation](../modules/betelgeuse.md) - Complete documentation of Notion management features
- [Configuration Guide](configuration.md) - Learn about advanced configuration options
- [Working with Databases](../tutorials/databases.md) - In-depth guide to database management
- [Managing Pages](../tutorials/pages.md) - Detailed page operations guide
