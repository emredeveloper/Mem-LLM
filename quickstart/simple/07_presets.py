"""
Quickstart: Config Presets (v2.1.4)
====================================
Initialize specialized agents with one line of code.
"""

from mem_llm import MemAgent

print("📋 Config Presets Demo\n")

# 1. Code Assistant (optimized for programming)
print("👨‍💻 Code Assistant:")
coder = MemAgent(preset="code_assistant", backend="ollama", model_name="granite4:3b")
print(f"   Temperature: {coder.preset_config.get('temperature')}")
print(f"   Max tokens: {coder.preset_config.get('max_tokens')}")
print("   Purpose: Programming expert")
print("   → Question: How do I read a CSV file in Python?")
code_response = coder.chat(
    "How do I read a CSV file in Python? Just show import.", user_id="dev_user"
)
print(f"   ✓ Response: {code_response[:100]}...\n")

# 2. Creative Writer (optimized for storytelling)
print("✍️  Creative Writer:")
writer = MemAgent(preset="creative_writer", backend="ollama", model_name="granite4:3b")
print(f"   Temperature: {writer.preset_config.get('temperature')}")
print(f"   Max tokens: {writer.preset_config.get('max_tokens')}")
print("   Purpose: Storytelling")
print("   → Prompt: Write the opening of a sci-fi story")
story_response = writer.chat(
    "Write one sentence opening for a sci-fi story about AI", user_id="writer_user"
)
print(f"   ✓ Response: {story_response[:100]}...\n")

# 3. Tutor (optimized for teaching)
print("👨‍🏫 Tutor:")
tutor = MemAgent(preset="tutor", backend="ollama", model_name="granite4:3b")
print(f"   Temperature: {tutor.preset_config.get('temperature')}")
print(f"   Max tokens: {tutor.preset_config.get('max_tokens')}")
print("   Purpose: Educational")
print("   → Question: Explain what a variable is in programming")
tutor_response = tutor.chat(
    "Explain what a variable is in programming in one sentence", user_id="student_user"
)
print(f"   ✓ Response: {tutor_response[:100]}...\n")

# Available presets:
print("📚 All available presets:")
presets = [
    "chatbot",
    "code_assistant",
    "creative_writer",
    "tutor",
    "analyst",
    "translator",
    "summarizer",
    "researcher",
]
for preset in presets:
    print(f"   - {preset}")

print("\n✅ Presets demo complete!")
