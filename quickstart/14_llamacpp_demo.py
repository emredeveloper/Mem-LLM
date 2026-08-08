"""Quickstart: talk to any OpenAI-compatible server (llama.cpp, vLLM, LM Studio).

Start llama.cpp with an OpenAI-compatible endpoint first:

    llama-server -m /path/to/model.gguf --alias local-model --host 127.0.0.1 --port 8080

Both backends below speak `/v1/chat/completions`, so the same code works for
llama.cpp, vLLM, LM Studio's server, or any other compatible endpoint.
"""

import os

from mem_llm import MemAgent

BASE_URL = os.getenv("LLAMACPP_BASE_URL", "http://localhost:8080")
MODEL = os.getenv("LLAMACPP_MODEL", "local-model")

# "llamacpp" also accepts the aliases "llama-cpp", "llama_cpp" and "llama.cpp".
# Use "openai-compatible" for any other server exposing /v1/chat/completions.
BACKEND = os.getenv("LLAMACPP_BACKEND", "llamacpp")


def main() -> None:
    try:
        agent = MemAgent(
            backend=BACKEND,
            model=MODEL,
            base_url=BASE_URL,
            check_connection=False,
        )
        agent.set_user("llamacpp_user")

        print("Bot:", agent.chat("Remember that I prefer concise answers."))
        print("Bot:", agent.chat("What did I just tell you about my preference?"))

        print("\nStreaming:", end=" ")
        for chunk in agent.chat_stream("Count from 1 to 5, numbers only."):
            print(chunk, end="", flush=True)
        print()
    except Exception as exc:
        print(f"[{BACKEND}] Error:", exc)
        print(f"Is a server running at {BASE_URL}?")


if __name__ == "__main__":
    main()
