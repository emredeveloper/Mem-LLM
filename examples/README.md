# 📚 Mem-LLM Examples# Mem-LLM Examples



Simple, easy-to-understand examples showing how to use Mem-LLM.This directory contains practical examples demonstrating various features of Mem-LLM.



## 🚀 Quick Start## 📚 Available Examples



Make sure Ollama is running first:### 1. **example_simple.py**

Basic memory functionality demonstration.

```bash```bash

ollama servepython example_simple.py

ollama pull granite4:tiny-h```

```**Shows:** Creating an agent, setting users, memory recall, profile extraction



Then run any example:### 2. **example_customer_service.py**

Multi-user customer service scenario.

```bash```bash

cd examplespython example_customer_service.py

python 01_hello_world.py```

```**Shows:** Multiple users, separate memories, returning customers



## 📖 Examples Overview### 3. **example_knowledge_base.py**

FAQ/support system using knowledge base (requires SQL mode).

### 1️⃣ Hello World```bash

**File:** `01_hello_world.py`  python example_knowledge_base.py

**The simplest possible example** - just 5 lines of code!```

**Shows:** Adding KB entries, KB-powered responses, category organization

- Create an agent

- Chat with memory### 4. **example_personal_mode.py**

- Perfect for beginnersPersonal assistant configuration.

```bash

### 2️⃣ Basic Memorypython example_personal_mode.py

**File:** `02_basic_memory.py`  ```

**Learn how memory works****Shows:** JSON memory mode, personal use case



- Share information with the bot### 5. **example_business_mode.py**

- Bot remembers across conversationsBusiness/enterprise configuration.

- View saved user profile```bash

python example_business_mode.py

### 3️⃣ Multiple Users```

**File:** `03_multi_user.py`  **Shows:** SQL memory mode, configuration file usage

**Separate memory for each user**

### 6. **example_memory_tools.py**

- Create multiple users (Alice and Bob)Memory management and tools.

- Each has their own memory```bash

- Switch between userspython example_memory_tools.py

```

### 4️⃣ Customer Service**Shows:** Memory search, data export, statistics

**File:** `04_customer_service.py`  

**Real-world customer service scenario**### 7. **demo_user_tools.py**

Interactive demo of user tools.

- Customer calls multiple times```bash

- Bot remembers previous conversationspython demo_user_tools.py

- Better customer experience```

**Shows:** Tool system, natural language commands

### 5️⃣ Knowledge Base

**File:** `05_knowledge_base.py`  ## 🚀 Quick Start

**Add FAQ and support knowledge**

1. Install: `pip install mem-llm`

- Requires SQL mode2. Start Ollama: `ollama serve`

- Add shipping/return/payment info3. Download model: `ollama pull granite4:tiny-h`

- Bot gives accurate answers from knowledge base4. Run: `python example_simple.py`



### 6️⃣ CLI Commands## 💡 Tips

**File:** `06_cli_demo.py`  

**Learn command-line interface**- Start with `example_simple.py` for basics

- Use `example_knowledge_base.py` for FAQ/support

- Lists all available CLI commands- Use `example_customer_service.py` for multi-user apps

- Interactive chat, stats, export

- No coding needed!## 🆘 Troubleshooting



## 🎯 Which Example Should I Start With?- **"Ollama not running"**: Run `ollama serve`

- **"Model not found"**: Run `ollama pull granite4:tiny-h`

| Your Goal | Recommended Example |- **Import error**: Run `pip install mem-llm --upgrade`

|-----------|-------------------|

| Complete Beginner | `01_hello_world.py` |

| Understand Memory | `02_basic_memory.py` |
| Multiple Users | `03_multi_user.py` |
| Customer Service Bot | `04_customer_service.py` |
| FAQ/Support System | `05_knowledge_base.py` |
| Use CLI (no code) | `06_cli_demo.py` |

## 💡 Tips

1. **Always check Ollama first**: Run `mem-llm check`
2. **Start simple**: Use JSON mode (default) before SQL
3. **Use SQL for production**: Better performance for multiple users
4. **Knowledge Base needs SQL**: Use `use_sql=True` for KB features

## 🆘 Troubleshooting

**Ollama not running?**
```bash
ollama serve
```

**Model not found?**
```bash
ollama pull granite4:tiny-h
```

**Import error?**
```bash
pip install mem-llm --upgrade
```

## 📚 More Resources

- **Main Documentation**: See `Memory LLM/README.md`
- **Configuration Guide**: See `Memory LLM/docs/CONFIG_GUIDE.md`
- **Integration Guide**: See `Memory LLM/INTEGRATION_GUIDE.md`
- **Changelog**: See `Memory LLM/CHANGELOG.md`

## 🤝 Contributing

Have a great example idea? Feel free to contribute!

1. Keep it simple and focused on one concept
2. Add clear comments
3. Include error handling
4. Follow the naming pattern: `XX_description.py`

---

**Happy coding!** 🎉
