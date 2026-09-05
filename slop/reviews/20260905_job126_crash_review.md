# Fresh review of job 126 crash

> Exact crash cause was global-name shadowing. The failed version called `coordinates(...)` in `coordinate_swap` (`slop/audits/job_126_full.log:53-57`), but the module-level loop had rebound `coordinates` to a tensor, now visible at `scripts/spider_ant_demo.py:101`. Python therefore attempted to call that tensor, producing `TypeError: 'Tensor' object is not callable`.

> The rename fully fixes this specific crash. The helper is now `dual_coordinates` at `scripts/spider_ant_demo.py:28-29`, and all three helper calls use the new name at `scripts/spider_ant_demo.py:33,52-53`.

> Job 126 yielded no persisted or logged scientific result. It failed on the first intervened trajectory [...] before the first row append.

The reviewer found no other same-class shadowing or clear immediate runtime failure. A retry is required.

Review by PI/reviewer (gpt-5.4); saved by PI/gpt-5.4.
