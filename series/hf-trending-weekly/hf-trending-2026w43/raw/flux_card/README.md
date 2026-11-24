---
language:
- en
license: other
license_name: flux-kommunity-license
license_link: LICENSE.md
pipeline_tag: image-to-image
library_name: diffusers
tags:
- image-generation
- image-editing
- flux
- flux-3
- black-forest-labs
---

# FLUX 3 Image Klein

![Launch gallery](./launch-gallery.jpg)

![Teaser](./teaser.jpg)

FLUX 3 Image Klein is a 5.6B open weights model for text-to-image generation and image editing. It takes a prompt and up to 10 reference images and returns one image. Text-to-image, single-reference edits and multi-reference compositions run through the same model, with Qwen3-VL-4B-Instruct as the text encoder.

The 5.6B parameter label refers to the image transformer; the text encoder is separate.

This repository holds the distilled checkpoint for generation and image editing. For fine-tuning, LoRA training and research, use [FLUX 3 Image Klein Base](https://huggingface.co/black-forest-labs/flux-3-image-klein-base).

Inference code, prompt upsampling and the bounding box format: [black-forest-labs/flux-3-image-klein](https://github.com/black-forest-labs/flux-3-image-klein) on GitHub.

**Do not use the model without a prompt upsampler.** FLUX 3 Image Klein takes full scene captions, for text-to-image, editing and layout with boxes alike; a short prompt sent as typed gives generic output. Use ours, [flux-3-image-klein-pup](https://huggingface.co/black-forest-labs/flux-3-image-klein-pup), which the reference code loads by default, or any LLM you prefer with a system prompt that expands the request into one full scene caption ([`system_prompts.json`](https://huggingface.co/black-forest-labs/flux-3-image-klein-pup/blob/main/system_prompts.json) has ours). Diffusers runs neither on its own; see [Prompt upsampling](#prompt-upsampling).

This repository includes the BF16 transformer and [FP8](https://huggingface.co/black-forest-labs/flux-3-image-klein/tree/main/variants/fp8r) and [NVFP4](https://huggingface.co/black-forest-labs/flux-3-image-klein/tree/main/variants/nvfp4) variants, together with the Qwen3-VL-4B-Instruct text encoder and image autoencoder.

| Checkpoint | Format | Steps | Guidance | Built for |
| --- | --- | --- | --- | --- |
| [Klein Base](https://huggingface.co/black-forest-labs/flux-3-image-klein-base) | undistilled, bfloat16 | 50 | 3.5 | fine-tuning, LoRA training, research |
| [Klein](https://huggingface.co/black-forest-labs/flux-3-image-klein) | distilled, bfloat16 | 16 | none | generation and editing, self-hosting; the checkpoint behind the BFL API |

## Key Features

1. Text-to-image, single-reference editing and multi-reference generation in one model.
2. Bounding boxes in the prompt. Place elements with boxes on a 0 to 1000 grid, then recolor, move, replace or remove them through the prompt. Boxes guide placement and scale; they do not constrain pixels to a hard mask.
3. Text rendering within generated images.
4. Released under the [FLUX Kommunity License](LICENSE.md). The license permits non-commercial use and provides a commercial-output exception for Qualifying Users, subject to its terms. See [License](#license) below.

## Download

Download the root BF16 distilled package, including its text encoder and image autoencoder, without downloading the quantized variants:

```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="black-forest-labs/flux-3-image-klein",
    local_dir="weights/flux-3-image-klein",
    allow_patterns=[
        "model.safetensors", "config.json", "manifest.json",
        "ae.safetensors", "text_encoder/*",
        "README.md", "LICENSE.md", "NOTICE.md",
    ],
)
```

To download a quantized distilled transformer instead, replace the three root transformer patterns (`model.safetensors`, `config.json`, and `manifest.json`) with `variants/fp8r/*` or `variants/nvfp4/*`. Keep `ae.safetensors` and `text_encoder/*` for the other components.

These files contain the model package, not a complete inference application. Use an inference implementation that supports flow-map sampling and this checkpoint format. Quantized packages need a loader that supports their format; their file size is not a measure of total GPU memory use.

## Using with reference code

The distilled checkpoint is served on the [BFL API](https://bfl.ai) as FLUX 3 Image Klein. The reference inference code is [black-forest-labs/flux-3-image-klein](https://github.com/black-forest-labs/flux-3-image-klein).

From the reference implementation checkout, install the package and download the two components the CLI loads besides this checkpoint. The CLI reads its weights from `weights/` (set `WEIGHTS_DIR` for another root), where the download above puts this repository.

```bash
pip install -e .

# safety classifier, always loaded
hf download Falconsai/nsfw_image_detection --local-dir weights/nsfw-classifier
# prompt upsampler (18.8 GB), on by default; --no-pup sends the prompt as typed, for captions written by another LLM
hf download black-forest-labs/flux-3-image-klein-pup --local-dir weights/pup

# text-to-image
python scripts/cli.py 'A chunky knitted diorama: three white cable-knit icebergs with tiny pale blue houses, a cream banner embroidered "KNITTED ICEBERG VILLAGE", a giant magenta knitted whale tail bursting from a yarn sea' \
  --model distilled --out knitted.png

# image editing; repeat --image for multiple references
python scripts/cli.py 'the same scene at night under a knitted full moon, embroidered stars above the peaks' \
  --model distilled --image knitted.png --out knitted_night.png
```

## Using with Diffusers

FLUX 3 Image Klein uses a modular pipeline. Pass `prompt` for text-to-image generation, or pass `image` with a prompt for editing; `image` can be one image or a list of reference images. The model takes full scene captions, not short prompts: a request sent as typed gives generic output. Every request below goes through the [prompt upsampler](#prompt-upsampling) first, a separate 9B model ([black-forest-labs/flux-3-image-klein-pup](https://huggingface.co/black-forest-labs/flux-3-image-klein-pup)) that the pipeline does not run on its own. Load it beside the pipeline, then generate:

```shell
pip install git+https://github.com/huggingface/diffusers.git
```

```python
import json

import torch
from diffusers import ModularPipeline
from huggingface_hub import hf_hub_download
from transformers import AutoProcessor, Qwen3_5ForConditionalGeneration

pipe = ModularPipeline.from_pretrained("black-forest-labs/flux-3-image-klein")
pipe.load_components(dtype=torch.bfloat16)
pipe.to("cuda")

pup_id = "black-forest-labs/flux-3-image-klein-pup"
processor = AutoProcessor.from_pretrained(pup_id)
upsampler = Qwen3_5ForConditionalGeneration.from_pretrained(pup_id, dtype=torch.bfloat16, device_map="auto").eval()
system_prompts = json.load(open(hf_hub_download(pup_id, "system_prompts.json")))


def upsample(prompt, images=()):
    if images:
        text = (
            "Reference images follow in order (the first image, the second image, ...).\n"
            f"User request: {prompt}\nOutput the caption."
        )
        content = [{"type": "image", "image": image} for image in images] + [{"type": "text", "text": text}]
        messages = [{"role": "system", "content": system_prompts["i2i"]}, {"role": "user", "content": content}]
    else:
        messages = [{"role": "system", "content": system_prompts["t2i"]}, {"role": "user", "content": prompt}]
    inputs = processor.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=True, return_dict=True, return_tensors="pt", enable_thinking=False
    ).to(upsampler.device)
    with torch.no_grad():
        output = upsampler.generate(**inputs, max_new_tokens=3584, do_sample=False)
    return processor.decode(output[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()


caption = upsample('A chunky knitted diorama: three white cable-knit icebergs with tiny pale blue houses, a cream banner embroidered "KNITTED ICEBERG VILLAGE", a giant magenta knitted whale tail bursting from a yarn sea')
image = pipe(prompt=caption, generator=torch.Generator().manual_seed(1), output="images")[0]
image.save("knitted.png")

night = pipe(
    prompt=upsample("the same scene at night under a knitted full moon, embroidered stars above the peaks", [image]),
    image=image,
    generator=torch.Generator().manual_seed(1),
    output="images",
)[0]
night.save("knitted_night.png")
```

### Prompt upsampling

The prompt upsampler turns a short request, together with the reference images when editing, into the full scene caption the model takes: medium and style, scene, lighting and camera, each subject with its colors, materials and position in the frame. The reference CLI runs it by default. `upsample` above runs it with Transformers: `system_prompts["t2i"]` for text-to-image, `system_prompts["i2i"]` with the references first in the user message for an edit, greedy decoding, thinking off. Its [model card](https://huggingface.co/black-forest-labs/flux-3-image-klein-pup) has the decoding settings and the layout form (`t2i_bbox`, `i2i_bbox`), which takes a list of boxes and writes the box table after the caption.

Any other LLM can take its place: give it `system_prompts["t2i"]` (or `"i2i"` with the references) as the system prompt, the request as the user message, and pass the caption it returns as `prompt`.

## Prompting
The caption controls composition; reference images anchor content, they do not lock structure.
- Always run a [prompt upsampler](#prompt-upsampling), ours or your own LLM: the model takes full scene captions (framing, subject, background, lighting), and a short prompt sent as typed gives generic output. A one-line edit instruction ("make it blue") reframes the shot.
- For edits, the [prompt upsampler](#prompt-upsampling) writes the caption from the instruction and the references: a complete caption of the reference with the edit folded in. For style, describe the attributes (palette, stroke, texture) rather than naming an artwork.
- For layout, append a JSON list of elements to the caption. Each box is `[top, left, bottom, right]` on a 0 to 1000 grid; tag the element in the caption with `<id>`:
```text
Minimalist graphic illustration featuring a black silhouette of a person <silhouette_1> centered against a solid, vibrant chartreuse background <background_1>. The figure is captured in a dynamic, mid-stride running pose, facing toward the left side of the frame. [{"id": "background_1", "bbox": [0, 0, 1000, 1000], "desc": "A flat field of neon yellow-green with a subtle paper texture and fine, organic grain."}, {"id": "silhouette_1", "bbox": [150, 150, 850, 850], "desc": "A black silhouette of a person in motion, made of dense stippled ink."}]
```
For edits by box, refer to the n-th reference as `<ref_image_n>` and give each element `from`, `src_bbox` and `tgt_bbox`; a `null` target removes it. The full format with worked examples: [Bounding boxes](https://docs.bfl.ai/flux_3/flux3_image_bounding_boxes).


## Limitations

- This model is not intended or able to provide factual information.
- While the model can output text, text rendered may be inaccurate or subject to distortion.
- As a statistical model, this checkpoint may represent or amplify biases observed in the training data.
- The model may fail to generate output that matches the prompts.
- Prompt following is heavily influenced by the prompting style. Short prompts produce generic output.
- Boxes set placement and scale, not a hard mask: an element can extend past its box, and small requested elements may not appear. Edits can change content outside the requested region.

## Hardware

Peak GPU memory with the [reference code](https://github.com/black-forest-labs/flux-3-image-klein), B200, 1024x1024, prompt upsampler off: 31 GB in BF16, 26 GB in FP8, 25 GB in NVFP4. The prompt upsampler adds about 28 GB on an 80 GB GPU.

## Out-of-scope use

See Section 4 of the [FLUX Kommunity License](LICENSE.md) for the full restrictions. They include military purposes; surveillance, including related research and development; biometric processing; unlawful, unsafe, fraudulent, defamatory, or abusive activity; generating unlawful content, including child sexual abuse material or non-consensual intimate images; violating third-party rights, including rights of publicity or digital replica rights; and using the model, its Derivatives, or its Outputs to improve another AI model that performs a function similar to a FLUX Model or Derivative.

The license also covers export controls and sanctions. Its commercial-use exception is not blanket permission for commercial fine-tuning or distribution. Consult the full license for the terms that apply to each use.

Nothing contained in this model card should be interpreted as or deemed a restriction or modification to the license the model is released under.

## Responsible AI Development

Black Forest Labs is committed to responsible model development and deployment. Prior to releasing FLUX 3 Image Klein, we evaluated and mitigated a number of risks, including child sexual abuse material (CSAM) and nonconsensual intimate imagery (NCII). For detailed information about our mitigations, evaluation processes, content provenance features, and policies, please see our post: [Capable, Open, and Safe: Combating AI Misuse](https://bfl.ai/blog/capable-open-and-safe-combating-ai-misuse). 
To report safety concerns, contact [safety@blackforestlabs.ai](mailto:safety@blackforestlabs.ai).

## License

This model is released under the [FLUX Kommunity License v.1.0](LICENSE.md): non-commercial use, plus commercial output generation by Qualifying Users with less than US$5M in gross annualized revenue, including affiliates, subject to the license terms. For other uses, see [commercial licensing](https://bfl.ai/licensing).

The Qwen3-VL-4B-Instruct text encoder is under [Apache-2.0](text_encoder/LICENSE).

## Trademarks and IP

Use of Black Forest Labs and FLUX trademarks requires prior written permission, except for required attribution or necessary descriptive references. Use must not cause confusion or imply sponsorship or endorsement. Third-party trademarks remain subject to their owners' policies.

## Citation

If you use FLUX 3 Image in your work, please cite:

```bibtex
@misc{bfl2026flux3image,
  author       = {{Black Forest Labs}},
  title        = {{FLUX} 3 Image Klein},
  year         = {2026},
  url          = {https://bfl.ai/blog/flux-3-image-klein},
}