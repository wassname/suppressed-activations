"""Saved spider-demo input and reader-facing table formatting. — PI/OpenAI"""
import json

from tabulate import tabulate

from . import ROOT

DEMO = json.loads((ROOT / "results/spider_demo.json").read_text())
READ = DEMO["prompt"].split("\n")


def format_table(data):
    def mark(word):
        meaning = data["gloss"].get(word, word).lower()
        if meaning in {"spider", "spiders"}:
            return f"**{word}**"
        if meaning in {"eight", "8", "-eight", "_eight"}:
            return f"*{word}*"
        return word

    rows = [["**input**", "<br>".join(data["prompt"].split("\n")),
             "<br>".join(data["reader_translation"])]]
    for i, readout in enumerate(data["readouts"]):
        words = readout["words"]
        rows.append([("**thoughts**, layer " if i == 0 else "layer ") + str(readout["layer"]),
                     "⟨" + " ".join(mark(w) for w in words) + "⟩",
                     "⟨" + " ".join(mark(data["gloss"].get(w, w)) for w in words) + "⟩"])
    rows.append(["**output**", mark(data["answer"]), mark(data["gloss"].get(data["answer"], data["answer"]))])
    return tabulate(rows, ["", "model", "English, for the reader"], "pipe", colalign=("left", "left", "left"))
