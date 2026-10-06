# Score every transform and write out/<timestamp>_leaderboard/leaderboard.md (one GPU)
score:
    uv run scripts/challenge/score.py

# Rebuild data/challenge/words.json (downloads the MUSE dictionaries; words.json is already committed)
word-lists:
    uv run scripts/challenge/make_word_lists.py

# Render README.qmd to README.md (gfm, citations, figure numbers)
docs:
    quarto render README.qmd
    quarto pandoc README.md -f gfm -t gfm --wrap=none --lua-filter docs/flatten-xref.lua -o README.md
    sed -i 's/\\[[]/[/g; s/\\[]]/]/g' README.md
