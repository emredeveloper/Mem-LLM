# Changelog

## [2.4.8] - 2026-03-05
### Changed
- Updated all README files for the current release and normalized remaining encoding artifacts.
- Aligned documentation and examples with the LM Studio default model qwen3.5-2b.

## [2.4.7] - 2026-03-05
### Fixed
- Hardened API auth defaults, upload path handling, workspace boundaries, and async tool execution behavior.
- Replaced unsafe calculator evaluation with AST-based parsing and normalized remaining encoding issues across code, docs, and tests.

### Changed
- Switched LM Studio default model and related tests to qwen3.5-2b.
- Added security hardening and LM Studio full-feature coverage tests.
## [2.4.7] - 2026-03-05
### Fixed
- Hardened API auth defaults, upload path handling, workspace boundaries, and async tool execution behavior.
- Replaced unsafe calculator evaluation with AST-based parsing and normalized remaining encoding issues across code, docs, and tests.

### Changed
- Switched LM Studio default model and related tests to qwen3.5-2b.
- Added security hardening and LM Studio full-feature coverage tests.
## [2.4.5] - 2026-02-28
### Fixed
- Replaced PyPI long description with clean UTF-8 and ASCII-safe README text.
- Normalized author metadata strings to avoid mojibake on package indexes.

## [2.4.4] - 2026-02-27
### Fixed
- Resolved 12 reported defects across mem_agent.py, memory_db.py, tool_system.py, conversation_analytics.py, memory_tools.py, prompt_security.py, and multi-agent registry.
- Fixed critical knowledge base state regression and SQL conversation ordering in prompt history.
- Added missing SQL thread lock in search_conversations.
- Restored consistent tool-call parsing behavior (has_tool_call / remove_tool_calls) and removed stale execution logging reference.
- Added backend-agnostic handling for analytics and memory tools (JSON/SQL compatibility).
- Improved streaming flow with post-response tool-call execution support.
- Added missing dependencies to manifests (psutil, networkx) and aligned public exports.

### Changed
- Default backend models aligned for current release:
  - Ollama: granite4:3b
  - LM Studio: google/gemma-3-12b
- Updated tests and docs to reflect current model defaults and backend behavior.
## [2.4.3] - 2026-02-08
### Fixed
- **MemAgent Tool Flow** - Corrected memory tool-call execution to use active memory backends and added `add_kb_entry` compatibility alias.
- **API Endpoints** - Fixed KB add, memory stats, profile interaction count, and clear-user-memory endpoint behavior.
- **Tool Parser** - Removed local import shadowing that could trigger `UnboundLocalError` in tool call parsing.
- **Ollama Integration Tests** - Made test model selection dynamic and stabilized user-context assertions for local environments.

### Changed
- **Docker Cleanup** - Removed Docker artifacts and related docs (`Dockerfile`, `docker-compose.yml`, `.dockerignore`).

## [2.4.2] - 2026-01-20
- **Docs** - Refreshed PyPI README release notes for current version.

## [2.4.1] - 2026-01-20
- **Security Defaults** - Optional API auth can be disabled for local UI demos.
- **Workflow** - Non-blocking execution for agent steps.
- **Graph** - Structured parsing and dedup updates for triplets.
- **Tooling** - Allowlist/denylist policy support.
- **UI** - Simplified auth UX for local usage.

## [2.4.0] - 2025-12-25
### Added
- **Release v2.4.0** - Bumped package metadata and published to PyPI.

### Changed
- **Docs**: Updated top-level README and package description used on PyPI.
- **Packaging**: Ensured Python >=3.8 support and refreshed build process.

### Fixed
- **Author**: Normalized author name to "Cihat Emre Karatas" across the codebase.


## [2.3.7] - 2025-12-25
### Fixed
- **Demo File**: Corrected undefined `translate_to_turkish` function in `18_function_calling.py` demo
- **Tool System**: Enhanced regex patterns for safer tool name validation to prevent injection
- **Tool Parsing**: Added validation for tool name format to prevent issues with generic names like 'tool_name'
- **Error Handling**: Improved error messages and logging for better debugging experience

### Changed
- **Security**: Tool names now validated using stricter regex patterns (`[a-zA-Z_][a-zA-Z0-9_]*`)
- **Robustness**: Tool calls with invalid names are now skipped instead of causing failures
- **Logging**: Added debug logging for tool call parsing and execution

## [2.3.3] - 2025-12-19
### Fixed
- **Tests**: Resolved major test failures in `test_extractor`, `test_health_check`, and `LLMClientFactory`.
- **Linting**: Fixed `B041` (duplicate keys in prompt security) and `PytestReturnNotNoneWarning`.
- **Stability**: Standardized mock objects and assertions in unit/integration tests.

### Changed
- **Workflow**: Completely removed `flake8` from pre-commit and dev dependencies to simplify linting process.
- **CI/CD**: Standardized on `black` and `isort` for code formatting.

## [2.3.1] - 2025-12-13
### Fixed
- **Package Structure**: Added missing subpackages (workflow, memory.graph, analytics) to setuptools
- **Dependencies**: Added `networkx>=3.0` for Knowledge Graph support
- **PyPI Metadata**: Updated description with new v2.3 features

