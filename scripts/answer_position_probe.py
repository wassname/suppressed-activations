"""Answer-position displacement probe.

Does the C-steered intervention move the L20 answer-position residual along d_act?

For a property prompt (spider source, animal target): compute the runner's span-correction
delta (prose delta) and d_act (activation answer-direction = mean L20 last-1 residual,
target - spider). Apply the patch at L20 prefill last-3, read the answer-position residual
h_answer (= patched residual at position content_end-1), and report:
  (a) cosine(delta, d_act): does the prose delta point along the decision direction;
  (b) displacement <h_C - h_C0, d_act_hat> / ||d_act||: does the patch push toward target.
Run C=0 and C=Ctarget (the cell under test) for an animal. Positive control = the animal's
transfer cell.

Usage: uv run --with pyarrow --with loguru --with accelerate scripts/answer_position_probe.py
       [--prompt '...'] [--target-prompt '...'] [--c-target 1.5] [--out ap.json]
"""
import sys, json, argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import torch
from scripts.oat_sweep import load_bundle, attenuation_basis, CONCEPT_TEMPLATES
from scripts.demo import trajectory
from scripts.prompt import assistant_prefill_input_ids
from suppressed_activation_subspace import component

INS = "Complete the following fact. Then describe the animal in three sentences."


def build_u_delta(b, target, peak, output):
    """U (span) and delta (prose delta) from the NAMING CONCEPT_TEMPLATES. Unchanged."""
    model, tokenizer, final_norm = b["model"], b["tokenizer"], b["final_norm"]
    device = b["device"]
    peaks, outs = [], []
    dl = []
    for tmpl in CONCEPT_TEMPLATES:
        pair = []
        for animal in ("spider", target):
            pre = assistant_prefill_input_ids(tokenizer, tmpl.format(animal=animal), device=device, instruction=INS)
            with torch.no_grad():
                res = trajectory(model, pre["input_ids"], final_norm)[0]
            end = pre["content_end"]
            seg = res[:, end - 3:end].float()
            pair.append(seg)
        peaks.append(pair[1][peak].mean(0) - pair[0][peak].mean(0))
        outs.append(pair[1][output].mean(0) - pair[0][output].mean(0))
    P, O = torch.stack(peaks), torch.stack(outs)
    U, _ = attenuation_basis(P, O, 4)
    # delta from the naming template last-position contrast (independent of property prompt)
    dl = []
    for tmpl in CONCEPT_TEMPLATES:
        s = assistant_prefill_input_ids(tokenizer, tmpl.format(animal="spider"), device=device, instruction=INS)
        t = assistant_prefill_input_ids(tokenizer, tmpl.format(animal=target), device=device, instruction=INS)
        with torch.no_grad():
            rs = trajectory(model, s["input_ids"], final_norm)[0]
            rt = trajectory(model, t["input_ids"], final_norm)[0]
        dl.append((rt[peak, rt.shape[1]-1] - rs[peak, rs.shape[1]-1]))
    delta_full = torch.stack(dl).mean(0).float()
    delta_proj = component(delta_full, U)
    delta = delta_proj * delta_full.norm() / delta_proj.norm()
    return U, delta


def d_act_property(b, src_prompt, tgt_prompt, peak):
    """d_act from CLEAN forward passes of the PROPERTY source/target prompts at the answer
    position (content_end - 1, L20), no patch, no U. Independent of the naming delta."""
    model, tokenizer, final_norm = b["model"], b["tokenizer"], b["final_norm"]
    device = b["device"]
    s = assistant_prefill_input_ids(tokenizer, src_prompt, device=device, instruction=INS)
    t = assistant_prefill_input_ids(tokenizer, tgt_prompt, device=device, instruction=INS)
    with torch.no_grad():
        rs = trajectory(model, s["input_ids"], final_norm)[0]
        rt = trajectory(model, t["input_ids"], final_norm)[0]
    d = rt[peak, rt.shape[1]-1].float() - rs[peak, rs.shape[1]-1].float()
    return d


def h_answer_at(b, prompt, U, delta, C, peak):
    """Patched answer-position residual at L20 (last-1) for a given C. Returns the residual."""
    model, tokenizer, final_norm = b["model"], b["tokenizer"], b["final_norm"]
    device = b["device"]
    pre = assistant_prefill_input_ids(tokenizer, prompt, device=device, instruction=INS)
    with torch.no_grad():
        res = trajectory(model, pre["input_ids"], final_norm)[0]
    end = pre["content_end"]
    h = res[peak, end - 1].float()
    span = component(h, U)
    patched = h + C * (delta - span)
    return patched, h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)          # spider source property prompt
    ap.add_argument("--target-prompt", required=True)   # target property prompt (for delta target)
    ap.add_argument("--target", default="dog")
    ap.add_argument("--c-target", type=float, default=1.5)
    ap.add_argument("--out", default="answer_position.json")
    ap.add_argument("--peak-layer", type=int, default=20)
    ap.add_argument("--output-layer", type=int, default=32)
    args = ap.parse_args()

    b = load_bundle()
    U, delta = build_u_delta(b, args.target, args.peak_layer, args.output_layer)
    d_act = d_act_property(b, args.prompt, args.target_prompt, args.peak_layer)
    dh = d_act / (d_act.norm() + 1e-12)
    hCs = h_answer_at(b, args.prompt, U, delta, args.c_target, args.peak_layer)[0]
    hC0 = h_answer_at(b, args.prompt, U, delta, 0.0, args.peak_layer)[0]
    disp = float((hCs - hC0) @ dh)
    cos_delta_dact = float((delta @ d_act) / (delta.norm() * d_act.norm() + 1e-12))
    d_act_inspan = float(((U @ U.T) @ d_act).norm() / (d_act.norm()+1e-12))
    out = {"target": args.target, "c_target": args.c_target,
           "cos_delta_dact": cos_delta_dact,
           "displacement_along_dact": disp,
           "d_act_norm": float(d_act.norm()), "delta_norm": float(delta.norm()),
           "d_act_inspan": d_act_inspan,
           "circular_check_cos_eq_inspan": abs(cos_delta_dact - d_act_inspan) < 1e-3}
    print(f"{args.target} C={args.c_target}: cos(delta,d_act)={cos_delta_dact:.4f} disp={disp:.4f} "
          f"d_act_norm={float(d_act.norm()):.3f} delta_norm={float(delta.norm()):.3f} "
          f"d_act_inspan={d_act_inspan:.4f} CIRCULAR={out['circular_check_cos_eq_inspan']}")
    Path(args.out).write_text(json.dumps(out, indent=1) + "\n")
    print("wrote", args.out)


if __name__ == "__main__":
    main()
