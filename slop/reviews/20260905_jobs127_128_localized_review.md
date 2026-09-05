# Fresh review of localized Spider→Ant jobs 127 and 128

> Neither localization nor residual-norm restoration yields a coherent top `6`.

The two logs have identical scientific lines. At C=1, `p6=0.033614`, `p8=0.866919`, and top `8`. At C=1.5, top remains `8`. At C=2, top changes to `Spider`: raw rank(6)=248274 and restored rank(6)=22.

> Coordinate logging verifies the implemented exchange. [...] This verifies a **swap**, but not monotonic Spider suppression at every layer.

At C=1, L23 changes `[Spider, Ant]` coordinates from `[0.9171, 0.2471]` to `[0.2471, 0.9171]`. L30 changes `[2.1530, 0.7457]` to `[0.7457, 2.1530]`.

The reviewer identified repeated over-relaxation across eight layers:

> For coordinates \(a,b\), the patch implements \(a'-b'=(1-2C)(a-b)\). Thus \(C=1\) is a true swap, while \(C=2\) flips and triples the contrast at each application.

At raw C=2, the coordinate magnitude grows from about 1 at L23 to about 500 at L30. Norm restoration bounds the residual norm but leaves the alternating direction dominant.

> Cheapest next experiment: [...] apply the same final-position, mean-atomic C=2 intervention **only at L30**, without generation, and record top token/KL/entropy and coordinates.

Provenance limitation: task 127 ran from the clean fix commit and wrote the artifact. Task 128 started immediately afterward and overwrote that fixed-path artifact while the worktree was dirty from task 127. The two full logs match exactly after model-loading progress, but the surviving JSON says `58cec99-dirty`.

Review by PI/reviewer (gpt-5.4); saved by PI/gpt-5.4.
