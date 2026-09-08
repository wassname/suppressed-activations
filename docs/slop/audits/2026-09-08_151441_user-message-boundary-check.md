# User-message boundary check

Codex, 2026-09-08. CPU tokenizer check, not a behavioral result.

The previous `chat-instructed` branch in `scripts/oat_sweep.py` omitted the supplied instruction when calling `chat_input_ids`. The helper reports the end of user text, before the assistant generation prefix. The runner used that boundary for extraction and intervention.

The runner now uses `render_input` for both extraction and generation. It passes the supplied instruction, retains `user_content_end`, and sets its intervention boundary to the full input length. The shared helper keeps its original user-content boundary for other consumers. The assistant-prefill path is unchanged.

## Observed CPU check

The test imported the actual runner's `render_input` and the pinned Qwen/Qwen3.5-4B tokenizer, revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`, with `local_files_only=True`. No model weights or GPU inference were used.

Input content was `Question: How many legs does the {animal} have? `, including a trailing space. Instruction was `Answer the question first.`. The spider rendering was:

```python
'<|im_start|>user\nAnswer the question first.\n\nQuestion: How many legs does the spider have? <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

The check printed:

```text
{'animal': 'spider', 'user_end': 20, 'generation_end': 29, 'patched_suffix': [271, 248069, 271]}
{'animal': 'dog', 'user_end': 20, 'generation_end': 29, 'patched_suffix': [271, 248069, 271]}
{'animal': 'ant', 'user_end': 20, 'generation_end': 29, 'patched_suffix': [271, 248069, 271]}
PASS: actual runner renderer honors instructions, preserves trailing spaces and assistant-prefill IDs, and aligns the final three generation-boundary tokens.
```

Assertions checked that the exact instruction and content occur once, changing the instruction changes input IDs, and the assistant-prefill IDs equal the original helper's IDs. The user end precedes the full prompt end for every species. All species have the same final three token IDs.

## Limits and next test

This verifies instruction forwarding and token positions. It does not prove clean answers, coherent steering, or a valid readout. The new comparison changes question role and fixes the intervention boundary; it must not be labelled wrapper-only. Template extraction also moves to the generation boundary. Existing queued assistant-prefill jobs keep their original prompt behavior.

Next: run clean source, clean donor and the fixed L22-24 C2 intervention through this path. Inspect complete generations before interpreting bare-token scores. The default GPU queue was paused at the time of this check, so no new behavioral result is claimed.

Jobs 778 (dog) and 779 (ant) were subsequently queued without resuming the group. They retain the questions, extraction/evaluation instructions, L22-24 C2 and 128-token generation limit from jobs 768/771. They change the prompt mode to `chat-instructed`, including the repaired boundary. Output paths are `out/2026-09-08_151650_user-boundary-dog-legs` and `out/2026-09-08_151650_user-boundary-ant-legs`.

The condition renderer was separately tested against the stored ant band condition 009 in `out/2026-09-08_133000_synchronized-band-ant/result.json`. Exact token-ID previews show 32 tokens from each of the 70-token steered, 61-token Base and 60-token donor continuations. The report labels each total and links the full raw data. It does not truncate generation or change historical files. -- Codex

## Independent source review

Codex/GPT-6 subagent reviewed the actual diff and its position consumers. No blocking position error was found for the planned final-three-token continuous intervention. The CPU test results above were supplied by the root agent; this review did not rerun them.

`sample` calls the tested `render_input` for both generation and extraction. For user-message modes, `content_end` now equals the input length. `subspace` reads the suffix ending at that boundary. Template extraction reads `[content_end-3:content_end]`. The synchronized intervention passes `content_end-1` to a hook that adds one before taking the three-position slice. Thus the prefill patch is exactly `[N-3:N]`, with no off-by-one shift. Cached decode uses one-token input and donor position zero. The shared `chat_input_ids` retains its original content boundary, so existing delayed-readout extraction keeps its prior positions.

The assistant-prefill branch still calls the same helper with the same instruction. Passing `.to("cuda")` instead of `.cuda()` retains the default device behavior. The new instruction forwarding is necessary because the old `chat-instructed` branch ignored that argument.

Scope limit: `content_end` also defines lexical scan limits and the `intervention_positions="all"` span. In user-message modes those spans now include the assistant prefix. This does not block the planned final-three-token run, but those other modes need their own interpretation. Matching suffix token IDs verifies alignment, not the semantic validity of the extracted subspace. Correct Base/donor answers and complete steering coverage remain the next runtime tests.
