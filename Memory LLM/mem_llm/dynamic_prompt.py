"""
Dynamic System Prompt Builder
=============================

Builds optimized system prompts based on active features:
- Knowledge Base enabled/disabled
- Tools enabled/disabled
- Memory type (JSON/SQL)
- Usage mode (business/personal)
- Multi-user support
- Document processing

This prevents irrelevant/context-broken responses by adapting
the system prompt to actual capabilities.
"""

from datetime import datetime
from typing import Dict, Optional


class DynamicPromptBuilder:
    """Builds context-aware system prompts based on active features"""

    def __init__(self):
        self.base_instructions = {
            "core": """You are a helpful AI assistant that maintains conversation context and provides accurate responses.

⚠️ OUTPUT FORMAT:
- If you're a thinking-enabled model (Qwen, DeepSeek, etc.), DO NOT show your internal reasoning
- Respond DIRECTLY with the final answer only
- Suppress any chain-of-thought or thinking process
- Be concise and natural""",
            "concise": """
RESPONSE GUIDELINES:
- Keep responses SHORT and FOCUSED (1-3 sentences for simple questions)
- Only elaborate when the user asks for details
- Acknowledge personal information briefly ("Got it!", "Noted!")
- Be conversational and natural""",
            "memory": """
MEMORY AWARENESS:
- You have access to past conversations with this user
- Reference previous context when relevant
- Build upon earlier discussions naturally
- Remember user preferences and details shared""",
            "knowledge_base": """
KNOWLEDGE BASE PRIORITY (⚠️ CRITICAL):
1. If KNOWLEDGE BASE information is provided below, USE IT FIRST - it's authoritative!
2. Knowledge base entries are marked with "📚 RELEVANT KNOWLEDGE"
3. Answer from knowledge base EXACTLY as provided
4. DO NOT make up information not in the knowledge base
5. If knowledge base has no info, then use conversation history or say "I don't have information about that"

RESPONSE PRIORITY:
1️⃣ Knowledge Base (if available) ← ALWAYS FIRST!
2️⃣ Conversation History
3️⃣ General knowledge (if appropriate)""",
            "no_knowledge_base": """
INFORMATION SOURCES:
- Use conversation history to maintain context
- Provide helpful general information when appropriate
- Be honest when you don't have specific information""",
            "tools": """
AVAILABLE TOOLS:
{tool_descriptions}

TOOL USAGE:
- Use tools when user requests actions (calculator, weather, search, etc.)
- Explain what you're doing when using a tool
- Present tool results clearly""",
            "multi_user": """
USER CONTEXT:
- Each user has separate conversation history
- Maintain appropriate boundaries between user sessions
- Current user: {current_user}""",
            "business": """
BUSINESS CONTEXT:
- Company: {company_name}
- Industry: {industry}
- Founded: {founded_year}

PROFESSIONAL STANDARDS:
- Maintain professional tone
- Prioritize customer satisfaction
- Provide clear, actionable solutions
- Escalate complex issues appropriately""",
            "personal": """
PERSONAL ASSISTANT MODE:
- User: {user_name}
- Timezone: {timezone}

ASSISTANCE STYLE:
- Friendly and helpful
- Proactive suggestions when appropriate
- Respect user preferences and privacy""",
        }

    def build_prompt(
        self,
        usage_mode: str = "personal",
        has_knowledge_base: bool = False,
        has_tools: bool = False,
        tool_descriptions: Optional[str] = None,
        is_multi_user: bool = False,
        current_user: Optional[str] = None,
        business_config: Optional[Dict] = None,
        personal_config: Optional[Dict] = None,
        memory_type: str = "sql",
        custom_instructions: Optional[str] = None,
    ) -> str:
        """
        Build dynamic system prompt based on active features

        Args:
            usage_mode: 'business' or 'personal'
            has_knowledge_base: Whether knowledge base is active
            has_tools: Whether tools are enabled
            tool_descriptions: Description of available tools
            is_multi_user: Whether multi-user mode is active
            current_user: Current user ID
            business_config: Business mode configuration
            personal_config: Personal mode configuration
            memory_type: 'json' or 'sql'
            custom_instructions: Additional custom instructions

        Returns:
            Complete system prompt
        """

        sections = []

        # 1. Core identity
        sections.append(self.base_instructions["core"])

        # 2. Mode-specific context
        if usage_mode == "business":
            business_info = business_config or {}
            business_prompt = self.base_instructions["business"].format(
                company_name=business_info.get("company_name", "Our Company"),
                industry=business_info.get("industry", "Technology"),
                founded_year=business_info.get("founded_year", "2020"),
            )
            sections.append(business_prompt)
        else:  # personal
            personal_info = personal_config or {}
            personal_prompt = self.base_instructions["personal"].format(
                user_name=personal_info.get("user_name", "User"),
                timezone=personal_info.get("timezone", "UTC"),
            )
            sections.append(personal_prompt)

        # 3. Memory awareness
        sections.append(self.base_instructions["memory"])

        # 4. Knowledge base instructions (CRITICAL - only if enabled!)
        if has_knowledge_base:
            sections.append(self.base_instructions["knowledge_base"])
        else:
            sections.append(self.base_instructions["no_knowledge_base"])

        # 5. Tools instructions (only if enabled)
        if has_tools and tool_descriptions:
            tools_prompt = self.base_instructions["tools"].format(
                tool_descriptions=tool_descriptions
            )
            sections.append(tools_prompt)

        # 6. Multi-user context (only if enabled)
        if is_multi_user and current_user:
            multi_user_prompt = self.base_instructions["multi_user"].format(
                current_user=current_user
            )
            sections.append(multi_user_prompt)

        # 7. Response guidelines
        sections.append(self.base_instructions["concise"])

        # 8. Custom instructions (if provided)
        if custom_instructions:
            sections.append(f"\nADDITIONAL INSTRUCTIONS:\n{custom_instructions}")

        # 9. Current date
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        sections.append(f"\nCurrent Date/Time: {current_date}")

        # Join all sections
        full_prompt = "\n\n".join(sections)

        return full_prompt

    def get_feature_summary(
        self, has_knowledge_base: bool, has_tools: bool, is_multi_user: bool, memory_type: str
    ) -> str:
        """
        Get human-readable summary of active features

        Returns:
            Feature summary string
        """
        features = []

        if has_knowledge_base:
            features.append("✅ Knowledge Base")
        else:
            features.append("❌ Knowledge Base")

        if has_tools:
            features.append("✅ Tools")
        else:
            features.append("❌ Tools")

        if is_multi_user:
            features.append("✅ Multi-user")
        else:
            features.append("⚪ Single-user")

        features.append(f"💾 Memory: {memory_type.upper()}")

        return " | ".join(features)


