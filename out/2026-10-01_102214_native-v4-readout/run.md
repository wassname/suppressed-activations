---
generations: 8
max_new_tokens: 32
original_rows_exact: 144
candidate_rows: 32
---
# Frozen prefix readout, native-chat v4

— PI/OpenAI. Known concepts under a new uniform frame, not heldout concepts. Same head as2686; original144 rows exact,32 candidates. Full-list semantic review pending. Generated text is evaluation-only; rescoring has zero transformer calls.

| Method                                  | Lexical joint ↑   |   Alias AUROC ↑ |   AUROC n | Expected-answer matches   |
|:----------------------------------------|:------------------|----------------:|----------:|:--------------------------|
| end-pass input-prefix erased0.5 J-lens  | 4/8               |          0.9073 |         8 | 6/8                       |
| end-pass input-prefix erased0.5 plain24 | 0/8               |          0.8867 |         8 | 6/8                       |
| end-pass input-prefix erased0.5 plain27 | 4/8               |          0.8948 |         8 | 6/8                       |
| end-pass input-prefix J-lens            | 3/8               |          0.8951 |         8 | 6/8                       |

## 0: December

Rendered input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Exact continuation:
```text
January<|im_end|>
```

Token count: 2.

### end-pass input-prefix erased0.5 J-lens

Lexical joint=True.

[' **', ' Calendar', ' Year', ' Next', '事实', ' ...', '...', '次年', ' calendar', ' Tomorrow', ' Leap', '**', ' February', ' December', ' Future', ' Week', ' Winter', ' next', 'calendar', ' Spring', 'Next', ' holidays', '…', ' weeks', '(next', 'Calendar', ' Summer', '-month', ' Seasons', ' Holidays', ' Season', ' year']

### end-pass input-prefix erased0.5 plain24

Lexical joint=False.

['事实', '_fact', ' صدا', 'вис', 'orías', ' Fakta', ' fakta', ' Câ', '名副其实的', '…the', ' Pôle', 'óź', '事实和', '版权声明', '事實', ' beleg', 'ヵ', 'の販', ' prekybos', ' факта', ':...', ' факт', '?...', 'ément', ' Situé', '探し', '…**', '...(', ' sacerdo', '事实上', 'eceğ', '小编为大家整理的']

### end-pass input-prefix erased0.5 plain27

Lexical joint=True.

['_Dec', '事实', '版权声明', '展望', '寒冷的', '冬', '腊', '闰', ' Ро', ' ...', ' December', '…', 'Leap', ' Empresarial', '越し', 'ajukan', ' Leap', 'Dec', '新年快乐', '乞', ' Dec', ' صدا', 'apt', ' Fakta', ' факта', 'December', '事實', '_dec', ' Yours', '...', '元旦', '赔']

### end-pass input-prefix J-lens

Lexical joint=True.

[' February', ' December', ' Calendar', ' Year', ' **', '事实', '次年', ' November', ' Next', ' July', ' Winter', ' calendar', ' September', 'calendar', ' Leap', ' Tomorrow', '-month', ' Week', ' October', 'Calendar', ' Holidays', ' Spring', ' holidays', ' April', '/month', ' Seasons', '...**', ' weeks', 'December', '_year', ' Future', ' Season']

## 1: Thursday

Rendered input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Exact continuation:
```text
Tuesday<|im_end|>
```

Token count: 2.

### end-pass input-prefix erased0.5 J-lens

Lexical joint=True.

[' Tomorrow', ' **', ' Saturday', ' Friday', ' Monday', ' Midnight', ' Yesterday', ' Night', ' Sunday', ' Wednesday', ' Thursday', ' tomorrow', ' Today', ' Tonight', ' Christmas', ' Weekend', ' Thanksgiving', '事实', ' Halloween', ' weekend', '明天的', ' Evening', ' Morning', ' nights', ' weekends', ' Nights', ' Holidays', ' NIGHT', ' Leap', ' night', ' Sundays', ' Easter']

### end-pass input-prefix erased0.5 plain24

Lexical joint=False.

['事实', '_fact', ' fakta', ' факт', 'ceptive', '的事实', '事实和', '明天的', ' compro', '当地的', 'eve', ' Empresarial', ' факта', ' beleg', '本题考查', 'IVAL', '事实上', '赔', '…**', ' 사실', ' Fakten', ' fatos', ' Fakta', 'eceğ', ' صدا', ' факты', ' chôm', ' sacerdo', ' Pôle', '医疗队', ' fato', '版权声明']

### end-pass input-prefix erased0.5 plain27

Lexical joint=False.

