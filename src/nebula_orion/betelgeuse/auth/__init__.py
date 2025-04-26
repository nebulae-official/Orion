from __future__ import annotations

# Makes the auth module importable and potentially exposes classes
from .token import API_TOKEN_ENV_VAR, APITokenAuth

__all__ = ["API_TOKEN_ENV_VAR", "APITokenAuth"]
