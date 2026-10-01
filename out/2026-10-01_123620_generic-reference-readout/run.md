---
generic_prefills: 1
case_forward_calls: 0
---
| Cohort / method                                                      | Lexical joint ↑   |   Gains |   Losses |   Alias AUROC ↑ |   AUROC n |
|:---------------------------------------------------------------------|:------------------|--------:|---------:|----------------:|----------:|
| native-v4: end-pass input-prefix generic-reference erased0.5 J-lens  | 3/8               |       0 |        1 |          0.8842 |         8 |
| native-v4: end-pass input-prefix random-reference erased0.5 J-lens   | 2/8               |       0 |        2 |          0.9008 |         8 |
| native-v4: end-pass input-prefix generic-reference erased0.5 plain24 | 0/8               |       0 |        0 |          0.8906 |         8 |
| native-v4: end-pass input-prefix random-reference erased0.5 plain24  | 0/8               |       0 |        0 |          0.8864 |         8 |
| native-v4: end-pass input-prefix generic-reference erased0.5 plain27 | 3/8               |       0 |        1 |          0.9000 |         8 |
| native-v4: end-pass input-prefix random-reference erased0.5 plain27  | 1/8               |       1 |        4 |          0.8967 |         8 |
| native-v4: end-pass input-prefix erased0.5 J-lens                    | 4/8               |       0 |        0 |          0.9073 |         8 |
| native-v4: end-pass input-prefix erased0.5 plain24                   | 0/8               |       0 |        0 |          0.8867 |         8 |
| native-v4: end-pass input-prefix erased0.5 plain27                   | 4/8               |       0 |        0 |          0.8948 |         8 |
| native-v4: end-pass input-prefix J-lens                              | 3/8               |       0 |        0 |          0.8951 |         8 |
| animals: end-pass input-prefix generic-reference erased0.5 J-lens    | 0/4               |       0 |        0 |          0.8750 |         3 |
| animals: end-pass input-prefix random-reference erased0.5 J-lens     | 0/4               |       0 |        0 |          0.9646 |         3 |
| animals: end-pass input-prefix generic-reference erased0.5 plain24   | 0/4               |       0 |        0 |          0.8833 |         3 |
| animals: end-pass input-prefix random-reference erased0.5 plain24    | 0/4               |       0 |        0 |          0.9958 |         3 |
| animals: end-pass input-prefix generic-reference erased0.5 plain27   | 0/4               |       0 |        0 |          0.8875 |         3 |
| animals: end-pass input-prefix random-reference erased0.5 plain27    | 0/4               |       0 |        0 |          0.9958 |         3 |
| animals: end-pass input-prefix erased0.5 J-lens                      | 0/4               |       0 |        0 |          0.9063 |         3 |
| animals: end-pass input-prefix erased0.5 plain24                     | 0/4               |       0 |        0 |          0.9958 |         3 |
| animals: end-pass input-prefix erased0.5 plain27                     | 0/4               |       0 |        0 |          0.9958 |         3 |
| animals: end-pass input-prefix J-lens                                | 0/4               |       0 |        0 |          0.9063 |         3 |

# Generic normalized-state subtraction

— PI/OpenAI. One generic prefill, no new case trajectories; semantic review pending. No second norm. Random references match before projection only. Known development cases; no v5.

## native-v4 (8 cases)

Full records: /workspace/2026/suppressed-activations/out/2026-10-01_123644_jlens-one-pass/readout.json

### 0: December

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The month immediately after the month containing Christmas Day is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Unchanged exact output:
```text
January<|im_end|>
```

end-pass input-prefix generic-reference erased0.5 J-lens; lexicaljoint=True:

['次年', '年末', '月份', '年底', ' next', 'weeks', '...', '月份的', '…', ' ...', '-month', '下旬', '月底', 'next', '.month', ' weeks', '明年的', '季度的', ' December', '_months', '旬', '月末', '翌', ' …', '第二年', '月份开始', 'เดือน', '下一个', ' week', '明年', ' fortn', '_month']

end-pass input-prefix random-reference erased0.5 J-lens; lexicaljoint=False:

[' **', ' Spring', ' Calendar', '**', 'next', ' next', 'calendar', '次年', 'spring', ' calendar', '明天的', '/calendar', ' Future', ' spring', 'icipation', ' Actually', ' February', ' Forget', '事实', ' weeks', ' Name', 'weeks', 'winter', ' Tomorrow', 'actually', ' September', ' Iceland', ' Next', '_calendar', 'argo', 'ef', ' July']

end-pass input-prefix generic-reference erased0.5 plain24; lexicaljoint=False:

['ifle', '人家', ' reck', 'unie', 'anness', '别样', '永兴', '追い', 'eves', 'gren', ' curs', ' Vista', '展望', ' Alasan', 'ivent', ' wards', '名义', '明年的', 'cidental', ' spok', 'tivo', 'كير', '和西', 'UST', 'ibert', 'ordert', '技术性', 'ivant', '準', '.sha', 'вест', 'odash']

end-pass input-prefix random-reference erased0.5 plain24; lexicaljoint=False:

['обе', 'icipation', 'undle', '人类的', 'argo', ' صدا', '_filled', '直辖', 'minen', '営', 'ایش', 'arily', '版权声明', 'èrement', 'ogos', '事实和', 'óa', '当地的', '_revision', ' neve', 'itom', '加拿大的', ' факт', '加拿大', '월까지', '[...,', '展望', ' spoiler', '赔', '-toast', '[]={', ' Forget']

end-pass input-prefix generic-reference erased0.5 plain27; lexicaljoint=True:

[' Dec', '展望', '新年的', ' dec', '_Dec', ' procur', 'cidental', 'Dec', '最后是', '.…', '元旦', ' Ро', ' next', ' December', '然后是', ' …', 'December', '过年的', '.Dec', '圣诞', ' called', '年货', ',..', ' Boxing', '次年', '年末', 'eves', '明年的', '-Jan', ',…', '接下来的', '紧接着']

end-pass input-prefix random-reference erased0.5 plain27; lexicaljoint=False:

['展望', ' neve', 'وج', '版权声明', '_Dec', 'awl', 'icipation', ' Ро', '人类的', 'undle', 'ajukan', '赔', '惊', 'обе', '加拿大', ' yours', '直辖', '有声', 'ایش', '新加坡', 'idez', 'oghi', '-toast', 'cak', 'ncer', 'áp', '.isFile', ' *))', '越し', 'andalkan', '陪', 'away']

end-pass input-prefix erased0.5 J-lens; lexicaljoint=True:

[' **', ' Calendar', ' Year', ' Next', '事实', ' ...', '...', '次年', ' calendar', ' Tomorrow', ' Leap', '**', ' February', ' December', ' Future', ' Week', ' Winter', ' next', 'calendar', ' Spring', 'Next', ' holidays', '…', ' weeks', '(next', 'Calendar', ' Summer', '-month', ' Seasons', ' Holidays', ' Season', ' year']

end-pass input-prefix erased0.5 plain24; lexicaljoint=False:

['事实', '_fact', ' صدا', 'вис', 'orías', ' Fakta', ' fakta', ' Câ', '名副其实的', '…the', ' Pôle', 'óź', '事实和', '版权声明', '事實', ' beleg', 'ヵ', 'の販', ' prekybos', ' факта', ':...', ' факт', '?...', 'ément', ' Situé', '探し', '…**', '...(', ' sacerdo', '事实上', 'eceğ', '小编为大家整理的']

end-pass input-prefix erased0.5 plain27; lexicaljoint=True:

['_Dec', '事实', '版权声明', '展望', '寒冷的', '冬', '腊', '闰', ' Ро', ' ...', ' December', '…', 'Leap', ' Empresarial', '越し', 'ajukan', ' Leap', 'Dec', '新年快乐', '乞', ' Dec', ' صدا', 'apt', ' Fakta', ' факта', 'December', '事實', '_dec', ' Yours', '...', '元旦', '赔']

end-pass input-prefix J-lens; lexicaljoint=True:

[' February', ' December', ' Calendar', ' Year', ' **', '事实', '次年', ' November', ' Next', ' July', ' Winter', ' calendar', ' September', 'calendar', ' Leap', ' Tomorrow', '-month', ' Week', ' October', 'Calendar', ' Holidays', ' Spring', ' holidays', ' April', '/month', ' Seasons', '...**', ' weeks', 'December', '_year', ' Future', ' Season']

