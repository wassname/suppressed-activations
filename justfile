# Score every transform and write out/<timestamp>_leaderboard/leaderboard.md (one GPU)
score:
    uv run scripts/eval/score.py

# Score an unrestricted-method adapter with resource disclosures. — PI/OpenAI
score-unrestricted adapter:
    uv run scripts/eval/score_unrestricted.py {{quote(adapter)}}

# Rebuild the two leaderboards without model inference. — PI/OpenAI
results:
    uv run scripts/docs/results.py
    uv run scripts/docs/spider_demo.py

# Replot saved notebook data without model inference. — PI/OpenAI
plot-layers evidence="results/layer_plot.json.gz":
    uv run --with matplotlib scripts/plots/layers.py {{quote(evidence)}}

# Redraw the compact spider demo without inference. — PI/OpenAI
plot-cartoon:
    uv run --with matplotlib scripts/plots/cartoon.py

# Rebuild data/challenge/words.json (downloads the MUSE dictionaries; words.json is already committed)
word-lists:
    uv run scripts/data/build_word_lists.py

# CPU regression and syntax checks. — PI/OpenAI
check:
    uv run python -m unittest discover -s tests/regression -v
    uv run python -m compileall -q src scripts/data scripts/docs scripts/eval scripts/plots nbs

# Render README.qmd to Markdown and HTML (citations, figure numbers). — PI/OpenAI
docs:
    quarto render README.qmd --to all
    quarto pandoc README.md -f gfm -t gfm --wrap=none --lua-filter docs/readme/flatten-xref.lua -o README.md
    sed -i 's/\\[[]/[/g; s/\\[]]/]/g' README.md
