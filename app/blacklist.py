"""
Token blacklist management for logout functionality
"""
from typing import Set
from datetime import datetime, timedelta
import threading

# In-memory blacklist (in production, use Redis or database)
_blacklisted_tokens: Set[str] = set()
_blacklist_lock = threading.Lock()


def add_token_to_blacklist(token: str) -> None:
    """Add a token to the blacklist"""
    with _blacklist_lock:
        _blacklisted_tokens.add(token)


def is_token_blacklisted(token: str) -> bool:
    """Check if a token is blacklisted"""
    with _blacklist_lock:
        return token in _blacklisted_tokens


def remove_token_from_blacklist(token: str) -> None:
    """Remove a token from the blacklist"""
    with _blacklist_lock:
        _blacklisted_tokens.discard(token)


def clear_blacklist() -> None:
    """Clear all tokens from the blacklist"""
    with _blacklist_lock:
        _blacklisted_tokens.clear()


def get_blacklist_size() -> int:
    """Get the number of blacklisted tokens"""
    with _blacklist_lock:
        return len(_blacklisted_tokens)


# Note: In production, you should:
# 1. Use Redis or a database to store blacklisted tokens
# 2. Implement token expiration cleanup
# 3. Consider using a more sophisticated approach like refresh tokens