### 1: Thursday

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The day immediately after the weekday named after Thor is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Unchanged exact output:
```text
Tuesday<|im_end|>
```

end-pass input-prefix generic-reference erased0.5 J-lens; lexicaljoint=True:

['第二天', ' Thursday', ' Saturday', '.week', ' Sunday', ' Wednesday', ' Friday', ' Christmas', ' evening', '晚上', '圣诞节', ' Sabbath', ' weekend', '第三天', ' nights', '星期六', '_week', ' night', '傍晚', ' Nights', '夜里', '-week', '星期日', '次日', 'weeks', 'Saturday', '最后一天', ' friday', 'Thursday', '星期四', '月底', ' Monday']

end-pass input-prefix random-reference erased0.5 J-lens; lexicaljoint=True:

['明天的', ' Monday', ' Tomorrow', ' Saturday', ' Sunday', ' **', ' Wednesday', ' tomorrow', ' Friday', '**', ' Tonight', ' Zod', ' Wake', ' Know', ' nights', ' Thanksgiving', ' Sabbath', ' Midnight', ' Sun', ' Thursday', ' Iceland', ' Forget', '明天', ' Nights', ' Queen', ' Santa', '事实', ' Truth', ' Halloween', ' Sund', ' Comet', ' Observatory']

end-pass input-prefix generic-reference erased0.5 plain24; lexicaljoint=False:

['ornos', 'ivant', '的西', 'eves', ' reck', '和西', '宕', 'tivo', ' curs', '形象', 'veau', '璐', '个性', '别样', '人家', 'ivin', 'yar', 'oriented', 'anness', 'ibert', '追い', '民用', 'gren', 'enste', 'stellungen', 'vester', 'yani', 'одук', 'orient', ' ори', 'eve', 'ivent']

end-pass input-prefix random-reference erased0.5 plain24; lexicaljoint=False:

[' факт', '明天的', '当地的', '営', 'icipation', ' neve', '事实和', 'andet', '赔', '人类的', 'undle', 'وج', '帳', '事实', '检查一下', 'áp', '惊', 'wand', '_filled', 'ランド', 'argo', '索', 'yar', 'ughter', '่ม', 'itom', '有声', '_fact', '直辖', 'ایش', 'ổ', '=count']

end-pass input-prefix generic-reference erased0.5 plain27; lexicaljoint=False:

[' wed', ' среду', '普通', '安息', 'Saturday', '星期三', ' Saturday', ' Sabbath', 'fr', 'borg', '星期六', '不顺', '星期四', ' Wednesday', ' среда', 'ond', 'aturday', 'neutral', 'undi', 'พร', '礼拜', '个性', '周三', 'yar', 'Wednesday', ' terça', ' среды', '法定', ' Sunday', ' 목', 'Friday', 'FR']

end-pass input-prefix random-reference erased0.5 plain27; lexicaljoint=True:

['赔', '索', 'undle', '人类的', 'ランド', 'وج', ' جم', '普通的', '惊', '체크', '금', 'Monday', '礼拜', ' مجرد', '่ม', '检查一下', ' thu', 'icipation', ' wed', 'たび', 'AK', 'andet', ' tradition', 'OfWeek', 'ries', 'نده', 'nosis', '産', 'ecz', ' Monday', '安息', 'yar']

end-pass input-prefix erased0.5 J-lens; lexicaljoint=True:

[' Tomorrow', ' **', ' Saturday', ' Friday', ' Monday', ' Midnight', ' Yesterday', ' Night', ' Sunday', ' Wednesday', ' Thursday', ' tomorrow', ' Today', ' Tonight', ' Christmas', ' Weekend', ' Thanksgiving', '事实', ' Halloween', ' weekend', '明天的', ' Evening', ' Morning', ' nights', ' weekends', ' Nights', ' Holidays', ' NIGHT', ' Leap', ' night', ' Sundays', ' Easter']

end-pass input-prefix erased0.5 plain24; lexicaljoint=False:

['事实', '_fact', ' fakta', ' факт', 'ceptive', '的事实', '事实和', '明天的', ' compro', '当地的', 'eve', ' Empresarial', ' факта', ' beleg', '本题考查', 'IVAL', '事实上', '赔', '…**', ' 사실', ' Fakten', ' fatos', ' Fakta', 'eceğ', ' صدا', ' факты', ' chôm', ' sacerdo', ' Pôle', '医疗队', ' fato', '版权声明']

end-pass input-prefix erased0.5 plain27; lexicaljoint=False:

['赔', '周一', 'Monday', '事实', ' Saturday', '圩', 'rides', ' среду', ' среда', ' Wednesday', ' Monday', '.tom', '安息', '普通的', ' weekends', ' Friday', '요일', '周六', '礼拜', '后天', 'Friday', 'fr', ' wed', ' Sunday', ' pazar', '中华人民共和国', ' sund', '금', '星期六', ' **', ' جم', '普通']

end-pass input-prefix J-lens; lexicaljoint=True:

[' Saturday', ' Monday', ' Friday', ' Wednesday', ' Thursday', ' Tomorrow', ' Sunday', ' Yesterday', ' tomorrow', ' Tonight', ' Midnight', ' Weekend', ' Night', ' Today', ' weekend', ' Mondays', ' Thanksgiving', ' Christmas', ' Sundays', '明天的', ' **', ' weekends', 'Monday', ' Evening', ' Morning', ' Halloween', ' Saturdays', '事实', ' Fridays', ' nights', ' Holidays', ' Nights']

### 2: autumn

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Unchanged exact output:
```text
winter<|im_end|>
```

end-pass input-prefix generic-reference erased0.5 J-lens; lexicaljoint=False:

['春季', '冬季', '…', '冬', '冬天', '秋季', ' spring', '...', ' colder', ' primavera', ' warmer', 'spring', ' frost', ' autumn', '季节', '次年', ' …', '-season', '雨季', '夏令', '淡季', ' summer', '秋冬', '回暖', '夏季', '倒退', 'Spring', '冬天的', ' drought', ' ...', '春天', '暖和']

end-pass input-prefix random-reference erased0.5 J-lens; lexicaljoint=False:

[' colder', ' **', '**', ' spring', ' warmer', ' tropical', ' Spring', ' Tropical', 'spring', 'Spring', ' Antarctic', ' warmth', ' summer', ' frost', ' sunshine', '变暖', '春季', ' Antarctica', ' snow', '冻', ' sunny', ' Arctic', '寒风', '干旱', '冬季', '温暖', '严寒', '回暖', ' freezing', ' primavera', 'undra', ' drought']

end-pass input-prefix generic-reference erased0.5 plain24; lexicaljoint=False:

['agin', ' wards', '人家', 'ivin', 'Ấ', '挨', 'asty', 'estiv', '倒退', 'anness', '翡', '逼', '準', 'tivo', 'come', ' ką', '盟', ' cocks', ' mell', 'дем', 'möglichkeit', 'cales', 'ivent', '和西', 'angat', ' Pru', '别样', 'eves', '屁股', '之音', 'ibert', 'hots']

end-pass input-prefix random-reference erased0.5 plain24; lexicaljoint=False:

['обе', '営', '当地的', 'itative', 'ایش', 'Ấ', 'தை', 'ergia', ' neve', '월까지', '่ม', ' факта', 'ughter', '友', 'arily', 'icipation', 'actually', '人类的', 'andet', 'undra', ' colder', 'undle', '谚语', 'cak', ' fatt', 'ectomy', '_revision', '[...,', '灌', '更没有', 'isez', '[]={']

end-pass input-prefix generic-reference erased0.5 plain27; lexicaljoint=True:

[' spring', 'spring', ' Spring', 'Spring', ' springs', '春意', '春季', '.spring', 'Ấ', ' summer', 'pring', '倒退', ' primavera', '春天', '夏季', '春的', 'summer', ' called', '夏天', 'estiv', '冬', ' colder', ' …', ' warmer', '봄', '温暖', ' bore', ' cooler', ' autumn', 'imą', '然后是', ' inver']

end-pass input-prefix random-reference erased0.5 plain27; lexicaljoint=False:

