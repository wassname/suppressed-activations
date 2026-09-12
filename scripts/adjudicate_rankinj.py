# /// script
# requires-python = ">=3.12"
# dependencies = ["torch>=2.8"]
# ///
"""Categorical adjudication of the 48 rankinj continuations: answer_initial/answer_final as
categories (8/Spider/Yes/No/ambiguous/flip), requested-fact correctness, stated identity,
explicit factual errors with the relevant quotes. Mechanical counts per condition.
-- PI[glm-5p3-flash]"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

B = Path(__file__).resolve().parents[1] / "out/2026-09-12_cb-rankinj"
ANSWERS = {"legs": {"dog": "4", "ant": "6"},
           "name": {"dog": "Dog", "ant": "Ant"},
           "prop-P1-spinneret": {"dog": "No", "ant": "No"},
           "prop-P2-liveyoung": {"dog": "Yes", "ant": "No"}}
TT = {
 ("k1","legs-L1-ant"): ("8","8",True,"spider",[]),
 ("k1","legs-L1-dog"): ("8","8",True,"spider",[]),
 ("k1","legs-L2-ant"): ("8","8",True,"spider",[]),
 ("k1","legs-L2-dog"): ("8","8",True,"spider",[]),
 ("k1","name-N1-ant"): ("Spider","Spider",True,"spider",[]),
 ("k1","name-N1-dog"): ("Spider","Spider",True,"spider",[]),
 ("k1","name-N2-ant"): ("Spider","Spider",True,"spider",[]),
 ("k1","name-N2-dog"): ("Spider","Spider",True,"spider",[]),
 ("k1","prop-P1-spinneret-ant"): ("No","No",False,"spider",
    ["'Spiders do not have spinnerets' - false; the same text describes silk 'extruded through spinnerets' (self-contradiction)"]),
 ("k1","prop-P1-spinneret-dog"): ("No","No",False,"spider",
    ["'Spiders do not possess spinnerets' - false (they do)"]),
 ("k1","prop-P2-liveyoung-ant"): ("No","No",True,"spider",[]),
 ("k1","prop-P2-liveyoung-dog"): ("No","ambiguous (hedging: 'some do give birth to live young... However')",True,"spider",
    ["hedged/confused reasoning about tarantulas and 'tarantula hawk which is not a spider but a wasp'"]),
 ("k2","legs-L1-ant"): ("8","8",True,"spider",[]),
 ("k2","legs-L1-dog"): ("8","8",True,"spider",["'spiders possess two pairs of chelicerae' - false (one pair)"]),
 ("k2","legs-L2-ant"): ("8","8",True,"spider",["'two pairs of chelicerae (fangs) and two pairs of pedipalps' - false counts"]),
 ("k2","legs-L2-dog"): ("8","8",True,"spider",[]),
 ("k2","name-N1-ant"): ("Spider","Spider",True,"spider",[]),
 ("k2","name-N1-dog"): ("Spider","Spider",True,"spider",[]),
 ("k2","name-N2-ant"): ("Spider","Spider",True,"spider",[]),
 ("k2","name-N2-dog"): ("Spider","Spider",True,"spider",[]),
 ("k2","prop-P1-spinneret-ant"): ("No","FLIPS to Yes ('**Corrected Answer:** Yes, spiders have spinnerets.')",True,"spider",
    ["initial 'No' false; explicit mid-continuation answer flip No->Yes (the final = the SOURCE answer)"]),
 ("k2","prop-P1-spinneret-dog"): ("No","No",False,"spider",
    ["final 'the answer to your question is no, spiders do not have spinnerets' - FALSE (they do)"]),
 ("k2","prop-P2-liveyoung-ant"): ("No","No",True,"spider",[]),
 ("k2","prop-P2-liveyoung-dog"): ("No","No",True,"spider",["donor answer would be Yes (dogs have live birth); stayed No"]),
 ("k4","legs-L1-ant"): ("8","8",True,"spider",[]),
 ("k4","legs-L1-dog"): ("8","8",True,"spider",["'two pairs of chelicerae' - false"]),
 ("k4","legs-L2-ant"): ("8","8",True,"spider",["'two pairs of front legs and two pairs of rear legs' - garbled arrangement"]),
 ("k4","legs-L2-dog"): ("8","8",True,"spider",["'arranged in two pairs on the front of the body and two pairs on the rear' - garbled count count"]),
 ("k4","name-N1-ant"): ("Spider","Spider",True,"spider",[]),
 ("k4","name-N1-dog"): ("Spider","Spider",True,"spider",[]),
 ("k4","name-N2-ant"): ("Spider","Spider",True,"spider",[]),
 ("k4","name-N2-dog"): ("Spider","Spider",True,"spider",[]),
 ("k4","prop-P1-spinneret-ant"): ("No","No",False,"spider",["'Spiders do not possess spinnerets' - false"]),
 ("k4","prop-P1-spinneret-dog"): ("No","No",False,"spider",
    ["self-contradiction: denials followed by silk extruded through specialized openings called spinnerets"]),
 ("k4","prop-P2-liveyoung-ant"): ("No","No",True,"spider",["'some species can reproduce asexually' - false for spiders"]),
 ("k4","prop-P2-liveyoung-dog"): ("No","No",True,"spider",["repetitive not-birds/not-fish/not-reptiles listing"]),
 ("k8","legs-L1-ant"): ("8","8",True,"spider",[]),
 ("k8","legs-L1-dog"): ("8","8",True,"spider",[]),
 ("k8","legs-L2-ant"): ("8","8",True,"spider",["'two pairs of chelicerae' - false"]),
 ("k8","legs-L2-dog"): ("8","8",True,"spider",["'typically arranged in two pairs of four' - garbled count"]),
 ("k8","name-N1-ant"): ("Spider","Spider",True,"spider",[]),
 ("k8","name-N1-dog"): ("Spider","Spider",True,"spider",[]),
 ("k8","name-N2-ant"): ("Spider","Spider",True,"spider",[]),
 ("k8","name-N2-dog"): ("Spider","Spider",True,"spider",[]),
 ("k8","prop-P1-spinneret-ant"): ("No","No",False,"spider",
    ["'Spiders do not have spinnerets; instead, they possess specialized organs called spinnerets' - self-contradictory in one sentence"]),
 ("k8","prop-P1-spinneret-dog"): ("No","No",False,"spider",["'Spiders do not possess spinnerets' - false"]),
 ("k8","prop-P2-liveyoung-ant"): ("No","No",True,"spider",
    ["false cascade: 'do not have a backbone; they are chordates' (spiders are arthropods, not chordates); 'do not have a heart' - false; 'do not have eyes; they have compound eyes' - false (spiders have simple eyes)"]),
 ("k8","prop-P2-liveyoung-dog"): ("No","No",True,"spider",
    ["fabricated species 'Latrodectus hassidii'; 'They are not mammals.' repeated 15+ times (loop)"]),
}


def main() -> None:
    A = []
    for (cond, cell), (ai, af, ok, ident, errs) in TT.items():
        donor = cell.rsplit("-", 1)[1]
        if cell.startswith("prop-P1"):
            qkey = "prop-P1-spinneret"
        elif cell.startswith("prop-P2"):
            qkey = "prop-P2-liveyoung"
        else:
            qkey = cell.split("-")[0]
        donor_ans = ANSWERS[qkey][donor]
        transfer = (ai == donor_ans) or (donor_ans in str(af))
        v = ("donor-direction answer present (not persistent with identity)" if transfer
             else "no transfer (source-bound)")
        if errs and transfer:
            v += "; with factual errors"
        A.append({"condition": cond, "cell": cell, "answer_initial": ai, "answer_final": af,
                  "requested_fact_correct": ok, "stated_identity": ident,
                  "explicit_errors": errs, "donor_answer": donor_ans, "verdict": v})
    json.dump(A, open(B / "categorical_adjudication.json", "w"), indent=1, ensure_ascii=False)
    cnt = defaultdict(lambda: defaultdict(int))
    for a in A:
        c = a["condition"]
        cnt[c]["n"] += 1
        is_prop = a["cell"].startswith("prop")
        donor_ans = a["donor_answer"]
        cnt[c]["initial_donor_direction"] += int(is_prop and a["answer_initial"] == donor_ans)
        cnt[c]["final_donor_direction"] += int(is_prop and donor_ans in str(a["answer_final"]))
        cnt[c]["final_flips"] += int("FLIP" in a["answer_final"] or "flip" in a["answer_final"])
        cnt[c]["with_errors"] += bool(a["explicit_errors"])
        cnt[c]["facts_correct"] += a["requested_fact_correct"]
        cnt[c]["identity_donor"] += int(a["stated_identity"] != "spider")
    counts = {k: dict(v) for k, v in cnt.items()}
    json.dump(counts, open(B / "categorical_counts.json", "w"), indent=1)
    for c in sorted(counts):
        print(c, counts[c])


if __name__ == "__main__":
    main()
