---
generations: 4
original_rows_exact: 72
candidate_rows: 16
---
# Frozen readout on person bridges

— PI/OpenAI. Development only; same-country shortcuts and name-fragment ambiguity remain. No first-hop filter. Full semantic review pending.

| Method                                  | Lexical joint   |   Alias AUROC |   AUROC n |   Expected matches /4 |
|:----------------------------------------|:----------------|--------------:|----------:|----------------------:|
| end-pass input-prefix erased0.5 J-lens  | 0/4             |        0.8404 |         4 |                     3 |
| end-pass input-prefix erased0.5 plain24 | 0/4             |        0.8460 |         4 |                     3 |
| end-pass input-prefix erased0.5 plain27 | 0/4             |        0.8163 |         4 |                     3 |
| end-pass input-prefix J-lens            | 0/4             |        0.8429 |         4 |                     3 |

## 0: George Orwell

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing country name. Use present-day country names:\nFact: The author of the novel Nineteen Eighty-Four was born in the country of<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Exact continuation (2 tokens):
```text
England<|im_end|>
```

end-pass input-prefix erased0.5 J-lens; lexicaljoint=False:

[' Russia', ' Canada', ' Britain', ' Germany', ' France', ' United', ' Greece', ' Ireland', ' Australia', ' Denmark', ' Romania', ' British', ' Egypt', ' Nigeria', ' Poland', ' Scotland', ' India', ' Ukraine', ' Hungary', ' Finland', ' UK', ' Norway', ' China', '英国', ' Sweden', ' Jamaica', ' Iceland', ' Spain', ' Austria', ' Wales', ' USA', ' Japan']

end-pass input-prefix erased0.5 plain24; lexicaljoint=False:

['本题考查', 'truc', '叔叔', 'ずつ', '祖国', ' työn', '齐齐', '<think>', 'IRTH', ' Nagy', 'znacz', ' pena', ' شور', 'lük', 'ยักษ์', 'สห', '当当', '_kwargs', ' União', '辞', '生的', '\ufeff', ' hels', 'postav', 'つも', ' paš', '哪家好', '虚构', 'واطن', ' zza', ' Câ', ' RÉ']

end-pass input-prefix erased0.5 plain27; lexicaljoint=False:

[' United', '社会主义', '英国', '中华人民共和国', 'United', '<think>', ' socialism', ' Great', ' British', ' socialist', '\ufeff', 'British', 'สห', ' شور', '中国共产党', ' UNITED', 'ずつ', ' Nagy', ' União', 'UK', '叔叔', '英语', 'Great', ' communism', ' جما', ' Juta', ' Britain', '-Smith', '苏联', '英国的', ' СССР', '英伦']

end-pass input-prefix J-lens; lexicaljoint=False:

[' Britain', ' Russia', ' Canada', ' Germany', ' France', ' Scotland', ' Ireland', ' Denmark', ' Greece', '英国', ' Australia', 'Britain', ' Poland', ' Romania', ' Egypt', ' Nigeria', ' Wales', ' Hungary', ' British', 'Russia', ' India', 'Canada', ' Finland', ' Sweden', 'Germany', ' Ukraine', ' Spain', ' Norway', ' United', ' Italy', ' Belgium', ' UK']

## 1: Salman Rushdie

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing country name. Use present-day country names:\nFact: The author of the novel The Satanic Verses was born in the country of<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Exact continuation (2 tokens):
```text
India<|im_end|>
```

end-pass input-prefix erased0.5 J-lens; lexicaljoint=False:

[' Pakistan', ' England', ' Nigeria', ' France', ' Canada', ' Egypt', ' Iraq', ' Bangladesh', ' Greece', ' Iran', ' Australia', ' Britain', ' Italy', ' Kenya', ' Argentina', ' Afghanistan', ' Switzerland', ' Lebanon', ' Malaysia', ' Qatar', ' Turkey', ' Israel', ' Morocco', ' Germany', ' Bahrain', ' Denmark', ' United', ' Tunisia', ' Mexico', ' Ireland', ' Romania', ' Indonesia']

end-pass input-prefix erased0.5 plain24; lexicaljoint=False:

['祖国', '叔叔', '祖国的', '齐齐', '�', 'OfBirth', ' Trin', ' työn', '风云', ' bolsas', 'IRTH', '虚构', '本题考查', '<think>', ' fictional', ' vaid', 'fuck', 'Birth', 'Hoa', 'truc', '驻', '이란', ' zza', ' republic', ' Teh', '肄', '兀', 'atorial', ' Consultants', ' граждани', ' Assistenza', '_hooks']

end-pass input-prefix erased0.5 plain27; lexicaljoint=False:

[' United', '��', '中华人民共和国', '英国', '이란', 'United', ' British', 'British', '<think>', 'U', 'ปาก', 'ghanistan', '叔叔', 'atively', ' UKM', '_kwargs', 'iture', 'bsites', '�', 'ktor', 'ettori', ' bomba', ' Consultants', 'ずつ', 'worm', ' virtu', '艺术团', ' Verein', ' UNITED', 'ốn', '凤凰', ' militants']

end-pass input-prefix J-lens; lexicaljoint=False:

[' Pakistan', ' Nigeria', ' England', ' France', ' Canada', ' Egypt', ' Bangladesh', ' Greece', ' Iraq', ' Italy', ' Britain', ' Australia', ' Iran', ' Malaysia', ' Argentina', ' Kenya', ' Indonesia', ' Germany', ' Turkey', ' Switzerland', ' Morocco', ' Afghanistan', ' Ireland', ' Tunisia', ' Mexico', 'Canada', 'France', ' Denmark', ' Algeria', ' Lebanon', ' Israel', ' Spain']