['赔', '周一', 'Monday', '事实', ' Saturday', '圩', 'rides', ' среду', ' среда', ' Wednesday', ' Monday', '.tom', '安息', '普通的', ' weekends', ' Friday', '요일', '周六', '礼拜', '后天', 'Friday', 'fr', ' wed', ' Sunday', ' pazar', '中华人民共和国', ' sund', '금', '星期六', ' **', ' جم', '普通']

### end-pass input-prefix J-lens

Lexical joint=True.

[' Saturday', ' Monday', ' Friday', ' Wednesday', ' Thursday', ' Tomorrow', ' Sunday', ' Yesterday', ' tomorrow', ' Tonight', ' Midnight', ' Weekend', ' Night', ' Today', ' weekend', ' Mondays', ' Thanksgiving', ' Christmas', ' Sundays', '明天的', ' **', ' weekends', 'Monday', ' Evening', ' Morning', ' Halloween', ' Saturdays', '事实', ' Fridays', ' nights', ' Holidays', ' Nights']

## 2: autumn

Rendered input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Exact continuation:
```text
winter<|im_end|>
```

Token count: 2.

### end-pass input-prefix erased0.5 J-lens

Lexical joint=False.

[' **', '**', ' colder', ' drought', ' summer', ' frost', ' warmer', '...', ' Spring', '…', ' Tropical', '淡季', '事实', ' Frost', ' tropical', ' spring', ' rainy', ' Summer', '冬季', '冬天', '春天', ' autumn', '寒冬', ' warm', '夏季', ' Warm', ' ...', '-season', '春季', 'Spring', 'summer', '�']

### end-pass input-prefix erased0.5 plain24

Lexical joint=False.

[' fakta', ' факта', '_fact', '事实', ' наступ', '当地的', ' fatos', ' Pôle', ' fatt', ' Croce', '乞', ' recherch', ' Empresarial', 'orías', 'дем', ' факты', ' صدا', ' pitan', 'ẩm', '名副其实的', '越し', 'rollers', 'つも', 'óź', 'レード', '版权声明', '월까지', '件事', ' temper', ' 사실을', 'ontaine', 'lated']

### end-pass input-prefix erased0.5 plain27

Lexical joint=True.

['spring', ' spring', ' Spring', 'Spring', ' springs', ' summer', 'pring', '夏', 'summer', '冬', '.spring', '春', ' наступ', ' colder', '春天', '暑', '夏天', ' verano', 'zim', ' primavera', 'ฤดู', ' warmer', ' Empresarial', ' ...', ' summers', ' autumn', '寒冷', ' bore', ' лето', '版权声明', '夏天的', 'fall']

### end-pass input-prefix J-lens

Lexical joint=False.

[' summer', '冬季', '冬天', ' colder', 'summer', ' **', ' frost', '寒冬', ' drought', '淡季', ' warmer', ' Summer', ' autumn', ' Spring', '冬天的', '冬', '-season', '夏季', '春季', '春天', ' spring', 'spring', ' Tropical', ' primavera', ' vinter', ' Autumn', 'Spring', ' Frost', '_season', ' зим', ' printemps', ' rainy']

## 3: apple

Rendered input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Exact continuation:
```text
red<|im_end|>
```

Token count: 2.

### end-pass input-prefix erased0.5 J-lens

Lexical joint=False.

[' purple', ' green', ' pink', ' black', ' blue', '黑色的', ' Purple', ' violet', ' yellow', '红色', 'pink', 'purple', ' brown', 'black', 'green', '黑色', ' orange', ':red', ' dark', 'blue', '蓝色', '绿色', ':black', ' crimson', '的颜色', ':green', '绿色的', 'brown', ' Pink', '…**', '红色的', ' gray']

### end-pass input-prefix erased0.5 plain24

Lexical joint=False.

[':red', '…**', ' warta', 'меется', ' pales', ' สี', 'acin', 'мали', 'acre', 'imson', 'bán', 'isers', 'geries', '眯眯', ' Rowling', '同期的', '红了', ' утвер', 'lep', ' uby', '加拿大的', ' setBackgroundColor', ' berüh', ' 스위트', 'rosa', ' Eventi', 'iciels', '及配件', ' сбы', 'の販', 'ائع', '죄']

### end-pass input-prefix erased0.5 plain27

Lexical joint=False.

[':red', 'imson', '…**', ' крас', '红色', ' pales', 'acre', 'мали', ' berüh', '加拿大的', '本题考查', '”…', '通红', '\xa0\xa0\xa0', ' warta', 'acin', '五颜六色的', 'struments', 'สีแดง', ' kı', '_red', 'eiß', ' الأحمر', '如荼', ' Eintritt', '../../../../', ':green', '죄', '{}".', ' сбы', '各种各样', ' утвер']

### end-pass input-prefix J-lens

Lexical joint=False.

