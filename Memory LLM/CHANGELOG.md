# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-10-21

### Added

- 📊 **Conversation Summarization**: Automatic conversation history compression
  - `ConversationSummarizer`: Generates concise summaries from conversation histories
  - `AutoSummarizer`: Threshold-based automatic summary updates
  - Token compression: ~40-60% reduction in context size
  - Key facts extraction: Automatic user profile insights
  - Configurable thresholds and conversation limits
  
- 📤 **Data Export/Import System**: Multi-format and multi-database support
  - `DataExporter`: Export conversations to JSON, CSV, SQLite, PostgreSQL, MongoDB
  - `DataImporter`: Import from JSON, CSV, SQLite, PostgreSQL, MongoDB
  - Auto-create databases: PostgreSQL and MongoDB databases created automatically if missing
  - Enterprise-ready: Support for analytics (PostgreSQL) and real-time dashboards (MongoDB)
  - Optional dependencies: `pip install mem-llm[postgresql]`, `pip install mem-llm[mongodb]`, `pip install mem-llm[databases]`
  
- 🗄️ **In-Memory Database Support**: Temporary database operations
  - `db_path=":memory:"` parameter for MemAgent
  - No file creation: Perfect for testing and temporary workflows
  - Full SQL functionality without persistent storage

### Changed

- 🔇 **Reduced Logging Verbosity**: Cleaner console output
  - Default log level changed from INFO to WARNING
  - Less noise in production environments
  - Users can still enable detailed logs via config
  - Examples suppress logs for cleaner demonstrations
  
- 📦 **Enhanced Package Structure**: Better optional dependencies
  - `pip install mem-llm[postgresql]` - PostgreSQL support only
  - `pip install mem-llm[mongodb]` - MongoDB support only  
  - `pip install mem-llm[databases]` - Both PostgreSQL and MongoDB
  - `pip install mem-llm[all]` - Everything included

### Fixed

- 🗄️ **Database Path Handling**: SQLite files now organized in memories/ folder
  - All SQLite files (.db, .db-shm, .db-wal) now in memories/ directory
  - Cleaner workspace: No database files cluttering project root
  - Automatic directory creation: memories/ folder created if missing
  
- 🔧 **MemAgent db_path Parameter**: Added missing parameter
  - New `db_path` parameter in MemAgent.__init__()
  - Enables custom database locations and in-memory databases
  - Better control over database file placement

## [1.1.0] - 2025-10-21

### Added

- 🔒 **Prompt Injection Protection** (Opt-in): Advanced security system to detect and block prompt injection attacks
  - `PromptInjectionDetector`: Detects 15+ attack patterns (role manipulation, system override, jailbreak attempts)
  - Risk assessment: safe, low, medium, high, critical levels
  - `InputSanitizer`: Neutralizes malicious patterns while preserving user intent
  - `SecurePromptBuilder`: Template-based secure prompt construction
  - Enable with `enable_security=True` parameter (default: False for backward compatibility)
  
- 📝 **Structured Logging System**: Production-ready logging infrastructure
  - `MemLLMLogger`: Centralized logging with file and console handlers
  - Specialized methods: `log_llm_call()`, `log_memory_operation()`, `log_error_with_context()`
  - Configurable log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - Timestamps and formatted output for debugging
  
- 🔄 **Retry Logic with Exponential Backoff**: Robust error handling for network operations
  - `exponential_backoff_retry` decorator: 3 retries with 1s, 2s, 4s delays
  - `SafeExecutor`: Context manager for safe operations with automatic rollback
  - `check_connection_with_retry()`: Connection validation before operations
  - Separate handling for timeout, connection, and general errors

### Changed

- ⚡ **Thread-Safe SQLite Operations**: Complete concurrency overhaul
  - Added `threading.RLock()` to all critical operations (add_user, add_interaction, get_recent, search)
  - Configured `isolation_level=None` (autocommit mode) to prevent transaction conflicts
  - Set `busy_timeout=30000` (30 seconds) for concurrent write handling
  - Performance: 15,346 messages/second write throughput, <1ms search latency
  
- 💾 **SQLite WAL Mode**: Write-Ahead Logging for better concurrency
  - Enabled WAL mode with `PRAGMA journal_mode=WAL`
  - Configured 64MB cache (`cache_size=-64000`)
  - Set `synchronous=NORMAL` for balanced safety/performance
  - Supports 200+ concurrent writes without errors

### Fixed

- 🐛 **Concurrent Write Errors**: Fixed "cannot start transaction within transaction" errors
  - Root cause: Multiple threads trying to start nested transactions
  - Solution: Autocommit mode + RLock on all operations
  - Validated: 200 concurrent writes in 0.03s with ZERO errors
  
