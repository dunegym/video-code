---
base_model: Qwen/Qwen3.8-27B
library_name: peft
license: apache-2.0
datasets:
- harness-hub/scale800-harbor
- harness-hub/harness-adapters
- harness-hub/termgrade-train-harbor
- ai-and/termgrade-environments
tags:
- trl
- grpo
- async-grpo
- lora
- agents
- harbor
- openenv
- opencode
pipeline_tag: image-text-to-text
---

![](banner.png)

A LoRA adapter for [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B), trained with reinforcement learning to work as the model
behind the [OpenCode](https://opencode.ai) coding agent on software-engineering and terminal tasks.

> [!Tip]
> **Maximum-effort thinking accuracy, at a sixth of the tokens.** With thinking off, this adapter matches the base
> model thinking at its highest reasoning effort (`xhigh`): 51.0% vs 47.1% on SWE-bench Pro, 53.0% vs 55.4% on
> Terminal-Bench 2.1, while generating 6–8× fewer tokens per task. Keep thinking off: turning it on for the adapter
> adds nothing significant. See [Thinking vs no thinking](#thinking).

- **SWE-bench Pro (hard 51):** 35.3% → 51.0% (+15.7 points; 11 tasks newly solved, 3 lost).
- **Terminal-Bench 2.1:** 46.4% → 52.4% (+6.0 points); +13.6 points on the 66 tasks not used to pick the checkpoint (12 newly solved, 3 lost; p = 0.035).
- **Less work per task:** a quarter of the base model's turns on SWE-bench Pro (13 vs 48) and half on Terminal-Bench
  2.1, on the tasks both solve, with 3.5× and 2.6× fewer generated tokens.

> [!Note]
> All results are under the OpenCode harness: one attempt per task, a 100-step budget, thinking off unless stated, text
> only (the vision tower is not served), sampling at temperature 0.8 with top-p 1.0 (the training sampling). Base model
> and adapter always run under identical settings. These numbers are not comparable with the ones on the
> [Qwen3.8-27B card](https://huggingface.co/Qwen/Qwen3.8-27B), which uses other harnesses (Terminus, Claude Code),
> thinking at maximum effort, larger budgets and the full SWE-bench Pro.

Full recipe will be shared in [the release blogpost](https://huggingface.co/blog/harness-adapters-at-scale) for anyone to build their own harness adapter.

**Pick your setup**

[![Results](https://img.shields.io/badge/results-pass%401_%2B_efficiency-555?style=flat)](#results)
[![vLLM](https://img.shields.io/badge/serve-vLLM-30A2FF?style=flat)](#use-with-opencode)
[![transformers](https://img.shields.io/badge/serve-transformers-ffd21e?style=flat)](#use-with-transformers)
[![llama.cpp](https://img.shields.io/badge/run-llama.cpp-1f1f1f?style=flat)](#use-with-llama-cpp)
[![GGUF](https://img.shields.io/badge/download-GGUF-ff9d0b?style=flat)](https://huggingface.co/harness-hub/Qwen3.8-27B-opencode-adapted-GGUF)
[![Merge](https://img.shields.io/badge/merge-PEFT-ffd21e?style=flat)](#merge)
[![Training](https://img.shields.io/badge/training-recipe-4b44c4?style=flat)](#training)


A real SWE-bench Pro task under OpenCode: the base model gets lost in a dependency and ends up repeating the same
command until it hits the 100-step limit; this adapter writes the schema, the validator and its tests, fixes one API
mistake and passes, in 17 tool calls.

![](trajectory.gif)

<details>
<summary>Still version, and the task</summary>

![](trajectory.png)

Task: `instance_flipt-io__flipt-c1728053367c753688f114ec26e703c8fdeda125` from SWE-bench Pro (hard 51): add an
`internal/cue` package that validates flipt configuration files against an embedded CUE schema. Both runs are from the
evaluation above: the base model was graded 0, this adapter 1. Each line is one tool call as the trajectory recorded it,
cut to fit.

</details>

<a id="results"></a>

## Results

![](card-opencode.png)

![](tokens-opencode.png)

| Benchmark | Qwen3.8-27B | Qwen3.8-27B, thinking | **Qwen3.8-27B-opencode-adapted** | Qwen3.8-27B-opencode-adapted, thinking |
|---|---|---|---|---|
| SWE-bench Pro (hard 51) | 35.3% | 47.1% | **51.0%** | 54.9% |
| Terminal-Bench 2.1 | 47.0% | 55.4% | **53.0%** | 56.6% |

On Terminal-Bench 2.1 the four runs are compared on the 83 tasks all of them graded, so the base model and adapter scores differ slightly from the paired results below, which use the 84 tasks those two graded. "Thinking" is the chat template's
thinking mode at its default reasoning effort (`xhigh`).

<details open>
<summary><b>Full paired results</b> (intervals and sign tests against the base model)</summary>

One attempt per task, thinking off, paired against the base model under OpenCode on the same tasks. The interval is
95%; the p-value is an exact sign test on the tasks that changed outcome.

| Benchmark | Tasks | Qwen3.8-27B | Qwen3.8-27B-opencode-adapted (step 150) | Difference (points) | Newly solved / lost |
|---|---|---|---|---|---|
| SWE-bench Pro (hard 51) | 51 | 35.3% | 51.0% | +15.7 ± 13.9 | 11 / 3 (p = 0.057) |
| Terminal-Bench 2.1 | 84 | 46.4% | 52.4% | +6.0 ± 10.7 | 13 / 8 (p = 0.38) |
| Terminal-Bench 2.1, the 66 tasks not used to pick the checkpoint | 66 | 45.5% | 59.1% | +13.6 ± 11.1 | 12 / 3 (p = 0.035) |

- **SWE-bench Pro (hard 51):** the 51 hardest tasks of [SWE-bench Pro](https://huggingface.co/datasets/harness-hub/swebench-pro-v2-hard51-harbor), 2 h and 100 agent steps per task.
- **Terminal-Bench 2.1:** all 89 tasks of [Terminal-Bench 2.1](https://huggingface.co/datasets/harborframework/terminal-bench-2.1), 1 h and 100 agent steps per task.

Step 150 was picked by looking at the checkpoints' scores on SWE-bench Pro and on an 18-task subset of Terminal-Bench
2.1, tracked during training.

</details>

<details open>
<summary><b>Work per solved task</b> (turns, visible content, reasoning and generated tokens)</summary>

Medians per task, this adapter / the base model, over the tasks both solved: same tasks, same outcome, so the numbers
measure only how much work each needed. Generated tokens are everything the model writes (visible content, reasoning and
tool calls); content is the visible text between tool calls.

| | Tasks | Turns | Content tokens | Reasoning tokens | Generated tokens |
|---|---|---|---|---|---|
| **vs the base model** | | | | | |
| SWE-bench Pro | 15 | 13 / 48 | 0.7k / 1.0k | 0 / 0 | 1.9k / 6.8k |
| Terminal-Bench 2.1 | 31 | 8 / 16 | n/a | 0 / 0 | 1.0k / 2.7k |
| **vs the base model with thinking** | | | | | |
| SWE-bench Pro | 19 | 12 / 51 | 0.9k / 0.8k | 0 / 28.2k | 1.9k / 33.5k |
| Terminal-Bench 2.1 | 34 | 8 / 11 | 0.4k / 0.8k | 0 / 7.2k | 1.1k / 7.2k |

- Against the base model, the adapter writes about as much text, but in far fewer turns: short reasoning between
  targeted actions (about 45 tokens of text per turn against about 20), instead of exploring with many commands.
- Against the base model with thinking, nearly all the difference is reasoning: the adapter reaches the same answers
  without it.
- Content for the base model on Terminal-Bench 2.1 is not available: its run's traces were not kept.

</details>

<a id="thinking"></a>

<details open>
<summary><b>Thinking vs no thinking</b></summary>

| | SWE-bench Pro (hard 51) | Terminal-Bench 2.1 |
|---|---|---|
| This adapter vs the base model with thinking (tasks only one solves) | 7 / 5 | 10 / 12 |
| Generated tokens per task (median), base model with thinking / this adapter | 31.8k / 3.9k | 15.8k / 2.6k |
| Model calls per task (median), base model with thinking / this adapter | 44 / 18 | 14 / 12 |
| This adapter with thinking vs without (tasks only one solves) | 8 / 6 | 13 / 10 |

Thinking mode on its own brings the base model to this adapter's accuracy, within noise; the adapter gets there without
it, at 6–8× fewer tokens. Thinking runs use the template's default reasoning effort (`xhigh`) and OpenCode's limit of
32,000 output tokens per model call; fewer than 0.5% of turns reached it, as often for the adapter as for the base model.

</details>

<details>
<summary><b>Evaluation checks</b></summary>

- **Infrastructure.** During evaluation, the public tunnel between the sandboxes and the model server went down a few
  times, failing rollouts for reasons unrelated to the model. We check every rollout for this and reran all affected
  ones, on both sides; the numbers above are the corrected ones (the base model's SWE-bench Pro score was 31.4% before
  the reruns).
- **Harness limits.** In this setup the model is served text only and web search is disabled. OpenCode reads image and
  video files as images, which the server rejects, and asks for web searches, which are cancelled: either ends the
  session. This happens on a handful of Terminal-Bench tasks, more often for the adapter than for the base model, so it
  understates the adapter there. With vision served and web access, these tasks run normally.
- **Test files.** Agents, the base model and this adapter alike, sometimes write or edit test files while working,
  mostly their own scratch scripts to check a change. This cannot affect a grade: SWE-bench Pro's grader resets all test
  files and applies the official tests before running them, and Terminal-Bench's tests are copied in only at grading.
- **Hidden reasoning.** The adapter's visible reasoning is plain text: `<think>` tags appear in its output in fewer than
  1 turn in 1,000, and with thinking off the template never opens a thinking block.

</details>

<a id="use-with-opencode"></a>

## Use with OpenCode

<details open>
<summary><b>Serve the adapter with vLLM and point OpenCode at it</b></summary>

### 1. Serve the adapter with vLLM

```sh
vllm serve Qwen/Qwen3.8-27B \
    --enable-lora --max-lora-rank 32 \
    --lora-modules qwen3.8-opencode=harness-hub/Qwen3.8-27B-opencode-adapted \
    --language-model-only --enable-prefix-caching --mamba-cache-mode align \
    --enable-auto-tool-choice --tool-call-parser qwen3_xml --reasoning-parser qwen3 \
    --default-chat-template-kwargs '{"enable_thinking": false}' \
    --max-model-len 131072
```

This is the configuration of the evaluations. Keep thinking off, as in training: with it on, the adapter is not
significantly more accurate and generates about 6× more tokens. Prefix caching on this hybrid model needs
`--mamba-cache-mode align`; without it, every agent turn re-reads its whole history.

### 2. Point OpenCode at it

Install OpenCode 2 (training and evaluation used `@opencode/cli` 2.2.7):

```sh
npm install -g @opencode/cli@2.2.7
```

Add the server to `~/.config/opencode/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "local": {
      "npm": "@ai-sdk/openai-compatible",
      "options": { "baseURL": "http://localhost:8000/v1", "apiKey": "dummy" },
      "models": { "qwen3.8-opencode": {} }
    }
  }
}
```

```sh
opencode run --standalone --model local/qwen3.8-opencode "Find out why the tests in tests/test_parser.py fail and fix the bug."
```

</details>

<a id="use-with-transformers"></a>

## Use with OpenCode (transformers serve)

<details open>
<summary><b>Serve with transformers and point OpenCode at it</b></summary>

[`transformers serve`](https://huggingface.co/docs/transformers/en/serve-cli/serving) is a lightweight OpenAI-compatible
server, for local use and experimentation (vLLM is faster under load). It handles Qwen's tool calls out of the box.
Serve the merged checkpoint from [Merge the adapter into the base model](#merge):

```sh
pip install "transformers[serving]"
transformers serve ./Qwen3.8-27B-opencode-merged --dtype bfloat16 --continuous-batching --reasoning off
```

`--reasoning off` keeps thinking off, as in training. The server listens on `http://localhost:8000`, so the OpenCode
configuration from [the vLLM section](#use-with-opencode) works as is, with the model key set to the name the server
serves, here `./Qwen3.8-27B-opencode-merged`.

</details>

<a id="use-with-llama-cpp"></a>

## Use with OpenCode (llama.cpp)

<details open>
<summary><b>Serve the GGUF adapter with llama.cpp and point OpenCode at it</b></summary>

The GGUF version of Qwen3.8-27B-opencode-adapted is in [harness-hub/Qwen3.8-27B-opencode-adapted-GGUF](https://huggingface.co/harness-hub/Qwen3.8-27B-opencode-adapted-GGUF). It runs on top of a GGUF of the base model:

```sh
hf download ggml-org/Qwen3.8-27B-GGUF Qwen3.8-27B-Q8_0.gguf --local-dir .
hf download harness-hub/Qwen3.8-27B-opencode-adapted-GGUF Qwen3.8-27B-opencode-lora-F16.gguf --local-dir .

llama serve -m Qwen3.8-27B-Q8_0.gguf --lora Qwen3.8-27B-opencode-lora-F16.gguf \
    --chat-template-kwargs '{"enable_thinking": false}' -c 65536 --port 8080 --alias qwen3.8-opencode
```

Then use the OpenCode configuration from [the vLLM section](#use-with-opencode) with `"baseURL": "http://localhost:8080/v1"`.

The adapter was trained on the BF16 weights: the closer the base GGUF is to them, the closer you get to the trained
behavior. `Q8_0` is a good default; lower-bit quants drift further. The GGUF version has not been re-evaluated.

</details>

<a id="merge"></a>

## Merge the adapter into the base model

<details open>
<summary><b>Get a standalone model, with no LoRA at serving time</b></summary>

The adapter can be merged into the base weights with PEFT. The result is a regular Qwen3.8-27B checkpoint (about 54 GB
in BF16) that any engine serves without LoRA support. Merge on CPU if the GPU is needed for serving afterwards:

```python
import torch
from peft import PeftModel
from transformers import AutoModelForImageTextToText, AutoTokenizer

base = AutoModelForImageTextToText.from_pretrained("Qwen/Qwen3.8-27B", dtype=torch.bfloat16, device_map="cpu")
model = PeftModel.from_pretrained(base, "harness-hub/Qwen3.8-27B-opencode-adapted").merge_and_unload()
model.save_pretrained("Qwen3.8-27B-opencode-merged")
AutoTokenizer.from_pretrained("harness-hub/Qwen3.8-27B-opencode-adapted").save_pretrained("Qwen3.8-27B-opencode-merged")
```

Then serve it like the base model, without the LoRA flags:

```sh
vllm serve Qwen3.8-27B-opencode-merged --served-model-name qwen3.8-opencode \
    --language-model-only --enable-prefix-caching --mamba-cache-mode align \
    --enable-auto-tool-choice --tool-call-parser qwen3_xml --reasoning-parser qwen3 \
    --default-chat-template-kwargs '{"enable_thinking": false}' --max-model-len 131072
```

The merged checkpoint can also be converted to GGUF and served with llama.cpp the same way.

</details>

<a id="training"></a>

## Training

<details open>
<summary><b>Method, data, hyperparameters and hardware</b></summary>

| | |
|---|---|
| Method | [AsyncGRPO](https://huggingface.co/docs/trl/main/en/async_grpo_trainer) (TRL, experimental), LoRA |
| Environment | [Harbor](https://github.com/laude-institute/harbor) tasks served by [OpenEnv](https://github.com/huggingface/OpenEnv), rollouts in HF sandboxes, tool calls screened by [safeagents](https://github.com/huggingface/safeagents) |
| Harness | OpenCode (`@opencode/cli` 2.2.7) |
| Tasks | 750 [scale800](https://huggingface.co/datasets/harness-hub/scale800-harbor) tasks interleaved with 300 [TermGrade](https://huggingface.co/datasets/harness-hub/termgrade-train-harbor) tasks; 1,705 task groups trained up to this checkpoint |
| Reward | the task verifier's `correctness` (falls back to `reward`), plus a tool-efficiency bonus of weight 0.1 |
| Steps | 150 (this checkpoint); the run was stopped at step 154 of 1000 planned |
| Learning rate | 2e-5 |
| LoRA | r = 32, alpha = 64, on q, k, v, o, gate, up and down projections |
| Rollouts | 8 per task, temperature 0.8, thinking off, up to 50 agent steps and 1,800 s per rollout |
| Batch | 16 micro-batches of up to 65,536 tokens per step, rollouts up to 16 policy versions stale |
| Hardware | 2× NVIDIA B200 per harness: vLLM on one, the trainer on the other |

The training script is
[`examples/async_grpo_harbor`](https://github.com/huggingface/trl/tree/main/examples/async_grpo_harbor) in TRL.

</details>

For a full write-up, please refer to [the release blogpost](https://huggingface.co/blog/harness-adapters-at-scale).
