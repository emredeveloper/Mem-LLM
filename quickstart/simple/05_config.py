"""
Simple Example 5: YAML Config
==============================
Load configuration from YAML file
"""

from mem_llm import MemAgent
import yaml

# Create config.yaml
config_yaml = """
backend: ollama
model: granite4:3b
use_sql: false
memory_dir: memories
temperature: 0.7
max_tokens: 1000
"""

# Write to file
with open("config.yaml", "w") as f:
    f.write(config_yaml)

# Load from YAML
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Create agent
agent = MemAgent(
    backend=config['backend'],
    model=config['model'],
    use_sql=config['use_sql'],
    memory_dir=config.get('memory_dir', 'memories')
)

agent.set_user("config_user")

response = agent.chat("I'm working with YAML config!")
print(response)

print(f"\n✅ Config loaded:")
print(f"  Backend: {config['backend']}")
print(f"  Model: {config['model']}")
print(f"  Memory: {'SQLite' if config['use_sql'] else 'JSON'}")
