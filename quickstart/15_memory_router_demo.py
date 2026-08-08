"""Quickstart: route long-term memory with MemoryRouter.

MemoryRouter unifies the memory layers into one context payload:

    core blocks  - stable facts you set explicitly (persona, preferences)
    archival     - long-term notes you write and search
    recall       - recent conversation history
    graph        - entity/relation triplets, when graph memory is enabled
"""

import os

from mem_llm import MemAgent, MemoryRouter

BACKEND = os.getenv("BACKEND", "ollama")
MODEL = os.getenv("MODEL", "granite4:3b")


def main() -> None:
    try:
        agent = MemAgent(
            backend=BACKEND,
            model=MODEL,
            enable_graph_memory=True,
            check_connection=False,
        )
        agent.set_user("router_user")

        router = MemoryRouter(agent.memory, graph_store=agent.graph_store)

        # Core memory: small, always-injected facts.
        router.set_core_block("router_user", "human", "Prefers concise answers.")

        # Archival memory: larger notes you can search later.
        router.add_archival_memory(
            "router_user",
            "Works at Acme Corp as a data scientist.",
            tags=["job"],
        )

        print("Core blocks:", list(router.get_core_blocks("router_user")))
        print("Archival hits:", router.search_archival_memory("router_user", "work"))

        # build_context returns the assembled payload plus each layer separately.
        context = router.build_context("router_user", "Where do I work?")
        print("Layers:", list(context))
        print("\nAssembled context:\n" + context["text"])
    except Exception as exc:
        print(f"[{BACKEND}] Error:", exc)


if __name__ == "__main__":
    main()
