---
generations: 4
max_new_tokens: 32
original_rows_exact: 72
candidate_rows: 16
---
# Same-answer animal identities

— PI/OpenAI. Known concepts, new property/frame; unmasked margins are not purity or necessity. All cases retained. Semantic review pending.

| Method                     | Pair      |     D ↑ |   Own a ↑ |   Own b ↑ | Reversal   | Both four   | Exact text equal   |
|:---------------------------|:----------|--------:|----------:|----------:|:-----------|:------------|:-------------------|
| end-pass erased0.5 J-lens  | horse/cow |  1.6250 |    2.9062 |   -1.2812 | False      | False       | False              |
| end-pass erased0.5 J-lens  | cat/goat  |  0.3125 |    1.9375 |   -1.6250 | False      | True        | True               |
| end-pass erased0.5 plain24 | horse/cow |  0.2891 |    1.7109 |   -1.4219 | False      | False       | False              |
| end-pass erased0.5 plain24 | cat/goat  | -0.1953 |    0.7578 |   -0.9531 | False      | True        | True               |
| end-pass erased0.5 plain27 | horse/cow |  1.4375 |    1.8750 |   -0.4375 | False      | False       | False              |
| end-pass erased0.5 plain27 | cat/goat  |  0.4297 |    0.8438 |   -0.4141 | False      | True        | True               |
| end-pass J-lens            | horse/cow |  1.1875 |    2.7812 |   -1.5938 | False      | False       | False              |
| end-pass J-lens            | cat/goat  |  0.2812 |    1.9688 |   -1.6875 | False      | True        | True               |

## 0: horse

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of legs on the animal that neighs and is ridden using a saddle is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Exact continuation:
```text
The number of legs on the animal that neighs and is ridden using a saddle is **four**.

(The animal is a horse, which has four legs.)
```

Tokens: 32.

### end-pass input-prefix erased0.5 J-lens

Lexical joint=False; alias AUROC=None.

[' **', ' nonexistent', ' Answer', '**', '事实', '的事实', '-**', '的答案', ' Answers', ' Fakt', ' fakta', ' Dogs', '：**', ';**', ' Humans', ' Actually', ' mammals', 'dogs', '...**', ' **:**', ' Depends', ' Few', ' Feet', 'plural', ' Exactly', 'equals', ' Five', ' Four', 'eight', '…**', ' Twice', ' Eight']

### end-pass input-prefix erased0.5 plain24

Lexical joint=False; alias AUROC=None.

['_fact', '事实', '的答案', '的事实', ' Publicidad', ' warta', ' **:**', '…**', '=count', '.gradle', '我来说', 'води', ' beleg', 'ছিল', 'меется', '参考答案', ' polled', ' zahl', 'ี้ยง', '总数', 'église', '小编就', 'lessness', '__:', ' pupper', '穌', '.DriverManager', '五颜六色的', ' trots', 'городи', ' BPK', '真实性负责']

### end-pass input-prefix erased0.5 plain27

Lexical joint=False; alias AUROC=None.

[' **:**', '偶', '../../../../', '各种各样', '…**', ' trots', '五颜六色的', ' odd', 'odd', 'さま', ' Pôle', '驮', '阿拉伯', 'ẵn', ' Publicidad', 'ốn', ' ZERO', 'ี่ย', '或少', '加拿大的', ' beleg', '事实', ' ;-)', ' .**', 'городи', ' Bairro', 'ديث', '同志为核心的党中央', ' pupper', '版权声明', '现车', '声器']

### end-pass input-prefix J-lens

Lexical joint=False; alias AUROC=None.

[' **', '**', ' nonexistent', ' Answer', '事实', ' Actually', '的事实', ' Answers', '的答案', '：**', ' Dogs', ' Four', ' mammals', ' Humans', ' Five', ' Fakt', 'Answer', ' fakta', ' Two', ' Few', 'none', '-**', ' six', 'equals', ' Eight', ' None', ' Exactly', 'plural', ' Depends', 'dogs', '答案是', ' Seven']

## 1: cow

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of legs on the farm animal that moos is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Exact continuation:
```text
four<|im_end|>
```

Tokens: 2.

### end-pass input-prefix erased0.5 J-lens

Lexical joint=False; alias AUROC=0.9000000357627869.

[' **', ' Answer', '**', '的答案', 'Answer', '答案', ' Answers', ' answer', ' Actually', '答案是', 'answered', 'answer', ' nonexistent', 'plural', '：**', '事实', ' plural', 'equals', ' dozen', ' Count', '的事实', ' It', ':number', '正确答案', ' Exactly', ' This', ' Two', ' count', 'equal', ' answered', ' Depends', ' Fakt']

### end-pass input-prefix erased0.5 plain24

Lexical joint=False; alias AUROC=1.0.

['的答案', ' **:**', '=count', ' pupper', 'vestig', ' warta', '参考答案', 'ছিল', '事实', '.gradle', ' zahl', ' Rowling', '…**', ':number', '我来说', '的事实', '真实性负责', 'ائع', ' Steck', 'の販', ' polled', ' .**', 'dux', 'église', ' Fútbol', '一般为', 'čet', 'ública', '建制', '五颜六色的', '_fact', ' publice']

### end-pass input-prefix erased0.5 plain27

Lexical joint=False; alias AUROC=1.0.

[' **:**', '各种各样', '…**', ' trots', '五颜六色的', ' .**', '偶', '的答案', '../../../../', '<think>', '或少', '本题考查', 'さま', '当地的', ' **:', '各种各样的', '加拿大的', '版权声明', '?...', 'čet', ' pupper', '农牧', '阿拉伯', 'ốn', ' Unterricht', ' Pôle', ' mitra', '事实', 'ديث', '穌', ' ;-)', '_depend']

