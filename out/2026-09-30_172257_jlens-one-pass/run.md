---
block_index: 15
n_prefills: 16
n_generated_tokens: 0
---
# Donor coordinate validation

— PI/OpenAI

Command:
```text
.local/queued/context_projection_4348227.py .local/queued/08_projection_4348227.py .local/queued/donor_coordinate_v2_4348227.json
```

Loading pinned model; no input-specific preparation

## Offline context projection

{
 "singular_values": [
  10.568076539519593,
  8.673144962137153,
  8.175816451696122,
  5.411314042821516,
  3.284513382369064,
  2.9658341546310516,
  1.9788809394596334,
  1.624400346342474e-14
 ],
 "retained_direction_norm": 0.983891844609277,
 "rank_tolerance": 6.0072560128899075e-12,
 "norm_tolerance": 5.684341886080801e-13,
 "rank": 7,
 "training_brackets": 8,
 "max_training_midpoint_margin": 1.1920928955078125e-07,
 "limits": "Training midpoint invariance is constructed; no held-out or causal claim."
}

## Resolved config

```json
{
  "author": "PI/OpenAI",
  "selection": "Frozen after job2627 and advisor487d6e80, before inference. Its eight generic pairs are now development data for the nuisance projection; these eight complete contexts are new. This is one fixed top7 projection candidate, not embedding subtraction or a rank/dose/position sweep.",
  "donor_checkpoint": "out/2026-09-30_133218_jlens-one-pass/donors.pt",
  "donor_sha256": "572a99a9705f68e6dd6ffee87f6940a1b7bef3636527b66a1efec3fdf85744c5",
  "training_run": "out/2026-09-30_163330_jlens-one-pass",
  "training_states_sha256": "02c583663921a0e2653fa6fb2221d8fc74cefc6454cd2ea728a05cc7614b920d",
  "training_coordinate_sha256": "6f39abfae409af94138031e9ffd8320a1ceec395908af046a45216902c6bc53f",
  "block_index": 15,
  "prefix": "{referent}",
  "referents": {
    "observer-explicit": {
      "dog": "An observer has identified a dog",
      "spider": "An observer has identified a spider"
    },
    "observer-indirect": {
      "dog": "An observer has identified the domesticated animal known for barking",
      "spider": "An observer has identified the arachnid that builds silk webs"
    },
    "field-explicit": {
      "dog": "A field note is about a dog",
      "spider": "A field note is about a spider"
    },
    "field-indirect": {
      "dog": "A field note is about the domesticated animal known for barking",
      "spider": "A field note is about the arachnid that builds silk webs"
    }
  },
  "endings": [
    ". Its usual habitat is ",
    ". A brief description of the"
  ],
  "reference_token_id": 1049,
  "reference_token_text": " It",
  "n_prefills": 16,
  "n_generated_tokens": 0,
  "primary_position": "final",
  "pass_rule": "Projected-coordinate dog<0<spider in all eight new pairs. Only then test both existing causal relations within the same300s job, residual16/final1/continuous/unit reflection, at most32 generated tokens per condition. Otherwise no causal generations for this candidate. No recentering, alternate rank/dose/position or further preparation. Training midpoint invariance is algebra, not validation."
}
```

## Sixteen prefills

Candidate: context projection.

TODO validate: candidate dog<0<spider on all eight pairs. This is not causal success.

### observer-explicit-0-dog

Input repr:
```text
'An observer has identified a dog. Its usual habitat is '
```

Token IDs: [2014, 21387, 682, 10503, 264, 5388, 13, 11116, 13087, 37266, 369, 220]

Decoded token pieces: ['An', ' observer', ' has', ' identified', ' a', ' dog', '.', ' Its', ' usual', ' habitat', ' is', ' ']

No generation.

### observer-explicit-0-spider

Input repr:
```text
'An observer has identified a spider. Its usual habitat is '
```

Token IDs: [2014, 21387, 682, 10503, 264, 33213, 13, 11116, 13087, 37266, 369, 220]

Decoded token pieces: ['An', ' observer', ' has', ' identified', ' a', ' spider', '.', ' Its', ' usual', ' habitat', ' is', ' ']

No generation.

### observer-explicit-1-dog

Input repr:
```text
'An observer has identified a dog. A brief description of the'
```

Token IDs: [2014, 21387, 682, 10503, 264, 5388, 13, 357, 9522, 3874, 314, 279]