## [2.3.0] - 2025-12-13
### Added
- **Workflow Engine**: Structured, multi-step agent workflows defined in Python or YAML.
- **Knowledge Graph Memory**: Graph-based memory storage using NetworkX and LLM extraction.
- **Premium Web UI**: Redesigned with dark mode, glassmorphism, and new Workflow/Graph tabs.
- **LM Studio Integration**: Auto-configuration for `google/gemma-3-12b`.

### Changed
- **Ollama Default**: Updated to `ministral-3:3b`.
- **API Server**: Added endpoints for graph data and workflow management.

### Removed
- **Voice Module**: Removed voice interaction features.


All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.9] - 2025-01-27

### [MAINTENANCE] Maintenance & Improvements
- Fixed linter errors in API authentication module
- Removed unused imports and fixed code quality issues
- Added proper exception handling (bare except â†’ Exception)
- Version bump for PyPI release

---

## [2.2.8] - 2025-12-07

### [MAINTENANCE] Maintenance & Improvements
- **Python Version Support**: Minimum Python version updated to 3.10 (removed 3.8, 3.9)
- **Development Status**: Updated to Production/Stable (5)
- **Classifiers**: Added "Topic :: Software Development :: Libraries :: Python Modules"
- **Tool Configuration**: Updated Black and mypy to target Python 3.10+

### [DOCS] Documentation
- Fixed PyPI README.md description display
- Updated project classifiers for better discoverability

---

## [2.2.7] - 2025-12-05

### [MAINTENANCE] Maintenance
- Version bump to fix PyPI README description display
- Updated README path configuration in pyproject.toml

---

## [2.2.6] - 2025-12-04

### [MAINTENANCE] Maintenance
- Version bump to fix PyPI README description display

---

## [2.2.5] - 2025-12-03

### [MAINTENANCE] Maintenance
- Version bump to fix PyPI README description display

---

## [2.2.4] - 2025-12-02

### [MAINTENANCE] Improvements
- **UUID Usage**: Improved trace_id generation using UUID instead of timestamp
- **Vector Store**: Enhanced document ID generation with UUID fallback

---

## [2.2.3] - 2025-12-01

### [MEMORY] Hierarchical Memory System *(NEW - Major Feature)*
- **4-Layer Memory Architecture** - Mimics human cognitive memory
  - **Episode Layer**: Raw interaction storage (bottom layer)
  - **Trace Layer**: Short-term memory traces and abstractions
  - **Category Layer**: Topic-based aggregation (e.g., "python_coding", "travel")
  - **Domain Layer**: High-level context summaries (e.g., "technology", "lifestyle")

- **AutoCategorizer** - Intelligent classification
  - Automatically analyzes interactions using LLM
  - Assigns specific categories and broad domains
  - Enables topic-aware retrieval

- **Context Injection** - Smarter LLM context
  - Injects hierarchical context (Active Domains, Recent Topics, Short-term Memory)
  - Reduces context window usage while maintaining relevance

### [MODULES] New Modules
- `mem_llm/memory/hierarchy/` - Core hierarchical memory implementation
- `mem_llm/memory/hierarchy/layers.py` - Layer definitions
- `mem_llm/memory/hierarchy/categorizer.py` - LLM-based categorization
- `mem_llm/memory/hierarchy/manager.py` - System orchestrator

### [MAINTENANCE] Improvements
- **MemAgent Integration**: Seamlessly integrated via `enable_hierarchical_memory=True`
- **Backward Compatibility**: Fully compatible with existing SQL/JSON memory systems

---

## [2.2.2] - 2025-12-01

### [DOCS] Documentation
- **README Updates** - Ensured all README files (root and package) are synchronized with v2.2.0 features
- **PyPI Description** - Updated package description to reflect multi-agent capabilities

### [MAINTENANCE] Maintenance
- Version bump to ensure PyPI displays correct documentation

---

## [2.2.1] - 2025-11-30

### [BUGFIX] Bug Fixes
- **Package Distribution** - Fixed multi-agent module not being included in PyPI package
- **MANIFEST.in** - Added `recursive-include mem_llm/multi_agent *.py` to ensure all multi-agent files are packaged

### [DOCS] Note
This is a critical bugfix release. Users who installed v2.2.0 should upgrade to v2.2.1 to access multi-agent features.

---

## [2.2.0] - 2025-11-30

### [AGENT] Multi-Agent Systems *(NEW - Major Feature)*
- **BaseAgent** - Role-based AI agents with specialized behaviors
  - 6 predefined roles: RESEARCHER, ANALYST, WRITER, VALIDATOR, COORDINATOR, GENERAL
  - Memory isolation (private/shared memory spaces)
  - Role-specific system prompts
  - Conversation history tracking
  - Inter-agent messaging capabilities

- **AgentRegistry** - Centralized agent management
  - Agent registration/deregistration
  - Lookup by ID, role, or status
  - Health monitoring and statistics
  - Agent lifecycle management

- **CommunicationHub** - Advanced inter-agent communication
  - Thread-safe message queuing (FIFO)
  - Direct agent-to-agent messaging
  - Broadcast channels with subscriptions
  - Message routing and delivery tracking
  - Communication statistics and monitoring

### [TEST] Testing & Quality
- **29 new tests** - Comprehensive test coverage for multi-agent features
  - 13 tests for BaseAgent and AgentRegistry
  - 16 tests for Communication system
  - 84-98% code coverage for new modules
  - Thread-safety validation
  - Deadlock prevention testing

