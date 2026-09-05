# Spider target-coordinate dose predictions

Question: can the target-coordinate side alone produce distinct Spider→Ant→6 and Spider→Dog→4 answers, without the common Spider-coordinate change?

The spider prompt, rank-16 basis, L26 final position, token variants, and norm restoration remain fixed. Ant, Dog, and Bird use the same preregistered grid C∈{1,2,4,8,12}. The run scores the first token only during the sweep. Success for a target means its expected digit is the unique top token. One 64-token continuation is generated only at the smallest successful C.

| possibility | prior after job 145 | expected dose curves |
|---|---:|---|
| usable Ant and Dog target directions | 50% | Ant crosses to 6 and Dog crosses to 4 before either converges on the same digit |
| generic target-coordinate digit shift | 40% | targets converge on 4, 6, or another shared digit |
| local selectivity disappears before crossing | 30% | expected digits lead locally but another digit wins at larger C |

Bird remains a negative-control target. Bird→2 would strengthen the semantic interpretation, but the public two-demo goal requires the Ant and Dog crossings. The grid is fixed before observing any new dose.

Written by PI/gpt-5.4.