['spring', ' spring', 'Spring', ' Spring', '.spring', ' colder', 'pring', ' springs', 'Ấ', 'undra', 'summer', ' neve', '加拿大', 'icipation', 'cak', '営', ' summer', ' primavera', '冬', 'ectomy', '版权声明', ' вес', 'ivy', ' warmer', '่ม', 'ean', 'ใบ', '春意', '谚语', '温暖', ' temper', 'othermal']

end-pass input-prefix erased0.5 J-lens; lexicaljoint=False:

[' **', '**', ' colder', ' drought', ' summer', ' frost', ' warmer', '...', ' Spring', '…', ' Tropical', '淡季', '事实', ' Frost', ' tropical', ' spring', ' rainy', ' Summer', '冬季', '冬天', '春天', ' autumn', '寒冬', ' warm', '夏季', ' Warm', ' ...', '-season', '春季', 'Spring', 'summer', '�']

end-pass input-prefix erased0.5 plain24; lexicaljoint=False:

[' fakta', ' факта', '_fact', '事实', ' наступ', '当地的', ' fatos', ' Pôle', ' fatt', ' Croce', '乞', ' recherch', ' Empresarial', 'orías', 'дем', ' факты', ' صدا', ' pitan', 'ẩm', '名副其实的', '越し', 'rollers', 'つも', 'óź', 'レード', '版权声明', '월까지', '件事', ' temper', ' 사실을', 'ontaine', 'lated']

end-pass input-prefix erased0.5 plain27; lexicaljoint=True:

['spring', ' spring', ' Spring', 'Spring', ' springs', ' summer', 'pring', '夏', 'summer', '冬', '.spring', '春', ' наступ', ' colder', '春天', '暑', '夏天', ' verano', 'zim', ' primavera', 'ฤดู', ' warmer', ' Empresarial', ' ...', ' summers', ' autumn', '寒冷', ' bore', ' лето', '版权声明', '夏天的', 'fall']

end-pass input-prefix J-lens; lexicaljoint=False:

[' summer', '冬季', '冬天', ' colder', 'summer', ' **', ' frost', '寒冬', ' drought', '淡季', ' warmer', ' Summer', ' autumn', ' Spring', '冬天的', '冬', '-season', '夏季', '春季', '春天', ' spring', 'spring', ' Tropical', ' primavera', ' vinter', ' Autumn', 'Spring', ' Frost', '_season', ' зим', ' printemps', ' rainy']

### 3: apple

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The usual color of the fruit poisoned in the story of Snow White is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Unchanged exact output:
```text
red<|im_end|>
```

end-pass input-prefix generic-reference erased0.5 J-lens; lexicaljoint=False:

[' purple', '黑色', ' pink', '红色', ' green', 'pink', ' black', ' violet', '紫色', '颜色', '绿色', ' orange', 'purple', ' grey', ' colour', ' yellow', '黑色的', 'colour', 'green', '蓝色', 'black', ' crimson', ' blue', '白色', ' brown', '粉红色', ' coloured', '黄色', '颜色的', '绿色的', ' tint', 'yellow']

end-pass input-prefix random-reference erased0.5 J-lens; lexicaljoint=False:

[':red', ' orange', ' rouge', ' green', ' blue', 'pink', ' purple', ' crimson', ' pink', 'สีแดง', ' violet', 'blue', ' darker', ' yellow', ' berries', '蓝色', '’**', 'cak', ' striped', 'สี', 'warning', '**', '/color', '红色', 'green', ' Farbe', 'orange', 'verde', ' dark', '_colors', ' rouges', '.color']

end-pass input-prefix generic-reference erased0.5 plain24; lexicaljoint=False:

['ivant', 'imson', 'gren', 'ornos', '殷', 'ivent', 'awas', 'âteaux', 'enste', 'وين', '呈', 'yers', '红色', ' ihan', 'iciels', 'agin', ' 심', 'ocking', ' Cun', 'иви', 'ensial', '別人', 'oref', 'rosso', 'enta', 'iach', 'imony', '黑色', '镖', ' curs', '及配件', '紫']

end-pass input-prefix random-reference erased0.5 plain24; lexicaljoint=False:

['acin', ':red', 'acre', '加拿大的', '=count', 'うちに', 'ổ', '営', 'lable', 'ablanca', 'cak', '่ม', 'warning', 'ehl', 'اصر', 'andet', '色列', 'yla', 'eceğini', ' *))', '_theme', 'itaine', 'wäl', 'đu', '当地的', 'iria', 'akai', '_WARNING', 'мали', 'umfang', 'giá', 'ivy']

end-pass input-prefix generic-reference erased0.5 plain27; lexicaljoint=False:

['imson', '红色', '黑色', 'yers', '…**', '紅色', '”…', 'undy', ')…', '绿色', 'ittal', ',…', '.…', 'gren', '-danger', ' BLACK', 'iciels', ' крас', 'iach', 'бором', 'enta', '.Transactional', '红线', '",[', ' czerw', 'atham', '{}".', ' poisoning', '黑色的', ' 빨', ' hitam', '殷']

end-pass input-prefix random-reference erased0.5 plain27; lexicaljoint=False:

[':red', 'acin', '加拿大的', 'acre', 'cak', 'imson', '’**', 'สีแดง', 'ablanca', 'itaine', '新加坡', 'โฉ', 'yla', '\xa0\xa0\xa0\xa0\xa0\xa0\xa0', ' крас', 'warning', ' *))', '注册地址', 'akai', 'мали', 'undra', 'うちに', 'しぶ', '=count', ' berüh', '根深', '红红的', '\xa0\xa0\xa0', '通红', 'ehl', '色列', '加拿大']

end-pass input-prefix erased0.5 J-lens; lexicaljoint=False:

[' purple', ' green', ' pink', ' black', ' blue', '黑色的', ' Purple', ' violet', ' yellow', '红色', 'pink', 'purple', ' brown', 'black', 'green', '黑色', ' orange', ':red', ' dark', 'blue', '蓝色', '绿色', ':black', ' crimson', '的颜色', ':green', '绿色的', 'brown', ' Pink', '…**', '红色的', ' gray']

end-pass input-prefix erased0.5 plain24; lexicaljoint=False:

[':red', '…**', ' warta', 'меется', ' pales', ' สี', 'acin', 'мали', 'acre', 'imson', 'bán', 'isers', 'geries', '眯眯', ' Rowling', '同期的', '红了', ' утвер', 'lep', ' uby', '加拿大的', ' setBackgroundColor', ' berüh', ' 스위트', 'rosa', ' Eventi', 'iciels', '及配件', ' сбы', 'の販', 'ائع', '죄']

end-pass input-prefix erased0.5 plain27; lexicaljoint=False:

[':red', 'imson', '…**', ' крас', '红色', ' pales', 'acre', 'мали', ' berüh', '加拿大的', '本题考查', '”…', '通红', '\xa0\xa0\xa0', ' warta', 'acin', '五颜六色的', 'struments', 'สีแดง', ' kı', '_red', 'eiß', ' الأحمر', '如荼', ' Eintritt', '../../../../', ':green', '죄', '{}".', ' сбы', '各种各样', ' утвер']

end-pass input-prefix J-lens; lexicaljoint=False:

[' purple', '红色', ' green', ' blue', ' pink', ' black', ':red', 'green', 'black', 'blue', ' yellow', 'pink', 'purple', '红色的', ' Purple', ' brown', '黑色的', ' orange', ' violet', ' crimson', '黑色', '_red', '蓝色', '-red', ' dark', '绿色', '(red', ' rouge', 'brown', 'orange', 'yellow', ':black']

### 4: violin

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Unchanged exact output:
```text
The orchestral family of the musical instrument played by Sherlock Holmes is **woodwind**.

**Reasoning:**
1.  **Identify the instrument:**
```

end-pass input-prefix generic-reference erased0.5 J-lens; lexicaljoint=False:

[' vocal', ' percussion', '声乐', ' Vocal', ' vocalist', ' vocals', ' violin', '活跃', ' auditory', ' wood', ' comprised', '乐器', ' singing', 'angat', ' consisted', ' guitars', 'AUDIO', ' chiefly', ' choir', ' acoustic', ' recorder', ' sonor', ' arty', ' voice', ' bass', ' trumpet', '有声', ' melod', '配音', '较轻', '声器', ' flute']

