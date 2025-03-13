# 🌠 Betelgeuse
A Python library for seamless interaction with Notion workspaces through Notion's REST API.

## 📋 Overview
Betelgeuse is a powerful Notion API wrapper that enables developers to programmatically interact with Notion pages, databases, and blocks. Part of the Nebula Orion project, it provides an intuitive interface for creating, reading, updating, and querying Notion content.

```python
from nebula_orion.betelgeuse import NotionClient

# Initialize client with your Notion API key
client = NotionClient(auth_token="secret_...")

# Retrieve a page
page = client.pages.retrieve("page-id")
print(f"Page title: {page.get_title()}")

# Create a new page in a database
new_page = client.pages.create(
    parent={"database_id": "database-id"},
    properties={
        "Name": {"title": [{"text": {"content": "Project Plan"}}]},
        "Status": {"select": {"name": "In Progress"}}
    }
)
```

## ✨ Features
- **Complete API Coverage**: Full support for Notion's REST API endpoints
- **Rich Object Models**: Pythonic object models for all Notion resources
- **Builder Patterns**: Fluent interfaces for creating complex Notion structures
- **Error Handling**: Robust exception handling and retry mechanisms
- **Type Hinting**: Comprehensive type annotations for improved developer experience
- **Async Support**: Both synchronous and asynchronous interfaces
- **Pagination Utilities**: Simplified handling of paginated API responses
- **Local Sync**: Synchronize Notion content with local storage
- **OAuth Support**: Authentication via Notion's OAuth 2.0 implementation

## 🚀 Getting Started

### Installation
```sh
pip install nebula-orion
```

### Basic Usage
```python
from nebula_orion.betelgeuse import NotionClient

# Initialize with API token
client = NotionClient(auth_token="secret_...")

# Query a database
results = client.databases.query(
    database_id="database-id",
    filter={
        "property": "Status",
        "select": {
            "equals": "In Progress"
        }
    }
)

# Process results
for page in results:
    print(f"Page: {page.get_title()}")
```

### Creating Content With Builders
```python
from nebula_orion.betelgeuse import NotionClient
from nebula_orion.betelgeuse.builders import PageBuilder

client = NotionClient(auth_token="secret_...")

# Use builder pattern for complex page creation
builder = PageBuilder(parent={"database_id": "database-id"})
builder.add_title("Weekly Report")
builder.add_property("Status", "In Progress")
builder.add_heading_1("Summary")
builder.add_paragraph("This week we accomplished several key objectives...")
builder.add_todo("Follow up with team", checked=False)

# Create the page
page = client.pages.create_from_builder(builder)
print(f"Created page: {page.url}")
```

## 📚 Content Management
### Working with Pages
```python
# Retrieve a page
page = client.pages.retrieve("page-id")

# Update properties
client.pages.update("page-id", properties={
    "Status": {"select": {"name": "Completed"}}
})

# Archive a page
client.pages.archive("page-id")
```

### Working with Databases
```python
# Create a database
db = client.databases.create(
    parent={"page_id": "page-id"},
    title=[{"text": {"content": "Task Tracker"}}],
    properties={
        "Task": {"title": {}},
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

# Query with advanced filtering
results = client.databases.query(
    database_id="database-id",
    filter={
        "and": [
            {"property": "Status", "select": {"equals": "In Progress"}},
            {"property": "Due Date", "date": {"before": "2024-04-01"}}
        ]
    },
    sorts=[{"property": "Due Date", "direction": "ascending"}]
)
```

### Blocks and Content
```python
# Add content blocks to a page
client.blocks.children.append(
    "page-id",
    children=[
        {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": "Project Overview"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "This project aims to..."}}]}}
    ]
)

# List all blocks on a page
blocks = client.blocks.children.list("page-id")
for block in blocks:
    if block.type == "paragraph":
        print(block.get_text_content())
```

## 🧪 Advanced Features

### Synchronization
```python
from nebula_orion.betelgeuse.sync import SyncManager

# Set up synchronization
sync = SyncManager(client, storage_path="./notion_sync")

# Register resources to sync
sync.register_database("database-id")
sync.register_page("page-id")

# Sync operations
sync.pull()  # Get latest from Notion
sync.push()  # Push local changes to Notion
```
### OAuth Authentication
```python
from nebula_orion.betelgeuse.auth import NotionOAuth

# Set up OAuth handler
oauth = NotionOAuth(
    client_id="your-client-id",
    client_secret="your-client-secret",
    redirect_uri="https://your-app.com/callback"
)

# Get authorization URL
auth_url = oauth.get_authorization_url()
# Redirect user to auth_url...

# Exchange code for token
tokens = oauth.exchange_code("received-authorization-code")

# Create client with OAuth token
client = NotionClient(access_token=tokens["access_token"])
```

## 📖 Documentation
Comprehensive documentation is available at docs.nebula-orion.dev:

- API Reference
- Getting Started Guide
- Tutorial: Database Management
- Tutorial: Content Creation

## ⚙️ Development Status
Betelgeuse is under active development. Check the roadmap for current status and upcoming features.

## 🔗 Related Modules
Sirius: Data manipulation and transformation utilities
Rigel: Task scheduling and workflow management
Pleiades: Integration with cloud services and platforms

## 🤝 Contributing
Contributions are welcome! See CONTRIBUTING.md for details on how to get started.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
