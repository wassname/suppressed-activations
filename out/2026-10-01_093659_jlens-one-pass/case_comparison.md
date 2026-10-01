# Complete-input-prefix mask, four development cases

Written by PI/OpenAI. Old72 rows exactly preserved;16 new candidate rows. No new transformer calls or generations. Lexical/AUROC results do not certify semantic exclusion.

## Oman

Input repr:
```text
'<|im_start|>user\nAnswer with only the continent name: On which continent is the country whose capital is Muscat?<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Cached continuation:
```text
Asia<|im_end|>
```

### end-pass input-prefix erased0.5 J-lens

Candidate lexical joint=True; own/partner ranks=4/17.

[' Arabia', ' Antarctica', ' Oce', ' Africa', ' Kazakhstan', ' Oman', 'Arab', ' Arabian', 'Africa', '大陆', ' Afghanistan', ' Morocco', ' Islands', ' Portugal', ' Madagascar', ' Pakistan', ' Europe', ' Qatar', ' Bahrain', ' Somalia', ' Yemen', ' UAE', ' Island', ' Australia', 'Europe', ' Desert', ' Saudi', ' Indonesia', ' Ethiopia', ' Euras', '非洲', ' Peninsula']

Original end-pass erased0.5 J-lens:

[' Arabia', ' Antarctica', ' Oce', ' Africa', ' Oman', ' Kazakhstan', ' Arabian', 'Arab', 'Africa', '大陆', ' Afghanistan', ' Morocco', ' Islands', ' continents', ' Portugal', ' Madagascar', ' Pakistan', ' Europe', ' Somalia', ' Bahrain', ' Qatar', ' Yemen', ' UAE', ' Australia', ' Island', ' Desert', ' Saudi', 'Europe', 'continental', ' Euras', ' Indonesia', ' Ethiopia']

### end-pass input-prefix erased0.5 plain24

Candidate lexical joint=False; own/partner ranks=8813/8257.

['Crime', '岛屿', '君主', ' desert', ' Penis', '教体', '冈', '散装', ' Arabia', '花岗岩', '蹦', '大陆', ' Arabian', '叔叔', ' premi', ' specifically', '岛', '祖国', ' Crime', '加工定制', ' Oce', '_specific', 'specific', '职业技术学校', ' vaid', '.Companion', ' peninsula', '神州', '半岛', ' 동아', 'inį', '幻灯片']

Original end-pass erased0.5 plain24:

['Crime', '岛屿', '君主', ' desert', ' Penis', '教体', '冈', '散装', ' Arabia', '花岗岩', '蹦', '大陆', ' Arabian', '叔叔', ' premi', ' specifically', '岛', '祖国', ' Crime', '加工定制', ' Oce', '_specific', 'specific', '职业技术学校', ' vaid', '.Companion', ' peninsula', '神州', '半岛', ' 동아', 'inį', '幻灯片']

### end-pass input-prefix erased0.5 plain27

Candidate lexical joint=False; own/partner ranks=2978/11298.

[' North', ' Africa', '非洲', '亚洲', ' Arabian', ' Arabia', '大洋', '东南亚', ' Euras', '-A', 'North', ' African', ' Oce', '北', '<think>', ' MEN', ' Southeast', '_A', ' Bắc', '[A', ' آسی', '南亚', ' Antar', '西亚', '-Saharan', '东北', ' 동아', '俑', '具体', ' Middle', ' Đông', 'Africa']

Original end-pass erased0.5 plain27:

[' North', ' Africa', '非洲', '亚洲', ' Arabian', ' Arabia', '大洋', '东南亚', ' Euras', '-A', ' continental', 'North', ' African', ' Oce', '北', '<think>', ' MEN', ' Southeast', '_A', '[A', ' Bắc', ' آسی', ' Antar', '南亚', '西亚', '-Saharan', ' 동아', '东北', '俑', '具体', ' Middle', 'Africa']

### end-pass input-prefix J-lens

Candidate lexical joint=True; own/partner ranks=8/22.

[' Arabia', 'Africa', ' Antarctica', ' Oce', ' Africa', 'Arab', ' Kazakhstan', '亚洲', ' Oman', ' Arabian', 'Europe', ' Afghanistan', ' Europe', '大陆', 'China', ' Euras', ' Morocco', 'India', ' Somalia', ' Islands', ' Australia', 'Australia', ' Portugal', ' Qatar', ' Pakistan', ' Madagascar', ' Bahrain', 'Indonesia', ' Yemen', ' Indonesia', ' Mongolia', ' Ethiopia']

Original end-pass J-lens:

[' Arabia', 'Africa', ' Antarctica', ' Oce', ' Africa', 'Arab', ' Kazakhstan', '亚洲', ' Oman', ' Arabian', 'Europe', ' continents', ' Afghanistan', ' Europe', '大陆', ' Euras', 'China', ' Morocco', 'India', ' Islands', ' Somalia', 'continental', ' Australia', 'Australia', ' Portugal', ' Qatar', ' Pakistan', ' Madagascar', 'Indonesia', ' Bahrain', ' Yemen', ' Indonesia']

## Qatar

Input repr:
```text
'<|im_start|>user\nAnswer with only the continent name: On which continent is the country whose capital is Doha?<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Cached continuation:
```text
Asia<|im_end|>
```