### [DOCS] Documentation & Examples
- **New demo** - `21_multi_agent_demo.py` showcasing all features
- **Comprehensive examples** - Agent creation, messaging, broadcast, task processing
- **API documentation** - Full docstrings for all new classes and methods

### [MAINTENANCE] Technical Improvements
- Thread-safe message queue implementation
- Deadlock prevention in broadcast messaging
- Efficient memory management for agent communication
- Clean separation of concerns (agents, registry, communication)

### [MODULES] New Modules
- `mem_llm/multi_agent/base_agent.py` - Core agent implementation
- `mem_llm/multi_agent/agent_registry.py` - Agent management
- `mem_llm/multi_agent/communication.py` - Communication infrastructure

---

## [2.1.4] - 2025-11-20

### [METRICS] Conversation Analytics
- **New Analytics Module** - Comprehensive conversation analysis and insights
- **Topic Extraction** - Automatically extracts key topics from conversations
- **Engagement Metrics** - Tracks user engagement, session length, and active days
- **Visual Reports** - Generates reports in JSON, CSV, or Markdown formats
- **Time Distribution** - Analyzes activity patterns by hour of day

### [CONFIG] Config Presets
- **Built-in Presets** - 8 optimized presets for common use cases:
  - `chatbot` (General purpose)
  - `code_assistant` (Programming expert)
  - `creative_writer` (Storytelling)
  - `tutor` (Educational)
  - `analyst` (Data analysis)
  - `translator` (Translation)
  - `summarizer` (Content summary)
  - `researcher` (Deep research)
- **Custom Presets** - Create, save, and load your own configuration presets
- **Easy Integration** - Initialize agent with `MemAgent(preset='code_assistant')`

### [TOOLS] Improvements & Fixes
- **Test Coverage** - Significant increase in test coverage (Analytics & Presets)
- **Code Quality** - Fixed syntax warnings and flake8 issues
- **LM Studio Integration** - Improved compatibility and testing with LM Studio
- **Ollama Integration** - Standardized on `ministral-3:14b` for testing

## [2.1.3] - 2025-11-10

### [ENHANCED] Enhanced Tool Execution

- **Smart Tool Call Parser** - Now understands natural language tool calls (not just `TOOL_CALL:` format)
- **Improved System Prompt** - Clearer instructions with examples ([OK]/[ERROR])
- **Better Error Messages** - More helpful validation feedback

### [DOCS] Details

LLMs often don't follow the exact `TOOL_CALL:` format. Now the parser also understands:
- `use tool_name(...)`
- `calling tool_name(...)`
- `` `tool_name(...)` `` (markdown format)

System prompt now includes clear DO/DON'T examples to guide the LLM.

## [2.1.2] - 2025-11-10

### [BUGFIX] Critical Fix

- **Fixed dynamic tool registration** - System prompt now rebuilds on every chat call to include newly registered tools
- **Fixed custom tools not visible to LLM** - Tools registered after agent initialization now properly appear in LLM's system prompt
- **Removed google-generativeai dependency** - No more Gemini dependencies (100% local)
- Affects both `chat()` and `chat_stream()` methods

### [DOCS] Details

When users called `agent.tool_registry.register_tool()` after creating the agent, those tools were registered in the registry but not included in the LLM's system prompt. Now the system prompt dynamically rebuilds before each chat to include all registered tools.

### [CLEANUP] Cleanup

- Removed `google-generativeai` from core dependencies - now truly 100% local and private

## [2.1.1] - 2025-11-10

### [BUGFIX] Bug Fixes

- **Fixed `register_tool()` method missing** - Added `register_tool()` as an alias to `register()` in `ToolRegistry` for backward compatibility
- **Fixed async tools not loading** - Updated `_load_builtin_tools()` to automatically load async tools from `builtin_tools_async.py`
- **Fixed export name** - Added `ASYNC_BUILTIN_TOOLS` export to async tools module

### [MAINTENANCE] Improvements

- `register_tool()` now accepts both `Tool` objects and decorated functions
- Better error handling for tool registration
- Improved documentation for registration methods

## [2.1.0] - 2025-11-10

### [NEW] New Features

- **Async Tool Support** [ENHANCED]
  - Full support for `async def` functions as tools
  - Automatic detection of async/sync functions
  - Proper event loop handling for async execution
  - Non-blocking I/O operations for better performance

- **Comprehensive Input Validation** [OK]
  - **Pattern Validation**: Regex patterns for string parameters (e.g., email, URL validation)
  - **Range Validation**: Min/max values for numbers
  - **Length Validation**: Min/max length for strings and lists
  - **Choice Validation**: Enum-like behavior with predefined allowed values
  - **Custom Validators**: User-defined validation functions
  - Detailed validation error messages

- **Built-in Async Tools** [ASYNC]
  - `fetch_url`: Async HTTP GET requests
  - `post_json`: Async HTTP POST with JSON
  - `read_file_async`: Non-blocking file reads
  - `write_file_async`: Non-blocking file writes
  - `async_sleep`: Async wait utility

### [MAINTENANCE] Enhanced Tool System

- `ToolParameter` dataclass extended with validation fields
- `Tool.validate_arguments()` method for pre-execution validation
- `Tool.is_async` flag to identify async functions
- Enhanced `@tool` decorator with validation parameters

### [DOCS] Documentation

- Added `examples/20_async_and_validation.py` - Complete async and validation demo
- Updated tool system documentation
- Added validation examples and best practices

### [BENEFITS] Benefits