- 🐛 **Race Conditions**: Fixed "bad parameter or other API misuse" in multi-threaded scenarios
  - Added thread-safe connection pooling
  - Eliminated tuple index errors in concurrent reads
  - All race conditions verified fixed in stress tests

### Security

- 🛡️ **Prompt Injection Detection Patterns**:
  - Role manipulation: "You are now...", "Ignore previous...", "Act as..."
  - System override: "Forget all instructions", "Disregard guidelines"
  - Jailbreak: "DAN mode", "developer mode", "unrestricted mode"
  - Token injection: Special tokens, control characters, encoding exploits
  - Context pollution: Excessive newlines, recursive instructions
  
- 🔐 **Input Sanitization**:
  - Escapes control characters and special sequences
  - Neutralizes role-switching patterns
  - Preserves legitimate user input while removing threats
  - Optional strict mode for high-security environments

### Performance

- 📊 **Benchmark Results** (Intel Core i7, 16GB RAM):
  - Write throughput: 15,346 messages/second (500 writes/0.0326s)
  - Search latency: <1ms for 500 conversations
  - Concurrent writes: 200 operations in 0.03s (ZERO errors)
  - Memory overhead: Minimal (~10MB for 10,000 conversations)

### Testing

- 🧪 **Enhanced Test Coverage**: New test suites added
  - `test_improvements.py`: Logging, retry logic, WAL mode (4/4 tests passed)
  - `test_advanced_coverage.py`: Concurrent access, corruption recovery, long history (9 tests)
  - `test_backward_compatibility.py`: Validates v1.0.x code still works (100% compatible)
  - Comprehensive test suite: 10/10 tests passed (100% success rate)

### Backward Compatibility

- ✅ **100% Backward Compatible**: All v1.0.x code works without modification
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
agent = MemAgent(model="granite4:tiny-h", use_sql=True)

# v1.1.0 with new features (opt-in)
from mem_llm import MemAgent, get_logger

