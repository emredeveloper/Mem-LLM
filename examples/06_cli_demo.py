"""
Example 6: CLI Commands
=======================
Shows available command-line interface commands.

Note: These commands work after installation:
    pip install mem-llm

Then you can run them directly in terminal!
"""

def print_cli_examples():
    """Display CLI command examples"""
    
    print("=" * 60)
    print("🖥️  Mem-LLM CLI Commands")
    print("=" * 60)
    print()
    print("After installing mem-llm, you can use these commands:\n")
    
    print("1️⃣  Interactive Chat:")
    print("   mem-llm chat --user alice")
    print("   mem-llm chat --user john --sql\n")
    
    print("2️⃣  Check System Status:")
    print("   mem-llm check")
    print("   mem-llm check --model llama3.2:3b\n")
    
    print("3️⃣  View Statistics:")
    print("   mem-llm stats")
    print("   mem-llm stats --user alice\n")
    
    print("4️⃣  Export User Data:")
    print("   mem-llm export alice")
    print("   mem-llm export alice --format json")
    print("   mem-llm export alice --output data.json\n")
    
    print("5️⃣  Clear User Data:")
    print("   mem-llm clear alice\n")
    
    print("6️⃣  Get Help:")
    print("   mem-llm --help")
    print("   mem-llm chat --help\n")
    
    print("=" * 60)
    print("Try them out after installing: pip install mem-llm")
    print("=" * 60)

if __name__ == "__main__":
    print_cli_examples()