- **Better Performance**: Async tools don't block the event loop
- **Safer Execution**: Input validation prevents errors before execution
- **Professional APIs**: Proper error handling and validation
- **Flexible Validation**: Multiple validation strategies (regex, range, choice, custom)

---

## [2.0.0] - 2025-11-10

### [NEW] Major Features

- **Function Calling / Tools System** [TOOLS]
  - Enabled LLMs to perform actions by calling external Python functions
  - `@tool` decorator for easy function registration with automatic schema generation
  - `ToolRegistry` to manage and execute tools with error handling
  - `ToolCallParser` to detect and parse tool calls from LLM responses
  - Dynamic system prompt integration to inform LLM about available tools
  - Support for custom tool categories and organization

- **Built-in Tools (13 total)** [MODULES]
  - **Math** (1): `calculate` - Safe expression evaluation with parentheses support
  - **Text** (4): `count_words`, `reverse_text`, `to_uppercase`, `to_lowercase`
  - **File System** (3): `read_file`, `write_file`, `list_files`
  - **Utility** (2): `get_current_time`, `create_json`
  - **Memory** *(NEW)* (3): `search_memory`, `get_user_info`, `list_conversations`

- **Memory-Aware Tools** [MEMORY] *(Game Changer)*
  - Agents can now access their own conversation history!
  - `search_memory`: Search through past conversations by keyword
  - `get_user_info`: Get current user profile and conversation stats
  - `list_conversations`: List recent conversation history with filtering
  - Enables truly self-aware AI agents with context access
  - Tool chaining: Combine memory search with other tools (e.g., search + count_words)

### [BUGFIX] Bug Fixes

- **Tool System**
  - Fixed ToolResult status enum comparison (`result.status.value == "success"`)
  - Improved argument parser to handle parentheses in expressions `(25 * 4) + 10`
  - Enhanced quote and comma handling in tool call parsing
  - Added expression cleaning for natural language math queries

- **API & Web UI**
  - Fixed memory search and stats endpoints in `api_server.py`
  - Resolved "Duplicate Operation ID" warning by properly organizing endpoints
  - Fixed HTML rendering issue (added `media_type="text/html"` to FileResponse)

### [DOCS] Documentation

- **README Updates**
  - Added comprehensive Function Calling section with examples
  - Documented all 13 built-in tools with usage examples
  - Added Memory Tools section demonstrating self-aware agents
  - Updated version numbers and feature list

- **New Examples**
  - `examples/18_function_calling.py` - Complete tool system demo
  - `examples/19_memory_tools_demo.py` - Memory-aware agent demo

### [MAINTENANCE] Technical Improvements

- Enhanced tool call pattern matching and parsing
- Better error handling for tool execution failures
- Improved system prompt formatting for tool instructions
- Added tool execution logging and debugging support

### [METRICS] Test Results

- [OK] All 13 built-in tools working correctly
- [OK] Custom tool registration and execution verified
- [OK] Memory tools successfully accessing conversation history
- [OK] Tool chaining (memory + calculation, memory + text processing)
- [OK] Parenthetical expressions in calculator: `(25 * 4) + 10 = 110`

---

## [1.3.6] - 2025-11-10

### [BREAKING] Breaking Changes

- **Removed Google Gemini Support**
  - Eliminated cloud backend dependency for 100% local operation
  - Removed `gemini_client.py` and all Gemini-related code
  - Updated all examples and documentation to reflect local-only backends
  - Strengthened privacy-first approach with Ollama and LM Studio only

### [SECURITY] Privacy Enhancements

- **100% Local Operation**
  - No external API calls or cloud services required
  - Complete data sovereignty and privacy control
  - All processing happens on local machine
  - Perfect for sensitive/confidential data use cases

### [MAINTENANCE] Updates

- **Default Model Changed**: `ministral-3:14b` (was `ministral-3:14b`)
- **Documentation**: Removed all Gemini references from README, examples, and guides
- **Examples**: Deleted `12_gemini_example.py`, updated multi-backend examples
- **Cleaner Codebase**: Removed unused cloud integration code

### [MODULES] What's Included

- [OK] Ollama backend (local)
- [OK] LM Studio backend (local)
- [OK] Auto-detection between local backends
- [OK] Streaming responses
- [OK] Web UI & REST API
- [OK] Vector search with ChromaDB
- [OK] Response metrics & analytics

---

## [1.3.2] - 2025-11-02

### [MILESTONE] Major Features

- [METRICS] **Response Metrics & Quality Analytics** (v1.3.1+)
  - `ChatResponse` dataclass: Comprehensive response tracking
  - `ResponseMetricsAnalyzer`: Aggregate analytics and monitoring
  - Confidence scoring: Based on KB usage, memory, temperature, and length
  - Real-time latency tracking: Monitor response performance
  - Quality labels: High/Medium/Low classification
  - Export metrics: JSON and summary formats for dashboards
  - Production monitoring: Health checks and SLA tracking

- [SEARCH] **Vector Search & Semantic Knowledge Base** (v1.3.2+)
  - ChromaDB integration: Semantic search with embeddings
  - Sentence-transformers support: `all-MiniLM-L6-v2` default model
  - Cross-lingual search: Understands meaning across languages
  - Hybrid search: Vector + keyword search combination
  - Better relevancy: Semantic understanding vs keyword matching
  - Optional feature: Install with `pip install chromadb sentence-transformers`