# Enable security protection
agent = MemAgent(
    model="granite4:tiny-h",
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
- 📝 **Enhanced README.md**: Comprehensive PyPI documentation
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
- 📚 **Documentation Quality**: Better structured for PyPI users
- 🎯 **User Onboarding**: Clearer getting started instructions
- 🔍 **Discoverability**: Enhanced keywords and descriptions

## [1.0.10] - 2025-10-20

### Added
- 🧠 **Dynamic Prompt System**: Context-aware system prompts that adapt to active features
  - Prevents hallucinations by only including instructions for enabled features
  - Separate prompt sections for KB, tools, business/personal modes
  - Automatic feature detection (Knowledge Base presence, tools availability)
  - Logging shows active features: "✅ Knowledge Base | ❌ Tools | 💾 Memory: SQL"
- 🔄 **Universal Ollama Model Compatibility**: Full support for ALL Ollama models
  - Thinking-enabled models (Qwen3, DeepSeek, etc.) now work correctly
  - Auto-detection and handling of thinking mode
  - `enable_thinking: false` parameter for direct responses
  - Fallback extraction from thinking process when needed
  - Empty response retry with simpler prompts
- 📊 **Comprehensive Test Suite**: Pre-publish validation system
  - 34 automated tests covering all major features
  - Tests: imports, CLI, Ollama, JSON/SQL memory, MemAgent, config, multi-user
  - User scenario testing with output analysis
  - Hallucination detection and context verification

### Changed
- ⚡ **LLM Token Limits**: Increased from 150 to 2000 tokens for thinking models
- 🧹 **Removed Obsolete Module**: Deleted `prompt_templates.py` (replaced by dynamic system)
- 📝 **Context Window**: Increased from 2048 to 4096 tokens for better context
- 🎯 **Response Quality**: Better handling of empty responses with automatic retry

### Fixed
- 🐛 **Thinking Model Issue**: Qwen3 and similar models now respond correctly
  - Fixed empty responses from thinking-mode models
  - Proper content extraction from model responses
  - System prompt instructions to suppress thinking process
- 🔧 **Stop Sequences**: Removed problematic stop sequences that interfered with models
- ⚠️ **Empty Response Handling**: Automatic retry with fallback for reliability

### Improved
- 🎨 **Prompt Quality**: Feature-specific instructions prevent confusion
- 🚀 **Model Performance**: Works seamlessly with granite4, qwen3, llama3, and all Ollama models
- 📈 **User Experience**: No more irrelevant feature mentions in responses
- 🧪 **Testing Coverage**: Complete validation before releases

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
- 📝 **PyPI-Optimized README**: Complete rewrite with practical examples
  - 5 comprehensive usage examples with full code and output
  - Print statements in all examples for better user experience
  - Step-by-step workflows showing complete processes
  - Real-world customer service scenario example
  - Turkish language support demonstration
  - User profile extraction example
- 📄 **Document Configuration Examples**: Added example demonstrating PDF/DOCX/TXT config generation
- 🧪 **Config Update Testing**: Verification that manual YAML edits work correctly

### Changed
- 🗑️ **Removed docs folder**: Consolidated documentation into main README
- 🪵 **Logging Behavior**: Changed from file+console to console-only logging
  - No more `mem_agent.log` files cluttering workspace
  - Keeps workspace clean with only `.db` and `.yaml` files
- 📖 **Example Format**: All examples now include:
  - Print statements for visibility
  - Expected output blocks
  - Full conversation flows
  - Real usage scenarios

### Fixed
- 🐛 **Log File Pollution**: Removed FileHandler from logging, only StreamHandler now
- 📝 **README Examples**: Fixed examples that didn't show actual output or complete process

### Improved
- 🎯 **User Experience**: Much clearer examples for new users
- 📚 **Documentation Quality**: Professional PyPI-ready documentation
- 🔍 **Example Clarity**: Each example shows input, process, and output

### Technical Details
- Modified `mem_llm/mem_agent.py` - removed FileHandler from logging setup
- Rewrote `README.md` with 5 detailed examples
- Created `examples/07_document_config.py` for PDF/DOCX/TXT feature
- Verified config changes work correctly with manual YAML edits

## [1.0.8] - 2025-10-20

### Added
- 🎯 **CLI Tool**: Full-featured command-line interface
  - `mem-llm chat` - Interactive chat sessions
  - `mem-llm check` - System verification
  - `mem-llm stats` - Statistics and analytics
  - `mem-llm export` - Data export (JSON/TXT)
  - `mem-llm clear` - User data deletion
- 📊 **Feature Comparison Matrix**: Clear comparison between JSON and SQL modes
- 📦 **Improved Dependencies**: Proper separation of core, dev, and optional requirements
  - `requirements.txt` - Core dependencies only
  - `requirements-dev.txt` - Development tools
  - `requirements-optional.txt` - Optional features (web, API, etc.)
- 🔧 **Better Error Handling**: Improved startup checks with user-friendly messages
- 📚 **Enhanced Documentation**: CLI usage examples and feature matrices

### Changed
- 🌍 **Multi-language Support**: Changed from "Turkish Support" to general multi-language
- 📖 **Documentation**: All content now in English for broader accessibility
- 🎨 **CLI Entry Point**: Added `mem-llm` console script in setup.py

### Fixed
- 🐛 Missing `click` dependency in requirements
- 🐛 Improved error messages when Ollama is not running

### Improved
- ⚡ Better user experience with CLI commands
- 📝 Clearer README with usage examples
- 🎯 More intuitive API design

## [1.0.4] - 2025-10-13

### Added
- ✨ Config-free knowledge base support - KB now works without config.yaml
- ✨ Smart keyword extraction for knowledge base search (Turkish & English stopwords)
- ✨ Enhanced KB context injection - KB data injected directly into user message
- ✨ Automatic user profile extraction (name, favorite_food, location)
- ✨ Turkish language support for profile extraction
- ✨ SQL-JSON memory compatibility methods
- 📚 New example: `example_knowledge_base.py`
- 🧪 Comprehensive test suite

### Fixed
- 🐛 Knowledge base not being used without config.yaml
- 🐛 LLM ignoring knowledge base information
- 🐛 User profiles returning empty dictionaries
- 🐛 Profile updates not working correctly with SQL memory
- 🐛 Keyword search failing with Turkish queries

### Improved
- ⚡ Better KB-first response priority in system prompts
- ⚡ More accurate answers from knowledge base
- ⚡ Enhanced search algorithm with stopword filtering

## [1.0.3] - 2025-10-12

### Added
- 📦 Initial PyPI release
- 🎯 Core memory features (JSON & SQL)
- 🤖 Ollama integration
- 💾 Knowledge base system
- 🛠️ User tools
- ⚙️ Configuration management

### Features
- Memory-enabled AI agent
- JSON and SQL memory backends
- Knowledge base integration
- User profile management
- Conversation history
- Configuration from YAML/documents

## [1.0.2] - 2025-10-11

### Internal
- 🔧 Package structure improvements
- 📝 Documentation updates

## [1.0.1] - 2025-10-10

### Fixed
- 🐛 Import errors after package rename
- 📦 Package directory naming issues

## [1.0.0] - 2025-10-09

### Initial Release
- 🎉 First stable release
- 🤖 Memory-enabled AI assistant
- 💾 JSON memory management
- 🔌 Ollama integration