end-pass input-prefix random-reference erased0.5 J-lens; lexicaljoint=False:

[' vocal', ' percussion', ' Sound', ' nonexistent', '声乐', ' acoustic', ' Vocal', ' Vibr', ' humans', 'actually', ' vocals', ' Rifle', ' Audio', 'icipation', ' microphone', 'andet', ' auditory', ' actually', ' known', '’**', ' Humans', ' Piano', ' sound', ' Guitar', ' Known', ' faktisk', '>**', ' tradition', ' Actually', "'**", '有声', '塘镇']

end-pass input-prefix generic-reference erased0.5 plain24; lexicaljoint=False:

['agin', '人家', 'holz', 'ust', 'тиви', 'ivent', 'дек', 'weite', '在用', 'aup', ' heck', 'ը', 'UST', '华人', ' vocals', 'oud', '..\\', 'верх', ' sauv', ' họ', 'ivant', ' eher', ' Vanguard', 'leden', 'awas', 'ึ่ง', ' wood', '由原告', 'strup', 'wind', ' percussion', ' woods']

end-pass input-prefix random-reference erased0.5 plain24; lexicaljoint=False:

['営', 'обе', 'đu', 'acre', 'тиви', '有声', 'xhr', ' neve', 'ổ', ' مجرد', 'opo', 'eria', '้น', ' صدا', 'actually', 'icipation', 'undra', 'の声', '树人', '=count', 'inde', 'afir', 'ughter', '哈萨', 'eceğini', '政部', '日以来', '采风', '伟大复兴', '_WARNING', '查证', '渉']

end-pass input-prefix generic-reference erased0.5 plain27; lexicaljoint=False:

['wind', ' wind', ' strings', ' percussion', ' Wind', ' winds', 'strings', 'Wind', ' viol', 'string', 'viol', '弦', ' brass', ' wood', 'Strings', ' uk', ' string', '/string', 'STRING', ' perc', 'perc', ' Strings', ' viento', '风管', '_wind', '_string', 'ucked', ' drums', ' Winds', ' viola', '鼓', '_STRING']

end-pass input-prefix random-reference erased0.5 plain27; lexicaljoint=False:

['wind', ' percussion', ' viento', ' wind', ' winds', ' Wind', '弦', '风能', 'Wind', '键盘', '管所', ' Strings', ' Perc', ' perc', '声器', 'andalkan', 'itom', 'ologne', 'struments', '风霜', '営', 'itative', '風', ' sax', ' pipa', '_wind', ':string', 'perc', '打击', 'active', ' риска', ' drums']

end-pass input-prefix erased0.5 J-lens; lexicaljoint=True:

[' percussion', ' nonexistent', ' Vocal', ' vocal', ' **', ' Known', ' Unknown', ' Sound', ' **—', '…**', ' vocals', ' Silent', ' Actually', ' Heard', ' auditory', ' Nothing', ' **:**', ' Founded', ' unknown', ' known', ' Guitar', ' violin', '声乐', ' piano', ' Based', ' **.**', 'actually', ' Audio', ' **.', ' drums', ' Choir', ' flute']

end-pass input-prefix erased0.5 plain24; lexicaljoint=False:

['xhr', ' صدا', ' beleg', '...(', ' warta', '的事实', ' percussion', 'ốn', ' pipa', '小编为大家整理的', ' факта', ' ですが', 'плы', ' Isles', ' fapt', 'acre', 'ässe', 'đu', '树人', 'ungi', '沉寂', ' gry', 'โปรด', '事实', 'ագ', 'đenje', '__;', ' ;-)', '祉', '(eventName', '단은', '(&:']

end-pass input-prefix erased0.5 plain27; lexicaljoint=True:

['wind', ' percussion', ' wind', '弦', 'struments', ' winds', ' viento', ' Wind', ' brass', 'Wind', ' Strings', ' strings', ' pipa', ' drums', '风能', '打击', 'Strings', '声器', '鼓', '风的', 'strings', '键盘', '.wind', ' Perc', '风管', '风和', '_string', ' Brass', ' sax', ' Winds', ' viol', 'STRING']

end-pass input-prefix J-lens; lexicaljoint=False:

[' percussion', ' nonexistent', ' **', ' vocal', ' Vocal', ' Known', ' Unknown', '**', ' Sound', ' Actually', ' Silent', ' known', ' vocals', ' Nothing', ' Based', ' auditory', ' unknown', ' piano', ' violin', ' Founded', ' Guitar', 'actually', ' Heard', ' Audio', '声乐', ' drums', 'unknown', ' Wood', '…**', ' acoustic', ' flute', ' none']

### 5: Hamlet