## 2: Cao Xueqin

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing country name. Use present-day country names:\nFact: The author of the novel Dream of the Red Chamber was born in the country of<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Exact continuation (2 tokens):
```text
China<|im_end|>
```

end-pass input-prefix erased0.5 J-lens; lexicaljoint=False:

[' Japan', ' Indonesia', ' Russia', ' Canada', ' United', ' Pakistan', ' Germany', ' Thailand', ' England', ' India', ' Poland', ' Bangladesh', ' Italy', ' Sweden', ' Australia', ' Netherlands', ' Mongolia', ' Ukraine', ' Greece', ' Denmark', ' France', ' Philippines', ' Austria', ' Venezuela', ' Korea', ' Hungary', ' Kingdom', ' Argentina', ' Taiwan', ' Scotland', ' Egypt', ' Romania']

end-pass input-prefix erased0.5 plain24; lexicaljoint=False:

['祖国', '现', '本题考查', 'current', ' beleg', 'IRTH', '汶', '今天的', '<think>', '爱奇艺', 'leitung', '肄', '中国的', 'ずつ', '现在的', '江苏', 'ยักษ์', ' Lâm', '中华人民共和国', '我国', 'меется', ' fapt', ' ceea', ' Pony', '靖', ' Brushes', ' spies', '清朝', ' Téléphone', '叔叔', ' Fixture', '邻']

end-pass input-prefix erased0.5 plain27; lexicaljoint=False:

['中国的', '中华人民共和国', '中国', '中国人民解放军', ' Chinese', '中國', 'Chinese', '的中国', '中国共产党', ' چین', '_Ch', ' Zhao', '中国人', '<think>', ' Китай', '中华', '中国经济', '清朝', '...', ' Китая', ' Chine', '了中国', '今天的', '中国队', '中國大陸', '在中国', ' Tiongkok', '是中国', '中国在', '亿元人民币', '中国古代', '中国人民']

end-pass input-prefix J-lens; lexicaljoint=False:

[' Japan', ' Russia', ' Indonesia', '-China', 'Japan', ' India', ' Canada', ' Germany', ' Thailand', ' Mongolia', ' Pakistan', ' Korea', ' Taiwan', ' Poland', ' Italy', ' England', ' Australia', ' Greece', ' France', ' Sweden', ' Chinese', ' Hungary', ' Bangladesh', ' Ukraine', ' Denmark', 'Russia', ' Egypt', ' Malaysia', 'Chinese', ' Austria', '中国', ' Philippines']

## 3: Wu Cheng'en

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing country name. Use present-day country names:\nFact: The author of the novel Journey to the West was born in the country of<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Exact continuation (2 tokens):
```text
China<|im_end|>
```

end-pass input-prefix erased0.5 J-lens; lexicaljoint=False:

[' Japan', ' Indonesia', ' Thailand', ' Philippines', ' Australia', ' Russia', ' United', ' Greece', ' Myanmar', ' India', ' Italy', ' Germany', ' England', ' Mongolia', ' Vietnam', ' Canada', ' Mexico', ' Bangladesh', ' Brazil', ' Malaysia', ' Egypt', ' Argentina', ' Nigeria', ' France', ' Pakistan', ' Spain', ' Kenya', ' Ukraine', ' Portugal', ' Korea', ' Kingdom', ' Poland']

end-pass input-prefix erased0.5 plain24; lexicaljoint=False:

['祖国', 'IRTH', 'ยักษ์', '中华人民共和国', '本题考查', 'ずつ', ' fapt', '_kwargs', 'меется', 'leitung', '叔叔', ' beleg', ' стрем', '<think>', ' Fixture', ' Lâm', 'さま', '็ก', ' صدا', ' União', '中国的', '我国', ' työn', '学籍', 'ujian', ' Kingdom', ' Brushes', ' راهن', '祖国的', '现', ' vaid', 'ceptive']

end-pass input-prefix erased0.5 plain27; lexicaljoint=False:

['中华人民共和国', '中国的', '中国', '中国人民解放军', ' Chinese', '中国共产党', ' چین', '<think>', 'Chinese', '的中国', '中國', '_Ch', '...', '中国人', ' Zhao', ' sino', ' Republic', '中华', ' **', '中国队', '我国', '亿元人民币', '了中国', ' الصين', '中国经济', '是中国', '在中国', ' Lâm', 'ào', ' DPR', '社会主义', ' Chine']

end-pass input-prefix J-lens; lexicaljoint=False:

[' Japan', ' Indonesia', ' Thailand', ' Russia', ' India', 'Japan', ' Mongolia', '-China', ' Australia', ' Philippines', ' Greece', ' Italy', ' Korea', ' Germany', ' Brazil', ' Malaysia', ' Vietnam', ' Taiwan', ' Egypt', ' Canada', ' England', ' France', ' Myanmar', ' Nigeria', ' Spain', ' Mexico', ' Bangladesh', ' Poland', ' Argentina', ' Pakistan', ' Portugal', ' Turkey']

Capture: /workspace/2026/suppressed-activations/out/2026-10-01_142056_jlens-one-pass/run.md

Full scores: /workspace/2026/suppressed-activations/out/2026-10-01_142107_jlens-one-pass/readout.json

Pair diagnostics: /workspace/2026/suppressed-activations/out/2026-10-01_142049_person-pairs-readout/pair_diagnostics.json