[' purple', '红色', ' green', ' blue', ' pink', ' black', ':red', 'green', 'black', 'blue', ' yellow', 'pink', 'purple', '红色的', ' Purple', ' brown', '黑色的', ' orange', ' violet', ' crimson', '黑色', '_red', '蓝色', '-red', ' dark', '绿色', '(red', ' rouge', 'brown', 'orange', 'yellow', ':black']

## 4: violin

Rendered input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Exact continuation:
```text
The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.

**Reasoning:**
1.  **Identify the instrument:**
```

Token count: 32.

### end-pass input-prefix erased0.5 J-lens

Lexical joint=True.

[' percussion', ' nonexistent', ' Vocal', ' vocal', ' **', ' Known', ' Unknown', ' Sound', ' **—', '…**', ' vocals', ' Silent', ' Actually', ' Heard', ' auditory', ' Nothing', ' **:**', ' Founded', ' unknown', ' known', ' Guitar', ' violin', '声乐', ' piano', ' Based', ' **.**', 'actually', ' Audio', ' **.', ' drums', ' Choir', ' flute']

### end-pass input-prefix erased0.5 plain24

Lexical joint=False.

['xhr', ' صدا', ' beleg', '...(', ' warta', '的事实', ' percussion', 'ốn', ' pipa', '小编为大家整理的', ' факта', ' ですが', 'плы', ' Isles', ' fapt', 'acre', 'ässe', 'đu', '树人', 'ungi', '沉寂', ' gry', 'โปรด', '事实', 'ագ', 'đenje', '__;', ' ;-)', '祉', '(eventName', '단은', '(&:']

### end-pass input-prefix erased0.5 plain27

Lexical joint=True.

['wind', ' percussion', ' wind', '弦', 'struments', ' winds', ' viento', ' Wind', ' brass', 'Wind', ' Strings', ' strings', ' pipa', ' drums', '风能', '打击', 'Strings', '声器', '鼓', '风的', 'strings', '键盘', '.wind', ' Perc', '风管', '风和', '_string', ' Brass', ' sax', ' Winds', ' viol', 'STRING']

### end-pass input-prefix J-lens

Lexical joint=False.

[' percussion', ' nonexistent', ' **', ' vocal', ' Vocal', ' Known', ' Unknown', '**', ' Sound', ' Actually', ' Silent', ' known', ' vocals', ' Nothing', ' Based', ' auditory', ' unknown', ' piano', ' violin', ' Founded', ' Guitar', 'actually', ' Heard', ' Audio', '声乐', ' drums', 'unknown', ' Wood', '…**', ' acoustic', ' flute', ' none']

## 5: Hamlet

