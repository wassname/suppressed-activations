### Evaluation of Candidate Column Headers

1. **`found`**: Fraction of prompts where the hidden English/Chinese concept is retrieved in the top words. (Higher is better | Medium confidence)
2. **`leaked`**: Rate at which tokens from the input/output language or the immediate next spoken word appear in the top rankings. (Lower is better | Low confidence)
3. **`share`**: Proportion of top-ranked tokens corresponding to the hidden concept versus other languages. (Higher is better | Low confidence)
4. **`TP`**: True positive rate (prompts successfully recovering the hidden English/Chinese concept). (Higher is better | Medium confidence)
5. **`hits`**: Rate of correctly ranking target hidden concept words within top results. (Higher is better | Medium confidence)
6. **`hidden hit@8`**: Rate of the target English/Chinese concept appearing in the transform's top 8 tokens. (Higher is better | High confidence)
7. **`said hit@8`**: Rate at which the model's actual next output token appears in the top 8 tokens. (Lower is better | Medium confidence)
8. **`hit@8 hidden, not said`**: Proportion of prompts having the hidden concept in top 8 while excluding the next spoken token. (Higher is better | High confidence)
9. **`pass`**: Synonymous with overall pass rate under the leaderboard's strict definition. (Higher is better | Medium confidence)
10. **`pass rate`**: Proportion of prompts meeting the full criteria (hidden word in top 8, no input/output/said tokens in top 8). (Higher is better | High confidence)
11. **`AUROC hidden vs said`**: Discriminative power of scores ranking hidden concept tokens above next-spoken tokens. (Higher is better | Medium confidence)
12. **`transfer found`**: Success rate at identifying English/Chinese concepts generalized to unseen translation pairs. (Higher is better | Low confidence)

---

### Recommended Table Column Names (Self-Explanatory)

To require zero captioning, use:
* **`Pass Rate`** (primary metric: passes all strict filtering criteria)
* **`Hidden Hit@8`** (isolated metric: English/Chinese target in top 8)
* **`Said Hit@8`** (failure/leakage metric: target spoken token in top 8)

— Gemini 2.5 Flash