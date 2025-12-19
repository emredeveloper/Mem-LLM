"""
Command Line Interface for Mem-LLM
Interactive chat, statistics, and data management
"""

import json
import sys
from typing import Optional

import click

from . import __version__
from .mem_agent import MemAgent


@click.group()
@click.version_option(version=__version__, prog_name="mem-llm")
def cli():
    """
    Mem-LLM - Memory-enabled AI Assistant CLI

    A powerful command-line interface for interacting with your AI assistant.
    """
    pass


@cli.command()
@click.option("--user", "-u", default="default", help="User ID for the chat session")
@click.option("--model", "-m", default="rnj-1:latest", help="LLM model to use")
@click.option("--sql/--json", default=False, help="Use SQL (default: JSON)")
@click.option("--config", "-c", type=click.Path(exists=True), help="Config file path")
def chat(user: str, model: str, sql: bool, config: Optional[str]):
    """
    Start an interactive chat session

    Examples:
        mem-llm chat --user john
        mem-llm chat --user alice --sql
        mem-llm chat --config config.yaml
    """
    click.echo("🤖 Mem-LLM Interactive Chat")
    click.echo("=" * 60)

    # Initialize agent
    try:
        if config:
            agent = MemAgent(config_file=config)
        else:
            agent = MemAgent(model=model, use_sql=sql)

        # Check setup
        status = agent.check_setup()
        if status["status"] != "ready":
            click.echo("\n❌ Setup Error!", err=True)
            if not status["ollama_running"]:
                click.echo("   → Ollama service is not running", err=True)
                click.echo("   → Start it with: ollama serve", err=True)
            elif not status["model_ready"]:
                click.echo(f"   → Model '{model}' not found", err=True)
                click.echo(f"   → Download it with: ollama pull {model}", err=True)
            sys.exit(1)

        agent.set_user(user)

        click.echo("\n✅ Chat session started")
        click.echo(f"   User: {user}")
        click.echo(f"   Model: {model}")
        click.echo(f"   Memory: {'SQL' if sql else 'JSON'}")
        click.echo("\nType your message and press Enter. Commands:")
        click.echo("  /profile  - Show user profile")
        click.echo("  /stats    - Show statistics")
        click.echo("  /history  - Show recent conversations")
        click.echo("  /exit     - Exit chat\n")

        # Chat loop
        while True:
            try:
                message = input(f"\n{user}> ").strip()

                if not message:
                    continue

                # Handle commands
                if message.lower() in ["/exit", "/quit", "exit", "quit"]:
                    click.echo("\n👋 Goodbye!")
                    break

                elif message.lower() == "/profile":
                    profile = agent.get_user_profile()
                    click.echo("\n👤 User Profile:")
                    click.echo(json.dumps(profile, indent=2, ensure_ascii=False))
                    continue

                elif message.lower() == "/stats":
                    stats = agent.get_statistics()
                    click.echo("\n📊 Statistics:")
                    click.echo(json.dumps(stats, indent=2, ensure_ascii=False))
                    continue

                elif message.lower() == "/history":
                    if hasattr(agent.memory, "get_recent_conversations"):
                        convs = agent.memory.get_recent_conversations(user, 5)
                        click.echo("\n📜 Recent Conversations:")
                        for i, conv in enumerate(convs, 1):
                            click.echo(f"\n{i}. [{conv.get('timestamp', 'N/A')}]")
                            click.echo(f"   You: {conv.get('user_message', '')[:100]}")
                            click.echo(f"   Bot: {conv.get('bot_response', '')[:100]}")
                    continue

                # Regular chat
                response = agent.chat(message)
                click.echo(f"\n🤖 Bot> {response}")

            except KeyboardInterrupt:
                click.echo("\n\n👋 Goodbye!")
                break
            except EOFError:
                click.echo("\n\n👋 Goodbye!")
                break

    except Exception as e:
        click.echo(f"\n❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--user", "-u", help="User ID (optional, shows all users if not specified)")
@click.option("--sql/--json", default=False, help="Use SQL (default: JSON)")
def stats(user: Optional[str], sql: bool):
    """
    Show memory statistics

    Examples:
        mem-llm stats
        mem-llm stats --user john
        mem-llm stats --sql
    """
    try:
        agent = MemAgent(use_sql=sql)

        if user:
            agent.set_user(user)
            profile = agent.get_user_profile()
            click.echo(f"\n👤 User Profile: {user}")
            click.echo("=" * 60)
            click.echo(json.dumps(profile, indent=2, ensure_ascii=False))
        else:
            stats = agent.get_statistics()
            click.echo("\n📊 Memory Statistics")
            click.echo("=" * 60)
            click.echo(json.dumps(stats, indent=2, ensure_ascii=False))

    except Exception as e:
        click.echo(f"\n❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("user")
@click.option(
    "--format", "-f", type=click.Choice(["json", "txt"]), default="json", help="Export format"
)
@click.option("--output", "-o", type=click.Path(), help="Output file (default: stdout)")
@click.option("--sql/--json", default=False, help="Use SQL (default: JSON)")
def export(user: str, format: str, output: Optional[str], sql: bool):
    """
    Export user conversation data

    Examples:
        mem-llm export john
        mem-llm export john --format txt
        mem-llm export john --output john_data.json
    """
    try:
        agent = MemAgent(use_sql=sql)
        agent.set_user(user)

        data = agent.export_memory(format=format)

        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(data)
            click.echo(f"✅ Exported to: {output}")
        else:
            click.echo(data)

    except Exception as e:
        click.echo(f"\n❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--model", "-m", default="rnj-1:latest", help="Model to check")
def check(model: str):
    """
    Check if Ollama and model are ready

    Example:
        mem-llm check
        mem-llm check --model llama3.2:3b
    """
    try:
        agent = MemAgent(model=model)
        status = agent.check_setup()

        click.echo("\n🔍 System Check")
        click.echo("=" * 60)
        click.echo(f"Ollama Running:    {'✅' if status['ollama_running'] else '❌'}")
        click.echo(f"Target Model:      {status['target_model']}")
        click.echo(f"Model Ready:       {'✅' if status['model_ready'] else '❌'}")
        click.echo(f"Memory Backend:    {status['memory_backend']}")
        click.echo(f"Total Users:       {status['total_users']}")
        click.echo(f"Total Chats:       {status['total_interactions']}")
        click.echo(f"KB Entries:        {status['kb_entries']}")

        if status["available_models"]:
            click.echo("\nAvailable Models:")
            for m in status["available_models"]:
                click.echo(f"  • {m}")

        click.echo(f"\nStatus: {'✅ READY' if status['status'] == 'ready' else '❌ NOT READY'}")

        if status["status"] != "ready":
            sys.exit(1)

    except Exception as e:
        click.echo(f"\n❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("user")
@click.confirmation_option(prompt="Are you sure you want to delete all data for this user?")
@click.option("--sql/--json", default=False, help="Use SQL (default: JSON)")
def clear(user: str, sql: bool):
    """
    Clear all data for a user (requires confirmation)

    Example:
        mem-llm clear john
    """
    try:
        agent = MemAgent(use_sql=sql)
        result = agent.clear_user_data(user, confirm=True)
        click.echo(f"✅ {result}")

    except Exception as e:
        click.echo(f"\n❌ Error: {str(e)}", err=True)
        sys.exit(1)


def main():
    """Entry point for the CLI"""
    cli()


if __name__ == "__main__":
    main()
