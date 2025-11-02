"""
Example 7: Document-Based Configuration
=======================================

Generate config.yaml from PDF/DOCX/TXT documents.

Quick Usage:
    from mem_llm import create_config_from_document
    create_config_from_document('company.pdf', 'config.yaml', 'Company Name')
"""

from mem_llm import create_config_from_document, MemAgent
import os

print("=" * 60)
print("Document-Based Configuration")
print("=" * 60)

# Create sample company info
company_info = """
Acme Corporation
Founded: 2010

About: Leading provider of innovative software solutions.
Services: Cloud Infrastructure, AI/ML, Custom Development
Support: support@acme.com, 1-800-ACME-HELP

Support Hours: Mon-Fri 9 AM - 6 PM EST
Return Policy: 14-day money-back guarantee
Shipping: Free on orders over $100
"""

# Save to file
doc_path = "sample_company_info.txt"
with open(doc_path, 'w', encoding='utf-8') as f:
    f.write(company_info)

print(f"\n✅ Created: {doc_path}")

# Generate config
print("\n📝 Generating config.yaml...")
result = create_config_from_document(
    doc_path=doc_path,
    output_path="generated_config.yaml",
    company_name="Acme Corporation"
)
print(result)

# Use generated config
if os.path.exists("generated_config.yaml"):
    print("\n🤖 Testing with generated config...")
    agent = MemAgent(config_file="generated_config.yaml", check_connection=False)
    agent.set_user("customer_001")
    
    response = agent.chat("What are your support hours?")
    print(f"Bot: {response}\n")

# Cleanup
os.remove(doc_path)
print("✅ Complete! Review 'generated_config.yaml'")