Input repr:
```text
"<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Unchanged exact output:
```text
William Shakespeare<|im_end|>
```

end-pass input-prefix generic-reference erased0.5 J-lens; lexicaljoint=False:

[' Shakespeare', 'akespeare', '莎士比亚', '鲍', 'Rod', ' Robert', '主要是', ' Elizabeth', ' novelist', ' Elisabeth', ' Henrik', '…', 'Robert', ' Rowling', '分别是', ' Boris', ' dramat', ' Rod', ' Laure', ' Welsh', ' Michel', ' himself', '用的是', ' …', ' Shakespe', ' Richard', ' Scottish', '原作者', ' Charles', ' Russ', ' Romano', ' Johannes']

end-pass input-prefix random-reference erased0.5 J-lens; lexicaljoint=False:

[' Shakespeare', ' Tolkien', ' Marie', ' John', ' Henry', ' Rowling', 'actually', ' Marcel', ' Sheikh', ' Robert', '莎士比亚', 'akespeare', ' Queen', 'John', ' Antoine', ' Harris', ' Bob', ' Aristotle', ' Churchill', 'ehl', ' Jacob', ' Mort', ' British', ' actually', ' Dumbledore', ' Franz', ' Spencer', ' Mary', ' Robin', ' Jane', ' Lars', ' Bernard']

end-pass input-prefix generic-reference erased0.5 plain24; lexicaljoint=False:

['ivant', 'ibas', '月份开始', ' vaid', 'agin', '(TM', 'borg', 'órd', 'etat', ' spok', '第三方', '裕', ' itse', 'روت', ' wrest', 'iach', ' uyg', 'وين', ' taky', '逼', 'akespeare', '绢', 'обо', '別人', 'eldes', 'igham', 'entially', ' kog', 'ρωση', ' 😉', ' Quo', 'uste']

end-pass input-prefix random-reference erased0.5 plain24; lexicaljoint=False:

['ehl', 'обе', '索', 'andet', 'ایش', '่ม', 'argo', '不自', 'vér', 'acre', 'undra', 'asaki', '佚', 'actually', ' greve', 'うちに', ' wacht', ' mily', 'anut', '帳', 'itative', 'elves', '人类的', 'ectomy', '営', ' onstage', 'しぶ', '是人类', 'locales', 'trol', 'ianie', '-toast']

end-pass input-prefix generic-reference erased0.5 plain27; lexicaljoint=False:

['akespeare', '署', '在台', ' onstage', '话剧', 'коле', '这部剧', ' suicides', 'arang', 'icke', 'ész', 'iach', '区委书记', 'yers', 'yec', ' taky', ' dramat', '刷新', 'acters', 'holm', '.MaxValue', 'etat', '王文', ' المسرح', ' immortal', ' Guild', 'qing', ' deaths', 'ibas', '镖', 'atre', '叨']

end-pass input-prefix random-reference erased0.5 plain27; lexicaljoint=False:

['akespeare', '索', 'ehl', ' Shakespeare', ' onstage', '莎士比亚', 'émie', 'обе', ' شك', 'ectomy', 'chnik', 'しぶ', 'atric', '新加坡', '療', ' Ár', '英国的', 'ecz', 'érc', 'らん', ' Shakespe', ' prolet', ' keny', 'icide', 'öld', 'وج', '人类的', '这部剧', 'atrice', 'åde', 'actually', '署名']

end-pass input-prefix erased0.5 J-lens; lexicaljoint=False:

[' Shakespeare', ' Robert', 'akespeare', ' Aristotle', ' Henry', ' Tolkien', ' Elizabeth', ' John', ' Edmund', ' Christopher', ' **', ' Sir', ' Richard', ' George', ' Julius', ' Samuel', ' Charles', ' Dickens', ' Hugo', ' Edward', ' Rowling', ' Daniel', ' Stephen', ' himself', '莎士比亚', ' Luke', ' Harry', ' Thomas', ' James', ' English', ' Benjamin', ' Jane']

end-pass input-prefix erased0.5 plain24; lexicaljoint=False:

['akespeare', '佚', ' onstage', '...(', 'ťa', ' tragedia', ' famously', 'чиной', ' **:**', ' spok', ' Ata', 'icide', 'র্ত', ' greve', '自来', ' Laufe', ' mily', '-fiction', ' _______,', '马拉', '?...', ' Hinblick', 'trar', ' berüh', 'vias', 'ehrte', ' spiritu', 'меется', 'टक', ' työn', ' vaid', ' fisse']

end-pass input-prefix erased0.5 plain27; lexicaljoint=False:

['akespeare', ' شك', ' onstage', ' Shakespeare', '莎士比亚', '这部剧', ' مسرح', ' Shakespe', '-play', 'icide', ' المسرح', ' tragedia', 'ốn', ' Mancha', '-fiction', '该剧', '话剧', 'ốc', 'коле', ' îns', ' teatr', ' sien', 'oling', 'åde', 'émie', ' théâtre', 'πτωση', 'erval', ' teb', 'Sir', 'engang', ' traged']

end-pass input-prefix J-lens; lexicaljoint=False:

[' Shakespeare', ' Robert', ' Henry', 'akespeare', ' Elizabeth', ' John', ' Christopher', ' Edmund', ' Aristotle', ' Tolkien', ' Richard', ' Charles', ' Edward', ' Samuel', ' George', 'Robert', ' Sir', ' Julius', ' Stephen', ' Dickens', ' Rowling', '莎士比亚', ' James', ' Hugo', ' Thomas', ' Benjamin', ' Daniel', 'Henry', ' Harry', 'John', ' Gabriel', ' **']

### 6: hydrogen

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The physical state at room temperature of the lightest chemical element is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Unchanged exact output:
```text
gas<|im_end|>
```

end-pass input-prefix generic-reference erased0.5 J-lens; lexicaljoint=False:

[' liquid', '液态', 'liquid', '固态', ' lique', ' liquids', 'Liquid', ' fluid', '液体', ' fluids', 'fluid', ' liquide', ' brittle', '固体', 'angat', '…', '较轻', 'lique', ' Liquid', '...', ' crystall', '熔化', '液体的', ' solid', 'solid', '气体', '的气体', '…**', ' líquido', ' جام', ' liqu', ' lightweight']

end-pass input-prefix random-reference erased0.5 J-lens; lexicaljoint=False:

['**', 'liquid', ' liquid', '液态', ' liquids', ' vapor', ' **', ' soluble', ' lique', '液体的', '液体', ' Liquid', ' Vapor', '’**', 'izzle', 'andet', ' fluids', ' frozen', ' Dome', '帳', ' Observatory', '冻', 'free', ':any', '检查一下', '液化', ' Vibr', ' freezing', 'actually', '>**', "'**", 'änder']

end-pass input-prefix generic-reference erased0.5 plain24; lexicaljoint=False:

['固态', '液态', '呈', 'ivant', 'ifle', '豁免', 'gren', ' liquid', 'olid', 'ément', ' ervan', 'рее', ' lique', '熔化', 'esses', 'โปร่ง', ' respiro', 'ivin', '和第', '淮', ' hơi', ' veille', 'azzo', '延展', 'ounge', 'awas', '固体', '游记', '民用', 'ونة', ' sauf', ' chiefly']

end-pass input-prefix random-reference erased0.5 plain24; lexicaljoint=False:

['обе', 'ایش', 'izzle', '営', 'ean', '加拿大的', '/interface', '液态', '检查一下', '_revision', ' مجرد', 'agua', '้น', 'andet', ' Dome', 'irie', 'acre', '_capabilities', '固态', ':any', 'icipation', '=count', 'änder', '有声', 'itom', 'actually', 'awa', 'wares', 'ectomy', 'وج', '_lm', '单纯的']

end-pass input-prefix generic-reference erased0.5 plain27; lexicaljoint=False:

['气体', ' solid', '固态', ' liquid', '的气体', ' fluid', ' газа', '气体的', ' газо', 'solid', '气', ' газ', '和气', '_gas', 'fluid', ' gaz', 'liquid', '液态', 'olid', '固体', ' fluids', ' liquids', ' Solid', '液体', ' الغاز', '-solid', ' gás', '气化', ' газов', 'Solid', ' lique', ' Fluid']

end-pass input-prefix random-reference erased0.5 plain27; lexicaljoint=False:

['气体的', '液态', ' liquid', '气体', '固态', '气', ' газа', '液体的', ' liquids', '液体', ' газо', 'liquid', '液化', ' газ', ' fluids', ' solid', ' lỏng', '_gas', ' گاز', '固体', 'andet', '営', '检查一下', '的气体', 'solid', '之气', '液', ' газов', '汽', 'izzle', 'änder', ' gaz']

end-pass input-prefix erased0.5 J-lens; lexicaljoint=False:

[' **', '**', 'liquid', ' liquid', ' Liquid', ' liquids', '液态', '…**', ' lique', '...**', ' vapor', 'fluid', ' Vapor', 'Liquid', ' fluids', ' fluid', ' Fluid', ' Answer', '固态', ':...', '**:', '�', ' frozen', '...', '液体', ' soluble', '：**', 'Answer', ' brittle', ' According', '____', '________']

end-pass input-prefix erased0.5 plain24; lexicaljoint=False:

['固态', '液态', 'ément', 'amu', ' namely', 'lep', 'โปร่ง', '常温', 'utow', '我来说', '英文名称', 'ائع', ' berüh', 'geries', ' lique', ' الاعتبار', 'anime', ' утвер', '加拿大的', 'vestig', '件事', 'irie', ' kwest', 'iration', 'liquid', '.freeze', ' liquids', ' Awake', ' physicists', '本题考查', 'free', '-free']

end-pass input-prefix erased0.5 plain27; lexicaljoint=False:

['固态', '气体', '气体的', '气', ' liquid', '液态', ' газо', ' газ', ' газа', '的气体', 'liquid', ' gaz', '_gas', ' liquids', ' گاز', ' غاز', '固体', ' الغاز', ' solid', '的气', ' твер', ' lỏng', ' fluids', 'solid', ' Liquid', ' gás', ' газов', '液体', ' rắn', 'غاز', ' gaze', 'fluid']

end-pass input-prefix J-lens; lexicaljoint=False:

['liquid', ' liquid', ' Liquid', ' **', ' liquids', '液态', '…**', ' lique', '**', '...**', ' vapor', 'fluid', ' Vapor', 'Liquid', ' fluids', ' fluid', ' Fluid', ':...', '固态', '液体', ' Answer', ' **—', '-fluid', ' Liqu', '：**', ' frozen', ' Frozen', ' soluble', ' **:**', '液体的', ' líqu', '**:']

### 7: triangle

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of sides of the shape formed by joining three non-collinear points is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Unchanged exact output:
```text
three<|im_end|>
```

end-pass input-prefix generic-reference erased0.5 J-lens; lexicaljoint=True:

['equal', '**', 'odd', '增加到', 'greater', 'angat', '最多', ' odd', '较高', '答案是', ' triangular', '的答案', 'уго', '较大', '或少', '专科学校', ' counted', '多い', '方形', ' fours', ' greater', '第七', ' thirds', '相等', '奇', 'ilateral', '方正', '大于', '长方形', '提高到', ' **', '第三人']

end-pass input-prefix random-reference erased0.5 J-lens; lexicaljoint=True:

['**', ' **', '>**', 'وج', ':number', '=count', ' greater', ' Answer', '’**', ' Actually', 'greater', '正确答案', 'Answer', ' Triangle', '**”', 'andet', 'elve', 'wijs', '的答案', "'**", 'ef', ' Neighbor', '帳', 'Actually', ';**', '事实', ' Circle', 'icens', ' Count', 'Spoiler', 'afir', ' Dome']

end-pass input-prefix generic-reference erased0.5 plain24; lexicaljoint=False:

['كير', ' Adolesc', 'eves', '鹹', 'gend', 'anc', ' thirds', 'coration', ' curs', ' tred', 'فذ', 'وين', 'âteaux', ' banged', '上限', 'ifle', 'arang', ' Maggi', '小编', ' incidental', '人家', ' Vigo', 'ellant', ' dime', '旺盛', ' 육', ' permanent', ' spok', 'olid', ' ordinal', ' lewat', '的一般']

end-pass input-prefix random-reference erased0.5 plain24; lexicaljoint=False:

['وج', '営', '当地的', 'ef', 'ectomy', '=count', '阿拉伯', 'ổ', '检查一下', 'undra', 'andet', ' truff', '_depend', 'icipation', 'nosis', 'обе', '陪', 'acre', '依法自主', 'warning', '_filled', '人类的', '่ม', 'atric', 'afir', 'fect', 'acin', '加拿大的', ' lạc', 'ندية', 'akor', 'うちに']

end-pass input-prefix generic-reference erased0.5 plain27; lexicaljoint=True:

[' odd', ' thirds', 'leven', '...**', 'odd', '最多', 'eves', ' greater', 'greater', 'uluh', '…**', ' porno', '通过对', ' triangles', ' trai', ' obt', ' tred', '偶', '叁', 'equal', 'ilateral', ' medial', '{}".', ' permanent', '人家', '奇', '่ง', '不倦', ' สาม', '首先是', '三是', ' triangular']

end-pass input-prefix random-reference erased0.5 plain27; lexicaljoint=False:

['阿拉伯', 'وج', '_depend', ' greater', '加拿大', 'andet', ' محد', '当地的', 'اصر', 'nosis', 'ectomy', '.isFile', 'greater', 'warning', 'acre', '営', 'undra', '=count', '่ม', '坦白', 'obble', '_filled', 'ologne', 'icipation', ' truff', '惊', 'ندية', 'ake', 'akor', 'åde', 'fect', ' minor']

end-pass input-prefix erased0.5 J-lens; lexicaljoint=True:

[' **', '**', ' Answer', ' Answers', '的答案', '答案是', 'Answer', '事实', '答案', ' Based', '...**', ' Always', '：**', ' Infinite', ' answer', 'answered', '…**', ' Greater', ' Depends', ' Fakt', ' fakta', 'greater', ' Triangle', ' Actually', ' **+', '的事实', ';**', ' According', ' Definitely', 'equal', '>**', '正确答案']

end-pass input-prefix erased0.5 plain24; lexicaljoint=False:

['.gradle', '的答案', '本题考查', 'ছিল', '事实', '_fact', '…**', ' zahl', '当地的', '<think>', '参考答案', ' ...(', '我来说', ' indefinitely', '陪', 'euillez', '答案是', ' факты', '的事实', ' beleg', 'église', '...\\', '_depend', '...(', ' Fakten', '通过使用', ' Vergangenheit', '偏方', '.gener', ' Öffentlichkeit', ' kebe', '阿拉伯']

end-pass input-prefix erased0.5 plain27; lexicaljoint=True:

['<think>', ' triangles', ' greater', '本题考查', 'greater', '_depend', '…**', '阿拉伯', '的答案', 'odd', '当地的', 'ilateral', '.isFile', '.gradle', ' odd', '_triangle', '参考答案', ' thirds', '事实', ' mitra', ' **:**', ' concurs', ' indefinitely', 'åde', '三角形', ' trots', ' pales', '_rectangle', 'always', '...**', '三角形的', '...,']

end-pass input-prefix J-lens; lexicaljoint=True:

[' **', ' Answer', '**', ' Answers', '的答案', '答案是', 'Answer', '...**', '答案', '事实', '…**', 'greater', ' Based', ' Always', 'answered', '：**', ' Infinite', ' Greater', ' Depends', ' Fakt', ' Triangle', ';**', ' fakta', 'equal', ' answer', ' **+', '>**', 'answer', ' Definitely', '的事实', ' Fakta', 'equals']

## animals (4 cases)

Full records: /workspace/2026/suppressed-activations/out/2026-10-01_123658_jlens-one-pass/readout.json

### 0: horse

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of legs on the animal that neighs and is ridden using a saddle is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Unchanged exact output:
```text
The number of legs on the animal that neighs and is ridden using a saddle is **four**.

