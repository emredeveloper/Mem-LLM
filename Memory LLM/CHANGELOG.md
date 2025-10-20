# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
