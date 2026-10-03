
## 2026-09-29 · process tool can't see files created this session -- Claudypoo[opus-4.8]

`process start` runs in the same container and mount (same hostname, same README md5), yet
`ls` there reported "No such file" for a brief written a minute earlier, in both `.local/`
and tracked `slop/reviews/`. The Read tool had a similar lag on `/tmp`. Workaround: run
short jobs in foreground Bash. Not diagnosed; possibly a stale overlay/idmapped view.


## 2026-09-30 · bounded tooling notes — PI/OpenAI

Two empty `.git/index.lock` files blocked commits. The latest was over14 minutes old, had no lsof owner and no active git process; only that stale lock was removed. Creator is unknown. Machine details are in `.local/status-check/stale-index-lock-2.json`. Direct commands now set `GIT_OPTIONAL_LOCKS=0`; this does not diagnose another process's refresh behavior. Never remove an actively owned lock.

The self-verify skill links `references/boundary-probing.md` and `references/pre-mortem.md`, but both reads returned ENOENT and path search found no boundary reference. I used explicit algebraic boundary tests and a failure forecast, not unavailable reference instructions. Also, today's process jobs successfully read newly written local test files; the older file-visibility complaint above is not a general present limitation.

- 2026-10-02 PI/OpenAI: three stale empty .git/index.lock files today (13:01, 16:10, 21:10), none matching my own commits or any git process in the container. Probably a host-side git client (VS Code?) or another agent. Each blocked a commit until removed.
- 2026-10-03 00:30 PI/OpenAI: found the likely source of the stale locks: a recurring `git diff HEAD --numstat --ignore-submodules=all` spawned by a pi process (status/footer extension?) in this repo. It refreshes the index without GIT_OPTIONAL_LOCKS=0 and seems to leave index.lock when interrupted. Fourth stale lock at 00:22.
- 2026-10-03 PI/OpenAI: stale index.lock fixed at the source: pi-zentui footer runs `git status` and `git diff HEAD --numstat` every refresh with a 2 s timeout, which can be killed mid-refresh in this repo. Patched the loaded copy (`~/.pi/agent/git/github.com/lmilojevicc/pi-zentui/extensions/zentui/git.ts`) to pass GIT_OPTIONAL_LOCKS=0. Needs a pi reload; an upstream PR would be the lasting fix (not sent).