(The animal is a horse, which has four legs.)
```

end-pass input-prefix generic-reference erased0.5 J-lens; lexicaljoint=False:

['six', ' six', ' fours', 'eight', 'four', ' seven', ' sixteen', 'five', ' four', ' twelve', ' five', ' eight', ' fourteen', 'nine', 'three', ' eighteen', ' seventeen', 'seven', '十六', ' three', ' twenty', 'twenty', ' thirteen', ' nine', ' thirty', ' counted', '的五', ' fifteen', '三四', ' cinq', 'plural', '第六']

end-pass input-prefix random-reference erased0.5 J-lens; lexicaljoint=False:

[' humans', ' Humans', ' seven', '人类的', ' nonexistent', ' six', '=count', '’**', ' mammals', 'elve', ':number', ' five', '是人类', 'five', '**', '>**', ' eight', 'twenty', 'actually', 'quine', 'nine', ' **', 'three', ' nine', ' Zod', ' twelve', ' Actually', 'eight', "'**", 'verte', '[count', ' Seven']

end-pass input-prefix generic-reference erased0.5 plain24; lexicaljoint=False:

[' tred', 'eves', '$$$$', 'tivo', '人家', 'wakili', 'quio', ' banged', '旺盛', ' curs', 'ounge', 'uluh', 'ifle', 'âteaux', ' svel', 'فذ', 'odat', 'ivent', '和讯', ' trup', '癒', ' sexu', 'osity', 'semb', 'adra', '小编', ' ono', '成群', ' vle', 'aup', 'koztat', ' عد']

end-pass input-prefix random-reference erased0.5 plain24; lexicaljoint=False:

['人类的', '=count', ' truff', 'undra', 'обе', '営', 'ổ', '加拿大的', 'atric', ':number', '总数', '.DriverManager', 'しぶ', 'afir', '阿拉伯', 'elve', '预包装', '้น', 'ablo', 'ugd', 'itative', 'itom', ' Lombok', '่ม', 'eria', '检查一下', 'warning', '依法自主', '分に', ' svel', 'ughter', '塘镇']

end-pass input-prefix generic-reference erased0.5 plain27; lexicaljoint=False:

['偶', ' odd', 'uluh', 'eves', 'odd', ' ZERO', '…**', 'odat', 'leven', ' FOUR', ' Odd', 'four', 'exceptions', '...**', '奇', ' ono', 'htm', 'zero', '多い', 'riers', '.zero', ' .**', '异常', ' fours', 'ews', 'Odd', '更少', '提问者', 'ordin', ' Cama', '».**', '_odd']

end-pass input-prefix random-reference erased0.5 plain27; lexicaljoint=False:

['人类的', 'undra', '加拿大的', '阿拉伯', 'обе', '加拿大', '営', '=count', '是人类', ' truff', '新加坡', 'obble', 'وج', 'ổ', 'nosis', ' trots', 'elve', ' **:**', '_depend', 'ào', '.DriverManager', 'atric', '当地的', '预包装', 'สง', 'itom', 'acre', 'even', 'ablanca', '’**', ':number', 'warning']

end-pass input-prefix erased0.5 J-lens; lexicaljoint=False:

[' **', ' nonexistent', ' Answer', '**', '事实', '的事实', '-**', '的答案', ' Answers', ' Fakt', ' fakta', ' Dogs', '：**', ';**', ' Humans', ' Actually', ' mammals', 'dogs', '...**', ' **:**', ' Depends', ' Few', ' Feet', 'plural', ' Exactly', 'equals', ' Five', ' Four', 'eight', '…**', ' Twice', ' Eight']

end-pass input-prefix erased0.5 plain24; lexicaljoint=False:

['_fact', '事实', '的答案', '的事实', ' Publicidad', ' warta', ' **:**', '…**', '=count', '.gradle', '我来说', 'води', ' beleg', 'ছিল', 'меется', '参考答案', ' polled', ' zahl', 'ี้ยง', '总数', 'église', '小编就', 'lessness', '__:', ' pupper', '穌', '.DriverManager', '五颜六色的', ' trots', 'городи', ' BPK', '真实性负责']

end-pass input-prefix erased0.5 plain27; lexicaljoint=False:

[' **:**', '偶', '../../../../', '各种各样', '…**', ' trots', '五颜六色的', ' odd', 'odd', 'さま', ' Pôle', '驮', '阿拉伯', 'ẵn', ' Publicidad', 'ốn', ' ZERO', 'ี่ย', '或少', '加拿大的', ' beleg', '事实', ' ;-)', ' .**', 'городи', ' Bairro', 'ديث', '同志为核心的党中央', ' pupper', '版权声明', '现车', '声器']

end-pass input-prefix J-lens; lexicaljoint=False:

[' **', '**', ' nonexistent', ' Answer', '事实', ' Actually', '的事实', ' Answers', '的答案', '：**', ' Dogs', ' Four', ' mammals', ' Humans', ' Five', ' Fakt', 'Answer', ' fakta', ' Two', ' Few', 'none', '-**', ' six', 'equals', ' Eight', ' None', ' Exactly', 'plural', ' Depends', 'dogs', '答案是', ' Seven']

### 1: cow

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of legs on the farm animal that moos is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Unchanged exact output:
```text
four<|im_end|>
```

end-pass input-prefix generic-reference erased0.5 J-lens; lexicaljoint=False:

[' counted', ' six', ' five', ' seven', ' three', ' twelve', 'plural', ' eight', ' twenty', ' sixteen', '十六', 'eight', ' eighteen', ' thirty', 'equal', ' thirds', '三四', 'three', 'six', ' fifteen', '的答案', ' seventeen', ' nine', ' plural', '二十', '三十', 'twenty', ' twice', ' twenties', '数量', '十五', 'nine']

end-pass input-prefix random-reference erased0.5 J-lens; lexicaljoint=False:

['**', ' humans', ' seven', '人类的', ':number', '=count', ' six', ' five', ' **', ' Actually', ' Humans', 'Actually', ' three', 'elve', 'actually', ' actually', ' two', ' nonexistent', ' mammals', ' eight', '[count', ' twenty', '检查一下', ' nine', '总数', 'Answer', 'three', '>**', '正确答案', '的答案', ' count', ' checked']

end-pass input-prefix generic-reference erased0.5 plain24; lexicaljoint=False:

['eves', '鹹', '的一般', ' curs', '的答案', 'فذ', ' tred', 'كير', '人家', 'quio', 'ifle', 'amage', 'âteaux', ' banged', 'koztat', ' vle', ' عد', 'ounge', ' sexu', 'ivent', '旺盛', ' Maggi', 'ulto', ' hud', 'aup', 'hardt', ' sauv', 'kiye', 'esn', 'atoires', 'anness', '癒']

end-pass input-prefix random-reference erased0.5 plain24; lexicaljoint=False:

['人类的', '=count', ' truff', 'обе', ':number', 'undra', 'afir', 'atric', '営', 'ổ', 'ablo', '加拿大的', 'ectomy', '检查一下', 'ughter', '依法自主', '总数', '当地的', 'وج', 'ablanca', '预包装', ' Rowling', 'acin', 'iah', '塘镇', 'ایش', 'áp', 'ef', '่ม', '้น', 'itom', ' **:**']

end-pass input-prefix generic-reference erased0.5 plain27; lexicaljoint=False:

['偶', ' odd', 'eves', ' .**', 'uluh', 'ordin', '…**', 'exceptions', ' ono', '...**', 'ews', 'odat', '不倦', ' **:**', '一般为', ')…', 'odd', '可梦', '{}".', 'leven', ' exceptions', 'equal', '”…', 'azole', '新加坡', ' Hurt', '.Checked', '三板', '多い', 'отор', '">//', '訊']

end-pass input-prefix random-reference erased0.5 plain27; lexicaljoint=False:

['人类的', '加拿大的', 'undra', '加拿大', '阿拉伯', '=count', 'обе', ' **:**', '当地的', 'وج', ' truff', '新加坡', 'ablo', ' trots', '営', 'acre', 'obble', '点播', '_depend', 'ổ', 'ughter', ':number', 'akor', 'nosis', '版权声明', 'atric', '农牧', 'warning', 'ablanca', 'ordinate', 'ingue', 'ectomy']

end-pass input-prefix erased0.5 J-lens; lexicaljoint=False:

[' **', ' Answer', '**', '的答案', 'Answer', '答案', ' Answers', ' answer', ' Actually', '答案是', 'answered', 'answer', ' nonexistent', 'plural', '：**', '事实', ' plural', 'equals', ' dozen', ' Count', '的事实', ' It', ':number', '正确答案', ' Exactly', ' This', ' Two', ' count', 'equal', ' answered', ' Depends', ' Fakt']

end-pass input-prefix erased0.5 plain24; lexicaljoint=False:

['的答案', ' **:**', '=count', ' pupper', 'vestig', ' warta', '参考答案', 'ছিল', '事实', '.gradle', ' zahl', ' Rowling', '…**', ':number', '我来说', '的事实', '真实性负责', 'ائع', ' Steck', 'の販', ' polled', ' .**', 'dux', 'église', ' Fútbol', '一般为', 'čet', 'ública', '建制', '五颜六色的', '_fact', ' publice']

end-pass input-prefix erased0.5 plain27; lexicaljoint=False:

[' **:**', '各种各样', '…**', ' trots', '五颜六色的', ' .**', '偶', '的答案', '../../../../', '<think>', '或少', '本题考查', 'さま', '当地的', ' **:', '各种各样的', '加拿大的', '版权声明', '?...', 'čet', ' pupper', '农牧', '阿拉伯', 'ốn', ' Unterricht', ' Pôle', ' mitra', '事实', 'ديث', '穌', ' ;-)', '_depend']

end-pass input-prefix J-lens; lexicaljoint=False:

[' Answer', ' **', '的答案', '**', 'Answer', ' Answers', '答案', ' five', ' answer', ' six', 'three', 'answer', 'plural', 'answered', ' nonexistent', '答案是', ' Actually', ' seven', ' three', ' eight', 'five', ' twelve', 'equals', '：**', '事实', ' Five', ' Three', ' dozen', 'eight', ' Two', ':number', ' plural']

### 2: cat

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of legs on the domestic animal that purrs is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Unchanged exact output:
```text
four<|im_end|>
```

end-pass input-prefix generic-reference erased0.5 J-lens; lexicaljoint=False:

[' six', ' seven', ' five', ' twelve', ' eight', ' counted', 'eight', ' sixteen', 'six', ' three', ' eighteen', '十六', ' seventeen', ' twenty', ' nine', ' thirty', 'nine', '第六', ' thirteen', '正常情况下', 'normally', ' fifteen', 'three', 'five', '的五', 'plural', 'seven', ' sixth', '一般是', '一般为', '十八', 'equal']

end-pass input-prefix random-reference erased0.5 J-lens; lexicaljoint=False:

[' seven', ' humans', ' six', '**', '人类的', ' **', ' five', ' Humans', ' nonexistent', ' eight', ':number', ' three', '=count', ' nine', ' Actually', 'actually', 'Actually', ' twelve', ' mammals', '总数', ' actually', ' twenty', ' two', 'elve', '是人类', 'three', 'verte', '检查一下', 'twenty', 'وج', '>**', ' checked']

end-pass input-prefix generic-reference erased0.5 plain24; lexicaljoint=False:

['eves', ' tred', '癒', '$$$$', ' banged', 'tivo', 'ivent', ' vle', '旺盛', 'ifle', 'osity', '鹹', 'âteaux', '的一般', ' sauv', 'atoires', '人家', ' trup', ' Weih', 'quio', '一般为', 'cales', ' svel', ' curs', 'ulto', ' sexu', 'ayne', 'amage', 'arang', 'aup', ' penipuan', '小编']

end-pass input-prefix random-reference erased0.5 plain24; lexicaljoint=False:

['人类的', '=count', ' truff', 'undra', 'обе', ':number', '営', '总数', '检查一下', 'ổ', '依法自主', 'atric', 'ectomy', '加拿大的', 'itom', 'وج', 'eria', 'ughter', 'afir', '้น', ' Lombok', '预包装', 'ablo', 'asaki', '_depend', ' Rowling', '.DriverManager', 'acin', 'ake', '่ม', ' svel', 'nosis']

end-pass input-prefix generic-reference erased0.5 plain27; lexicaljoint=False:

['偶', ' odd', 'odd', 'eves', '...**', 'ordin', '…**', '异常', ' ono', 'uluh', '一般为', ' Odd', 'ews', 'exceptions', 'odle', '奇', 'odat', '靠前', 'bite', ' .**', '不倦', '{}".', '最多', 'leven', '.Checked', '癒', 'enco', ' eer', ')…', '更少', '提问者', '$$$$']

end-pass input-prefix random-reference erased0.5 plain27; lexicaljoint=False:

['人类的', 'undra', '=count', '加拿大的', 'obble', 'обе', '_depend', 'وج', ' truff', '是人类', 'akor', 'ổ', 'nosis', '営', ':number', ' **:**', '当地的', '陪', ' trots', 'ectomy', 'ake', 'عادة', 'ughter', 'typically', '阿拉伯', 'ào', ' Zod', 'ingue', 'warning', '预包装', 'eria', '.DriverManager']

end-pass input-prefix erased0.5 J-lens; lexicaljoint=False:

[' **', '**', ' nonexistent', ' Actually', ' six', ' Depends', 'plural', '：**', ' Answer', ' seven', ' fewer', ' twelve', ' varies', ' five', ' plural', '...**', ' infinite', ' Count', 'equals', ' eight', ' odd', '的答案', ' Based', ' Five', ' Usually', ' Exactly', ' dozen', ' thirteen', ' mammals', ' Dogs', ' Two', ' none']

end-pass input-prefix erased0.5 plain24; lexicaljoint=False:

[' **:**', '=count', '的答案', '.gradle', '一般为', ' Rowling', '…**', ':number', ' \u200b\u200b', '总数', 'の販', '我来说', 'ائع', 'unia', ' pupper', ' warta', ' beleg', ' truff', 'ছিল', '_fact', 'vestig', 'undra', 'ivable', '人类的', ' ...(', '五颜六色的', ' Blasio', 'ceptive', '事实', ' zahl', ' trots', ' svel']

end-pass input-prefix erased0.5 plain27; lexicaljoint=False:

['偶', ' **:**', '…**', ' odd', '各种各样', ' trots', 'odd', '../../../../', '五颜六色的', 'ẵn', '_depend', 'pairs', 'さま', '陪', '奇', '或少', 'ốn', 'čet', '人类的', ' beleg', '.gradle', '一般为', ' pupper', '各种各样的', ' .**', ' **:', '...**', '这个问题的', '{}".', 'undra', '声器', '病情分析']

end-pass input-prefix J-lens; lexicaljoint=False:

[' **', ' six', ' seven', ' nonexistent', ' five', '**', ' eight', 'five', ' twelve', 'eight', 'three', ' three', ' Five', ' thirteen', ' sixteen', 'six', 'plural', ' Actually', ' Eight', ' Depends', ' nine', ' Three', ' fewer', ' Seven', ' twenty', '...**', ' Answer', '：**', 'Five', ' Two', ' Six', 'equals']

### 3: goat

Input repr:
```text
'<|im_start|>user\nComplete the fact with only the missing word or phrase:\nFact: The number of legs on the farm animal with a beard and curved horns is<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Unchanged exact output:
```text
four<|im_end|>
```

