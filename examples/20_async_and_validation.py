"""
Example 20: Async Tools & Validation (v2.1.0)
=============================================

Demonstrates new v2.1.0 features:
- Async tool support for I/O operations
- Input validation (regex, min/max, choices)
- Custom validators

Key Features:
- Non-blocking I/O with async tools
- Automatic input validation
- Better error handling
"""

import sys
from pathlib import Path

# Add parent directory to path for local testing
sys.path.insert(0, str(Path(__file__).parent.parent / "Memory LLM"))

from mem_llm import MemAgent, tool
import re

print("=" * 70)
print("🚀 Async Tools & Validation Demo (v2.1.0)")
print("=" * 70)
print()

# ============================================================================
# DEMO 1: Validation Examples
# ============================================================================

print("=" * 70)
print("DEMO 1: Tool Input Validation")
print("=" * 70)
print()

# Email validation
@tool(
    name="send_email",
    description="Send email with validation",
    pattern={"email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'},
    min_length={"email": 5, "subject": 1},
    max_length={"email": 254, "subject": 100}
)
def send_email(email: str, subject: str) -> str:
    """Send an email (validated)"""
    return f"✉️ Email sent to {email} with subject: {subject}"

# Age validation
@tool(
    name="set_age",
    description="Set user age",
    min_value={"age": 0},
    max_value={"age": 150}
)
def set_age(age: int) -> str:
    """Set age with range validation"""
    return f"✅ Age set to {age}"

# Choice validation
@tool(
    name="set_language",
    description="Set programming language",
    choices={"language": ["python", "javascript", "java", "go", "rust"]}
)
def set_language(language: str) -> str:
    """Set language from predefined choices"""
    return f"🔧 Language set to {language}"

# Custom validator
def is_even(x: int) -> bool:
    return x % 2 == 0

@tool(
    name="process_even",
    description="Process even numbers only",
    validators={"number": is_even}
)
def process_even(number: int) -> str:
    """Process only even numbers"""
    return f"✅ Processed even number: {number}"

print("📊 Test 1: Email Validation")
try:
    agent = MemAgent(enable_tools=True, tools=[send_email])
    agent.set_user("test_validation")
    
    # Valid email
    print("✅ Valid: send_email('user@example.com', 'Hello')")
    result = send_email('user@example.com', 'Hello')
    print(f"   Result: {result}")
    
    # Invalid email
    print("\n❌ Invalid: send_email('invalid-email', 'Test')")
    try:
        result = send_email('invalid-email', 'Test')
        print(f"   Result: {result}")
    except ValueError as e:
        print(f"   ✅ Caught validation error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n📊 Test 2: Range Validation")
try:
    # Valid age
    print("✅ Valid: set_age(25)")
    result = set_age(25)
    print(f"   Result: {result}")
    
    # Invalid age
    print("\n❌ Invalid: set_age(200)")
    try:
        result = set_age(200)
        print(f"   Result: {result}")
    except ValueError as e:
        print(f"   ✅ Caught validation error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n📊 Test 3: Choice Validation")
try:
    # Valid choice
    print("✅ Valid: set_language('python')")
    result = set_language('python')
    print(f"   Result: {result}")
    
    # Invalid choice
    print("\n❌ Invalid: set_language('cobol')")
    try:
        result = set_language('cobol')
        print(f"   Result: {result}")
    except ValueError as e:
        print(f"   ✅ Caught validation error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n📊 Test 4: Custom Validator")
try:
    # Valid even number
    print("✅ Valid: process_even(10)")
    result = process_even(10)
    print(f"   Result: {result}")
    
    # Invalid odd number
    print("\n❌ Invalid: process_even(7)")
    try:
        result = process_even(7)
        print(f"   Result: {result}")
    except ValueError as e:
        print(f"   ✅ Caught validation error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

# ============================================================================
# DEMO 2: Async Tools
# ============================================================================

print("\n" + "=" * 70)
print("DEMO 2: Async Tool Support")
print("=" * 70)
print()

import asyncio

@tool(name="async_wait", description="Wait asynchronously")
async def async_wait(seconds: float) -> str:
    """Async wait demonstration"""
    print(f"⏳ Starting {seconds}s wait...")
    await asyncio.sleep(seconds)
    return f"✅ Waited {seconds} seconds"

@tool(name="async_multiply", description="Async multiplication")
async def async_multiply(a: int, b: int) -> int:
    """Async math operation"""
    await asyncio.sleep(0.1)  # Simulate I/O
    return a * b

print("📊 Test 1: Single Async Tool")
try:
    result = asyncio.run(async_wait(1.0))
    print(f"Result: {result}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n📊 Test 2: Multiple Async Tools")
try:
    async def run_multiple():
        tasks = [
            async_multiply(3, 4),
            async_multiply(5, 6),
            async_multiply(7, 8)
        ]
        results = await asyncio.gather(*tasks)
        return results
    
    results = asyncio.run(run_multiple())
    print(f"✅ Results: {results}")
except Exception as e:
    print(f"❌ Error: {e}")

# ============================================================================
# Summary
# ============================================================================

print("\n" + "=" * 70)
print("✅ ASYNC & VALIDATION DEMO COMPLETED!")
print("=" * 70)
print()
print("🎯 New Features in v2.1.0:")
print("  ✅ Async tool support (I/O-bound operations)")
print("  ✅ Pattern validation (regex for strings)")
print("  ✅ Range validation (min/max for numbers)")
print("  ✅ Length validation (min/max for strings)")
print("  ✅ Choice validation (enum-like behavior)")
print("  ✅ Custom validators (your own logic)")
print()
print("💡 Benefits:")
print("  - Better input validation prevents errors")
print("  - Async tools improve performance")
print("  - Safer tool execution")
print("  - More professional APIs")
print()

