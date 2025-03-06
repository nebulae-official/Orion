# 🔴 Betelgeuse - Notion Management

<div class="module-card">
  <h2><span class="emoji-icon">🔴</span> Betelgeuse</h2>
  <p>Named after the bright red supergiant star in the Orion constellation, Betelgeuse powers your Notion workspace with advanced features for content organization, database management, and workspace automation.</p>
</div>

## Overview

The Betelgeuse module provides comprehensive tools for managing your Notion workspace. Whether you're organizing documentation, managing projects, or building a knowledge base, Betelgeuse streamlines your workflow and enhances your Notion experience.

## Key Features

- **Database Management**: Create, query, and manage Notion databases with ease
- **Page Operations**: Create, update, and organize pages with rich content blocks
- **Content Blocks**: Support for all Notion block types including text, lists, tables, and embeds
- **Property System**: Flexible property management for databases and pages
- **OAuth Integration**: Secure authentication and authorization flow
- **Automated Workflows**: Create automated processes for content management
- **Rich API**: Comprehensive API for all Notion operations

## Installation

Betelgeuse can be installed as part of Nebula Orion:

```bash
pip install nebula-orion
```

## Basic Usage

### Authentication

```python
from nebula_orion import betelgeuse

# Initialize with API token
notion = betelgeuse.NotionClient(auth_token="your-notion-api-token")

# Or use OAuth
oauth = betelgeuse.NotionOAuth(
    client_id="your-client-id",
    client_secret="your-client-secret",
    redirect_uri="your-redirect-uri"
)
```

### Working with Databases

```python
# Create a new database
database = notion.databases.create(
    parent={"page_id": "parent-page-id"},
    title=[{"text": {"content": "Project Tracker"}}],
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
        "Due Date": {"date": {}}
    }
)

# Query a database
results = notion.databases.query(
    database_id="database-id",
    filter={
        "property": "Status",
        "select": {
            "equals": "In Progress"
        }
    },
    sorts=[
        {
            "property": "Due Date",
            "direction": "ascending"
        }
    ]
)
```

### Managing Pages

```python
# Create a new page
page = notion.pages.create(
    parent={"database_id": "database-id"},
    properties={
        "Name": {"title": [{"text": {"content": "New Feature Planning"}}]},
        "Status": {"select": {"name": "Not Started"}},
        "Due Date": {"date": {"start": "2024-04-01"}}
    },
    children=[
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"text": {"content": "Feature Overview"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"text": {"content": "Details about the new feature..."}}]
            }
        }
    ]
)

# Update a page
notion.pages.update(
    page_id="page-id",
    properties={
        "Status": {"select": {"name": "In Progress"}}
    }
)

# Get page content
page = notion.pages.retrieve("page-id")
blocks = notion.blocks.children.list("page-id")
```

## Advanced Features

### Using the Page Builder

```python
from nebula_orion.betelgeuse.page_builder import PageBuilder
from nebula_orion.betelgeuse.blocks import Heading1, Paragraph, TodoBlock

# Create a page with structured content
builder = PageBuilder(parent={"database_id": "database-id"})

# Add properties
builder.add_property("Name", "title", "Weekly Planning")
builder.add_property("Status", "select", "Not Started")

# Add content blocks
builder.add_block(Heading1("Objectives"))
builder.add_block(Paragraph("Key objectives for this week:"))
builder.add_block(TodoBlock("Review documentation", checked=False))
builder.add_block(TodoBlock("Update schemas", checked=False))

# Create the page
page = notion.pages.create_from_builder(builder)
```

### Query Builder

```python
from nebula_orion.betelgeuse.query import QueryBuilder

# Build a complex database query
query = QueryBuilder("database-id")

# Add filters
query.filter_property("Status", "select", "equals", "In Progress")
query.filter_property("Due Date", "date", "before", "2024-04-01")

# Add sorting
query.sort("Due Date", "ascending")

# Execute query
results = notion.databases.execute_query(query)
```

### Bulk Operations

```python
# Update multiple pages
pages = notion.databases.query("database-id").results
for page in pages:
    if page.properties["Status"]["select"]["name"] == "Complete":
        notion.pages.update(
            page_id=page.id,
            archived=True  # Archive completed pages
        )

# Copy database structure
template_db = notion.databases.retrieve("template-db-id")
new_db = notion.databases.create(
    parent={"page_id": "target-page-id"},
    title=template_db.title,
    properties=template_db.properties
)
```

## API Reference

For complete API documentation, see the [Betelgeuse API Reference](../api/betelgeuse.md).

## Examples and Tutorials

- [Setting Up Notion Integration](../tutorials/betelgeuse/setup.md)
- [Building a Project Management System](../tutorials/betelgeuse/project-management.md)
- [Automated Documentation Management](../tutorials/betelgeuse/documentation.md)
