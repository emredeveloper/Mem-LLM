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

Author: C. Emre Karataş
Version: 1.3.3
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from pathlib import Path
import json
import logging
import asyncio
from contextlib import asynccontextmanager

# Import Mem-LLM components
from .mem_agent import MemAgent
from .response_metrics import ChatResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store active agents for each user
agents: Dict[str, MemAgent] = {}

# Default agent configuration
DEFAULT_CONFIG = {
    "model": "granite4:3b",
    "backend": "ollama",
    "base_url": "http://localhost:11434",
    "use_sql": True,
    "load_knowledge_base": True
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
    if user_id not in agents:
        agent_config = DEFAULT_CONFIG.copy()
        if config:
            agent_config.update(config)
        
        logger.info(f"Creating new agent for user: {user_id}")
        agent = MemAgent(**agent_config)
        agent.set_user(user_id)
        agents[user_id] = agent
    
    return agents[user_id]

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Mem-LLM API Server starting...")
    logger.info(f"📝 API Documentation: http://localhost:8000/docs")
    logger.info(f"🔌 WebSocket endpoint: ws://localhost:8000/ws/chat/{'{user_id}'}")
    yield
    # Shutdown
    logger.info("🛑 Mem-LLM API Server shutting down...")
    agents.clear()

# Create FastAPI app
app = FastAPI(
    title="Mem-LLM API",
    description="REST API for Mem-LLM - Privacy-first, Memory-enabled AI Assistant (100% Local)",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware for web frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
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

# ============================================================================
# Health & Info Endpoints
# ============================================================================

@app.get("/api/v1/info", tags=["General"])
async def api_info():
    """API information endpoint"""
    return {
        "name": "Mem-LLM API",
        "version": "2.1.0",
        "status": "running",
        "documentation": "/docs",
        "endpoints": {
            "chat": "/api/v1/chat",
            "websocket": "/ws/chat/{user_id}",
            "knowledge_base": "/api/v1/kb",
            "memory": "/api/v1/memory",
            "users": "/api/v1/users"
        }
    }

@app.get("/health", tags=["General"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_users": len(agents)
    }

# ============================================================================
# Chat Endpoints
# ============================================================================

@app.post("/api/v1/chat", response_model=ChatResponse_API, tags=["Chat"])
async def chat(request: ChatRequest):
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
                message=request.message,
                metadata=request.metadata,
                return_metrics=True
            )
            
            return ChatResponse_API(
                text=response.text,
                user_id=request.user_id,
                confidence=response.confidence,
                source=response.source,
                latency=response.latency,
                timestamp=response.timestamp.isoformat(),
                metadata=response.metadata
            )
        else:
            response_text = agent.chat(
                message=request.message,
                metadata=request.metadata
            )
            
            return ChatResponse_API(
                text=response_text,
                user_id=request.user_id,
                timestamp=datetime.now().isoformat()
            )
    
    except Exception as e:
        logger.error(f"Chat error for user {request.user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/chat/stream", tags=["Chat"])
async def chat_stream(request: ChatRequest):
    """
    Send a chat message and get streaming response
    
    Returns a Server-Sent Events (SSE) stream.
    """
    try:
        agent = get_or_create_agent(request.user_id)
        
        async def generate():
            """Generate streaming response"""
            try:
                for chunk in agent.chat_stream(
                    message=request.message,
                    metadata=request.metadata
                ):
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
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no"
            }
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
    logger.info(f"WebSocket connected: {user_id}")
    
    try:
        # Get or create agent
        agent = get_or_create_agent(user_id)
        
        while True:
            # Receive message from client
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
                    await websocket.send_json({
                        "type": "chunk",
                        "content": chunk
                    })
                    # Small delay to prevent overwhelming the client
                    await asyncio.sleep(0.01)
                
                # Send completion
                await websocket.send_json({"type": "done"})
            
            except Exception as e:
                logger.error(f"Error during streaming: {e}")
                await websocket.send_json({
                    "type": "error",
                    "content": str(e)
                })
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {user_id}")
    except Exception as e:
        logger.error(f"WebSocket error for {user_id}: {e}")
        try:
            await websocket.send_json({"type": "error", "content": str(e)})
        except:
            pass

# ============================================================================
# Knowledge Base Endpoints
# ============================================================================

@app.post("/api/v1/kb/add", tags=["Knowledge Base"])
async def add_knowledge(entry: KnowledgeEntryRequest, user_id: str = "admin"):
    """Add entry to knowledge base"""
    try:
        agent = get_or_create_agent(user_id)
        agent.add_kb_entry(
            category=entry.category,
            question=entry.question,
            answer=entry.answer
        )
        return {"status": "success", "message": "Entry added to knowledge base"}
    except Exception as e:
        logger.error(f"KB add error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/kb/search", tags=["Knowledge Base"])
async def search_knowledge(search: KnowledgeSearchRequest, user_id: str = "admin"):
    """Search knowledge base"""
    try:
        agent = get_or_create_agent(user_id)
        
        if hasattr(agent.memory, 'search_knowledge'):
            results = agent.memory.search_knowledge(
                query=search.query,
                limit=search.limit
            )
            return {"results": results, "count": len(results)}
        else:
            raise HTTPException(
                status_code=400,
                detail="Knowledge base not available. Use use_sql=True"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"KB search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/kb/categories", tags=["Knowledge Base"])
async def get_kb_categories(user_id: str = "admin"):
    """Get all knowledge base categories"""
    try:
        agent = get_or_create_agent(user_id)
        
        if hasattr(agent.memory, 'get_kb_categories'):
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
async def get_user_profile(user_id: str):
    """Get user profile"""
    try:
        agent = get_or_create_agent(user_id)
        profile = agent.get_user_profile()
        
        return UserProfileResponse(
            user_id=user_id,
            name=profile.get("name"),
            preferences=profile.get("preferences"),
            summary=profile.get("summary"),
            interaction_count=len(profile.get("conversations", []))
        )
    except Exception as e:
        logger.error(f"Profile error for {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/memory/search", tags=["Memory"])
async def search_memory(search: MemorySearchRequest):
    """Search user's memory"""
    try:
        agent = get_or_create_agent(search.user_id)
        # Use memory manager's get_conversation_history instead
        history = agent.memory.get_conversation_history(user_id=search.user_id)
        
        # Filter by query if provided
        if search.query:
            results = [
                msg for msg in history 
                if search.query.lower() in str(msg).lower()
            ][:search.limit]
        else:
            results = history[:search.limit]
            
        return {"results": results, "count": len(results)}
    except Exception as e:
        logger.error(f"Memory search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/memory/stats", tags=["Memory"])
async def get_memory_stats():
    """Get memory statistics"""
    try:
        total_memories = 0
        total_users = len(agents)
        
        # Count memories from all agents
        for agent in agents.values():
            try:
                if hasattr(agent.memory, 'get_all_users'):
                    users = agent.memory.get_all_users()
                    total_users = len(users)
                    for user_id in users:
                        history = agent.memory.get_conversation_history(user_id=user_id)
                        total_memories += len(history)
                    break  # Only need one agent for DB stats
            except:
                pass
        
        return {
            "total_users": total_users,
            "total_memories": total_memories,
            "active_agents": len(agents)
        }
    except Exception as e:
        logger.error(f"Memory stats error: {e}")
        # Return empty stats instead of error
        return {
            "total_users": len(agents),
            "total_memories": 0,
            "active_agents": len(agents)
        }

@app.delete("/api/v1/users/{user_id}/memory", tags=["Users"])
async def clear_user_memory(user_id: str):
    """Clear user's memory"""
    try:
        if user_id in agents:
            agent = agents[user_id]
            # Clear memory (implementation depends on memory backend)
            if hasattr(agent.memory, 'clear_user'):
                agent.memory.clear_user(user_id)
            
            # Remove agent from cache
            del agents[user_id]
            
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
async def configure_agent(user_id: str, config: AgentConfigRequest):
    """Configure agent settings for a user"""
    try:
        # Remove existing agent if exists
        if user_id in agents:
            del agents[user_id]
        
        # Create new agent with config
        config_dict = {k: v for k, v in config.dict().items() if v is not None}
        agent = get_or_create_agent(user_id, config_dict)
        
        return {
            "status": "success",
            "message": "Agent configured",
            "config": agent.get_info()
        }
    except Exception as e:
        logger.error(f"Configure error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/agent/info/{user_id}", tags=["Agent"])
async def get_agent_info(user_id: str):
    """Get agent information"""
    try:
        agent = get_or_create_agent(user_id)
        return agent.get_info()
    except Exception as e:
        logger.error(f"Agent info error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("  🚀 Starting Mem-LLM API Server")
    print("="*60)
    print("\n📝 API Documentation: http://localhost:8000/docs")
    print("🔌 WebSocket endpoint: ws://localhost:8000/ws/chat/{user_id}")
    print("\nPress CTRL+C to stop the server\n")
    
    uvicorn.run(
        "mem_llm.api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

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
        return {"message": "Mem-LLM API Server", "version": "2.1.0"}
    
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