### end-pass input-prefix erased0.5 J-lens

Candidate lexical joint=True; own/partner ranks=4/126.

[' Antarctica', ' Arabia', ' Africa', ' Oce', ' Qatar', 'Africa', 'Arab', ' Kazakhstan', ' Sahara', '大陆', ' Arabian', ' Afghanistan', ' Americas', ' Europe', ' Bahrain', ' Scandin', ' Egypt', ' Islands', ' Palestine', ' Morocco', ' Pakistan', ' Caribbean', ' Greenland', 'Europe', ' Saudi', 'North', '非洲', ' Desert', ' Yemen', ' Hemisphere', ' Nigeria', ' Island']

Original end-pass erased0.5 J-lens:

[' Antarctica', ' Arabia', ' Africa', ' Oce', ' Qatar', 'Africa', 'Arab', ' Kazakhstan', ' continents', ' Sahara', ' Arabian', '大陆', ' Afghanistan', ' Americas', ' Europe', ' Bahrain', ' Scandin', ' Egypt', ' Islands', ' Palestine', ' Morocco', ' Caribbean', ' Pakistan', 'continental', ' Greenland', 'Europe', ' Saudi', 'North', '非洲', ' Continental', ' Desert', ' Yemen']

### end-pass input-prefix erased0.5 plain24

Candidate lexical joint=False; own/partner ranks=598/41573.

['蹦', '叔叔', '玲玲', '教体', 'خلي', ' specifically', '_specific', 'specific', '散装', 'IRTH', 'Crime', ' peninsula', '神州', 'inį', '舌尖上的', ' desert', ' înt', ' caucus', 'влека', '岛屿', ' tiek', ' prezent', ' Oce', '君主', 'Birth', ' specif', ' Beacon', '岛', '伶', '一个个', 'ạm', ' Penis']

Original end-pass erased0.5 plain24:

['蹦', '叔叔', '玲玲', '教体', 'خلي', ' specifically', '_specific', 'specific', '散装', 'IRTH', 'Crime', ' peninsula', '神州', 'inį', '舌尖上的', ' desert', ' înt', ' caucus', 'влека', '岛屿', ' tiek', ' prezent', ' Oce', '君主', 'Birth', ' specif', ' Beacon', '岛', '伶', '一个个', 'ạm', ' Penis']

### end-pass input-prefix erased0.5 plain27

Candidate lexical joint=False; own/partner ranks=1330/89051.

[' North', '亚洲', '北美', ' Africa', '非洲', '北', 'North', ' Bắc', '美洲', '大洋', '-A', ' châu', ' Antar', '西亚', '东南亚', ' Arabian', ' Euras', ' African', ' Europe', '蹴', ' Middle', '茫茫', '[A', '<think>', 'ทวี', ' Oce', ' MEN', ' Latin', ' آسی', ' Arabia', 'Africa', '-Saharan']

Original end-pass erased0.5 plain27:

[' North', '亚洲', '北美', ' Africa', '非洲', '北', 'North', ' Bắc', '美洲', '大洋', '-A', ' châu', '西亚', ' Antar', ' Arabian', '东南亚', ' continental', ' Euras', ' continents', ' Europe', ' African', '蹴', ' Middle', '茫茫', '<think>', '[A', 'ทวี', ' Oce', ' MEN', ' آسی', ' Latin', ' Arabia']

### end-pass input-prefix J-lens

Candidate lexical joint=True; own/partner ranks=7/159.

[' Arabia', 'Africa', ' Africa', ' Antarctica', ' Oce', 'Arab', ' Kazakhstan', ' Qatar', 'Europe', '亚洲', ' Americas', ' Europe', ' Afghanistan', ' Arabian', ' Sahara', '大陆', ' africa', ' Scandin', ' Bahrain', ' Palestine', 'India', 'Argentina', ' Euras', ' Hemisphere', 'China', ' Morocco', ' Egypt', ' Pakistan', ' Islands', 'North', '非洲', ' Caribbean']

Original end-pass J-lens:

[' Arabia', 'Africa', ' Africa', ' Antarctica', ' Oce', 'Arab', ' continents', ' Kazakhstan', ' Qatar', 'Europe', '亚洲', ' Americas', ' Europe', ' Afghanistan', ' Arabian', ' Sahara', '大陆', ' africa', 'continental', ' Scandin', ' Palestine', ' Bahrain', 'Argentina', 'India', ' Hemisphere', ' Euras', 'China', ' Morocco', ' Egypt', ' Pakistan', ' Islands', 'North']

