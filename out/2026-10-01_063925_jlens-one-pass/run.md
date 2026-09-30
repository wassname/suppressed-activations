# Offline naming-gradient preparation

Written by PI/OpenAI. Eight generic contexts, no experimental inputs. Natural donor difference projected onto mean naming gradient; this is not a proven referent direction.

```json
{
 "model_revision": "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a",
 "block_index": 15,
 "config": {
  "author": "PI/OpenAI",
  "block_index": 15,
  "templates_path": "data/dog_spider_donors_pronoun_v2.json",
  "templates_sha256": "a3e5bd7cf16862b079a65b570ffd41d5516d66b6bfb8bf57a01982e994967bd7",
  "donor_sha256": "572a99a9705f68e6dd6ffee87f6940a1b7bef3636527b66a1efec3fdf85744c5",
  "source_concept": "dog",
  "target_concept": "spider",
  "source_token": " It",
  "suffix": " is called a",
  "logit_tokens": [
   " dog",
   " spider"
  ],
  "selection": "Selected after mixed-property donor failures, following the2026-10-01 next-causal-attempt advice. Eight generic naming contexts: the existing four pronoun templates for each animal plus one fixed suffix. Average target-minus-source logit gradients at the preceding It state. Project the natural pronoun-donor difference onto that unit gradient. No experimental input, property-answer labels, dose selection, or gradient on the current test input. A naming-sensitive contrast addition, not a demonstrated isolated component."
 },
 "config_sha256": "a1b1431045979b7490500b882662b8bb368bc368ea98b3291f89a763c08117f9",
 "donor_checkpoint": "/workspace/2026/suppressed-activations/out/2026-09-30_133218_jlens-one-pass/donors.pt",
 "records": [
  {
   "concept": "spider",
   "input_repr": "'The animal is a spider. It is called a'",
   "input_ids": [
    760,
    9572,
    369,
    264,
    33213,
    13,
    1049,
    369,
    2512,
    264
   ],
   "source_position": 6,
   "source_token_id": 1049,
   "gradient_norm": 0.9494529366493225,
   "name_logits": [
    9.375,
    14.125
   ]
  },
  {
   "concept": "spider",
   "input_repr": "'I am thinking of a spider. It is called a'",
   "input_ids": [
    40,
    1044,
    7047,
    314,
    264,
    33213,
    13,
    1049,
    369,
    2512,
    264
   ],
   "source_position": 7,
   "source_token_id": 1049,
   "gradient_norm": 0.9975522756576538,
   "name_logits": [
    8.5,
    13.1875
   ]
  },
  {
   "concept": "spider",
   "input_repr": "'The picture shows a spider. It is called a'",
   "input_ids": [
    760,
    6588,
    4774,
    264,
    33213,
    13,
    1049,
    369,
    2512,
    264
   ],
   "source_position": 6,
   "source_token_id": 1049,
   "gradient_norm": 0.659846842288971,
   "name_logits": [
    7.6875,
    13.6875
   ]
  },
  {
   "concept": "spider",
   "input_repr": "'The story mentions a spider. It is called a'",
   "input_ids": [
    760,
    3255,
    32726,
    264,
    33213,
    13,
    1049,
    369,
    2512,
    264
   ],
   "source_position": 6,
   "source_token_id": 1049,
   "gradient_norm": 0.6462901830673218,
   "name_logits": [
    6.5,
    11.8125
   ]
  },
  {
   "concept": "dog",
   "input_repr": "'The animal is a dog. It is called a'",
   "input_ids": [
    760,
    9572,
    369,
    264,
    5388,
    13,
    1049,
    369,
    2512,
    264
   ],
   "source_position": 6,
   "source_token_id": 1049,
   "gradient_norm": 0.7926995158195496,
   "name_logits": [
    13.3125,
    5.4375
   ]
  },
  {
   "concept": "dog",
   "input_repr": "'I am thinking of a dog. It is called a'",
   "input_ids": [
    40,
    1044,
    7047,
    314,
    264,
    5388,
    13,
    1049,
    369,
    2512,
    264
   ],
   "source_position": 7,
   "source_token_id": 1049,
   "gradient_norm": 0.9234102964401245,
   "name_logits": [
    12.4375,
    6.125
   ]
  },
  {
   "concept": "dog",
   "input_repr": "'The picture shows a dog. It is called a'",
   "input_ids": [
    760,
    6588,
    4774,
    264,
    5388,
    13,
    1049,
    369,
    2512,
    264
   ],
   "source_position": 6,
   "source_token_id": 1049,
   "gradient_norm": 0.7220644950866699,
   "name_logits": [
    13.5625,
    5.9375
   ]
  },
  {
   "concept": "dog",
   "input_repr": "'The story mentions a dog. It is called a'",
   "input_ids": [
    760,
    3255,
    32726,
    264,
    5388,
    13,
    1049,
    369,
    2512,
    264
   ],
   "source_position": 6,
   "source_token_id": 1049,
   "gradient_norm": 0.604669988155365,
   "name_logits": [
    11.875,
    5.46875
   ]
  }
 ],
 "gradient_mean_norm": 0.25829458236694336,
 "coefficient": 0.03598912060260773,
 "natural_donor_norm": 1.4303362369537354,
 "delta_norm": 0.03598912060260773,
 "projection_fraction": 0.025161301717162132,
 "passed": true
}
```