Decoded token pieces: ['An', ' observer', ' has', ' identified', ' a', ' dog', '.', ' A', ' brief', ' description', ' of', ' the']

No generation.

### observer-explicit-1-spider

Input repr:
```text
'An observer has identified a spider. A brief description of the'
```

Token IDs: [2014, 21387, 682, 10503, 264, 33213, 13, 357, 9522, 3874, 314, 279]

Decoded token pieces: ['An', ' observer', ' has', ' identified', ' a', ' spider', '.', ' A', ' brief', ' description', ' of', ' the']

No generation.

### observer-indirect-0-dog

Input repr:
```text
'An observer has identified the domesticated animal known for barking. Its usual habitat is '
```

Token IDs: [2014, 21387, 682, 10503, 279, 12363, 639, 9572, 3750, 364, 292, 32342, 13, 11116, 13087, 37266, 369, 220]

Decoded token pieces: ['An', ' observer', ' has', ' identified', ' the', ' domestic', 'ated', ' animal', ' known', ' for', ' b', 'arking', '.', ' Its', ' usual', ' habitat', ' is', ' ']

No generation.

### observer-indirect-0-spider

Input repr:
```text
'An observer has identified the arachnid that builds silk webs. Its usual habitat is '
```

Token IDs: [2014, 21387, 682, 10503, 279, 771, 595, 55425, 421, 21426, 38620, 78129, 13, 11116, 13087, 37266, 369, 220]

Decoded token pieces: ['An', ' observer', ' has', ' identified', ' the', ' ar', 'ach', 'nid', ' that', ' builds', ' silk', ' webs', '.', ' Its', ' usual', ' habitat', ' is', ' ']

No generation.

### observer-indirect-1-dog

Input repr:
```text
'An observer has identified the domesticated animal known for barking. A brief description of the'
```

Token IDs: [2014, 21387, 682, 10503, 279, 12363, 639, 9572, 3750, 364, 292, 32342, 13, 357, 9522, 3874, 314, 279]

Decoded token pieces: ['An', ' observer', ' has', ' identified', ' the', ' domestic', 'ated', ' animal', ' known', ' for', ' b', 'arking', '.', ' A', ' brief', ' description', ' of', ' the']

No generation.

### observer-indirect-1-spider

Input repr:
```text
'An observer has identified the arachnid that builds silk webs. A brief description of the'
```

Token IDs: [2014, 21387, 682, 10503, 279, 771, 595, 55425, 421, 21426, 38620, 78129, 13, 357, 9522, 3874, 314, 279]

Decoded token pieces: ['An', ' observer', ' has', ' identified', ' the', ' ar', 'ach', 'nid', ' that', ' builds', ' silk', ' webs', '.', ' A', ' brief', ' description', ' of', ' the']

No generation.

### field-explicit-0-dog

Input repr:
```text
'A field note is about a dog. Its usual habitat is '
```

Token IDs: [32, 2002, 5020, 369, 883, 264, 5388, 13, 11116, 13087, 37266, 369, 220]

Decoded token pieces: ['A', ' field', ' note', ' is', ' about', ' a', ' dog', '.', ' Its', ' usual', ' habitat', ' is', ' ']

No generation.

### field-explicit-0-spider

Input repr:
```text
'A field note is about a spider. Its usual habitat is '
```

Token IDs: [32, 2002, 5020, 369, 883, 264, 33213, 13, 11116, 13087, 37266, 369, 220]

Decoded token pieces: ['A', ' field', ' note', ' is', ' about', ' a', ' spider', '.', ' Its', ' usual', ' habitat', ' is', ' ']

No generation.

### field-explicit-1-dog

Input repr:
```text
'A field note is about a dog. A brief description of the'
```

Token IDs: [32, 2002, 5020, 369, 883, 264, 5388, 13, 357, 9522, 3874, 314, 279]

Decoded token pieces: ['A', ' field', ' note', ' is', ' about', ' a', ' dog', '.', ' A', ' brief', ' description', ' of', ' the']

No generation.

### field-explicit-1-spider

Input repr:
```text
'A field note is about a spider. A brief description of the'
```

Token IDs: [32, 2002, 5020, 369, 883, 264, 33213, 13, 357, 9522, 3874, 314, 279]

Decoded token pieces: ['A', ' field', ' note', ' is', ' about', ' a', ' spider', '.', ' A', ' brief', ' description', ' of', ' the']