## Namibia

Input repr:
```text
'<|im_start|>user\nAnswer with only the continent name: On which continent is the country whose capital is Windhoek?<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Cached continuation:
```text
Africa<|im_end|>
```

### end-pass input-prefix erased0.5 J-lens

Candidate lexical joint=False; own/partner ranks=121361/929.

[' Antarctica', ' Kazakhstan', ' Oce', '大陆', ' Asia', 'Asia', ' Sahara', '南非', ' Zambia', '非洲', ' Europe', '南极', 'South', ' Zimbabwe', ' Desert', 'Europe', ' Afrika', ' Americas', '**', '<|endoftext|>', ' Scandin', 'North', ' Afghanistan', ' Greenland', ' Ethiopia', ' Mongolia', ' South', ' Arabia', ' Euras', ' Belgium', ' Morocco', ' Madagascar']

Original end-pass erased0.5 J-lens:

[' Antarctica', ' Kazakhstan', ' Oce', '大陆', ' Asia', ' continents', 'Asia', ' Sahara', '南非', ' Zambia', ' Continental', '非洲', ' continental', 'continental', ' Europe', '南极', 'South', ' Zimbabwe', 'Europe', ' Desert', ' Afrika', '**', ' Americas', '<|endoftext|>', ' Scandin', ' Afghanistan', 'North', ' Ethiopia', ' Mongolia', ' Greenland', ' Arabia', ' South']

### end-pass input-prefix erased0.5 plain24

Candidate lexical joint=False; own/partner ranks=14477/30660.

['叔叔', '_specific', ' Bunda', 'ẹo', 'ạm', '散装', '冈', 'iền', '大陆', ' specifically', '蹦', '撒', '统计局', 'specific', '教体', '舌尖上的', ' slik', ' înt', '加工定制', ' FUCK', "').'", ' desert', ' pang', ' Lâm', 'Crime', ' sinking', 'ставка', '盾', ' technik', '中生', 'xia', 'IRTH']

Original end-pass erased0.5 plain24:

['叔叔', '_specific', ' Bunda', 'ẹo', 'ạm', '散装', '冈', 'iền', '大陆', ' specifically', '蹦', '撒', '统计局', 'specific', '教体', '舌尖上的', ' slik', ' înt', '加工定制', ' FUCK', "').'", ' desert', ' pang', ' Lâm', 'Crime', ' sinking', 'ставка', '盾', ' technik', '中生', 'xia', 'IRTH']

### end-pass input-prefix erased0.5 plain27

Candidate lexical joint=False; own/partner ranks=26324/190.

['非洲', ' Afrika', '南非', '洲', ' kont', ' África', ' конт', ' Афри', '-Saharan', ' South', ' Antarctica', 'AF', ' 남아', '大洋', 'Afrique', ' châu', 'ทวี', ' Af', ' North', ' apartheid', ' Afro', '大陆', '-A', ' Kont', ' Afrique', ' continuum', '�', ' Asia', 'Af', '叔叔', '撒', '<think>']

Original end-pass erased0.5 plain27:

['非洲', ' Afrika', ' continental', '南非', '洲', ' kont', ' África', ' continents', ' конт', ' Афри', '-Saharan', ' South', ' Antarctica', 'AF', ' 남아', '大洋', 'Afrique', ' continente', ' châu', 'ทวี', ' Af', ' North', ' apartheid', 'continental', ' Afro', '大陆', '-A', ' Kont', ' Afrique', ' continuum', '�', ' Asia']

### end-pass input-prefix J-lens

Candidate lexical joint=False; own/partner ranks=83426/1628.

[' Antarctica', 'Asia', '非洲', ' Kazakhstan', ' Asia', ' Oce', '南非', ' África', '大陆', ' Afrika', ' Sahara', ' Zambia', 'Europe', ' Europe', ' Afrique', ' Ethiopia', ' Arabia', 'frica', ' Zimbabwe', ' Americas', ' Mongolia', ' Morocco', ' Kenya', 'South', ' Tanzania', '南极', ' Afghanistan', ' Somalia', 'Afrique', ' Scandin', ' Nigeria', 'Argentina']

Original end-pass J-lens:

[' Antarctica', 'Asia', '非洲', ' Kazakhstan', ' Asia', ' Oce', '南非', ' África', ' continents', '大陆', ' Afrika', ' Sahara', ' Zambia', 'Europe', 'continental', ' Afrique', ' Europe', ' Ethiopia', ' Arabia', 'frica', ' Zimbabwe', ' Americas', ' Mongolia', ' Morocco', ' Kenya', ' Continental', ' Tanzania', 'South', '南极', 'Afrique', ' Afghanistan', ' Somalia']

## Botswana

Input repr:
```text
'<|im_start|>user\nAnswer with only the continent name: On which continent is the country whose capital is Gaborone?<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Cached continuation:
```text
Africa<|im_end|>
```

