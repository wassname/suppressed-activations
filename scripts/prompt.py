"""Exact prompt rendering shared by experiments and notebooks. Written by Codex/gpt-5.6-sol."""

from __future__ import annotations

PREFILL_INSTRUCTION = "Complete the following fact, then explain your answer."


def find_subsequence(sequence: list[int], subsequence: list[int]) -> int:
    matches = [
        start
        for start in range(len(sequence) - len(subsequence) + 1)
        if sequence[start:start + len(subsequence)] == subsequence
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one content span, found {len(matches)}")
    return matches[0]


def assistant_prefill_input_ids(
    tokenizer, content: str, *, device: str = "cuda", instruction: str = PREFILL_INSTRUCTION,
) -> dict:
    rendered = tokenizer.apply_chat_template(
        [
            {
                "role": "user",
                "content": instruction,
            },
            {"role": "assistant", "content": content},
        ],
        tokenize=False,
        continue_final_message=True,
    )
    trimmed_content = content.rstrip()
    if rendered.endswith(content):
        pass
    elif rendered.endswith(trimmed_content):
        rendered = rendered.removesuffix(trimmed_content) + content
    else:
        raise ValueError("chat template did not end at the assistant prefill")
    content_ids = tokenizer(content, add_special_tokens=False).input_ids
    input_ids = tokenizer(rendered, add_special_tokens=False, return_tensors="pt").input_ids
    content_start = find_subsequence(input_ids[0].tolist(), content_ids)
    if tokenizer.decode(input_ids[0], skip_special_tokens=False) != rendered:
        raise ValueError("assistant-prefill chat prompt changed during tokenization")
    return {
        "input_ids": input_ids.to(device),
        "content_start": content_start,
        "content_end": content_start + len(content_ids),
        "rendered": rendered,
    }


# -- Codex/gpt-5.6-sol
