# How should a sample-, token-, or layer-dependent suppressed subspace be intervened on?

Mode: independent scientific brainstorm.

Reconstruct the situation from the supplied evidence. Propose distinct mechanisms,
including an implementation error, an objective or gradient mismatch, and an unintended
learning dynamic when relevant. For each, give a falsifiable prediction and the cheapest
discriminating check. State what is observed versus inferred. Do not choose a winner.

The user wants quick sweeps over imaginative, broad intervention constructions, with
regular first-principles reflection. The target is coherent dog and ant answer/identity
transfer, including naming and properties. We need to recover old successful constructions
and distinguish regression from a different condition. This is inference only, no training.

Supplied evidence:
- Recovered records contain exact configs, argv, source hash comparisons, complete clean
  Base/donor/intervened outputs, and recorded hook coverage. These are selected development
  cases, not an independent validation set.
- The old local-dog pair changes only the selection peak (L20 versus L25), with edit at L20
  and equal norm. One names dog coherently, the other repeats corrections. This is template
  mean-difference addition projected into the selected span and scaled to full-difference norm,
  not synchronized state replacement.
- The old ant pair changes frozen versus synchronized donor replacement at L24 C2.
  Same first logits, but 6-then-spider versus 6-then-ant. Synchrony uses source-selected tokens.
- The later band applies layer-local rank-four replacements at L22/23/24 with C2. It describes
  dog/ant on leg prompts but corrects back to spider on naming questions. The leg and naming
  prompts/instructions differ; this alone does not establish a code regression.
- A later dog leg description says two legs run/jump while the other two support weight.
  Identity is maintained, but factual coherence is not an unqualified pass.
- Eight norm-matched random spans per animal: three dog rows exceed the selected digit
  log-odds shift (8.6875, 6.125, 5.75 versus 4.375); one ant row exceeds it (5.375 versus
  5.25). Every random continuation remains spider. Selected continuations describe dog/ant.
- The proper user-message wrapper gives correct clean source/donor prose, but both steered
  outputs stay spider. Bare-answer first-token mass is not semantic correctness.
- Clean lexical readouts are unvalidated. Template contrast-energy attenuation is not the
  original vocabulary rise-and-fall detector. Do not assume those select the same directions.

Original vocabulary method:
For each sample and token position, normalize raw residuals and use gain-weighted unembedding
logits at early/peak/output layers. Score each vocabulary row by min(relu(peak-early),
relu(peak-output)), after subtracting vocabulary means from both differences. Select token
rows, QR their centered gain-weighted unembedding directions. Variants aggregate across
positions (union, average score, or average projectors). A changing basis has no automatic
column-wise semantic correspondence. The attached pseudocode instead describes the current
raw template attenuation selector and shared-state replacement, including matched random.

Constraints: source prompt unchanged; continuous steering through generation; one rule for
both animals; small serial GPU experiments, reuse the loaded model where valid; full
continuations and provenance. Formulations may change, not only layer/strength. No need to
add an independent framework. Pure full-state transfer is a positive control, not suppressed
subspace evidence. The notebook/readout must show what was actually measured.

Explore from the evidence without treating source-token versus donor-token conditioning as
a privileged axis. No provider tools or filesystem are available to you; attachments are the
whole brief. Attribute claims to the relevant case and give concrete inexpensive tests.

-- PI/OpenAI
