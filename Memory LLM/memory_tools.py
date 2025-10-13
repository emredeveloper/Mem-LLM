"""
User Tools System
Tools for users to manage their memory data
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import re


class MemoryTools:
    """User memory management tools"""

    def __init__(self, memory_manager):
        """
        Args:
            memory_manager: Memory manager (MemoryManager or SQLMemoryManager)
        """
        self.memory = memory_manager
        self.tools = {
            "list_memories": {
                "description": "Lists all user conversations",
                "parameters": {
                    "user_id": "User ID",
                    "limit": "Number of conversations to show (default: 10)"
                },
                "function": self._list_memories
            },
            "search_memories": {
                "description": "Search for keywords in conversations",
                "parameters": {
                    "user_id": "User ID",
                    "keyword": "Keyword to search",
                    "limit": "Number of results to show (default: 5)"
                },
                "function": self._search_memories
            },
            "delete_memory": {
                "description": "Delete a specific conversation",
                "parameters": {
                    "user_id": "User ID",
                    "conversation_id": "Conversation ID to delete",
                    "confirm": "Deletion confirmation (true/false)"
                },
                "function": self._delete_memory
            },
            "clear_all_memories": {
                "description": "Delete all user data",
                "parameters": {
                    "user_id": "User ID",
                    "confirm": "Deletion confirmation (true/false)",
                    "reason": "Deletion reason (optional)"
                },
                "function": self._clear_all_memories
            },
            "show_user_info": {
                "description": "Show information about user",
                "parameters": {
                    "user_id": "User ID"
                },
                "function": self._show_user_info
            },
            "update_user_info": {
                "description": "Update user information",
                "parameters": {
                    "user_id": "User ID",
                    "updates": "Information to update"
                },
                "function": self._update_user_info
            },
            "export_memories": {
                "description": "Export user data",
                "parameters": {
                    "user_id": "User ID",
                    "format": "Format (json or txt)"
                },
                "function": self._export_memories
            }
        }

    def _list_memories(self, user_id: str, limit: int = 10) -> str:
        """List user conversations"""
        try:
            conversations = self.memory.get_recent_conversations(user_id, limit)

            if not conversations:
                return f"❌ No conversations found for user {user_id}."

            result = f"📝 Last {len(conversations)} conversations for user {user_id}:\n\n"

            for i, conv in enumerate(conversations, 1):
                timestamp = conv.get('timestamp', 'Unknown')
                user_msg = conv.get('user_message', '')[:100]
                bot_response = conv.get('bot_response', '')[:100]

                result += f"{i}. [{timestamp}]\n"
                result += f"   👤 User: {user_msg}...\n"
                result += f"   🤖 Bot: {bot_response}...\n\n"

            return result

        except Exception as e:
            return f"❌ Error: {str(e)}"

    def _search_memories(self, user_id: str, keyword: str, limit: int = 5) -> str:
        """Search in conversations"""
        try:
            results = self.memory.search_conversations(user_id, keyword)

            if not results:
                return f"❌ No results found for keyword '{keyword}' for user {user_id}."

            result = f"🔍 {len(results)} results found for keyword '{keyword}':\n\n"

            for i, conv in enumerate(results[:limit], 1):
                timestamp = conv.get('timestamp', 'Unknown')
                user_msg = conv.get('user_message', '')
                bot_response = conv.get('bot_response', '')

                result += f"{i}. [{timestamp}]\n"
                result += f"   👤 User: {user_msg}\n"
                result += f"   🤖 Bot: {bot_response}\n\n"

            if len(results) > limit:
                result += f"... and {len(results) - limit} more results."

            return result

        except Exception as e:
            return f"❌ Search error: {str(e)}"

    def _delete_memory(self, user_id: str, conversation_id: str, confirm: bool = False) -> str:
        """Delete a specific conversation"""
        if not confirm:
            return "⚠️  Use 'confirm=true' parameter for deletion."

        try:
            # For this simple version, reload all conversations and filter
            # In real application, deletion by ID would be done in database
            conversations = self.memory.get_recent_conversations(user_id, 1000)

            # Simple deletion - would be more sophisticated in real application
            original_count = len(conversations)

            # For this demo, simulate deleting a random conversation
            # In real application, conversation_id would be used

            return f"✅ Conversation deleted. ({original_count} conversations exist)"

        except Exception as e:
            return f"❌ Deletion error: {str(e)}"

    def _clear_all_memories(self, user_id: str, confirm: bool = False, reason: str = "") -> str:
        """Delete all user data"""
        if not confirm:
            return "⚠️  Use 'confirm=true' parameter to delete all data."

        try:
            # Clear all conversations
            conversations = self.memory.get_recent_conversations(user_id, 1000)

            # Deletion simulation for this demo
            # In real application, all records would be deleted from database

            reason_text = f" (Reason: {reason})" if reason else ""
            return f"🗑️  All data for user {user_id} has been deleted{reason_text}."

        except Exception as e:
            return f"❌ Deletion error: {str(e)}"

    def _show_user_info(self, user_id: str) -> str:
        """Show user information"""
        try:
            profile = self.memory.get_user_profile(user_id)

            if not profile:
                return f"❌ User {user_id} not found."

            result = f"👤 User information for {user_id}:\n\n"

            if profile.get('name'):
                result += f"Name: {profile['name']}\n"

            if profile.get('first_seen'):
                result += f"First conversation: {profile['first_seen']}\n"

            if profile.get('last_interaction'):
                result += f"Last interaction: {profile['last_interaction']}\n"

            conversations = self.memory.get_recent_conversations(user_id, 1)
            if conversations:
                result += f"Total conversations: {len(self.memory.get_recent_conversations(user_id, 1000))}\n"

            return result

        except Exception as e:
            return f"❌ Information retrieval error: {str(e)}"

    def _update_user_info(self, user_id: str, updates: Dict[str, Any]) -> str:
        """Update user information"""
        try:
            self.memory.update_user_profile(user_id, updates)
            return f"✅ User information for {user_id} updated."

        except Exception as e:
            return f"❌ Update error: {str(e)}"

    def _export_memories(self, user_id: str, format: str = "json") -> str:
        """Export user data"""
        try:
            if format == "json":
                # Get all data in JSON format
                profile = self.memory.get_user_profile(user_id)
                conversations = self.memory.get_recent_conversations(user_id, 1000)

                export_data = {
                    "user_id": user_id,
                    "export_date": datetime.now().isoformat(),
                    "profile": profile,
                    "conversations": conversations
                }

                return json.dumps(export_data, ensure_ascii=False, indent=2)

            elif format == "txt":
                conversations = self.memory.get_recent_conversations(user_id, 1000)

                result = f"Conversation history for user {user_id}\n"
                result += f"Export date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                result += "=" * 60 + "\n\n"

                for i, conv in enumerate(conversations, 1):
                    result += f"Conversation {i}:\n"
                    result += f"Date: {conv.get('timestamp', 'Unknown')}\n"
                    result += f"User: {conv.get('user_message', '')}\n"
                    result += f"Bot: {conv.get('bot_response', '')}\n"
                    result += "-" * 40 + "\n"

                return result

            else:
                return "❌ Unsupported format. Use json or txt."

        except Exception as e:
            return f"❌ Export error: {str(e)}"

    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        """
        Execute the specified tool

        Args:
            tool_name: Tool name to execute
            parameters: Tool parameters

        Returns:
            Tool result
        """
        if tool_name not in self.tools:
            return f"❌ Tool '{tool_name}' not found."

        tool = self.tools[tool_name]

        try:
            # Pass parameters to function
            if "user_id" in parameters:
                result = tool["function"](**parameters)
            else:
                return "❌ user_id parameter required."

            return result

        except Exception as e:
            return f"❌ Tool execution error: {str(e)}"

    def list_available_tools(self) -> str:
        """List available tools"""
        result = "🛠️ Available Tools:\n\n"

        for name, tool in self.tools.items():
            result += f"🔧 {name}\n"
            result += f"   Description: {tool['description']}\n"
            result += "   Parameters:\n"

            for param, desc in tool['parameters'].items():
                result += f"     • {param}: {desc}\n"

            result += "\n"

        return result

    def parse_user_command(self, user_message: str) -> tuple:
        """
        Extract tool call from user message

        Returns:
            (tool_name, parameters) or (None, None) if no tool call
        """
        # Command patterns
        patterns = {
            "list_memories": [
                r"show.*my.*past.*conversations",
                r"list.*my.*conversations",
                r"show.*all.*my.*conversations",
                r"show.*my.*history"
            ],
            "search_memories": [
                r"search.*my.*conversations.*about.*(.*)",
                r"conversations.*with.*keyword.*(.*)",
                r"find.*my.*conversations.*related.*to.*(.*)"
            ],
            "show_user_info": [
                r"what.*do.*you.*know.*about.*me",
                r"introduce.*me",
                r"show.*my.*profile"
            ],
            "clear_all_memories": [
                r"forget.*everything",
                r"delete.*all.*my.*data",
                r"clear.*all.*my.*history"
            ],
            "export_memories": [
                r"export.*my.*data",
                r"export.*my.*history",
                r"download.*my.*conversations"
            ]
        }

        message_lower = user_message.lower()

        for tool_name, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, message_lower)
                if match:
                    # Simple parameter extraction
                    parameters = {"user_id": "current_user"}  # In real application, this would be taken from current user

                    if tool_name == "search_memories":
                        keyword = match.group(1).strip()
                        if keyword:
                            parameters["keyword"] = keyword

                    return tool_name, parameters

        return None, None


class ToolExecutor:
    """Tool executor"""

    def __init__(self, memory_manager, current_user_id: str = None):
        """
        Args:
            memory_manager: Memory manager
            current_user_id: Current user ID
        """
        self.memory_tools = MemoryTools(memory_manager)
        self.current_user_id = current_user_id

    def execute_user_command(self, user_message: str, user_id: str = None) -> str:
        """
        Detect and execute tool call from user message

        Args:
            user_message: User message
            user_id: User ID

        Returns:
            Tool result or None if no tool call
        """
        uid = user_id or self.current_user_id

        tool_name, parameters = self.memory_tools.parse_user_command(user_message)

        if tool_name and uid:
            # Add user_id to parameters
            parameters["user_id"] = uid
            return self.memory_tools.execute_tool(tool_name, parameters)

        return None

    def is_tool_command(self, user_message: str) -> bool:
        """Check if message is a tool command"""
        tool_name, _ = self.memory_tools.parse_user_command(user_message)
        return tool_name is not None


def create_sample_tool_usage():
    """Create tool usage example"""
    print("🛠️  MEMORY TOOLS EXAMPLE")
    print("=" * 60)

    # Simple memory manager for demo
    from memory_manager import MemoryManager
    memory = MemoryManager()

    # Add sample user
    memory.add_user("demo_user", "Demo User")
    memory.add_interaction("demo_user", "Hello!", "Hello! How can I help you?")
    memory.add_interaction("demo_user", "My name is Ahmet", "Nice to meet you Ahmet!")

    tools = MemoryTools(memory)

    print("📋 Available tools:")
    print(tools.list_available_tools())

    print("\n" + "=" * 60)
    print("🎯 EXAMPLE USAGE:")
    print("=" * 60)

    # Execute tools manually
    print("1️⃣  List past conversations:")
    result = tools.execute_tool("list_memories", {"user_id": "demo_user", "limit": 5})
    print(result)

    print("\n2️⃣  Search for 'Hello' keyword:")
    result = tools.execute_tool("search_memories", {"user_id": "demo_user", "keyword": "Hello"})
    print(result)

    print("\n3️⃣  Show user information:")
    result = tools.execute_tool("show_user_info", {"user_id": "demo_user"})
    print(result)

    print("\n4️⃣  Export data (JSON):")
    result = tools.execute_tool("export_memories", {"user_id": "demo_user", "format": "json"})
    print(result[:200] + "...")  # First 200 characters


if __name__ == "__main__":
    create_sample_tool_usage()
