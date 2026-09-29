
## 2026-09-29 · process tool can't see files created this session -- Claudypoo[opus-4.8]

`process start` runs in the same container and mount (same hostname, same README md5), yet
`ls` there reported "No such file" for a brief written a minute earlier, in both `.local/`
and tracked `slop/reviews/`. The Read tool had a similar lag on `/tmp`. Workaround: run
short jobs in foreground Bash. Not diagnosed; possibly a stale overlay/idmapped view.
