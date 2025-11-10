"""
Advanced Example 1: Function Calling (Tools)
=============================================
Tüm tool özellikleri tek dosyada - ALL tool features in ONE file

✅ Built-in tools (18 araç)
✅ Custom tools (özel araçlar)
✅ Tool chaining (zincirleme)
✅ Memory tools (hafıza araçları)
"""

from mem_llm import MemAgent, tool

print("=" * 60)
print("🛠️  MEM-LLM TOOLS DEMO")
print("=" * 60)

# Agent oluştur (tools enabled)
agent = MemAgent(
    backend='ollama',
    model='llama3.2:3b',
    enable_tools=True,  # ⚠️ ÖNEMLI: Tools'u aktif et
    use_sql=False
)
agent.set_user("tool_user")

# ============================================================================
# 1️⃣ BUILT-IN TOOLS (Hazır Araçlar)
# ============================================================================
print("\n1️⃣  Built-in Tools (Hazır Araçlar)")
print("-" * 60)

# Math tool
print("\n📐 Math:")
response = agent.chat("Calculate: (25 * 4) + 100")
print(f"  {response[:100]}...")

# Text tool
print("\n📝 Text:")
response = agent.chat("Count words in: Hello world from AI")
print(f"  {response[:100]}...")

# File tool (workspace'e kaydeder)
print("\n📁 File:")
response = agent.chat("Create file 'test.txt' with content 'Hello Tools!'")
print(f"  {response[:100]}...")

# Time tool
print("\n⏰ Time:")
response = agent.chat("What's the current time?")
print(f"  {response[:100]}...")

# ============================================================================
# 2️⃣ CUSTOM TOOLS (Özel Araçlar)
# ============================================================================
print("\n\n2️⃣  Custom Tools (Özel Araçlar)")
print("-" * 60)

# Basit custom tool
@tool(name="greet", description="Greet someone by name")
def greet(name: str) -> str:
    return f"Hello, {name}! Nice to meet you!"

# Matematiksel custom tool
@tool(name="power", description="Calculate power of a number")
def power(base: float, exponent: float) -> float:
    return base ** exponent

# Register custom tools
agent.tool_registry.register_tool(greet)
agent.tool_registry.register_tool(power)

print("\n🎨 Custom Tool 1 - Greet:")
response = agent.chat("Use greet tool with name 'Alice'")
print(f"  {response[:100]}...")

print("\n🔢 Custom Tool 2 - Power:")
response = agent.chat("Calculate 2 to the power of 8")
print(f"  {response[:100]}...")

# ============================================================================
# 3️⃣ TOOL CHAINING (Zincirleme Kullanım)
# ============================================================================
print("\n\n3️⃣  Tool Chaining (Zincirleme)")
print("-" * 60)

response = agent.chat("""
Calculate 10 * 5, then write the result to a file named 'result.txt'
""")
print(f"  {response[:150]}...")

# ============================================================================
# 4️⃣ MEMORY TOOLS (Hafıza Araçları)
# ============================================================================
print("\n\n4️⃣  Memory Tools (Hafıza Araçları)")
print("-" * 60)

# Önce bilgi ekle
agent.chat("My favorite color is blue and I love pizza")

# Hafızayı ara
print("\n🔍 Search Memory:")
response = agent.chat("Search my memory for 'favorite'")
print(f"  {response[:100]}...")

# Kullanıcı bilgisi
print("\n👤 User Info:")
response = agent.chat("Get my user information")
print(f"  {response[:100]}...")

# ============================================================================
# 5️⃣ WORKSPACE TOOLS (Dosya Yönetimi)
# ============================================================================
print("\n\n5️⃣  Workspace Tools (Dosya Yönetimi)")
print("-" * 60)

# List workspace files
print("\n📂 List Files:")
response = agent.chat("List all files in workspace")
print(f"  {response[:100]}...")

# Workspace stats
print("\n📊 Workspace Stats:")
response = agent.chat("Show workspace statistics")
print(f"  {response[:100]}...")

# ============================================================================
# 6️⃣ TOOL REGISTRY (Tüm Araçları Listele)
# ============================================================================
print("\n\n6️⃣  Available Tools")
print("-" * 60)

tools = agent.tool_registry.list_tools()
print(f"\n📦 Total: {len(tools)} tools\n")

# Kategorilere göre grupla
categories = {}
for t in tools:
    if t.category not in categories:
        categories[t.category] = []
    categories[t.category].append(t.name)

for category, tool_names in sorted(categories.items()):
    print(f"  {category.upper()}: {', '.join(tool_names[:3])}...")

print("\n" + "=" * 60)
print("✅ Tools Demo Complete!")
print("=" * 60)