### end-pass input-prefix erased0.5 J-lens

Candidate lexical joint=False; own/partner ranks=759/141804.

[' Antarctica', 'Asia', ' Asia', ' Oce', ' Zimbabwe', '大陆', ' Nigeria', '非洲', ' Kazakhstan', '**', ' Afghanistan', 'Europe', ' Mongolia', ' Europe', ' Madagascar', 'South', ' Zambia', ' Sahara', ' Tanzania', ' Paraguay', '南非', 'asia', ' Island', ' Ethiopia', ' Americas', ' Caribbean', '<|endoftext|>', ' Australia', ' Euras', ' Afrika', ' Argentina', ' Niger']

Original end-pass erased0.5 J-lens:

[' Antarctica', 'Asia', ' Asia', ' Oce', ' Zimbabwe', '大陆', ' Nigeria', '非洲', ' Kazakhstan', ' Afghanistan', '**', 'Europe', ' Mongolia', ' Europe', ' Madagascar', ' continents', 'South', ' Zambia', ' Sahara', 'continental', ' Paraguay', ' Tanzania', '南非', 'asia', ' Americas', ' Ethiopia', ' Island', ' Caribbean', '<|endoftext|>', ' Afrika', ' Australia', ' Euras']

### end-pass input-prefix erased0.5 plain24

Candidate lexical joint=False; own/partner ranks=18636/46389.

[' Bunda', '叔叔', '_specific', '冈', 'xia', ' technik', 'ẹo', 'iền', '舌尖上的', ' specifically', 'ardia', ' tiek', '玲玲', ' FUCK', 'itic', ' Lâm', '变性', ' zza', '统计局', '伶', 'IRTH', '文明办', '教体', '颁奖', '辞', 'خلي', ' pagal', 'specific', '人民网', ' Lundi', '蹦', '大陆']

Original end-pass erased0.5 plain24:

[' Bunda', '叔叔', '_specific', '冈', 'xia', ' technik', 'ẹo', 'iền', '舌尖上的', ' specifically', 'ardia', ' tiek', '玲玲', ' FUCK', 'itic', ' Lâm', '变性', ' zza', '统计局', '伶', 'IRTH', '文明办', '教体', '颁奖', '辞', 'خلي', ' pagal', 'specific', '人民网', ' Lundi', '蹦', '大陆']

### end-pass input-prefix erased0.5 plain27

Candidate lexical joint=False; own/partner ranks=116/66898.

['非洲', '洲', ' kont', ' Afrika', ' конт', ' África', ' Афри', '南非', '大陆', ' châu', '大洋', ' 남아', 'Afrique', '-Saharan', ' continuum', ' Kont', ' South', ' Rhodes', 'AF', '_CONT', '-A', ' Af', ' North', 'ทวี', ' Antarctica', '北美', ',A', ' Afrique', '<think>', ' kulinar', ' Zimbabwe', '�']

Original end-pass erased0.5 plain27:

['非洲', '洲', ' continental', ' kont', ' Afrika', ' continents', ' конт', ' continente', ' África', '南非', ' Афри', '大陆', ' châu', '大洋', ' 남아', 'Afrique', '-Saharan', ' continuum', ' Kont', ' South', ' Rhodes', 'AF', '_CONT', 'continental', '-A', ' Af', ' North', 'ทวี', ' Antarctica', '北美', ',A', ' Afrique']

### end-pass input-prefix J-lens

Candidate lexical joint=False; own/partner ranks=1950/103499.

['Asia', ' Antarctica', '非洲', ' Asia', ' Oce', 'Europe', ' Nigeria', ' África', ' Zimbabwe', ' Afrika', ' Zambia', ' Mongolia', ' Kazakhstan', '大陆', ' Tanzania', ' Ethiopia', '南非', ' Afghanistan', ' Afrique', ' Europe', ' Madagascar', ' Sahara', 'India', 'Afrique', ' Arabia', 'asia', ' Americas', 'South', 'Argentina', 'frica', ' Niger', ' Somalia']

Original end-pass J-lens:

['Asia', ' Antarctica', '非洲', ' Asia', ' Oce', 'Europe', ' Nigeria', ' África', ' Zimbabwe', ' Afrika', ' Zambia', ' Mongolia', ' Kazakhstan', ' Ethiopia', ' Tanzania', '大陆', '南非', ' Afrique', ' Europe', ' Afghanistan', ' continents', 'continental', ' Madagascar', ' Sahara', 'India', 'Afrique', ' Arabia', ' Americas', 'asia', 'South', 'Argentina', 'frica']