end-pass input-prefix generic-reference erased0.5 J-lens; lexicaljoint=False:

[' six', ' counted', ' seven', 'plural', ' twelve', ' five', ' three', ' sixteen', ' eight', 'six', 'eight', '十六', ' thirty', ' eighteen', '第六', ' twenty', 'nine', ' seventeen', ' plural', 'three', ' nine', ' thirteen', '三十', '三四', '三十六', ' fifteen', '第五', '二十', '五', '第七', ' thirds', ' sixth']

end-pass input-prefix random-reference erased0.5 J-lens; lexicaljoint=False:

['**', ' seven', ' humans', ' **', ' six', '人类的', ' Humans', ':number', ' five', 'elve', '=count', ' three', '[count', ' Actually', ' eight', ' nine', ' Seven', 'وج', '是人类', '总数', 'verte', '检查一下', ' mammals', 'three', '>**', 'Actually', ' twenty', ' twelve', ' Count', 'actually', ' checked', ' two']

end-pass input-prefix generic-reference erased0.5 plain24; lexicaljoint=False:

[' tred', ' sexu', 'eves', '旺盛', '人家', 'âteaux', 'quio', ' curs', 'ifle', ' sauv', 'كير', 'tivo', '鹹', ' banged', ' Weih', 'amage', 'فذ', 'wakili', ' Leip', ' repell', 'osity', 'odat', ' ono', 'ivent', '$$$$', ' Auskunft', 'ensual', '的答案', '偶', 'ości', 'atoires', ' عد']