Rendered input repr:
```text
"<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Exact continuation:
```text
William Shakespeare<|im_end|>
```

Token count: 3.

### end-pass input-prefix erased0.5 J-lens

Lexical joint=False.

[' Shakespeare', ' Robert', 'akespeare', ' Aristotle', ' Henry', ' Tolkien', ' Elizabeth', ' John', ' Edmund', ' Christopher', ' **', ' Sir', ' Richard', ' George', ' Julius', ' Samuel', ' Charles', ' Dickens', ' Hugo', ' Edward', ' Rowling', ' Daniel', ' Stephen', ' himself', '莎士比亚', ' Luke', ' Harry', ' Thomas', ' James', ' English', ' Benjamin', ' Jane']

### end-pass input-prefix erased0.5 plain24

Lexical joint=False.

['akespeare', '佚', ' onstage', '...(', 'ťa', ' tragedia', ' famously', 'чиной', ' **:**', ' spok', ' Ata', 'icide', 'র্ত', ' greve', '自来', ' Laufe', ' mily', '-fiction', ' _______,', '马拉', '?...', ' Hinblick', 'trar', ' berüh', 'vias', 'ehrte', ' spiritu', 'меется', 'टक', ' työn', ' vaid', ' fisse']

### end-pass input-prefix erased0.5 plain27

Lexical joint=False.

['akespeare', ' شك', ' onstage', ' Shakespeare', '莎士比亚', '这部剧', ' مسرح', ' Shakespe', '-play', 'icide', ' المسرح', ' tragedia', 'ốn', ' Mancha', '-fiction', '该剧', '话剧', 'ốc', 'коле', ' îns', ' teatr', ' sien', 'oling', 'åde', 'émie', ' théâtre', 'πτωση', 'erval', ' teb', 'Sir', 'engang', ' traged']

### end-pass input-prefix J-lens

Lexical joint=False.

[' Shakespeare', ' Robert', ' Henry', 'akespeare', ' Elizabeth', ' John', ' Christopher', ' Edmund', ' Aristotle', ' Tolkien', ' Richard', ' Charles', ' Edward', ' Samuel', ' George', 'Robert', ' Sir', ' Julius', ' Stephen', ' Dickens', ' Rowling', '莎士比亚', ' James', ' Hugo', ' Thomas', ' Benjamin', ' Daniel', 'Henry', ' Harry', 'John', ' Gabriel', ' **']

## 6: hydrogen

Rendered input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Exact continuation:
```text
gas<|im_end|>
```

Token count: 2.

### end-pass input-prefix erased0.5 J-lens

Lexical joint=False.

[' **', '**', 'liquid', ' liquid', ' Liquid', ' liquids', '液态', '…**', ' lique', '...**', ' vapor', 'fluid', ' Vapor', 'Liquid', ' fluids', ' fluid', ' Fluid', ' Answer', '固态', ':...', '**:', '�', ' frozen', '...', '液体', ' soluble', '：**', 'Answer', ' brittle', ' According', '____', '________']

### end-pass input-prefix erased0.5 plain24

Lexical joint=False.

['固态', '液态', 'ément', 'amu', ' namely', 'lep', 'โปร่ง', '常温', 'utow', '我来说', '英文名称', 'ائع', ' berüh', 'geries', ' lique', ' الاعتبار', 'anime', ' утвер', '加拿大的', 'vestig', '件事', 'irie', ' kwest', 'iration', 'liquid', '.freeze', ' liquids', ' Awake', ' physicists', '本题考查', 'free', '-free']

### end-pass input-prefix erased0.5 plain27

Lexical joint=False.

['固态', '气体', '气体的', '气', ' liquid', '液态', ' газо', ' газ', ' газа', '的气体', 'liquid', ' gaz', '_gas', ' liquids', ' گاز', ' غاز', '固体', ' الغاز', ' solid', '的气', ' твер', ' lỏng', ' fluids', 'solid', ' Liquid', ' gás', ' газов', '液体', ' rắn', 'غاز', ' gaze', 'fluid']

### end-pass input-prefix J-lens

Lexical joint=False.

['liquid', ' liquid', ' Liquid', ' **', ' liquids', '液态', '…**', ' lique', '**', '...**', ' vapor', 'fluid', ' Vapor', 'Liquid', ' fluids', ' fluid', ' Fluid', ':...', '固态', '液体', ' Answer', ' **—', '-fluid', ' Liqu', '：**', ' frozen', ' Frozen', ' soluble', ' **:**', '液体的', ' líqu', '**:']

## 7: triangle

Rendered input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Exact continuation:
```text
three<|im_end|>
```

Token count: 2.

### end-pass input-prefix erased0.5 J-lens

Lexical joint=True.

[' **', '**', ' Answer', ' Answers', '的答案', '答案是', 'Answer', '事实', '答案', ' Based', '...**', ' Always', '：**', ' Infinite', ' answer', 'answered', '…**', ' Greater', ' Depends', ' Fakt', ' fakta', 'greater', ' Triangle', ' Actually', ' **+', '的事实', ';**', ' According', ' Definitely', 'equal', '>**', '正确答案']

### end-pass input-prefix erased0.5 plain24

Lexical joint=False.

['.gradle', '的答案', '本题考查', 'ছিল', '事实', '_fact', '…**', ' zahl', '当地的', '<think>', '参考答案', ' ...(', '我来说', ' indefinitely', '陪', 'euillez', '答案是', ' факты', '的事实', ' beleg', 'église', '...\\', '_depend', '...(', ' Fakten', '通过使用', ' Vergangenheit', '偏方', '.gener', ' Öffentlichkeit', ' kebe', '阿拉伯']

### end-pass input-prefix erased0.5 plain27

Lexical joint=True.

['<think>', ' triangles', ' greater', '本题考查', 'greater', '_depend', '…**', '阿拉伯', '的答案', 'odd', '当地的', 'ilateral', '.isFile', '.gradle', ' odd', '_triangle', '参考答案', ' thirds', '事实', ' mitra', ' **:**', ' concurs', ' indefinitely', 'åde', '三角形', ' trots', ' pales', '_rectangle', 'always', '...**', '三角形的', '...,']

### end-pass input-prefix J-lens

Lexical joint=True.

[' **', ' Answer', '**', ' Answers', '的答案', '答案是', 'Answer', '...**', '答案', '事实', '…**', 'greater', ' Based', ' Always', 'answered', '：**', ' Infinite', ' Greater', ' Depends', ' Fakt', ' Triangle', ';**', ' fakta', 'equal', ' answer', ' **+', '>**', 'answer', ' Definitely', '的事实', ' Fakta', 'equals']

Capture: /workspace/2026/suppressed-activations/out/2026-10-01_102219_jlens-one-pass/run.md

Full candidate records: /workspace/2026/suppressed-activations/out/2026-10-01_102255_jlens-one-pass/readout.json
