"""CPU position audit: where do the patched prefill spans land? -- PI/OpenAI"""
import json
import sys

sys.path.insert(0, "scripts")
from prompt import assistant_prefill_input_ids  # noqa: E402
from transformers import AutoTokenizer  # noqa: E402

TOK = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", trust_remote_code=True)
CASES = {
    "fixed-dog-legs": ("Question: How many legs does the animal that spins webs have?\nAnswer: ",
                        "Answer the question with the answer first. Then describe the animal in three sentences."),
    "fixed-ant-legs": ("Question: How many legs does the animal that spins webs have?\nAnswer: ",
                        "Answer the question with the answer first. Then describe the animal in three sentences."),
    "fixed-dog-name": ("Question: What is the animal that spins webs called?\nAnswer: ",
                        "Answer the question with the answer first. Then describe the animal in three sentences."),
    "fixed-ant-name": ("Question: What is the animal that spins webs called?\nAnswer: ",
                        "Answer the question with the answer first. Then describe the animal in three sentences."),
}
for name, (content, instruction) in CASES.items():
    r = assistant_prefill_input_ids(TOK, content, device="cpu", instruction=instruction)
    ids = r["input_ids"][0].tolist()
    n = len(ids)
    span = (n - 3, n)
    toks = [TOK.decode([i]) for i in ids]
    print(f"### {name}: n={n} content=[{r['content_start']},{r['content_end']}) patched={list(range(*span))}")
    print("  last-6 tokens:", [repr(t) for t in toks[-6:]])
    print("  patched decodes:", [repr(t) for t in toks[span[0]:span[1]]])
    print("  content tail:", [repr(t) for t in toks[r['content_start']:r['content_end']]][-4:])
    for d, cond in (("fixed-band-dog-legs", "009"), ("fixed-band-ant-legs", "009"),
                    ("fixed-band-dog-name", "009"), ("fixed-band-ant-name", "009")):
        pass
# recorded spans
import glob
for f in sorted(glob.glob("out/2026-09-08_134000_fixed-band-*/result.json")):
    d = json.load(open(f))
    row = [x for x in d["rows"] if "009_" in x["condition_id"]][0]
    print(f.split("/")[1], "recorded:", {k: v["prefill_positions"] for k, v in row["intervention_record"].items()})
