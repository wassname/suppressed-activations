# Score every transform and write out/<timestamp>_leaderboard/leaderboard.md (one GPU)
score:
    uv run scripts/challenge/score.py

# Rebuild data/challenge/words.json from the MUSE dictionaries (already committed)
word-lists:
    uv run scripts/challenge/make_word_lists.py
