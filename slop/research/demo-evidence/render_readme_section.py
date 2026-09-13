#!/usr/bin/env python3
"""Regenerate the README 'Full continuations: dog and ant' section from the
demo-evidence snapshots (byte-exact strings; run from the main repo root).
-- PI[glm-5p3-flash]"""
import json
from pathlib import Path

d = json.load(open("slop/research/demo-evidence/legs-dog.json"))
a = json.load(open("slop/research/demo-evidence/legs-ant.json"))
SRC = d["rendered_source_prompt"]
assert a["rendered_source_prompt"] == SRC
BASE = d["base_generation"]["text"]
DOG = d["steered_generation"]["text"]
ANT = a["steered_generation"]["text"]
DONOR_D = d["rendered_donor_prompt"]
DONOR_A = a["rendered_donor_prompt"]


def block(s):
    return f"```text\n{s}\n```"


def src_block():
    return (
        "Input (full rendered source prompt, multiline, special tokens included; the\n"
        "prompt ends with one trailing ASCII space after `Answer:`):\n\n"
        f"{block(SRC)}\n\n"
        "<details>\n"
        "<summary>Same prompt as <code>repr</code> (shows the trailing space explicitly)</summary>\n\n"
        f"```text\n{SRC!r}\n```\n\n"
        "</details>"
    )


def donor_block(p):
    return (
        "<details>\n"
        "<summary>Separate donor input used to extract the component</summary>\n\n"
        f"{block(p)}\n\n"
        f"```text\n{p!r}\n```\n\n"
        "</details>"
    )


section = f"""## Full continuations: dog and ant

<!-- New prose in this section written by PI/GLM-5p3-flash, 2026-09-13, on the user's
request. Exact strings are byte-verbatim snapshots; see slop/research/demo-evidence/. -->

A different experiment from the C=4 demo above: a separate layer-20 (h20) run with
tuned settings (rank 8, detector layers 18/20/32, three token positions, strength
1.5; edit `h' = h + C(Δ − U Uᵀ h)` with no component-norm matching and no residual
renormalization in the executed branch). The source question is never changed; each
donor input is used only to extract the intervention component. The think block in
the rendered prompts below is part of the input template, not generated reasoning.

### Base (source prompt, no intervention)

{src_block()}

Generation (58 tokens, verbatim, ends with `<|im_end|>`):

{block(BASE)}

### Dog intervention

The source prompt is repeated unchanged; the component comes from the dog input.

{src_block()}

{donor_block(DONOR_D)}

Generation after intervention (65 tokens, verbatim, ends with `<|im_end|>`):

{block(DOG)}

### Ant intervention

The source prompt is repeated unchanged; the component comes from the ant input.

{src_block()}

{donor_block(DONOR_A)}

Generation after intervention (65 tokens, verbatim, ends with `<|im_end|>`):

{block(ANT)}

### Limitations

- These rows are selected illustrations from a layer and strength exploration; the
  runs were chosen after the fact as working examples, not drawn as a held-out sample.
- The frozen fresh-set evaluation for this candidate scored
  [6/12 complete successes](slop/research/demo-evidence/eval_fresh_adjudications.json)
  (random-donor control: 1/12). That is the measured rate on those 12; it is not a
  general success rate, and these replay rows are development-exposed and are not
  pooled into it.
- The dog answer's "short history" sentence is factually weak (dog domestication
  predates most recorded history).
- This layer-20 family is a separate experiment from the C=4 demo above; the results
  of the two are not pooled.
- Improving the reliability of the transfer is open work.

"""

readme = Path("README.md")
text = readme.read_text()
# replace the old-titled section if present, else insert before Limits
for old in ("## Full continuations: dog and ant",
            "## Historical full continuations: the Question family (dog and ant)"):
    if old in text:
        start = text.index(old)
        text = text[:start] + section + text[text.index("## Limits"):]
        break
else:
    text = text.replace("## Limits", section + "## Limits", 1)
readme.write_text(text)
print("section replaced; README", len(text), "chars")
