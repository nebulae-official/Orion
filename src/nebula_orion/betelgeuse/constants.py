from __future__ import annotations

"""
Constants used within the Betelgeuse library, particularly for API interactions.
"""

# --- API Details ---
DEFAULT_NOTION_API_URL: str = "https://api.notion.com"
DEFAULT_NOTION_VERSION: str = "2022-06-28"  # Notion API version header value

# --- HTTP Methods ---
GET: str = "GET"
POST: str = "POST"
PATCH: str = "PATCH"
DELETE: str = "DELETE"

# --- Timeouts ---
DEFAULT_REQUEST_TIMEOUT_SECONDS: int = 30  # Default timeout for API requests