### [NEW] New Components

- `response_metrics.py`: `ChatResponse`, `ResponseMetricsAnalyzer`, `calculate_confidence`
- `vector_store.py`: `VectorStore`, `ChromaVectorStore`, `create_vector_store`
- Enhanced `SQLMemoryManager`: Vector search integration
- Enhanced `MemAgent`: Response metrics and vector search support

### [CHANGED] Enhanced Features

- **MemAgent.chat()**: New `return_metrics` parameter for detailed response analysis
- **Memory Metadata**: Automatic saving of response metrics in conversations
- **User Profile**: Improved preferences and summary extraction/parsing
- **Knowledge Base Search**: Optional vector search with `use_vector_search=True`
- **ChromaDB Sync**: `sync_all_kb_to_vector_store()` method for existing KB entries

### [DOCS] New Examples

- `15_response_metrics.py`: Response quality metrics and analytics
- `16_vector_search.py`: Semantic/vector search demonstration

### [BUGFIX] Bug Fixes

- Fixed metadata not being saved in conversation history
- Fixed preferences parsing from JSON string to dict
- Fixed summary generation for existing users
- Fixed `get_user_profile()` SQL/JSON memory detection logic
- Fixed ChromaDB embedding function compatibility

### [DOCS] Documentation

- Updated all examples: Simplified and more readable
- Enhanced README with new features
- Vector search usage guide

### [IMPROVED] Improved

- Better error handling for ChromaDB initialization
- Fallback mechanism for embedding function loading
- Enhanced similarity score calculation for vector search
- Improved conversation metadata tracking

## [1.3.1] - 2025-10-31

### [DOCS] Documentation

- [OK] **README Update**: Fixed PyPI package README to show v1.3.0 features correctly
- [OK] No code changes - all v1.3.0 functionality remains the same

## [1.3.0] - 2025-10-31

### [MILESTONE] Major Features

- [BACKEND] **Multi-Backend LLM Support**: Choose your preferred LLM backend
  - **Ollama**: Local, privacy-first, 100+ models
  - **LM Studio**: Fast local inference with easy GUI
  - **Google Gemini**: Powerful cloud models (gemini-2.5-flash)
  - Unified API across all backends
  - Seamless switching between backends

- [ARCHITECTURE] **Factory Pattern Architecture**: Clean, extensible design
  - `LLMClientFactory`: Central backend management
  - `BaseLLMClient`: Abstract interface for all backends
  - Easy to add new backends in the future

- [SEARCH] **Auto-Detection**: Automatically find available LLM service
  - `auto_detect_backend=True` parameter
  - Checks Ollama â†’ LM Studio â†’ other local services
  - No manual configuration needed

### [NEW] New Components

- `BaseLLMClient`: Abstract base class for all LLM backends
- `LLMClientFactory`: Factory pattern for backend creation
- `OllamaClient` (refactored): Now inherits from BaseLLMClient
- `LMStudioClient`: OpenAI-compatible local inference
- `GeminiClient`: Google Gemini API integration

### [DOCS] New Examples

- `11_lmstudio_example.py`: Using LM Studio backend
- `12_gemini_example.py`: Using Google Gemini API
- `13_multi_backend_comparison.py`: Compare backend performance
- `14_auto_detect_backend.py`: Auto-detection feature

### [DOCS] New Documentation

- `MULTI_BACKEND_GUIDE.md`: Comprehensive guide for multi-backend setup

### [CHANGED] Changed

- **MemAgent**: Now supports multiple backends (backward compatible)
- **Examples**: All simplified for clarity
- **Package structure**: Better organized with `clients/` subdirectory

### [IMPROVED] Improved

- **Backward Compatibility**: All v1.2.0 code still works
- **Error Messages**: Backend-specific troubleshooting
- **Connection Checks**: Improved availability detection

### [TEST] Testing

- 16+ new tests for multi-backend support
- Factory pattern tests
- Backend availability checks
- MemAgent integration tests

## [1.2.0] - 2025-10-21

### Added

- [METRICS] **Conversation Summarization**: Automatic conversation history compression
  - `ConversationSummarizer`: Generates concise summaries from conversation histories
  - `AutoSummarizer`: Threshold-based automatic summary updates
  - Token compression: ~40-60% reduction in context size
  - Key facts extraction: Automatic user profile insights
  - Configurable thresholds and conversation limits

- [EXPORT] **Data Export/Import System**: Multi-format and multi-database support
  - `DataExporter`: Export conversations to JSON, CSV, SQLite, PostgreSQL, MongoDB
  - `DataImporter`: Import from JSON, CSV, SQLite, PostgreSQL, MongoDB
  - Auto-create databases: PostgreSQL and MongoDB databases created automatically if missing
  - Enterprise-ready: Support for analytics (PostgreSQL) and real-time dashboards (MongoDB)
  - Optional dependencies: `pip install mem-llm[postgresql]`, `pip install mem-llm[mongodb]`, `pip install mem-llm[databases]`

- [DATABASE] **In-Memory Database Support**: Temporary database operations
  - `db_path=":memory:"` parameter for MemAgent
  - No file creation: Perfect for testing and temporary workflows
  - Full SQL functionality without persistent storage

### Changed

- [LOGGING] **Reduced Logging Verbosity**: Cleaner console output
  - Default log level changed from INFO to WARNING
  - Less noise in production environments
  - Users can still enable detailed logs via config
  - Examples suppress logs for cleaner demonstrations

