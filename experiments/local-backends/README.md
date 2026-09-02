# Local backend experiments

Test date: 2026-09-03

## Hardware and local software

- GPU: NVIDIA GeForce RTX 4060, 8 GB VRAM
- llama.cpp: build `b10621` (`0.3.0-dev`, CUDA 13.3 bundle)
- Ollama: `0.33.2`
- LM Studio CLI: commit `07b7252`, server on port `1234`
- Bionic: `1.1.1+5`
- Model: `LFM2.5-2.6B-Q8_0.gguf` (2.7B parameters, Q8_0)

## 1. llama.cpp smoke test

Server configuration:

```powershell
llama-server.exe `
  --model "$env:USERPROFILE\Downloads\LFM2.5-2.6B-Q8_0.gguf" `
  --alias lfm2.5-2.6b-q8 `
  --host 127.0.0.1 `
  --port 8080 `
  --ctx-size 4096 `
  --n-gpu-layers 999
```

Results:

- `/health`: `ok`
- Model discovery: passed
- Warm generation: about 61–72 tokens/s
- Mem-LLM `backend="llamacpp"`: passed, returned `OK`
- LFM2.5 always opens a reasoning block. A small output limit can expire before visible `content` is produced.
- Request-level `reasoning_effort="none"` and `reasoning_budget=0` allowed the short test to reach visible content, although `reasoning_content` was still present.

## 2. Ollama smoke test

The local GGUF was imported as `mem-llm-lfm2.5:2.6b-q8` using the adjacent Modelfile.

```powershell
ollama create mem-llm-lfm2.5:2.6b-q8 `
  -f experiments\local-backends\Modelfile.lfm2.5
```

Results:

- Detected capabilities: `tools`, `thinking`, `completion`
- GPU offload: 100%
- Warm generation: about 69 tokens/s
- Mem-LLM `backend="ollama"`: passed, returned `OK`
- `think=false` does not suppress thinking for this model because its official chat template unconditionally starts `<think>`.

## 3. LM Studio smoke test

The original GGUF was preserved and hard-linked into the LM Studio model directory:

```powershell
lms import "$env:USERPROFILE\Downloads\LFM2.5-2.6B-Q8_0.gguf" `
  --user-repo local/mem-llm-lfm2.5 `
  --hard-link `
  --yes
```

Results:

- Model key/API identifier: `mem-llm-lfm2.5`
- Load time: 2.9–3.7 seconds
- GPU memory estimate: 2.68 GiB
- OpenAI-compatible chat: passed, returned `OK` in about 1.2 seconds
- Mem-LLM `backend="lmstudio"`: passed, returned `OK`
- Native tool calling: passed; the model emitted a valid `get_weather({"city":"Istanbul"})` call with `finish_reason="tool_calls"`.
- Both CLI and REST load attempts requested a 4096-token context, but the effective LM Studio configuration reported 128000. Always verify `load_config` after loading.

## Response envelope implementation

Mem-LLM now exposes `chat_response()` on its provider clients. The returned
`LLMResponse` preserves `content`, reasoning, native tool calls, token usage,
finish reason, model identifier, and the raw provider response. The legacy
`chat()` method still returns plain text.

A focused LM Studio native-tool regression test and a live LM Studio/LFM2.5
check both passed. The agent loop does not execute native tool calls yet; that
is the next integration step.

## References

- [llama.cpp server](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- [Ollama GGUF import](https://docs.ollama.com/import)
- [LM Studio model import](https://lmstudio.ai/docs/cli/local-models/import)
- [LM Studio model loading](https://lmstudio.ai/docs/developer/rest/load)
- [LM Studio Bionic](https://lmstudio.ai/docs/bionic)
- [LiquidAI LFM2.5-2.6B](https://huggingface.co/LiquidAI/LFM2.5-2.6B)
