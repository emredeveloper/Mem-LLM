"""
Example 7: Document-Based Configuration
========================================
Shows how to create config.yaml from PDF/DOCX/TXT documents.
This is useful for quickly setting up the bot with company information.
"""

from mem_llm import create_config_from_document, MemAgent
import os

def test_with_text_file():
    """Test with a simple text file"""
    
    print("=" * 60)
    print("📄 Document-Based Configuration Example")
    print("=" * 60)
    print()
    
    # Create a sample company info text file
    company_info = """
    Acme Corporation
    Founded: 2010
    Industry: Technology and Software Solutions
    
    About Us:
    Acme Corporation is a leading provider of innovative software solutions.
    We specialize in AI, cloud computing, and enterprise applications.
    
    Our Services:
    - Cloud Infrastructure
    - AI/ML Solutions
    - Custom Software Development
    - 24/7 Technical Support
    
    Contact:
    Email: support@acme.com
    Phone: 1-800-ACME-HELP
    
    Support Hours:
    Monday-Friday: 9 AM - 6 PM EST
    Saturday: 10 AM - 4 PM EST
    Sunday: Closed
    
    Return Policy:
    14-day money-back guarantee
    Products must be in original packaging
    
    Shipping:
    Free shipping on orders over $100
    Standard shipping: 3-5 business days
    Express shipping: 1-2 business days
    """
    
    # Save to file
    doc_path = "sample_company_info.txt"
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(company_info)
    
    print(f"✅ Created sample document: {doc_path}\n")
    
    # Generate config from document
    print("📝 Generating config.yaml from document...")
    result = create_config_from_document(
        doc_path=doc_path,
        output_path="generated_config.yaml",
        company_name="Acme Corporation"
    )
    print(f"{result}\n")
    
    # Now use the generated config
    print("=" * 60)
    print("🤖 Testing Agent with Generated Config")
    print("=" * 60)
    
    if os.path.exists("generated_config.yaml"):
        agent = MemAgent(config_file="generated_config.yaml")
        
        # Check setup
        status = agent.check_setup()
        if status['status'] != 'ready':
            print("❌ Please start Ollama: ollama serve")
            return
        
        print("✅ Agent initialized with document-based config\n")
        
        # Test conversation
        agent.set_user("customer_001", name="John")
        
        print("👤 Customer: What are your support hours?")
        response = agent.chat("What are your support hours?")
        print(f"🤖 Bot: {response}\n")
        
        print("👤 Customer: What's your return policy?")
        response = agent.chat("What's your return policy?")
        print(f"🤖 Bot: {response}\n")
        
        print("=" * 60)
        print("✅ Config-based agent working!")
        print("=" * 60)
    
    # Cleanup
    print("\n🧹 Cleanup...")
    if os.path.exists(doc_path):
        os.remove(doc_path)
        print(f"   Deleted: {doc_path}")
    if os.path.exists("generated_config.yaml"):
        print(f"   Kept: generated_config.yaml (you can review it)")


def show_pdf_docx_usage():
    """Show how to use with PDF and DOCX files"""
    
    print("\n" + "=" * 60)
    print("📚 Using with PDF and DOCX Files")
    print("=" * 60)
    print()
    
    print("To use with PDF files:")
    print("   1. Install PyPDF2:")
    print("      pip install PyPDF2")
    print()
    print("   2. Generate config:")
    print("      from mem_llm import create_config_from_document")
    print("      create_config_from_document('company.pdf', 'config.yaml')")
    print()
    
    print("To use with DOCX files:")
    print("   1. Install python-docx:")
    print("      pip install python-docx")
    print()
    print("   2. Generate config:")
    print("      create_config_from_document('company.docx', 'config.yaml')")
    print()
    
    print("Command-line usage:")
    print("   python -m mem_llm.config_from_docs company_info.pdf")
    print("   python -m mem_llm.config_from_docs business.docx my_config.yaml")
    print("   python -m mem_llm.config_from_docs info.txt config.yaml 'Acme Corp'")
    print()
    
    print("=" * 60)
    print("💡 Benefits:")
    print("   ✅ Quickly set up bot with company info")
    print("   ✅ No manual config editing needed")
    print("   ✅ Extract info directly from documents")
    print("   ✅ Supports PDF, DOCX, and TXT formats")
    print("=" * 60)


def main():
    """Run the demonstration"""
    
    # Test with text file
    test_with_text_file()
    
    # Show PDF/DOCX usage
    show_pdf_docx_usage()
    
    print("\n✨ Example complete!")
    print("📝 You can now edit 'generated_config.yaml' and use it with:")
    print("   agent = MemAgent(config_file='generated_config.yaml')")


if __name__ == "__main__":
    main()
