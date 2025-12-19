"""
API Authentication Module for Mem-LLM
======================================

Provides authentication and authorization for the REST API.

Features:
- API Key authentication
- Optional JWT token support
- Rate limiting
- User session management

Author: C. Emre Karataş
Version: 2.3.2
"""

import hashlib
import os
import secrets
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, APIKeyQuery

# ============================================================================
# Configuration
# ============================================================================

# Default API key for development (should be overridden in production)
DEFAULT_API_KEY = os.environ.get("MEM_LLM_API_KEY", "dev-api-key-change-in-production")

# Rate limiting settings
RATE_LIMIT_REQUESTS = int(os.environ.get("MEM_LLM_RATE_LIMIT", "60"))  # requests per minute
RATE_LIMIT_WINDOW = 60  # seconds


# ============================================================================
# Data Classes
# ============================================================================


@dataclass
class APIUser:
    """Represents an authenticated API user"""

    api_key: str
    user_id: str
    name: str = "API User"
    permissions: List[str] = field(default_factory=lambda: ["read", "write"])
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True


@dataclass
class RateLimitInfo:
    """Rate limiting information for a user"""

    requests: List[float] = field(default_factory=list)
    blocked_until: Optional[float] = None


# ============================================================================
# API Key Store (In-memory for simplicity, use Redis/DB in production)
# ============================================================================


class APIKeyStore:
    """Manages API keys and users"""

    def __init__(self):
        self._keys: Dict[str, APIUser] = {}
        self._rate_limits: Dict[str, RateLimitInfo] = {}

        # Add default development key
        self.add_key(
            api_key=DEFAULT_API_KEY,
            user_id="admin",
            name="Admin User",
            permissions=["read", "write", "admin"],
        )

    def add_key(
        self,
        api_key: str,
        user_id: str,
        name: str = "API User",
        permissions: Optional[List[str]] = None,
    ) -> APIUser:
        """Add a new API key"""
        user = APIUser(
            api_key=self._hash_key(api_key),
            user_id=user_id,
            name=name,
            permissions=permissions or ["read", "write"],
        )
        self._keys[self._hash_key(api_key)] = user
        return user

    def validate_key(self, api_key: str) -> Optional[APIUser]:
        """Validate an API key and return the user"""
        hashed = self._hash_key(api_key)
        user = self._keys.get(hashed)
        if user and user.is_active:
            return user
        return None

    def revoke_key(self, api_key: str) -> bool:
        """Revoke an API key"""
        hashed = self._hash_key(api_key)
        if hashed in self._keys:
            self._keys[hashed].is_active = False
            return True
        return False

    def generate_key(self) -> str:
        """Generate a new secure API key"""
        return secrets.token_urlsafe(32)

    def _hash_key(self, api_key: str) -> str:
        """Hash an API key for secure storage"""
        return hashlib.sha256(api_key.encode()).hexdigest()

    def check_rate_limit(self, api_key: str) -> bool:
        """Check if request is within rate limit"""
        hashed = self._hash_key(api_key)
        now = time.time()

        if hashed not in self._rate_limits:
            self._rate_limits[hashed] = RateLimitInfo()

        info = self._rate_limits[hashed]

        # Check if blocked
        if info.blocked_until and now < info.blocked_until:
            return False

        # Clean old requests
        info.requests = [t for t in info.requests if now - t < RATE_LIMIT_WINDOW]

        # Check limit
        if len(info.requests) >= RATE_LIMIT_REQUESTS:
            info.blocked_until = now + RATE_LIMIT_WINDOW
            return False

        # Record request
        info.requests.append(now)
        return True

    def get_rate_limit_remaining(self, api_key: str) -> int:
        """Get remaining requests in current window"""
        hashed = self._hash_key(api_key)
        if hashed not in self._rate_limits:
            return RATE_LIMIT_REQUESTS

        now = time.time()
        info = self._rate_limits[hashed]
        recent = [t for t in info.requests if now - t < RATE_LIMIT_WINDOW]
        return max(0, RATE_LIMIT_REQUESTS - len(recent))


# Global API key store instance
api_key_store = APIKeyStore()


# ============================================================================
# FastAPI Security Dependencies
# ============================================================================

# API Key can be provided via header or query parameter
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
api_key_query = APIKeyQuery(name="api_key", auto_error=False)


async def get_api_key(
    api_key_header: Optional[str] = Security(api_key_header),  # noqa: B008
    api_key_query: Optional[str] = Security(api_key_query),  # noqa: B008
) -> str:
    """Extract API key from header or query parameter"""
    api_key = api_key_header or api_key_query
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required. Provide via X-API-Key header or api_key query parameter.",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return api_key


async def authenticate(api_key: str = Depends(get_api_key)) -> APIUser:  # noqa: B008
    """Authenticate request using API key"""
    user = api_key_store.validate_key(api_key)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    # Check rate limit
    if not api_key_store.check_rate_limit(api_key):
        remaining = api_key_store.get_rate_limit_remaining(api_key)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Try again in {RATE_LIMIT_WINDOW} seconds.",
            headers={
                "X-RateLimit-Limit": str(RATE_LIMIT_REQUESTS),
                "X-RateLimit-Remaining": str(remaining),
                "Retry-After": str(RATE_LIMIT_WINDOW),
            },
        )

    return user


def require_permission(permission: str):
    """Decorator to require specific permission"""

    async def permission_checker(user: APIUser = Depends(authenticate)) -> APIUser:  # noqa: B008
        if permission not in user.permissions and "admin" not in user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied. Required: {permission}",
            )
        return user

    return permission_checker


# ============================================================================
# Optional Authentication (for endpoints that work with or without auth)
# ============================================================================


async def optional_authenticate(
    api_key_header: Optional[str] = Security(api_key_header),  # noqa: B008
    api_key_query: Optional[str] = Security(api_key_query),  # noqa: B008
) -> Optional[APIUser]:
    """Optionally authenticate - returns None if no key provided"""
    api_key = api_key_header or api_key_query
    if not api_key:
        return None

    user = api_key_store.validate_key(api_key)
    if user and api_key_store.check_rate_limit(api_key):
        return user
    return None


# ============================================================================
# Utility Functions
# ============================================================================


def create_api_key(
    user_id: str, name: str = "API User", permissions: Optional[List[str]] = None
) -> str:
    """Create a new API key for a user"""
    key = api_key_store.generate_key()
    api_key_store.add_key(key, user_id, name, permissions)
    return key


def revoke_api_key(api_key: str) -> bool:
    """Revoke an API key"""
    return api_key_store.revoke_key(api_key)
