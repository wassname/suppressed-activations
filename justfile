# Score every transform and write out/<timestamp>_leaderboard/leaderboard.md (one GPU)
score:
    uv run scripts/challenge/score.py

# Score an open-method adapter without changing the geometry table. — PI/OpenAI
score-open adapter:
    uv run scripts/challenge/score_open.py {{quote(adapter)}}

# Replot saved notebook data without model inference. — PI/OpenAI
plot-layers run:
    uv run --with matplotlib scripts/challenge/plot_layers.py {{quote(run)}}

# Rebuild data/challenge/words.json (downloads the MUSE dictionaries; words.json is already committed)
word-lists:
    uv run scripts/challenge/make_word_lists.py

# Render README.qmd to Markdown and HTML (citations, figure numbers). — PI/OpenAI
docs:
    quarto render README.qmd --to all
    quarto pandoc README.md -f gfm -t gfm --wrap=none --lua-filter docs/flatten-xref.lua -o README.md
    sed -i 's/\\[[]/[/g; s/\\[]]/]/g' README.md
