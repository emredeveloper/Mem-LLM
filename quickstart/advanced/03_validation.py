"""
Advanced Example 3: Input Validation
=====================================
Input validation - min/max, pattern, choices
"""

from mem_llm import MemAgent, tool

agent = MemAgent(
    backend='ollama',
    model='llama3.2:3b',
    enable_tools=True,
    use_sql=False
)
agent.set_user("validation_user")

# ============================================================================
# Validation Examples
# ============================================================================

# 1️⃣  Min/Max Length
@tool(
    name="validate_username",
    description="Validate username (3-20 chars)",
    min_length={"username": 3},
    max_length={"username": 20}
)
def validate_username(username: str) -> str:
    return f"✅ Username '{username}' is valid!"

# 2️⃣  Min/Max Value
@tool(
    name="validate_age",
    description="Validate age (18-120)",
    min_value={"age": 18},
    max_value={"age": 120}
)
def validate_age(age: int) -> str:
    return f"✅ Age {age} is valid!"

# 3️⃣  Choices (enum)
@tool(
    name="select_plan",
    description="Select subscription plan",
    choices={"plan": ["free", "pro", "enterprise"]}
)
def select_plan(plan: str) -> str:
    return f"✅ Selected plan: {plan}"

# 4️⃣  Regex Pattern
@tool(
    name="validate_email",
    description="Validate email address",
    pattern={"email": r"^[\w\.-]+@[\w\.-]+\.\w+$"}
)
def validate_email(email: str) -> str:
    return f"✅ Email '{email}' is valid!"

# Register all
for func in [validate_username, validate_age, select_plan, validate_email]:
    agent.tool_registry.register_tool(func)

# ============================================================================
# Test Validations
# ============================================================================
print("🔒 Validation Tests:")
print("-" * 50)

# Valid inputs
print("\n✅ Valid inputs:")
tests = [
    ("validate_username", {"username": "john_doe"}),
    ("validate_age", {"age": 25}),
    ("select_plan", {"plan": "pro"}),
    ("validate_email", {"email": "test@example.com"})
]

for tool_name, params in tests:
    result = agent.tool_registry.execute(tool_name, **params)
    print(f"  {tool_name}{params}: {result.result if result.status.value == 'success' else 'FAIL'}")

print("\n❌ Invalid inputs (will be rejected):")
invalid_tests = [
    ("validate_username", {"username": "ab"}),           # Too short
    ("validate_age", {"age": 15}),                       # Too young  
    ("select_plan", {"plan": "ultimate"}),               # Not in choices
    ("validate_email", {"email": "not-an-email"})        # Invalid pattern
]

for tool_name, params in invalid_tests:
    result = agent.tool_registry.execute(tool_name, **params)
    print(f"  {tool_name}{params}: {result.error[:50]}...")

print("\n✅ Validation demo complete!")