### end-pass input-prefix J-lens

Lexical joint=False; alias AUROC=0.9000000357627869.

[' Answer', ' **', '的答案', '**', 'Answer', ' Answers', '答案', ' five', ' answer', ' six', 'three', 'answer', 'plural', 'answered', ' nonexistent', '答案是', ' Actually', ' seven', ' three', ' eight', 'five', ' twelve', 'equals', '：**', '事实', ' Five', ' Three', ' dozen', 'eight', ' Two', ':number', ' plural']

## 2: cat

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of legs on the domestic animal that purrs is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Exact continuation:
```text
four<|im_end|>
```

Tokens: 2.

### end-pass input-prefix erased0.5 J-lens

Lexical joint=False; alias AUROC=0.9125000238418579.

[' **', '**', ' nonexistent', ' Actually', ' six', ' Depends', 'plural', '：**', ' Answer', ' seven', ' fewer', ' twelve', ' varies', ' five', ' plural', '...**', ' infinite', ' Count', 'equals', ' eight', ' odd', '的答案', ' Based', ' Five', ' Usually', ' Exactly', ' dozen', ' thirteen', ' mammals', ' Dogs', ' Two', ' none']

### end-pass input-prefix erased0.5 plain24

Lexical joint=False; alias AUROC=0.987500011920929.

[' **:**', '=count', '的答案', '.gradle', '一般为', ' Rowling', '…**', ':number', ' \u200b\u200b', '总数', 'の販', '我来说', 'ائع', 'unia', ' pupper', ' warta', ' beleg', ' truff', 'ছিল', '_fact', 'vestig', 'undra', 'ivable', '人类的', ' ...(', '五颜六色的', ' Blasio', 'ceptive', '事实', ' zahl', ' trots', ' svel']

### end-pass input-prefix erased0.5 plain27

Lexical joint=False; alias AUROC=0.987500011920929.

['偶', ' **:**', '…**', ' odd', '各种各样', ' trots', 'odd', '../../../../', '五颜六色的', 'ẵn', '_depend', 'pairs', 'さま', '陪', '奇', '或少', 'ốn', 'čet', '人类的', ' beleg', '.gradle', '一般为', ' pupper', '各种各样的', ' .**', ' **:', '...**', '这个问题的', '{}".', 'undra', '声器', '病情分析']

### end-pass input-prefix J-lens

Lexical joint=False; alias AUROC=0.9125000238418579.

[' **', ' six', ' seven', ' nonexistent', ' five', '**', ' eight', 'five', ' twelve', 'eight', 'three', ' three', ' Five', ' thirteen', ' sixteen', 'six', 'plural', ' Actually', ' Eight', ' Depends', ' nine', ' Three', ' fewer', ' Seven', ' twenty', '...**', ' Answer', '：**', 'Five', ' Two', ' Six', 'equals']

## 3: goat

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of legs on the farm animal with a beard and curved horns is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Exact continuation:
```text
four<|im_end|>
```

Tokens: 2.

### end-pass input-prefix erased0.5 J-lens

Lexical joint=False; alias AUROC=0.90625.

[' **', '**', ' Answer', '的答案', 'plural', ' Answers', ' plural', ' Actually', 'Answer', '：**', '答案', ' Count', '...**', ' Three', ' Two', ' Depends', ' Five', 'answered', ' nonexistent', ' dozen', '事实', ' **[', ' This', ' It', '答案是', ' six', ' Based', ' Seven', ' seven', ' Usually', ':number', '<think>']

### end-pass input-prefix erased0.5 plain24

Lexical joint=False; alias AUROC=1.0.

['的答案', ' **:**', '…**', '=count', 'の販', 'ছিল', '我来说', ' warta', ':number', '.gradle', ' pupper', '总数', ' trots', ' BPK', ' Publicidad', '五颜六色的', '事实', 'čet', ' Rowling', '_fact', ' zahl', ' ...(', '駅から徒歩', '参考答案', '_depend', '一般为', ' Blasio', 'ivable', 'ائع', ' publice', ' beleg', 'geries']

### end-pass input-prefix erased0.5 plain27

Lexical joint=False; alias AUROC=1.0.

[' **:**', '…**', '偶', ' trots', '各种各样', 'ốn', '五颜六色的', '<think>', '../../../../', '_depend', 'さま', ' .**', ' odd', 'ี่ย', '的答案', '...**', '本题考查', 'odd', 'ẵn', ' ;-)', '这个问题的', '阿拉伯', ' Pôle', ' **:', ' Publicidad', 'の販', '各种各样的', '加拿大的', '版权声明', '病情分析', 'čet', '或少']

### end-pass input-prefix J-lens

Lexical joint=False; alias AUROC=0.90625.

[' **', '**', ' Answer', ' six', 'plural', ' seven', ' Three', ' Five', 'three', ' Answers', ' five', '的答案', ' twelve', ' eight', 'five', ' three', ' Seven', ' plural', ' Two', '...**', 'eight', 'Answer', ' thirteen', ' Eight', '：**', ' Actually', ' dozen', ' Twelve', ' nonexistent', 'six', ' Six', 'Five']

Capture: /workspace/2026/suppressed-activations/out/2026-10-01_110004_jlens-one-pass/run.md

Complete candidate records: /workspace/2026/suppressed-activations/out/2026-10-01_110021_jlens-one-pass/readout.json
