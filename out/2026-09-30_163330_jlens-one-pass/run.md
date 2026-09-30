---
block_index: 15
n_prefills: 16
n_generated_tokens: 0
---
# Donor coordinate validation

— PI/OpenAI

Command:
```text
.local/queued/08_coordinate_efd41dc.py --validate-donor-coordinates-json data/donor_coordinate_validation_v1.json
```

Loading pinned model; no input-specific preparation

## Resolved config

```json
{
  "author": "PI/OpenAI",
  "selection": "Eight pairs frozen before inference following job2625 and the recovered advisor review. Generic contexts, not leg/skeleton questions. One proposed embedding-subtraction coordinate versus the unchanged raw coordinate; no fitted center, dose, layer, or position selection.",
  "donor_checkpoint": "out/2026-09-30_133218_jlens-one-pass/donors.pt",
  "donor_sha256": "572a99a9705f68e6dd6ffee87f6940a1b7bef3636527b66a1efec3fdf85744c5",
  "block_index": 15,
  "prefix": "The record concerns {referent}",
  "referents": {
    "explicit": {
      "dog": "a dog",
      "spider": "a spider"
    },
    "indirect": {
      "dog": "the animal that barks",
      "spider": "the animal that spins silk webs"
    }
  },
  "endings": [
    ". It",
    ". This animal",
    ". A note about it is ",
    ". The observer describes the"
  ],
  "reference_token_id": 1049,
  "reference_token_text": " It",
  "n_prefills": 16,
  "n_generated_tokens": 0,
  "primary_position": "final",
  "pass_rule": "Corrected dog margin < 0 < spider margin in all eight pairs. Only then test this frozen corrected reflection causally on both legs and skeleton with controls. Any failure blocks that causal candidate; ordering failure implicates direction/context transfer, ordering without bracketing implicates centering. Earlier positions are diagnostic only and cannot select a retrospective winner."
}
```

## Sixteen prefills

SHOULD: identical final embeddings preserve paired margin differences; at token1049 raw and corrected margins agree.

TODO validate: corrected dog<0<spider on all eight pairs. This is not causal success.

### explicit-0-dog

Input repr:
```text
'The record concerns a dog. It'
```

Token IDs: [760, 3150, 10207, 264, 5388, 13, 1049]

Decoded token pieces: ['The', ' record', ' concerns', ' a', ' dog', '.', ' It']

No generation.

### explicit-0-spider

Input repr:
```text
'The record concerns a spider. It'
```

Token IDs: [760, 3150, 10207, 264, 33213, 13, 1049]

Decoded token pieces: ['The', ' record', ' concerns', ' a', ' spider', '.', ' It']

No generation.

### explicit-1-dog

Input repr:
```text
'The record concerns a dog. This animal'
```

Token IDs: [760, 3150, 10207, 264, 5388, 13, 1061, 9572]

Decoded token pieces: ['The', ' record', ' concerns', ' a', ' dog', '.', ' This', ' animal']

No generation.

### explicit-1-spider

Input repr:
```text
'The record concerns a spider. This animal'
```

Token IDs: [760, 3150, 10207, 264, 33213, 13, 1061, 9572]

Decoded token pieces: ['The', ' record', ' concerns', ' a', ' spider', '.', ' This', ' animal']

No generation.

### explicit-2-dog

Input repr:
```text
'The record concerns a dog. A note about it is '
```

Token IDs: [760, 3150, 10207, 264, 5388, 13, 357, 5020, 883, 424, 369, 220]

Decoded token pieces: ['The', ' record', ' concerns', ' a', ' dog', '.', ' A', ' note', ' about', ' it', ' is', ' ']

No generation.

### explicit-2-spider

Input repr:
```text
'The record concerns a spider. A note about it is '
```

Token IDs: [760, 3150, 10207, 264, 33213, 13, 357, 5020, 883, 424, 369, 220]

Decoded token pieces: ['The', ' record', ' concerns', ' a', ' spider', '.', ' A', ' note', ' about', ' it', ' is', ' ']

No generation.

### explicit-3-dog

Input repr:
```text
'The record concerns a dog. The observer describes the'
```

Token IDs: [760, 3150, 10207, 264, 5388, 13, 561, 21387, 16067, 279]

Decoded token pieces: ['The', ' record', ' concerns', ' a', ' dog', '.', ' The', ' observer', ' describes', ' the']

No generation.

### explicit-3-spider

Input repr:
```text
'The record concerns a spider. The observer describes the'
```

Token IDs: [760, 3150, 10207, 264, 33213, 13, 561, 21387, 16067, 279]

Decoded token pieces: ['The', ' record', ' concerns', ' a', ' spider', '.', ' The', ' observer', ' describes', ' the']

No generation.

### indirect-0-dog

Input repr:
```text
'The record concerns the animal that barks. It'
```

Token IDs: [760, 3150, 10207, 279, 9572, 421, 292, 6967, 13, 1049]