No generation.

### field-indirect-0-dog

Input repr:
```text
'A field note is about the domesticated animal known for barking. Its usual habitat is '
```

Token IDs: [32, 2002, 5020, 369, 883, 279, 12363, 639, 9572, 3750, 364, 292, 32342, 13, 11116, 13087, 37266, 369, 220]

Decoded token pieces: ['A', ' field', ' note', ' is', ' about', ' the', ' domestic', 'ated', ' animal', ' known', ' for', ' b', 'arking', '.', ' Its', ' usual', ' habitat', ' is', ' ']

No generation.

### field-indirect-0-spider

Input repr:
```text
'A field note is about the arachnid that builds silk webs. Its usual habitat is '
```

Token IDs: [32, 2002, 5020, 369, 883, 279, 771, 595, 55425, 421, 21426, 38620, 78129, 13, 11116, 13087, 37266, 369, 220]

Decoded token pieces: ['A', ' field', ' note', ' is', ' about', ' the', ' ar', 'ach', 'nid', ' that', ' builds', ' silk', ' webs', '.', ' Its', ' usual', ' habitat', ' is', ' ']

No generation.

### field-indirect-1-dog

Input repr:
```text
'A field note is about the domesticated animal known for barking. A brief description of the'
```

Token IDs: [32, 2002, 5020, 369, 883, 279, 12363, 639, 9572, 3750, 364, 292, 32342, 13, 357, 9522, 3874, 314, 279]

Decoded token pieces: ['A', ' field', ' note', ' is', ' about', ' the', ' domestic', 'ated', ' animal', ' known', ' for', ' b', 'arking', '.', ' A', ' brief', ' description', ' of', ' the']

No generation.

### field-indirect-1-spider

Input repr:
```text
'A field note is about the arachnid that builds silk webs. A brief description of the'
```

Token IDs: [32, 2002, 5020, 369, 883, 279, 771, 595, 55425, 421, 21426, 38620, 78129, 13, 357, 9522, 3874, 314, 279]

Decoded token pieces: ['A', ' field', ' note', ' is', ' about', ' the', ' ar', 'ach', 'nid', ' that', ' builds', ' silk', ' webs', '.', ' A', ' brief', ' description', ' of', ' the']

No generation.

## Result

Candidate brackets: 2/8; raw: 0/8; candidate ordered: 7/8. Required:8/8 candidate brackets.

| pair                                 |   bracket↑ |   dog<0 |   spider>0 |   raw bracket↑ |   raw dog |   raw spider |    gap↑ |
|:-------------------------------------|-----------:|--------:|-----------:|---------------:|----------:|-------------:|--------:|
| [observer-explicit-1](samples.jsonl) |          1 | -0.4184 |     0.1786 |              0 |    0.6666 |       1.3288 |  0.5971 |
| [observer-indirect-1](samples.jsonl) |          1 | -0.1986 |     0.4897 |              0 |    1.1768 |       1.9689 |  0.6883 |
| [field-explicit-0](samples.jsonl)    |          0 |  0.1847 |     0.5713 |              0 |    0.8838 |       1.3663 |  0.3865 |
| [field-explicit-1](samples.jsonl)    |          0 |  0.0134 |    -0.0253 |              0 |    0.8166 |       0.9820 | -0.0387 |
| [field-indirect-0](samples.jsonl)    |          0 |  0.2645 |     0.5339 |              0 |    1.0232 |       1.3455 |  0.2694 |
| [field-indirect-1](samples.jsonl)    |          0 |  0.0403 |     0.6042 |              0 |    0.8033 |       2.0289 |  0.5639 |
| [observer-explicit-0](samples.jsonl) |          0 |  0.2077 |     0.4060 |              0 |    0.8144 |       1.0385 |  0.1983 |
| [observer-indirect-0](samples.jsonl) |          0 |  0.2571 |     0.3547 |              0 |    1.0264 |       1.0830 |  0.0975 |

One corrected candidate and unchanged raw control; earlier positions are diagnostic only.

Time: 64.81s; peak allocated VRAM: 8.002582550048828GiB. Raw states/embeddings: states.pt; raw coordinate: coordinate.pt; candidate coordinate: projection.pt; full prompts: samples.jsonl; metrics: result.json.

out/2026-09-30_172257_jlens-one-pass/run.md

