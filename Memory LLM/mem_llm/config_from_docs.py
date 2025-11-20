"""
Config Generator from Documents (PDF, DOCX, TXT)
Automatically creates config.yaml from business documents
"""

import os
from typing import Any, Dict, Optional

import yaml


def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from PDF, DOCX, or TXT files

    Args:
        file_path: Path to document

    Returns:
        Extracted text
    """
    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    elif file_ext == ".pdf":
        try:
            import PyPDF2

            text = []
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text.append(page.extract_text())
            return "\n".join(text)
        except ImportError:
            return "⚠️ PyPDF2 not installed. Run: pip install PyPDF2"

    elif file_ext in [".docx", ".doc"]:
        try:
            import docx

            doc = docx.Document(file_path)
            text = []
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
            return "\n".join(text)
        except ImportError:
            return "⚠️ python-docx not installed. Run: pip install python-docx"

    else:
        return f"⚠️ Unsupported file format: {file_ext}"


def generate_config_from_text(text: str, company_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate config.yaml structure from text

    Args:
        text: Extracted text from document
        company_name: Company name (optional)

    Returns:
        Config dictionary
    """
    # Simple config template
    config = {
        "usage_mode": "business",  # or "personal"
        "llm": {
            "model": "granite4:3b",
            "temperature": 0.3,
            "max_tokens": 300,
            "ollama_url": "http://localhost:11434",
        },
        "memory": {"use_sql": True, "db_path": "memories.db", "json_dir": "memories"},
        "response": {"use_knowledge_base": True, "recent_conversations_limit": 5},
        "business": {
            "company_name": company_name or "Your Company",
            "industry": "Technology",
            "founded_year": "2024",
        },
        "knowledge_base": {"auto_load": True, "search_limit": 5},
        "logging": {"level": "INFO", "file": "mem_agent.log"},
    }

    # Try to extract company name from text if not provided
    if not company_name:
        lines = text.split("\n")[:10]  # First 10 lines
        for line in lines:
            if any(keyword in line.lower() for keyword in ["company", "corp", "inc", "ltd"]):
                config["business"]["company_name"] = line.strip()[:50]
                break

    return config


def create_config_from_document(
    doc_path: str, output_path: str = "config.yaml", company_name: Optional[str] = None
) -> str:
    """
    Create config.yaml from a business document

    Args:
        doc_path: Path to PDF/DOCX/TXT document
        output_path: Output config.yaml path
        company_name: Company name (optional)

    Returns:
        Success message
    """
    if not os.path.exists(doc_path):
        return f"❌ File not found: {doc_path}"

    # Extract text
    print(f"📄 Reading document: {doc_path}")
    text = extract_text_from_file(doc_path)

    if text.startswith("⚠️"):
        return text  # Error message

    print(f"✅ Extracted {len(text)} characters")

    # Generate config
    config = generate_config_from_text(text, company_name)

    # Save to YAML
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

    print(f"✅ Config created: {output_path}")
    print(f"📌 Company: {config['business']['company_name']}")

    return f"✅ Config successfully created at {output_path}"


# Simple CLI
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(
            """
🔧 Config Generator from Documents

Usage:
    python -m mem_llm.config_from_docs <document_path> [output_path] [company_name]

Examples:
    python -m mem_llm.config_from_docs company_info.pdf
    python -m mem_llm.config_from_docs business.docx my_config.yaml "Acme Corp"
    python -m mem_llm.config_from_docs info.txt
        """
        )
        sys.exit(1)

    doc_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "config.yaml"
    company_name = sys.argv[3] if len(sys.argv) > 3 else None

    result = create_config_from_document(doc_path, output_path, company_name)
    print(result)
