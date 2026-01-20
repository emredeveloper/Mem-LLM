"""
Mem-LLM REST API Server
========================

FastAPI-based REST API server for Mem-LLM.
Provides HTTP endpoints and WebSocket support for streaming responses.

Features:
- RESTful API endpoints
- WebSocket streaming support
- Multi-user management
- Knowledge base operations
- Memory search and export
- CORS support for web frontends
- Auto-generated API documentation (Swagger UI)

Usage:
    # Run server
    python -m mem_llm.api_server

    # Or with uvicorn directly
    uvicorn mem_llm.api_server:app --reload --host 0.0.0.0 --port 8000

API Documentation:
    - Swagger UI: http://localhost:8000/docs
    - ReDoc: http://localhost:8000/redoc

Author: Cihat Emre Karataş
Version: 2.4.2
"""

import asyncio
import json
import logging
import os
import time
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Optional

from fastapi import (
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Import Mem-LLM components
from .mem_agent import MemAgent
from .api_auth import AUTH_DISABLED, create_api_key, require_permission, api_key_store, revoke_api_key

# Note: In a real app, we'd probably have a WorkflowManager attached to the agent or global


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentStore:
    """Simple LRU + TTL in-memory agent store."""

    def __init__(self, ttl_seconds: int = 3600, max_size: int = 500):
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self._entries: Dict[str, Dict[str, Any]] = {}
        self._lru: Dict[str, float] = {}
        self._lock = Lock()

    def _purge_expired(self) -> None:
        if self.ttl_seconds <= 0:
            return
        now = time.time()
        expired = [
            user_id
            for user_id, meta in self._entries.items()
            if now - meta["last_access"] > self.ttl_seconds
        ]
        for user_id in expired:
            self._entries.pop(user_id, None)
            self._lru.pop(user_id, None)

    def get(self, user_id: str) -> Optional[MemAgent]:
        with self._lock:
            self._purge_expired()
            if user_id not in self._entries:
                return None
            meta = self._entries[user_id]
            meta["last_access"] = time.time()
            self._lru[user_id] = meta["last_access"]
            return meta["agent"]

    def set(self, user_id: str, agent: MemAgent) -> None:
        with self._lock:
            now = time.time()
            self._entries[user_id] = {"agent": agent, "created_at": now, "last_access": now}
            self._lru[user_id] = now
            self._purge_expired()
            if self.max_size > 0 and len(self._entries) > self.max_size:
                # Remove least recently used entries
                to_remove = sorted(self._lru.items(), key=lambda item: item[1])[
                    : len(self._entries) - self.max_size
                ]
                for remove_id, _ in to_remove:
                    self._entries.pop(remove_id, None)
                    self._lru.pop(remove_id, None)

    def delete(self, user_id: str) -> None:
        with self._lock:
            self._entries.pop(user_id, None)
            self._lru.pop(user_id, None)

    def values(self):
        with self._lock:
            self._purge_expired()
            return [meta["agent"] for meta in self._entries.values()]

    def size(self) -> int:
        with self._lock:
            self._purge_expired()
            return len(self._entries)


_fallback_store = AgentStore()


def _get_agent_store() -> AgentStore:
    try:
        store = getattr(app.state, "agent_store", None)
        if store:
            return store
    except NameError:
        pass
    return _fallback_store

# Default agent configuration
DEFAULT_CONFIG = {
    "model": "rnj-1:latest",
    "backend": "ollama",
    "base_url": "http://localhost:11434",
    "use_sql": True,
    "load_knowledge_base": True,
    "enable_graph_memory": True,
}


def get_or_create_agent(user_id: str, config: Optional[Dict] = None) -> MemAgent:
    """
    Get existing agent or create new one for user

    Args:
        user_id: User identifier
        config: Optional agent configuration

    Returns:
        MemAgent instance
    """
    store = _get_agent_store()
    existing = store.get(user_id)
    if existing:
        return existing

    agent_config = DEFAULT_CONFIG.copy()
    if config:
        agent_config.update(config)

    logger.info(f"Creating new agent for user: {user_id}")
    agent = MemAgent(**agent_config)
    agent.set_user(user_id)
    store.set(user_id, agent)

    return agent


# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Mem-LLM API Server starting...")
    logger.info("📝 API Documentation: http://localhost:8000/docs")
    logger.info(f"🔌 WebSocket endpoint: ws://localhost:8000/ws/chat/{'{user_id}'}")
    ttl_seconds = int(os.environ.get("MEM_LLM_AGENT_TTL_SECONDS", "3600"))
    max_size = int(os.environ.get("MEM_LLM_AGENT_MAX_SIZE", "500"))
    app.state.agent_store = AgentStore(ttl_seconds=ttl_seconds, max_size=max_size)
    yield
    # Shutdown
    logger.info("🛑 Mem-LLM API Server shutting down...")
    app.state.agent_store = AgentStore()


# Create FastAPI app
app = FastAPI(
    title="Mem-LLM API",
    description="REST API for Mem-LLM - Privacy-first, Memory-enabled AI Assistant (100% Local)",
    version="2.4.2",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

def _get_allowed_origins() -> list:
    raw = os.environ.get("MEM_LLM_ALLOW_ORIGINS", "*")
    if raw.strip() == "*":
        return ["*"]
    origins = [item.strip() for item in raw.split(",")]
    return [origin for origin in origins if origin]


# Add CORS middleware for web frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Request/Response Models
# ============================================================================


class ChatRequest(BaseModel):
    """Chat request model"""

    message: str = Field(..., description="User's message")
    user_id: str = Field(..., description="User identifier")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    stream: bool = Field(False, description="Enable streaming response")
    return_metrics: bool = Field(False, description="Return detailed metrics")


class ChatResponse_API(BaseModel):
    """Chat response model"""

    text: str = Field(..., description="Bot's response text")
    user_id: str = Field(..., description="User identifier")
    confidence: Optional[float] = Field(None, description="Response confidence score (0-1)")
    source: Optional[str] = Field(None, description="Response source (model/kb/hybrid)")
    latency: Optional[float] = Field(None, description="Response latency in milliseconds")
    timestamp: str = Field(..., description="Response timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class KnowledgeEntryRequest(BaseModel):
    """Knowledge base entry request"""

    category: str = Field(..., description="Entry category")
    question: str = Field(..., description="Question text")
    answer: str = Field(..., description="Answer text")


class KnowledgeSearchRequest(BaseModel):
    """Knowledge base search request"""

    query: str = Field(..., description="Search query")
    limit: int = Field(5, description="Maximum number of results")


class UserProfileResponse(BaseModel):
    """User profile response"""

    user_id: str
    name: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    interaction_count: int = 0


class MemorySearchRequest(BaseModel):
    """Memory search request"""

    user_id: str = Field(..., description="User identifier")
    query: str = Field(..., description="Search query")
    limit: int = Field(10, description="Maximum number of results")


class AgentConfigRequest(BaseModel):
    """Agent configuration request"""

    model: Optional[str] = Field(None, description="LLM model name")
    backend: Optional[str] = Field(None, description="LLM backend (ollama/lmstudio)")
    base_url: Optional[str] = Field(None, description="Backend base URL")
    temperature: Optional[float] = Field(None, description="Sampling temperature")


class ApiKeyCreateRequest(BaseModel):
    """Admin API key creation request"""

    user_id: str = Field(..., description="User identifier for the key")
    name: Optional[str] = Field(None, description="Display name")
    permissions: Optional[list[str]] = Field(
        None, description="Permissions list (e.g. read/write/admin)"
    )


class ApiKeyCreateResponse(BaseModel):
    """Admin API key creation response"""

    api_key: str = Field(..., description="New API key (show once)")
    user_id: str = Field(..., description="User identifier")
    name: Optional[str] = None
    permissions: list[str] = Field(default_factory=list)


class ApiKeyRevokeRequest(BaseModel):
    """Admin API key revoke request"""

    api_key: str = Field(..., description="API key to revoke")


class ApiKeyUserResponse(BaseModel):
    """API user listing entry (no raw key)"""

    user_id: str
    name: str
    permissions: list[str]
    created_at: str
    is_active: bool


# ============================================================================
# Health & Info Endpoints
# ============================================================================


@app.get("/api/v1/info", tags=["General"])
async def api_info(user=Depends(require_permission("read"))):  # noqa: B008
    """API information endpoint"""
    return {
        "name": "Mem-LLM API",
        "version": "2.4.2",
        "status": "running",
        "documentation": "/docs",
        "endpoints": {
            "chat": "/api/v1/chat",
            "websocket": "/ws/chat/{user_id}",
            "knowledge_base": "/api/v1/kb",
            "memory": "/api/v1/memory",
            "users": "/api/v1/users",
        },
    }


@app.get("/api/v1/health", tags=["General"])
async def health_check(user=Depends(require_permission("read"))):  # noqa: B008
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_users": _get_agent_store().size(),
    }


# ============================================================================
# Chat Endpoints
# ============================================================================


@app.post("/api/v1/chat", response_model=ChatResponse_API, tags=["Chat"])
async def chat(request: ChatRequest, user=Depends(require_permission("write"))):  # noqa: B008
    """
    Send a chat message and get response

    This endpoint supports both regular and streaming responses.
    For streaming, use the WebSocket endpoint instead.
    """
    try:
        # Get or create agent for user
        agent = get_or_create_agent(request.user_id)

        # Get response
        if request.return_metrics:
            response = agent.chat(
                message=request.message, metadata=request.metadata, return_metrics=True
            )

            return ChatResponse_API(
                text=response.text,
                user_id=request.user_id,
                confidence=response.confidence,
                source=response.source,
                latency=response.latency,
                timestamp=response.timestamp.isoformat(),
                metadata=response.metadata,
            )
        else:
            response_text = agent.chat(message=request.message, metadata=request.metadata)

            return ChatResponse_API(
                text=response_text, user_id=request.user_id, timestamp=datetime.now().isoformat()
            )

    except Exception as e:
        logger.error(f"Chat error for user {request.user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/chat/stream", tags=["Chat"])
async def chat_stream(request: ChatRequest, user=Depends(require_permission("write"))):  # noqa: B008
    """
    Send a chat message and get streaming response

    Returns a Server-Sent Events (SSE) stream.
    """
    try:
        agent = get_or_create_agent(request.user_id)

        async def generate():
            """Generate streaming response"""
            try:
                for chunk in agent.chat_stream(message=request.message, metadata=request.metadata):
                    # Send as SSE format
                    yield f"data: {json.dumps({'chunk': chunk})}\n\n"

                # Send completion marker
                yield f"data: {json.dumps({'done': True})}\n\n"

            except Exception as e:
                logger.error(f"Streaming error: {e}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

    except Exception as e:
        logger.error(f"Chat stream error for user {request.user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# WebSocket Endpoint (For Real-time Streaming)
# ============================================================================


@app.websocket("/ws/chat/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: str):
    """
    WebSocket endpoint for real-time streaming chat

    Client sends: {"message": "Hello", "metadata": {}}
    Server streams: {"type": "chunk", "content": "..."} or {"type": "done"}
    """
    await websocket.accept()
    api_key = websocket.headers.get("x-api-key") or websocket.query_params.get("api_key")
    if not AUTH_DISABLED:
        if not api_key:
            await websocket.close(code=1008)
            return

        user = api_key_store.validate_key(api_key)
        if not user:
            await websocket.close(code=1008)
            return

    logger.info(f"WebSocket connected: {user_id}")

    try:
        # Get or create agent
        agent = get_or_create_agent(user_id)

        while True:
            # Receive message from client
            if not AUTH_DISABLED and not api_key_store.check_rate_limit(api_key):
                await websocket.send_json({"type": "error", "content": "Rate limit exceeded"})
                await websocket.close(code=1011)
                return

            data = await websocket.receive_json()
            message = data.get("message", "")
            metadata = data.get("metadata")

            if not message:
                await websocket.send_json({"type": "error", "content": "Empty message"})
                continue

            # Send acknowledgment
            await websocket.send_json({"type": "start"})

            # Stream response
            try:
                for chunk in agent.chat_stream(message=message, metadata=metadata):
                    await websocket.send_json({"type": "chunk", "content": chunk})
                    # Small delay to prevent overwhelming the client
                    await asyncio.sleep(0.01)

                # Send completion
                await websocket.send_json({"type": "done"})

            except Exception as e:
                logger.error(f"Error during streaming: {e}")
                await websocket.send_json({"type": "error", "content": str(e)})

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {user_id}")
    except Exception as e:
        logger.error(f"WebSocket error for {user_id}: {e}")
        try:
            await websocket.send_json({"type": "error", "content": str(e)})
        except Exception:
            pass


# ============================================================================
# Knowledge Base Endpoints
# ============================================================================


@app.post("/api/v1/kb/add", tags=["Knowledge Base"])
async def add_knowledge(
    entry: KnowledgeEntryRequest,
    user_id: str = "admin",
    user=Depends(require_permission("write")),  # noqa: B008
):
    """Add entry to knowledge base"""
    try:
        agent = get_or_create_agent(user_id)
        agent.add_kb_entry(category=entry.category, question=entry.question, answer=entry.answer)
        return {"status": "success", "message": "Entry added to knowledge base"}
    except Exception as e:
        logger.error(f"KB add error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/kb/search", tags=["Knowledge Base"])
async def search_knowledge(
    search: KnowledgeSearchRequest,
    user_id: str = "admin",
    user=Depends(require_permission("read")),  # noqa: B008
):
    """Search knowledge base"""
    try:
        agent = get_or_create_agent(user_id)

        if hasattr(agent.memory, "search_knowledge"):
            results = agent.memory.search_knowledge(query=search.query, limit=search.limit)
            return {"results": results, "count": len(results)}
        else:
            raise HTTPException(
                status_code=400, detail="Knowledge base not available. Use use_sql=True"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"KB search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/kb/categories", tags=["Knowledge Base"])
async def get_kb_categories(user_id: str = "admin", user=Depends(require_permission("read"))):  # noqa: B008
    """Get all knowledge base categories"""
    try:
        agent = get_or_create_agent(user_id)

        if hasattr(agent.memory, "get_kb_categories"):
            categories = agent.memory.get_kb_categories()
            return {"categories": categories, "count": len(categories)}
        else:
            return {"categories": [], "count": 0}
    except Exception as e:
        logger.error(f"KB categories error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Memory & User Endpoints
# ============================================================================


@app.get("/api/v1/users/{user_id}/profile", response_model=UserProfileResponse, tags=["Users"])
async def get_user_profile(user_id: str, user=Depends(require_permission("read"))):  # noqa: B008
    """Get user profile"""
    try:
        agent = get_or_create_agent(user_id)
        profile = agent.get_user_profile()

        return UserProfileResponse(
            user_id=user_id,
            name=profile.get("name"),
            preferences=profile.get("preferences"),
            summary=profile.get("summary"),
            interaction_count=len(profile.get("conversations", [])),
        )
    except Exception as e:
        logger.error(f"Profile error for {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/memory/search", tags=["Memory"])
async def search_memory(search: MemorySearchRequest, user=Depends(require_permission("read"))):  # noqa: B008
    """Search user's memory"""
    try:
        agent = get_or_create_agent(search.user_id)
        # Use appropriate method based on backend
        if hasattr(agent.memory, "search_conversations"):
            # SQL backend
            results = agent.memory.search_conversations(search.user_id, search.query)[
                : search.limit
            ]
        elif hasattr(agent.memory, "get_recent_conversations"):
            # SQL backend - if search not available
            history = agent.memory.get_recent_conversations(search.user_id, limit=search.limit)
            results = [msg for msg in history if search.query.lower() in str(msg).lower()]
        else:
            # JSON backend fallback
            results = []

        return {"results": results, "count": len(results)}
    except Exception as e:
        logger.error(f"Memory search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/memory/stats", tags=["Memory"])
async def get_memory_stats(user=Depends(require_permission("read"))):  # noqa: B008
    """Get memory statistics"""
    try:
        total_memories = 0
        store = _get_agent_store()
        total_users = store.size()

        # Count memories from all agents
        for agent in store.values():
            try:
                if hasattr(agent.memory, "get_all_users"):
                    users = agent.memory.get_all_users()
                    total_users = len(users)
                    for user_id in users:
                        history = agent.memory.get_conversation_history(user_id=user_id)
                        total_memories += len(history)
                    break  # Only need one agent for DB stats
            except Exception:
                pass

        return {
            "total_users": total_users,
            "total_memories": total_memories,
            "active_agents": store.size(),
        }
    except Exception as e:
        logger.error(f"Memory stats error: {e}")
        # Return empty stats instead of error
        return {"total_users": 0, "total_memories": 0, "active_agents": 0}


@app.delete("/api/v1/users/{user_id}/memory", tags=["Users"])
async def clear_user_memory(user_id: str, user=Depends(require_permission("write"))):  # noqa: B008
    """Clear user's memory"""
    try:
        store = _get_agent_store()
        agent = store.get(user_id)
        if agent:
            # Clear memory (implementation depends on memory backend)
            if hasattr(agent.memory, "clear_user"):
                agent.memory.clear_user(user_id)

            # Remove agent from cache
            store.delete(user_id)

            return {"status": "success", "message": f"Memory cleared for user {user_id}"}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Clear memory error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Agent Configuration
# ============================================================================


@app.post("/api/v1/agent/configure/{user_id}", tags=["Agent"])
async def configure_agent(
    user_id: str, config: AgentConfigRequest, user=Depends(require_permission("admin"))  # noqa: B008
):
    """Configure agent settings for a user"""
    try:
        # Remove existing agent if exists
        store = _get_agent_store()
        store.delete(user_id)

        # Create new agent with config
        config_dict = {k: v for k, v in config.dict().items() if v is not None}
        agent = get_or_create_agent(user_id, config_dict)

        return {"status": "success", "message": "Agent configured", "config": agent.get_info()}
    except Exception as e:
        logger.error(f"Configure error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/agent/info/{user_id}", tags=["Agent"])
async def get_agent_info(user_id: str, user=Depends(require_permission("read"))):  # noqa: B008
    """Get agent information"""
    try:
        agent = get_or_create_agent(user_id)
        return agent.get_info()
    except Exception as e:
        logger.error(f"Agent info error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Admin API Key Management
# ============================================================================


@app.get("/api/v1/admin/api-keys", response_model=list[ApiKeyUserResponse], tags=["Admin"])
async def list_api_keys(user=Depends(require_permission("admin"))):  # noqa: B008
    """List API users (no raw keys)."""
    users = []
    for entry in api_key_store.list_users():
        users.append(
            ApiKeyUserResponse(
                user_id=entry.user_id,
                name=entry.name,
                permissions=entry.permissions,
                created_at=entry.created_at.isoformat(),
                is_active=entry.is_active,
            )
        )
    return users


@app.post(
    "/api/v1/admin/api-keys",
    response_model=ApiKeyCreateResponse,
    tags=["Admin"],
)
async def create_api_key_admin(
    request: ApiKeyCreateRequest, user=Depends(require_permission("admin"))  # noqa: B008
):
    """Create an API key for a user (returns raw key once)."""
    key = create_api_key(
        user_id=request.user_id, name=request.name or "API User", permissions=request.permissions
    )
    return ApiKeyCreateResponse(
        api_key=key,
        user_id=request.user_id,
        name=request.name or "API User",
        permissions=request.permissions or ["read", "write"],
    )


@app.post("/api/v1/admin/api-keys/revoke", tags=["Admin"])
async def revoke_api_key_admin(
    request: ApiKeyRevokeRequest, user=Depends(require_permission("admin"))  # noqa: B008
):
    """Revoke an API key."""
    success = revoke_api_key(request.api_key)
    if not success:
        raise HTTPException(status_code=404, detail="API key not found")
    return {"status": "success"}


# ============================================================================
# Graph Endpoints (v2.3.0)
# ============================================================================


@app.get("/api/v1/graph/data", tags=["Graph"])
async def get_graph_data(user_id: str, user=Depends(require_permission("read"))):  # noqa: B008
    """Get knowledge graph data for visualization"""
    try:
        agent = get_or_create_agent(user_id)
        if hasattr(agent, "graph_store") and agent.graph_store:
            # Convert networkx graph to Cytoscape format or simpler JSON
            # Using node-link data which is compatible with D3/Cytoscape usually
            import networkx as nx

            data = nx.node_link_data(agent.graph_store.graph)
            return data
        return {"nodes": [], "links": []}
    except Exception as e:
        logger.error(f"Graph data error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/graph/clear", tags=["Graph"])
async def clear_graph(user_id: str, user=Depends(require_permission("write"))):  # noqa: B008
    """Clear knowledge graph for a user"""
    try:
        agent = get_or_create_agent(user_id)
        if hasattr(agent, "clear_graph_memory"):
            success = agent.clear_graph_memory(user_id)
            if success:
                return {"status": "success", "message": "Graph memory cleared"}
        return {"status": "error", "message": "Graph memory not available"}
    except Exception as e:
        logger.error(f"Graph clear error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Check for a global workflow registry or simple directory scan


@app.get("/api/v1/workflows", tags=["Workflow"])
async def list_workflows(user=Depends(require_permission("read"))):  # noqa: B008
    """List available workflows"""
    # Mocking for now, or scanning a directory
    return {
        "workflows": [
            {
                "id": "research",
                "name": "Deep Research",
                "description": "Research a topic and summarize findings",
            },
            {
                "id": "content_creation",
                "name": "Content Creation",
                "description": "Generate blog post from topic",
            },
        ]
    }


@app.post("/api/v1/workflow/run/{workflow_id}", tags=["Workflow"])
async def run_workflow(
    workflow_id: str,
    user_id: str,
    input_data: Dict[str, Any],
    user=Depends(require_permission("write")),  # noqa: B008
):
    """Run a workflow (Blocking)"""
    # ... existing code ...
    try:
        agent = get_or_create_agent(user_id)

        # Define available workflows dynamically or via registry (simplified for demo)
        workflow = _get_workflow(workflow_id, agent)  # Refactored helper

        # Run workflow
        context = await workflow.run(initial_data=input_data)

        # Return all context data as result
        return {"status": "completed", "workflow_id": workflow_id, "results": context.data}

    except Exception as e:
        logger.error(f"Workflow execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/workflow/stream/{workflow_id}", tags=["Workflow"])
async def run_workflow_stream(
    workflow_id: str,
    user_id: str,
    topic: str = "General",
    user=Depends(require_permission("write")),  # noqa: B008
):
    """Run a workflow and stream events (SSE)"""
    try:
        agent = get_or_create_agent(user_id)
        import json

        # Helper to get workflow (duplicate logic for now, should refactor)
        workflow = _get_workflow(workflow_id, agent)

        async def event_generator():
            try:
                async for event in workflow.run_generator(initial_data={"topic": topic}):
                    yield f"data: {json.dumps(event)}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except Exception as e:
        logger.error(f"Workflow stream error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _get_workflow(workflow_id, agent):
    from mem_llm.workflow import Step, Workflow

    if workflow_id == "research":
        workflow = Workflow("Deep Research")
        workflow.add_step(
            Step(
                "Research",
                agent=agent,
                action="Research the topic provided.",
                input_key="topic",
                output_key="facts",
                description="Researching topic deeply...",
            )
        )
        workflow.add_step(
            Step(
                "Summarize",
                agent=agent,
                action="Summarize the facts.",
                input_key="facts",
                output_key="summary",
                description="Summarizing findings...",
            )
        )
        return workflow
    elif workflow_id == "content_creation":
        workflow = Workflow("Content Creation")
        workflow.add_step(
            Step(
                "Draft",
                agent=agent,
                action="Draft a blog post about the topic.",
                input_key="topic",
                output_key="draft",
                description="Drafting blog post...",
            )
        )
        return workflow
    else:
        raise ValueError("Workflow not found")


@app.post("/api/v1/upload", tags=["Knowledge"])
async def upload_file(
    file: UploadFile = File(...),  # noqa: B008
    user_id: str = Form(...),  # noqa: B008
    user=Depends(require_permission("write")),  # noqa: B008
):
    """Upload a file to the knowledge base"""
    try:
        # Create uploads directory if not exists
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)

        # Save file
        file_path = upload_dir / file.filename
        with open(file_path, "wb") as buffer:
            import shutil

            shutil.copyfileobj(file.file, buffer)

        return {
            "status": "success",
            "filename": file.filename,
            "message": "File uploaded successfully",
        }

    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 60)
    print("  🚀 Starting Mem-LLM API Server")
    print("=" * 60)
    print("\n📝 API Documentation: http://localhost:8000/docs")
    print("🔌 WebSocket endpoint: ws://localhost:8000/ws/chat/{user_id}")
    print("\nPress CTRL+C to stop the server\n")

    uvicorn.run("mem_llm.api_server:app", host="0.0.0.0", port=8000, reload=True, log_level="info")

# Mount Web UI static files
web_ui_path = Path(__file__).parent / "web_ui"
if web_ui_path.exists():
    app.mount("/static", StaticFiles(directory=str(web_ui_path)), name="static")

    @app.get("/")
    async def root():
        """Serve Web UI index page"""
        index_path = web_ui_path / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path), media_type="text/html")
        return {"message": "Mem-LLM API Server", "version": "2.4.2"}

    @app.get("/memory")
    async def memory_page():
        """Serve memory management page"""
        memory_path = web_ui_path / "memory.html"
        if memory_path.exists():
            return FileResponse(str(memory_path), media_type="text/html")
        return {"error": "Page not found"}

    @app.get("/metrics")
    async def metrics_page():
        """Serve metrics dashboard page"""
        metrics_path = web_ui_path / "metrics.html"
        if metrics_path.exists():
            return FileResponse(str(metrics_path), media_type="text/html")
        return {"error": "Page not found"}