end-pass input-prefix random-reference erased0.5 plain24; lexicaljoint=False:

['人类的', '=count', 'обе', ' truff', 'undra', ':number', '営', '总数', '้น', '检查一下', '加拿大的', 'ổ', 'ughter', '_depend', 'ectomy', 'وج', '依法自主', 'ablo', '่ม', 'eria', '预包装', 'ایش', 'atric', 'asaki', 'itative', 'afir', '.DriverManager', 'acin', '当地的', 'ingue', 'itom', 'elve']

end-pass input-prefix generic-reference erased0.5 plain27; lexicaljoint=False:

['偶', ' odd', '...**', '…**', 'eves', 'uluh', ' ono', 'ordin', 'odd', ' .**', '不倦', 'leven', 'odat', 'ews', ')…', '”…', '{}".', '异常', ' sexu', '多い', 'exceptions', 'bite', '.Checked', ' sauv', '一般为', '新加坡', ' curs', ' **:**', 'azole', '靠前', 'htm', 'riers']

end-pass input-prefix random-reference erased0.5 plain27; lexicaljoint=False:

['人类的', '加拿大的', 'undra', '阿拉伯', '_depend', 'وج', '=count', '営', 'obble', 'обе', '加拿大', '新加坡', ' trots', '当地的', ' **:**', ' truff', 'ổ', 'nosis', 'akor', 'ughter', '点播', ':number', 'ingue', 'ectomy', '是人类', 'itom', 'idez', '版权声明', 'acre', 'ablo', 'ologne', '预包装']

end-pass input-prefix erased0.5 J-lens; lexicaljoint=False:

[' **', '**', ' Answer', '的答案', 'plural', ' Answers', ' plural', ' Actually', 'Answer', '：**', '答案', ' Count', '...**', ' Three', ' Two', ' Depends', ' Five', 'answered', ' nonexistent', ' dozen', '事实', ' **[', ' This', ' It', '答案是', ' six', ' Based', ' Seven', ' seven', ' Usually', ':number', '<think>']

end-pass input-prefix erased0.5 plain24; lexicaljoint=False:

['的答案', ' **:**', '…**', '=count', 'の販', 'ছিল', '我来说', ' warta', ':number', '.gradle', ' pupper', '总数', ' trots', ' BPK', ' Publicidad', '五颜六色的', '事实', 'čet', ' Rowling', '_fact', ' zahl', ' ...(', '駅から徒歩', '参考答案', '_depend', '一般为', ' Blasio', 'ivable', 'ائع', ' publice', ' beleg', 'geries']

end-pass input-prefix erased0.5 plain27; lexicaljoint=False:

[' **:**', '…**', '偶', ' trots', '各种各样', 'ốn', '五颜六色的', '<think>', '../../../../', '_depend', 'さま', ' .**', ' odd', 'ี่ย', '的答案', '...**', '本题考查', 'odd', 'ẵn', ' ;-)', '这个问题的', '阿拉伯', ' Pôle', ' **:', ' Publicidad', 'の販', '各种各样的', '加拿大的', '版权声明', '病情分析', 'čet', '或少']

end-pass input-prefix J-lens; lexicaljoint=False:

[' **', '**', ' Answer', ' six', 'plural', ' seven', ' Three', ' Five', 'three', ' Answers', ' five', '的答案', ' twelve', ' eight', 'five', ' three', ' Seven', ' plural', ' Two', '...**', 'eight', 'Answer', ' thirteen', ' Eight', '：**', ' Actually', ' dozen', ' Twelve', ' nonexistent', 'six', ' Six', 'Five']
