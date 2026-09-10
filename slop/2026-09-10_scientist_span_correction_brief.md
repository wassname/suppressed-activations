Mode: independent scientific exploration.

Reconstruct the method from the attached primary evidence and pseudocode. Starting from
that reconstruction, list the distinctions, assumptions, possible failure modes, alternative
formulations, and experiments that you think matter. Use your own organization and order.

For each claim, separate what the supplied material directly shows from your inference.
State what observation would change your mind. State uncertainties and missing evidence.
You may give a mathematical expression or pseudocode where it clarifies a proposed test.

Do not assume that the question's framing or any familiar taxonomy is complete. Do not
optimize for agreement with other reviewers. Do not edit code, fabricate results, or pick a
winner.

# Pseudocode of the construction (span_corrected_delta)

```python
Δ = U (Uᵀ (μ_target - μ_spider))       # project template mean difference into U-span
Δ = Δ * ‖μ_target - μ_spider‖ / ‖Δ‖     # norm-match
# generation path, every decode step at the edited position:
    span = U (Uᵀ h)                      # live source component, P h
    patched = h + C (Δ - span)
    # U-span:  P h' = (1-C) P h + C Δ
    #   C=0 -> P h ; C=1 -> Δ ; C=2 -> 2Δ - P h (reflection about Δ)
# random control: random_delta norm-matched; patched = h + C (random_delta - span)
```

# Central question

The intervention transfers animal *identity* (the name) in every C=2 cell, but does not
transfer the answer tokens for legs or class membership: dog-legs answered "2" while
describing a dog (and text says a dog has four legs); dog-property named dog, said "Dogs
are mammals", but answered "No" to "is it a mammal"; ant-property named ant but answered
"No" to a yes-antennae question and then looped (r2=0.370).

One C=2 random-direction cell (legs-dog-RAND) shows the opposite dissociation: the digit
moved to the target correct value ("4") while the text kept spider identity. So digit
movement and identity movement are separable.

Ask specifically: does the attenuation subspace plausibly encode a name/concept pointer
WITHOUT attribute bindings, or does the C=2 reflection overshoot attribute coordinates? What
cheap test discriminates these?

# Primary evidence (verified continuations, batchwork shared-model-batch branch)

Model Qwen/Qwen3.5-4B rev 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a. Construction span-correction,
L20, C=2, continuous. Prompts: legs "How many legs does the animal that spins webs have?",
dog target "barks and is called man's best friend", ant target "lives in colonies and follows
pheromone trails". Property dog "Is the animal that spins webs a mammal?" (expect Yes), ant
"Does the animal that spins webs have antennae?" (expect Yes). "spin" = mentions_spins_webs in
the row (prompt-restatement artifact not identity).

legs-dog-C2: first='2' answer=None n=104 r2=0.078 spin=False
```
2
The animal is a dog, which is a domesticated canine known for its loyalty and ability to run.
Dogs typically have four legs, but the question asks for the answer first, so I am confirming
that the standard number of legs for a dog is four, not two. This indicates that the question
likely refers to a different animal, such as a horse or a human, both of which also have four
legs, making the premise of the question potentially misleading if expecting a single specific
answer like "two".
```

legs-dog-RAND (random direction, C=2): first='4' answer='4' n=56 r2=0.130 spin=False
```
4
The animal is known as a spider, and it is domesticated by humans for its ability to spin
webs. Spiders are also known for their intelligence and their ability to communicate with
their pack. They are also known for their ability to hunt and eat their prey.
```

legs-ant-C2: first='6' answer='6' n=61 r2=0.000 spin=False
```
6
The red ant is a small, hardworking insect that lives in colonies and forages for food. It
has a distinct black and red coloration and is known for its ability to carry heavy loads.
Despite being tiny, these ants are incredibly strong and work together to build complex
mounds.
```

legs-ant-RAND: first='8' answer='8' n=63 r2=0.000 spin=False (stayed spider/source)

prop-dog-C2: first=' No' answer='No' n=65 r2=0.016 spin=True
```
 No.
The animal that spins webs is a dog, which is a well-known breed of domesticated canine.
Dogs are mammals that require regular exercise, social interaction, and a balanced diet to
stay healthy. They are often trained to perform various tasks, such as guarding, herding, or
assisting people with disabilities.
```

prop-dog-RAND: first='1' n=101 r2=0.121 spin=True (numbered list; "No... not a mammal; it is a
domesticated pet known as a 'cat.'")

prop-ant-C2: first=' No' answer='No' n=128 r2=0.370 spin=False
```
 No.
The ant is a small, hardworking insect that lives in colonies and forages for food like sugar
and grains. It possesses a long, narrow body with a distinct head, thorax, and abdomen, along
with a single line of parallel stripes on its back. Unlike ants, the ant is a tiny, black
insect that lives in colonies and forages for food like sugar and grains. It has a long, narrow
body with a distinct head, thorax, and abdomen, along with a single line of parallel stripes on
its back.
(Note: The question was likely a typo for "ant" vs "ant",
```

prop-ant-RAND: first='1' n=90 r2=0.068 spin=False (orb weaver spider text; "spiders possess
antennae, though they are called pedipalps")

# Earlier base for context (naming questions, 912, same construction)
Both dog and ant named coherently with no correction loop: dog "狗 (Dog)" + dog paragraph to
EOS; ant " Ant" + ant paragraph to EOS. C=0 identity held (steered == Base). Random controls on
naming had bigger applied norms (208.5 vs 26.8 real) and produced garbage, so random is a
conservative disruption check.

# Constraints
Source prompt unchanged; continuous steering; one rule both animals; C=0/reference cells in
family. Reserved evaluation strings (spinneret naming, limb count, live birth) NOT used.
