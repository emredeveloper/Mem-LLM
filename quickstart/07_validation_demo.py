"""
Mem-LLM v2.1.0 - Input Validation Demo
Demonstrates comprehensive input validation for tools
"""

from mem_llm import MemAgent, tool

print("=" * 60)
print("Mem-LLM v2.1.0 - Input Validation Demo")
print("=" * 60)

# Create agent with tools enabled
# Option 1: Ollama
agent = MemAgent(
    backend='ollama',
    model='granite4:3b',
    enable_tools=True,
    use_sql=False
)

# Option 2: LM Studio
# agent = MemAgent(
#     backend='lmstudio',
#     model='local-model',
#     enable_tools=True,
#     use_sql=False
# )

# Option 3: Auto-detect
# agent = MemAgent(
#     auto_detect_backend=True,
#     enable_tools=True,
#     use_sql=False
# )

agent.set_user("validation_demo_user")

print("\n1️⃣  Pattern Validation (Email)")
print("-" * 60)

@tool(
    name="send_email",
    description="Sends email to a valid email address",
    pattern={"email": r'^[\w\.-]+@[\w\.-]+\.\w+$'}
)
def send_email(email: str) -> str:
    return f"Email sent to: {email}"

agent.tool_registry.register_tool(send_email)

# Valid email
response = agent.chat("Use send_email to send to user@example.com")
print(f"Valid: {response}\n")

# Invalid email (will fail validation)
print("Testing invalid email...")
response = agent.chat("Use send_email to send to invalid-email")
print(f"Invalid: {response}\n")

print("\n2️⃣  Range Validation (Numbers)")
print("-" * 60)

@tool(
    name="set_volume",
    description="Sets volume between 0 and 100",
    min_value={"volume": 0},
    max_value={"volume": 100}
)
def set_volume(volume: int) -> str:
    return f"Volume set to: {volume}"

agent.tool_registry.register_tool(set_volume)

# Valid volume
response = agent.chat("Use set_volume to set volume to 75")
print(f"Valid: {response}\n")

# Invalid volume (will fail validation)
print("Testing invalid volume...")
response = agent.chat("Use set_volume to set volume to 150")
print(f"Invalid: {response}\n")

print("\n3️⃣  Length Validation (Strings)")
print("-" * 60)

@tool(
    name="create_username",
    description="Creates username with 3-20 characters",
    min_length={"username": 3},
    max_length={"username": 20}
)
def create_username(username: str) -> str:
    return f"Username created: {username}"

agent.tool_registry.register_tool(create_username)

# Valid username
response = agent.chat("Use create_username to create username 'alice123'")
print(f"Valid: {response}\n")

# Too short (will fail validation)
print("Testing too short username...")
response = agent.chat("Use create_username to create username 'ab'")
print(f"Invalid: {response}\n")

print("\n4️⃣  Choice Validation (Enum-like)")
print("-" * 60)

@tool(
    name="set_language",
    description="Sets language preference",
    choices={"language": ["en", "tr", "de", "fr", "es"]}
)
def set_language(language: str) -> str:
    return f"Language set to: {language}"

agent.tool_registry.register_tool(set_language)

# Valid language
response = agent.chat("Use set_language to set language to 'tr'")
print(f"Valid: {response}\n")

# Invalid language (will fail validation)
print("Testing invalid language...")
response = agent.chat("Use set_language to set language to 'xyz'")
print(f"Invalid: {response}\n")

print("\n5️⃣  Custom Validator")
print("-" * 60)

def is_even(value: int) -> bool:
    """Custom validator: checks if number is even"""
    return value % 2 == 0

@tool(
    name="process_even",
    description="Processes even numbers only",
    validators={"number": is_even}
)
def process_even(number: int) -> str:
    return f"Processing even number: {number}"

agent.tool_registry.register_tool(process_even)

# Valid (even number)
response = agent.chat("Use process_even to process number 42")
print(f"Valid: {response}\n")

# Invalid (odd number)
print("Testing odd number...")
response = agent.chat("Use process_even to process number 43")
print(f"Invalid: {response}\n")

print("\n6️⃣  Combined Validation")
print("-" * 60)

def is_strong_password(password: str) -> bool:
    """Custom validator: checks password strength"""
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_upper and has_lower and has_digit

@tool(
    name="create_account",
    description="Creates account with strong password",
    pattern={"email": r'^[\w\.-]+@[\w\.-]+\.\w+$'},
    min_length={"password": 8},
    max_length={"password": 50},
    validators={"password": is_strong_password}
)
def create_account(email: str, password: str) -> str:
    return f"Account created for {email}"

agent.tool_registry.register_tool(create_account)

# Valid account
response = agent.chat("""
Use create_account with email 'user@example.com' and password 'SecurePass123'
""")
print(f"Valid: {response}\n")

# Weak password (will fail validation)
print("Testing weak password...")
response = agent.chat("""
Use create_account with email 'user@example.com' and password 'weak'
""")
print(f"Invalid: {response}\n")

print("\n7️⃣  Multiple Parameters with Different Validations")
print("-" * 60)

@tool(
    name="book_flight",
    description="Books a flight with validation",
    pattern={"passenger_email": r'^[\w\.-]+@[\w\.-]+\.\w+$'},
    min_value={"passengers": 1, "age": 0},
    max_value={"passengers": 9, "age": 120},
    choices={"flight_class": ["economy", "business", "first"]}
)
def book_flight(
    passenger_email: str,
    passengers: int,
    age: int,
    flight_class: str
) -> str:
    return f"Flight booked: {passengers} passenger(s), {flight_class} class"

agent.tool_registry.register_tool(book_flight)

# Valid booking
response = agent.chat("""
Use book_flight with:
- passenger_email: user@example.com
- passengers: 2
- age: 30
- flight_class: business
""")
print(f"Valid: {response}\n")

print("\n✅ Validation Demo Completed!")
print("=" * 60)
print("\n📊 Validation Types Demonstrated:")
print("  1. Pattern validation (regex)")
print("  2. Range validation (min/max for numbers)")
print("  3. Length validation (min/max for strings)")
print("  4. Choice validation (enum-like)")
print("  5. Custom validators (any Python function)")
print("  6. Combined validation (multiple rules)")
print("  7. Multi-parameter validation")
print("\n💡 Benefits:")
print("  - Pre-validation prevents runtime errors")
print("  - Clear error messages for invalid input")
print("  - Safer tool execution")
print("  - Better user experience")