- [MODULES] **Enhanced Package Structure**: Better optional dependencies
  - `pip install mem-llm[postgresql]` - PostgreSQL support only
  - `pip install mem-llm[mongodb]` - MongoDB support only
  - `pip install mem-llm[databases]` - Both PostgreSQL and MongoDB
  - `pip install mem-llm[all]` - Everything included

### Fixed

- [DATABASE] **Database Path Handling**: SQLite files now organized in memories/ folder
  - All SQLite files (.db, .db-shm, .db-wal) now in memories/ directory
  - Cleaner workspace: No database files cluttering project root
  - Automatic directory creation: memories/ folder created if missing

- [MAINTENANCE] **MemAgent db_path Parameter**: Added missing parameter
  - New `db_path` parameter in MemAgent.__init__()
  - Enables custom database locations and in-memory databases
  - Better control over database file placement

## [1.1.0] - 2025-10-21

### Added

- [SECURITY] **Prompt Injection Protection** (Opt-in): Advanced security system to detect and block prompt injection attacks
  - `PromptInjectionDetector`: Detects 15+ attack patterns (role manipulation, system override, jailbreak attempts)
  - Risk assessment: safe, low, medium, high, critical levels
  - `InputSanitizer`: Neutralizes malicious patterns while preserving user intent
  - `SecurePromptBuilder`: Template-based secure prompt construction
  - Enable with `enable_security=True` parameter (default: False for backward compatibility)

- [DOCS] **Structured Logging System**: Production-ready logging infrastructure
  - `MemLLMLogger`: Centralized logging with file and console handlers
  - Specialized methods: `log_llm_call()`, `log_memory_operation()`, `log_error_with_context()`
  - Configurable log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - Timestamps and formatted output for debugging

- [CHANGED] **Retry Logic with Exponential Backoff**: Robust error handling for network operations
  - `exponential_backoff_retry` decorator: 3 retries with 1s, 2s, 4s delays
  - `SafeExecutor`: Context manager for safe operations with automatic rollback
  - `check_connection_with_retry()`: Connection validation before operations
  - Separate handling for timeout, connection, and general errors

### Changed

- [IMPROVED] **Thread-Safe SQLite Operations**: Complete concurrency overhaul
  - Added `threading.RLock()` to all critical operations (add_user, add_interaction, get_recent, search)
  - Configured `isolation_level=None` (autocommit mode) to prevent transaction conflicts
  - Set `busy_timeout=30000` (30 seconds) for concurrent write handling
  - Performance: 15,346 messages/second write throughput, <1ms search latency

- [STORAGE] **SQLite WAL Mode**: Write-Ahead Logging for better concurrency
  - Enabled WAL mode with `PRAGMA journal_mode=WAL`
  - Configured 64MB cache (`cache_size=-64000`)
  - Set `synchronous=NORMAL` for balanced safety/performance
  - Supports 200+ concurrent writes without errors

### Fixed

- [BUGFIX] **Concurrent Write Errors**: Fixed "cannot start transaction within transaction" errors
  - Root cause: Multiple threads trying to start nested transactions
  - Solution: Autocommit mode + RLock on all operations
  - Validated: 200 concurrent writes in 0.03s with ZERO errors

- [BUGFIX] **Race Conditions**: Fixed "bad parameter or other API misuse" in multi-threaded scenarios
  - Added thread-safe connection pooling
  - Eliminated tuple index errors in concurrent reads
  - All race conditions verified fixed in stress tests

### Security

- [SECURITY] **Prompt Injection Detection Patterns**:
  - Role manipulation: "You are now...", "Ignore previous...", "Act as..."
  - System override: "Forget all instructions", "Disregard guidelines"
  - Jailbreak: "DAN mode", "developer mode", "unrestricted mode"
  - Token injection: Special tokens, control characters, encoding exploits
  - Context pollution: Excessive newlines, recursive instructions

- [INPUT] **Input Sanitization**:
  - Escapes control characters and special sequences
  - Neutralizes role-switching patterns
  - Preserves legitimate user input while removing threats
  - Optional strict mode for high-security environments

### Performance

- [METRICS] **Benchmark Results** (Intel Core i7, 16GB RAM):
  - Write throughput: 15,346 messages/second (500 writes/0.0326s)
  - Search latency: <1ms for 500 conversations
  - Concurrent writes: 200 operations in 0.03s (ZERO errors)
  - Memory overhead: Minimal (~10MB for 10,000 conversations)

### Testing

- [TEST] **Enhanced Test Coverage**: New test suites added
  - `test_improvements.py`: Logging, retry logic, WAL mode (4/4 tests passed)
  - `test_advanced_coverage.py`: Concurrent access, corruption recovery, long history (9 tests)
  - `test_backward_compatibility.py`: Validates v1.0.x code still works (100% compatible)
  - Comprehensive test suite: 10/10 tests passed (100% success rate)

### Backward Compatibility

- [OK] **100% Backward Compatible**: All v1.0.x code works without modification
  - `enable_security=False` by default (opt-in security)
  - All new imports wrapped in try/except (graceful degradation)
  - No breaking changes to existing API
  - Existing databases work without migration
  - Validated with comprehensive compatibility tests

### Technical Details