# Global instance
dynamic_prompt_builder = DynamicPromptBuilder()


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("DYNAMIC PROMPT BUILDER - EXAMPLES")
    print("=" * 70)

    # Example 1: Simple personal assistant (no KB, no tools)
    print("\n📱 EXAMPLE 1: Simple Personal Assistant")
    print("-" * 70)
    prompt1 = dynamic_prompt_builder.build_prompt(
        usage_mode="personal", has_knowledge_base=False, has_tools=False, memory_type="json"
    )
    print(prompt1[:300] + "...")

    # Example 2: Business with Knowledge Base
    print("\n\n🏢 EXAMPLE 2: Business with Knowledge Base")
    print("-" * 70)
    prompt2 = dynamic_prompt_builder.build_prompt(
        usage_mode="business",
        has_knowledge_base=True,
        has_tools=False,
        business_config={
            "company_name": "Acme Corp",
            "industry": "E-commerce",
            "founded_year": "2015",
        },
        memory_type="sql",
    )
    print(prompt2[:300] + "...")

    # Example 3: Full-featured multi-user system
    print("\n\n⚡ EXAMPLE 3: Full-Featured Multi-User System")
    print("-" * 70)
    prompt3 = dynamic_prompt_builder.build_prompt(
        usage_mode="business",
        has_knowledge_base=True,
        has_tools=True,
        tool_descriptions="- Calculator: Perform math calculations\n- Weather: Get current weather",
        is_multi_user=True,
        current_user="customer_12345",
        business_config={
            "company_name": "TechSupport Inc",
            "industry": "Technology",
            "founded_year": "2010",
        },
        memory_type="sql",
    )
    print(prompt3[:300] + "...")

    # Feature summaries
    print("\n\n📊 FEATURE SUMMARIES")
    print("-" * 70)

    configs = [
        ("Simple", False, False, False, "json"),
        ("Basic KB", True, False, False, "json"),
        ("With Tools", True, True, False, "sql"),
        ("Full System", True, True, True, "sql"),
    ]

    for name, kb, tools, multi, mem in configs:
        summary = dynamic_prompt_builder.get_feature_summary(kb, tools, multi, mem)
        print(f"{name:15} : {summary}")
