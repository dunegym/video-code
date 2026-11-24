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
- pi
pipeline_tag: image-text-to-text
---

![](banner.png)

A LoRA adapter for [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B), trained with reinforcement learning to work as the model
behind the [pi](https://github.com/earendil-works/pi) coding agent on software-engineering and terminal tasks.

> [!Tip]
> **Most of the gain of maximum-effort thinking, at a quarter of the tokens.** With thinking off, this adapter
> matches the base model thinking at its highest reasoning effort (`xhigh`) on Terminal-Bench 2.1 (56.6% vs 54.2%),
> and gets 25 of thinking's 35 points on SWE-bench Pro (64.7% vs 74.5%), while generating about 4.5× fewer tokens per
> task. See [Thinking vs no thinking](#thinking).

- **SWE-bench Pro (hard 51):** 39.2% → 64.7% (+25.5 points; 15 tasks newly solved, 2 lost).
- **Terminal-Bench 2.1:** 39.5% → 55.8% (+16.3 points; 16 newly solved, 2 lost).
- **Close to thinking-level accuracy, without thinking:** level with the base model at its highest reasoning effort
  on Terminal-Bench 2.1, 10 points behind on SWE-bench Pro, with about 4.5× fewer generated tokens.
- **Less work per task:** under half the turns of the base model on the tasks both solve.

> [!Note]
> All results are under the pi harness: one attempt per task, a 100-step budget, thinking off unless stated, text only
> (the vision tower is not served), sampling at temperature 0.8 with top-p 1.0 (the training sampling). Base model and
> adapter always run under identical settings. These numbers are not comparable with the ones on the
> [Qwen3.8-27B card](https://huggingface.co/Qwen/Qwen3.8-27B), which uses other harnesses (Terminus, Claude Code),
> thinking at maximum effort, larger budgets and the full SWE-bench Pro.

Full recipe will be shared in [the release blogpost](https://huggingface.co/blog/harness-adapters-at-scale) for anyone to build their own harness adapter.

**Pick your setup**

[![Results](https://img.shields.io/badge/results-pass%401_%2B_efficiency-555?style=flat)](#results)
[![transformers](https://img.shields.io/badge/serve-transformers-ffd21e?style=flat)](#use-with-transformers)
[![vLLM](https://img.shields.io/badge/serve-vLLM-30A2FF?style=flat)](#use-with-pi)
[![llama.cpp](https://img.shields.io/badge/run-llama.cpp-1f1f1f?style=flat)](#use-with-llama-cpp)
[![Llama.app](https://img.shields.io/badge/macOS-Llama.app-7f7f7f?style=flat)](#run-with-llama-app)
[![GGUF](https://img.shields.io/badge/download-GGUF-ff9d0b?style=flat)](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted-GGUF)
[![Merge](https://img.shields.io/badge/merge-PEFT-ffd21e?style=flat)](#merge)
[![Training](https://img.shields.io/badge/training-recipe-4b44c4?style=flat)](#training)
[![Trajectories](https://img.shields.io/badge/trajectories-bucket-ff9d0b?style=flat)](#trajectories)


A real SWE-bench Pro task under pi: the base model searches and re-runs snippets until it hits the
100-step limit; this adapter finds the function, edits it, runs the tests and fixes the last case, in 8 tool calls.

![](trajectory.gif)

<details>
<summary>Still version, and the task</summary>

![](trajectory.png)

Task: `instance_ansible__ansible-d62496fe416623e88b90139dc7917080cb04ce70` from SWE-bench Pro (hard 51), fix
`human_to_bytes`. Both runs are from the evaluation above: the base model was graded 0, this adapter 1. Each line is one
tool call as the trajectory recorded it, cut to fit.

</details>

<a id="results"></a>

## Results

![](card-pi.png)

| Benchmark | Qwen3.8-27B  | Qwen3.8-27B, `xhigh` thinking | **Qwen3.8-27B-pi-adapted** | Qwen3.8-27B-pi-adapted, `xhigh` thinking |
|---|---|---|---|---|
| SWE-bench Pro (hard 51) | 39.2% | 74.5% | **64.7%** | 74.5% |
| Terminal-Bench 2.1 | 41.0% | 54.2% | **56.6%** | 56.6% |

On Terminal-Bench 2.1 the four runs are compared on the 83 tasks all of them graded, so the base model and adapter scores differ slightly from the paired results below, which use the 86 tasks those two graded. "Thinking" is the chat template's
thinking mode at its default reasoning effort (`xhigh`).

<details open>
<summary><b>Full paired results</b> (intervals and sign tests against the base model)</summary>

One attempt per task, thinking off, paired against the base model under pi on the same tasks. The interval is 95%; the
p-value is an exact sign test on the tasks that changed outcome.

| Benchmark | Tasks | Qwen3.8-27B | Qwen3.8-27B-pi-adapted  (step 160) | Difference (points) | Newly solved / lost |
|---|---|---|---|---|---|
| SWE-bench Pro (hard 51) | 51 | 39.2% | 64.7% | +25.5 ± 14.2 | 15 / 2 (p = 0.0023) |
| Terminal-Bench 2.1 | 86 | 39.5% | 55.8% | +16.3 ± 9.1 | 16 / 2 (p = 0.0013) |
| Terminal-Bench 2.1, the 68 tasks not used to pick the checkpoint | 68 | 39.7% | 55.9% | +16.2 ± 10.6 | 13 / 2 (p = 0.0074) |

- **SWE-bench Pro (hard 51):** the 51 hardest tasks of [SWE-bench Pro](https://huggingface.co/datasets/harness-hub/swebench-pro-v2-hard51-harbor), 2 h and 100 agent steps per task.
- **Terminal-Bench 2.1:** all 89 tasks of [Terminal-Bench 2.1](https://huggingface.co/datasets/harborframework/terminal-bench-2.1), 1 h and 100 agent steps per task.

Step 160 was picked by looking at the checkpoints' scores on SWE-bench Pro and on an 18-task subset of Terminal-Bench
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
| SWE-bench Pro | 18 | 23 / 59 | 3.5k / 0.6k | 0 / 0 | 6.9k / 9.6k |
| Terminal-Bench 2.1 | 32 | 8 / 18 | n/a | 0 / 0 | 1.5k / 2.9k |
| **vs the base model with thinking** | | | | | |
| SWE-bench Pro | 27 | 27 / 74 | 3.5k / 1.3k | 0 / 34.8k | 8.8k / 46.7k |
| Terminal-Bench 2.1 | 35 | 8 / 18 | 0.9k / 0.8k | 0 / 9.9k | 1.4k / 11.6k |

- Against the base model, the adapter writes short reasoning between tool calls (about 160 tokens per turn against
  about 10) and needs less than half the turns.
- Against the base model with thinking, nearly all the difference is reasoning: the adapter reaches the same answers
  without it.
- Content for the base model on Terminal-Bench 2.1 is not available: its run's traces were not kept.

</details>

<a id="thinking"></a>

<details open>
<summary><b>Thinking vs no thinking</b></summary>

| | SWE-bench Pro (hard 51) | Terminal-Bench 2.1 |
|---|---|---|
| This adapter vs the base model with thinking (tasks only one solves) | 6 / 11 (p = 0.33) | 12 / 10 |
| Generated tokens per task (median), base model with thinking / this adapter | 48.8k / 9.4k* | 16.5k / 3.7k |
| Model calls per task (median), base model with thinking / this adapter | 61 / 21 | 19 / 9 |
| This adapter with thinking vs without (tasks only one solves) | 8 / 3 (p = 0.23) | 9 / 9 |

On Terminal-Bench 2.1 the adapter without thinking is level with the base model thinking. On SWE-bench Pro, thinking
takes the base model further (74.5% against the adapter's 64.7%; not significant on 51 tasks), at about 4.5× the
tokens and 3× the model calls. With thinking on, the adapter reaches the same 74.5%. Thinking runs use the template's
default reasoning effort (`xhigh`) and up to 32k output tokens per model call.

\* Counted from the trajectories: the server's token counts are missing for a third of the SWE-bench Pro thinking
rollouts, mostly long ones.

</details>

<details>
<summary><b>Evaluation checks</b></summary>

- **Correction, thinking on.** An earlier version of this card reported 64.7% (base model) and 66.7% (this adapter) on
  SWE-bench Pro with thinking on. pi then capped each model call at 16k output tokens, which cut long reasoning short.
  We reran both with the 32k cap used everywhere else; the numbers above (74.5% for both) are the corrected ones.
  Thinking-off results were not affected.
- **Correction, tunnel.** An earlier version of this card reported 29.4% → 62.7% on SWE-bench Pro. Nine of the base
  model's rollouts there had failed because the public tunnel between the sandboxes and the model server went down
  mid-run. We now check every rollout for this and reran all affected ones, on both sides; the numbers above are the
  corrected ones.
- **Budget and time.** The base model often works until it runs out of its 100 model calls: on SWE-bench Pro, 20 of its
  31 failed attempts ended this way, against none for this adapter. With thinking on, Terminal-Bench sessions often hit
  the one-hour limit (18 of the base model's 39 failed attempts). Limits are the same for every run, so the comparisons
  are fair, but part of the adapter's gain is finishing within them. pi never ran out of the 131,072-token context.
- **Network access.** The sandboxes had internet access. Calls outside the task were almost all dependency lookups (a
  module path or version a task needed); we found no attempt by this adapter to look up a task's upstream fix.
- **Test files.** Agents, the base model and this adapter alike, sometimes write or edit test files while working,
  mostly their own scratch scripts to check a change. This cannot affect a grade: SWE-bench Pro's grader resets all test
  files and applies the official tests before running them, and Terminal-Bench's tests are copied in only at grading.
  We found no tampering with tests or the verifier.
- **Hidden reasoning.** The adapter's visible reasoning is plain text: `<think>` tags appear in its output in fewer than
  1 turn in 1,000, and with thinking off the template never opens a thinking block.

</details>

<a id="trajectories"></a>

## Evaluation trajectories

Every evaluation attempt behind this card, solved or not, is in the
[harness-hub/harness-adapters-trajectories](https://huggingface.co/buckets/harness-hub/harness-adapters-trajectories)
bucket: base model and adapter, thinking on and off, on both benchmarks, with each attempt's grade, trajectory, harness
log and verifier output, scrubbed of secrets. The files carry canary strings: keep them out of training data.

<a id="use-with-pi"></a>

## Use with pi

<details open>
<summary><b>Serve the adapter with vLLM and point pi at it</b></summary>

### 1. Serve the adapter with vLLM

```sh
vllm serve Qwen/Qwen3.8-27B \
    --enable-lora --max-lora-rank 32 \
    --lora-modules qwen3.8-pi=harness-hub/Qwen3.8-27B-pi-adapted \
    --language-model-only --enable-prefix-caching --mamba-cache-mode align \
    --enable-auto-tool-choice --tool-call-parser qwen3_xml --reasoning-parser qwen3 \
    --default-chat-template-kwargs '{"enable_thinking": false}' \
    --max-model-len 131072
```

This is the configuration of the evaluations. Thinking off is what the adapter was trained for: with it on, it
generates about 4× more tokens for at most a few more solved tasks. Prefix caching on this hybrid model needs
`--mamba-cache-mode align`; without it, every agent turn re-reads its whole history.

### 2. Point pi at it

Install pi (Node.js 22.19 or newer):

```sh
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

Add the server to `~/.pi/agent/models.json`:

```json
{
  "providers": {
    "local": {
      "baseUrl": "http://localhost:8000/v1",
      "api": "openai-completions",
      "apiKey": "dummy",
      "models": [{ "id": "qwen3.8-pi" }]
    }
  }
}
```

`"api": "openai-completions"` matters: without it pi uses the Responses API, which this adapter was not trained or
evaluated with.

```sh
pi --provider local --model qwen3.8-pi --print "Find out why the tests in tests/test_parser.py fail and fix the bug."
```

</details>

<a id="use-with-transformers"></a>

## Use with pi (transformers serve)

<details open>
<summary><b>Serve with transformers and point pi at it</b></summary>

[`transformers serve`](https://huggingface.co/docs/transformers/en/serve-cli/serving) is a lightweight OpenAI-compatible
server, for local use and experimentation (vLLM is faster under load). It handles Qwen's tool calls out of the box.
Serve the merged checkpoint from [Merge the adapter into the base model](#merge):

```sh
pip install "transformers[serving]"
transformers serve ./Qwen3.8-27B-pi-merged --dtype bfloat16 --continuous-batching --reasoning off
```

`--reasoning off` keeps thinking off, as in training. The server listens on `http://localhost:8000`, so the pi
configuration from [the vLLM section](#use-with-pi) works as is, with the model `id` set to the name the server
serves, here `./Qwen3.8-27B-pi-merged`:

```sh
pi --provider local --model ./Qwen3.8-27B-pi-merged --print "Find out why the tests in tests/test_parser.py fail and fix the bug."
```

</details>

<a id="use-with-llama-cpp"></a>

## Use with pi (llama.cpp)

<details open>
<summary><b>Serve the GGUF adapter with llama.cpp and point pi at it</b></summary>

The GGUF version of Qwen3.8-27B-pi-adapted is in [harness-hub/Qwen3.8-27B-pi-adapted-GGUF](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted-GGUF). It runs on top of a GGUF of the base model:

```sh
hf download ggml-org/Qwen3.8-27B-GGUF Qwen3.8-27B-Q8_0.gguf --local-dir .
hf download harness-hub/Qwen3.8-27B-pi-adapted-GGUF Qwen3.8-27B-pi-lora-F16.gguf --local-dir .

llama serve -m Qwen3.8-27B-Q8_0.gguf --lora Qwen3.8-27B-pi-lora-F16.gguf \
    --chat-template-kwargs '{"enable_thinking": false}' -c 65536 --port 9931 --alias qwen3.8-pi
```

Then point pi at it with the [pi-llama](https://github.com/huggingface/pi-llama) extension:

```sh
pi install git:github.com/huggingface/pi-llama
pi --model llama-cpp/qwen3.8-pi
```

The adapter was trained on the BF16 weights: the closer the base GGUF is to them, the closer you get to the trained
behavior. `Q8_0` is a good default; lower-bit quants drift further. The GGUF version has not been re-evaluated.

</details>

<a id="run-with-llama-app"></a>

## Run it with Llama.app (macOS)

<details open>
<summary><b>Load the GGUF adapter on top of a Qwen3.8-27B GGUF</b></summary>

1. Install [Llama.app](https://github.com/ggml-org/Llama-macOS) and launch it once. On first launch it creates `~/.config/llama/models.user.ini`.
2. Download the adapter and register the model:

   ```sh
   LORA=$(hf download harness-hub/Qwen3.8-27B-pi-adapted-GGUF Qwen3.8-27B-pi-lora-F16.gguf)
   cat >> ~/.config/llama/models.user.ini <<EOF

   [harness-hub/Qwen3.8-27B-pi]
   hf-repo = unsloth/Qwen3.8-27B-GGUF:Q4_K_XL ; This is just an example but you can also use any GGUF that is derived from Qwen3.8-27B 
   lora = $LORA
   temp = 0.7
   ctx-size = 32768
   EOF
   ```

   `hf-repo` sets the base model: the app downloads it on first use, about 17 GB. To use another quant of the same base, change the part after the colon, for example `:Q8_0`.
3. Restart Llama.app and choose **harness-hub/Qwen3.8-27B-pi** from the model list.

You can also use it through the app's OpenAI-compatible server. Llama.app shows the port; the example below uses 9931:

```sh
curl localhost:9931/v1/chat/completions -d '{"model":"harness-hub/Qwen3.8-27B-pi","messages":[{"role":"user","content":"hi"}]}'
```

The adapter must be loaded on top of Qwen3.8-27B. It does not work with other base models.

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
model = PeftModel.from_pretrained(base, "harness-hub/Qwen3.8-27B-pi-adapted").merge_and_unload()
model.save_pretrained("Qwen3.8-27B-pi-merged")
AutoTokenizer.from_pretrained("harness-hub/Qwen3.8-27B-pi-adapted").save_pretrained("Qwen3.8-27B-pi-merged")
```

Then serve it like the base model, without the LoRA flags:

```sh
vllm serve Qwen3.8-27B-pi-merged --served-model-name qwen3.8-pi \
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
| Harness | pi |
| Tasks | 750 [scale800](https://huggingface.co/datasets/harness-hub/scale800-harbor) tasks interleaved with 300 [TermGrade](https://huggingface.co/datasets/harness-hub/termgrade-train-harbor) tasks; 1,919 task groups trained up to this checkpoint |
| Reward | the task verifier's `correctness` (falls back to `reward`), plus a tool-efficiency bonus of weight 0.1 |
| Steps | 160 (this checkpoint); the run was stopped at step 191 of 1000 planned |
| Learning rate | 2e-5 |
| LoRA | r = 32, alpha = 64, on q, k, v, o, gate, up and down projections |
| Rollouts | 8 per task, temperature 0.8, thinking off, up to 50 agent steps and 1,800 s per rollout |
| Batch | 16 micro-batches of up to 65,536 tokens per step, rollouts up to 16 policy versions stale |
| Hardware | 2× NVIDIA B200 per harness: vLLM on one, the trainer on the other |

The training script is
[`examples/async_grpo_harbor`](https://github.com/huggingface/trl/tree/main/examples/async_grpo_harbor) in TRL.

Below is an animated training curve of the evolution of the number of tool calls on the train set:

![](train-tool-calls.gif)

</details>

For a full write-up, please refer to [the release blogpost](https://huggingface.co/blog/harness-adapters-at-scale).