- **New Modules**:
  - `mem_llm/logger.py` - Structured logging system (MemLLMLogger)
  - `mem_llm/retry_handler.py` - Exponential backoff retry logic (exponential_backoff_retry, SafeExecutor)
  - `mem_llm/prompt_security.py` - Security detection/sanitization (PromptInjectionDetector, InputSanitizer, SecurePromptBuilder)

- **Modified Modules**:
  - `mem_llm/memory_db.py` - Thread-safe operations, WAL mode, busy timeout
  - `mem_llm/llm_client.py` - Retry logic integration
  - `mem_llm/mem_agent.py` - Security parameter, input validation
  - `mem_llm/__init__.py` - New exports (security, logging, retry classes)
  - `pyproject.toml` - Version bump to 1.1.0

### Migration Guide

**From v1.0.x to v1.1.0:**

```python
# v1.0.x code (still works exactly the same)
agent = MemAgent(model="ministral-3:14b", use_sql=True)

# v1.1.0 with new features (opt-in)
from mem_llm import MemAgent, get_logger

# Enable security protection
agent = MemAgent(
    model="ministral-3:14b",
    use_sql=True,
    enable_security=True  # NEW: Prompt injection protection
)

# Use structured logging
logger = get_logger()
logger.info("Agent created with security enabled")

# All old code works without changes!
agent.set_user("alice")
response = agent.chat("Hello!")  # Security checks applied automatically
```

### Dependencies

- No new required dependencies
- All new features use Python standard library
- Optional dependencies remain optional

### Notes

- **Production Ready**: All features tested in multi-threaded environments
- **Performance Tested**: Benchmarked up to 15K+ messages/second
- **Security Validated**: 15+ injection patterns detected and blocked
- **Stress Tested**: 200+ concurrent operations without failures
- **Backward Compatible**: Drop-in replacement for v1.0.x

## [1.0.11] - 2025-10-20

### Changed
- [DOCS] **Enhanced README.md**: Comprehensive PyPI documentation
  - Professional badges (version, Python support, license)
  - Detailed feature list with emojis
  - Quick start guide with 5-line example
  - Multiple usage examples (multi-user, advanced config, memory tools)
  - CLI command documentation
  - Configuration guide
  - Complete model compatibility information
  - Architecture overview
  - Test coverage details
  - Development and contribution guidelines
  - SEO-optimized for PyPI discovery

### Improved
- [DOCS] **Documentation Quality**: Better structured for PyPI users
- [BENEFITS] **User Onboarding**: Clearer getting started instructions
- [SEARCH] **Discoverability**: Enhanced keywords and descriptions

## [1.0.10] - 2025-10-20

### Added
- [MEMORY] **Dynamic Prompt System**: Context-aware system prompts that adapt to active features
  - Prevents hallucinations by only including instructions for enabled features
  - Separate prompt sections for KB, tools, business/personal modes
  - Automatic feature detection (Knowledge Base presence, tools availability)
  - Logging shows active features: "[OK] Knowledge Base | [ERROR] Tools | [STORAGE] Memory: SQL"
- [CHANGED] **Universal Ollama Model Compatibility**: Full support for ALL Ollama models
  - Thinking-enabled models (Qwen3, DeepSeek, etc.) now work correctly
  - Auto-detection and handling of thinking mode
  - `enable_thinking: false` parameter for direct responses
  - Fallback extraction from thinking process when needed
  - Empty response retry with simpler prompts
- [METRICS] **Comprehensive Test Suite**: Pre-publish validation system
  - 34 automated tests covering all major features
  - Tests: imports, CLI, Ollama, JSON/SQL memory, MemAgent, config, multi-user
  - User scenario testing with output analysis
  - Hallucination detection and context verification

### Changed
- [IMPROVED] **LLM Token Limits**: Increased from 150 to 2000 tokens for thinking models
- [CLEANUP] **Removed Obsolete Module**: Deleted `prompt_templates.py` (replaced by dynamic system)
- [DOCS] **Context Window**: Increased from 2048 to 4096 tokens for better context
- [BENEFITS] **Response Quality**: Better handling of empty responses with automatic retry

### Fixed
- [BUGFIX] **Thinking Model Issue**: Qwen3 and similar models now respond correctly
  - Fixed empty responses from thinking-mode models
  - Proper content extraction from model responses
  - System prompt instructions to suppress thinking process
- [MAINTENANCE] **Stop Sequences**: Removed problematic stop sequences that interfered with models
- [WARN] **Empty Response Handling**: Automatic retry with fallback for reliability

### Improved
- [PROMPT] **Prompt Quality**: Feature-specific instructions prevent confusion
- [ENHANCED] **Model Performance**: Works seamlessly with granite4, qwen3, llama3, and all Ollama models
- [UX] **User Experience**: No more irrelevant feature mentions in responses
- [TEST] **Testing Coverage**: Complete validation before releases

### Technical Details
- Created `mem_llm/dynamic_prompt.py` (350+ lines) - modular prompt builder
- Modified `mem_llm/mem_agent.py`:
  - Added `has_knowledge_base` and `has_tools` tracking flags
  - Implemented `_build_dynamic_system_prompt()` method
  - Removed ~70 lines of old static prompt code
  - Added empty response retry logic
- Modified `mem_llm/llm_client.py`:
  - Added thinking mode detection and suppression
  - Increased token limits and context window
  - Improved response extraction logic
  - Added fallback for thinking-enabled models