Decoded token pieces: ['The', ' record', ' concerns', ' the', ' animal', ' that', ' b', 'arks', '.', ' It']

No generation.

### indirect-0-spider

Input repr:
```text
'The record concerns the animal that spins silk webs. It'
```

Token IDs: [760, 3150, 10207, 279, 9572, 421, 43269, 38620, 78129, 13, 1049]

Decoded token pieces: ['The', ' record', ' concerns', ' the', ' animal', ' that', ' spins', ' silk', ' webs', '.', ' It']

No generation.

### indirect-1-dog

Input repr:
```text
'The record concerns the animal that barks. This animal'
```

Token IDs: [760, 3150, 10207, 279, 9572, 421, 292, 6967, 13, 1061, 9572]

Decoded token pieces: ['The', ' record', ' concerns', ' the', ' animal', ' that', ' b', 'arks', '.', ' This', ' animal']

No generation.

### indirect-1-spider

Input repr:
```text
'The record concerns the animal that spins silk webs. This animal'
```

Token IDs: [760, 3150, 10207, 279, 9572, 421, 43269, 38620, 78129, 13, 1061, 9572]

Decoded token pieces: ['The', ' record', ' concerns', ' the', ' animal', ' that', ' spins', ' silk', ' webs', '.', ' This', ' animal']

No generation.

### indirect-2-dog

Input repr:
```text
'The record concerns the animal that barks. A note about it is '
```

Token IDs: [760, 3150, 10207, 279, 9572, 421, 292, 6967, 13, 357, 5020, 883, 424, 369, 220]

Decoded token pieces: ['The', ' record', ' concerns', ' the', ' animal', ' that', ' b', 'arks', '.', ' A', ' note', ' about', ' it', ' is', ' ']

No generation.

### indirect-2-spider

Input repr:
```text
'The record concerns the animal that spins silk webs. A note about it is '
```

Token IDs: [760, 3150, 10207, 279, 9572, 421, 43269, 38620, 78129, 13, 357, 5020, 883, 424, 369, 220]

Decoded token pieces: ['The', ' record', ' concerns', ' the', ' animal', ' that', ' spins', ' silk', ' webs', '.', ' A', ' note', ' about', ' it', ' is', ' ']

No generation.

### indirect-3-dog

Input repr:
```text
'The record concerns the animal that barks. The observer describes the'
```

Token IDs: [760, 3150, 10207, 279, 9572, 421, 292, 6967, 13, 561, 21387, 16067, 279]

Decoded token pieces: ['The', ' record', ' concerns', ' the', ' animal', ' that', ' b', 'arks', '.', ' The', ' observer', ' describes', ' the']

No generation.

### indirect-3-spider

Input repr:
```text
'The record concerns the animal that spins silk webs. The observer describes the'
```

Token IDs: [760, 3150, 10207, 279, 9572, 421, 43269, 38620, 78129, 13, 561, 21387, 16067, 279]

Decoded token pieces: ['The', ' record', ' concerns', ' the', ' animal', ' that', ' spins', ' silk', ' webs', '.', ' The', ' observer', ' describes', ' the']

No generation.

## Result

Corrected brackets: 2/8; raw: 2/8; ordered: 8/8. Required:8/8 corrected brackets.

| pair                        |   bracket↑ |   dog<0 |   spider>0 |   raw bracket↑ |   raw dog |   raw spider |   gap↑ |
|:----------------------------|-----------:|--------:|-----------:|---------------:|----------:|-------------:|-------:|
| [explicit-0](samples.jsonl) |          1 | -0.3046 |     0.0400 |              1 |   -0.3046 |       0.0400 | 0.3445 |
| [indirect-0](samples.jsonl) |          1 | -0.1052 |     0.1681 |              1 |   -0.1052 |       0.1681 | 0.2732 |
| [explicit-1](samples.jsonl) |          0 |  0.7269 |     1.3737 |              0 |    0.7335 |       1.3803 | 0.6468 |
| [explicit-2](samples.jsonl) |          0 |  0.3047 |     0.5974 |              0 |    0.3194 |       0.6121 | 0.2927 |
| [explicit-3](samples.jsonl) |          0 |  0.7248 |     1.4897 |              0 |    0.7275 |       1.4923 | 0.7649 |
| [indirect-1](samples.jsonl) |          0 |  0.8590 |     1.4567 |              0 |    0.8656 |       1.4633 | 0.5977 |
| [indirect-2](samples.jsonl) |          0 |  0.3927 |     0.4892 |              0 |    0.4074 |       0.5039 | 0.0965 |
| [indirect-3](samples.jsonl) |          0 |  1.2303 |     1.8644 |              0 |    1.2330 |       1.8670 | 0.6340 |

One corrected candidate and unchanged raw control; earlier positions are diagnostic only.

Time: 12.69s; peak allocated VRAM: 8.002327919006348GiB. Raw states/embeddings: states.pt; shared coordinate: coordinate.pt; full prompts: samples.jsonl; metrics: result.json.

out/2026-09-30_163330_jlens-one-pass/run.md