- Updated `mem_llm/__init__.py` - exported `dynamic_prompt_builder`
- Cleaned `MANIFEST.in` - removed non-existent files
- Created `comprehensive_test.py` - 34 automated tests
- Created `user_test.py` - real-world scenario validation

### Breaking Changes
- None - fully backward compatible

## [1.0.9] - 2025-10-20

### Added
- [DOCS] **PyPI-Optimized README**: Complete rewrite with practical examples
  - 5 comprehensive usage examples with full code and output
  - Print statements in all examples for better user experience
  - Step-by-step workflows showing complete processes
  - Real-world customer service scenario example
  - Turkish language support demonstration
  - User profile extraction example
- [CONFIG] **Document Configuration Examples**: Added example demonstrating PDF/DOCX/TXT config generation
- [TEST] **Config Update Testing**: Verification that manual YAML edits work correctly

### Changed
- [REMOVED] **Removed docs folder**: Consolidated documentation into main README
- [LOGGING] **Logging Behavior**: Changed from file+console to console-only logging
  - No more `mem_agent.log` files cluttering workspace
  - Keeps workspace clean with only `.db` and `.yaml` files
- [DOCS] **Example Format**: All examples now include:
  - Print statements for visibility
  - Expected output blocks
  - Full conversation flows
  - Real usage scenarios

### Fixed
- [BUGFIX] **Log File Pollution**: Removed FileHandler from logging, only StreamHandler now
- [DOCS] **README Examples**: Fixed examples that didn't show actual output or complete process

### Improved
- [BENEFITS] **User Experience**: Much clearer examples for new users
- [DOCS] **Documentation Quality**: Professional PyPI-ready documentation
- [SEARCH] **Example Clarity**: Each example shows input, process, and output

### Technical Details
- Modified `mem_llm/mem_agent.py` - removed FileHandler from logging setup
- Rewrote `README.md` with 5 detailed examples
- Created `examples/07_document_config.py` for PDF/DOCX/TXT feature
- Verified config changes work correctly with manual YAML edits

## [1.0.8] - 2025-10-20

### Added
- [BENEFITS] **CLI Tool**: Full-featured command-line interface
  - `mem-llm chat` - Interactive chat sessions
  - `mem-llm check` - System verification
  - `mem-llm stats` - Statistics and analytics
  - `mem-llm export` - Data export (JSON/TXT)
  - `mem-llm clear` - User data deletion
- [METRICS] **Feature Comparison Matrix**: Clear comparison between JSON and SQL modes
- [MODULES] **Improved Dependencies**: Proper separation of core, dev, and optional requirements
  - `requirements.txt` - Core dependencies only
  - `requirements-dev.txt` - Development tools
  - `requirements-optional.txt` - Optional features (web, API, etc.)
- [MAINTENANCE] **Better Error Handling**: Improved startup checks with user-friendly messages
- [DOCS] **Enhanced Documentation**: CLI usage examples and feature matrices

### Changed
- [LANGUAGE] **Multi-language Support**: Changed from "Turkish Support" to general multi-language
- [DOCS] **Documentation**: All content now in English for broader accessibility
- [PROMPT] **CLI Entry Point**: Added `mem-llm` console script in setup.py

### Fixed
- [BUGFIX] Missing `click` dependency in requirements
- [BUGFIX] Improved error messages when Ollama is not running

### Improved
- [IMPROVED] Better user experience with CLI commands
- [DOCS] Clearer README with usage examples
- [BENEFITS] More intuitive API design

## [1.0.4] - 2025-10-13

### Added
- [NEW] Config-free knowledge base support - KB now works without config.yaml
- [NEW] Smart keyword extraction for knowledge base search (Turkish & English stopwords)
- [NEW] Enhanced KB context injection - KB data injected directly into user message
- [NEW] Automatic user profile extraction (name, favorite_food, location)
- [NEW] Turkish language support for profile extraction
- [NEW] SQL-JSON memory compatibility methods
- [DOCS] New example: `example_knowledge_base.py`
- [TEST] Comprehensive test suite

### Fixed
- [BUGFIX] Knowledge base not being used without config.yaml
- [BUGFIX] LLM ignoring knowledge base information
- [BUGFIX] User profiles returning empty dictionaries
- [BUGFIX] Profile updates not working correctly with SQL memory
- [BUGFIX] Keyword search failing with Turkish queries

### Improved
- [IMPROVED] Better KB-first response priority in system prompts
- [IMPROVED] More accurate answers from knowledge base
- [IMPROVED] Enhanced search algorithm with stopword filtering

## [1.0.3] - 2025-10-12

### Added
- [MODULES] Initial PyPI release
- [BENEFITS] Core memory features (JSON & SQL)
- [AGENT] Ollama integration
- [STORAGE] Knowledge base system
- [TOOLS] User tools
- [CONFIG] Configuration management

### Features
- Memory-enabled AI agent
- JSON and SQL memory backends
- Knowledge base integration
- User profile management
- Conversation history
- Configuration from YAML/documents

## [1.0.2] - 2025-10-11

### Internal
- [MAINTENANCE] Package structure improvements
- [DOCS] Documentation updates

## [1.0.1] - 2025-10-10

### Fixed
- [BUGFIX] Import errors after package rename
- [MODULES] Package directory naming issues

## [1.0.0] - 2025-10-09

### Initial Release
- [MILESTONE] First stable release
- [AGENT] Memory-enabled AI assistant
- [STORAGE] JSON memory management
- [BACKEND] Ollama integration



