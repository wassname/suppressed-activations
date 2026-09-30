# Four native-chat geography probes

Written by PI/OpenAI. Fixed method, selected geography task; these counts are lexical, not semantic certification.4 prompts/2 dependent pairs.

## Oman (expected output Asia)

Input repr:
```text
'<|im_start|>user\nAnswer with only the continent name: On which continent is the country whose capital is Muscat?<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Continuation (2 tokens; EOS=True), verbatim:
```text
Asia<|im_end|>
```

end-pass erased0.5 J-lens: lexical joint=True; own/partner ranks=4/18.

[' Arabia', ' Antarctica', ' Oce', ' Africa', ' Oman', ' Kazakhstan', ' Arabian', 'Arab', 'Africa', '大陆', ' Afghanistan', ' Morocco', ' Islands', ' continents', ' Portugal', ' Madagascar', ' Pakistan', ' Europe', ' Somalia', ' Bahrain', ' Qatar', ' Yemen', ' UAE', ' Australia', ' Island', ' Desert', ' Saudi', 'Europe', 'continental', ' Euras', ' Indonesia', ' Ethiopia']

end-pass erased0.5 plain24: lexical joint=False; own/partner ranks=8833/8275.

['Crime', '岛屿', '君主', ' desert', ' Penis', '教体', '冈', '散装', ' Arabia', '花岗岩', '蹦', '大陆', ' Arabian', '叔叔', ' premi', ' specifically', '岛', '祖国', ' Crime', '加工定制', ' Oce', '_specific', 'specific', '职业技术学校', ' vaid', '.Companion', ' peninsula', '神州', '半岛', ' 동아', 'inį', '幻灯片']

end-pass erased0.5 plain27: lexical joint=False; own/partner ranks=2986/11326.

[' North', ' Africa', '非洲', '亚洲', ' Arabian', ' Arabia', '大洋', '东南亚', ' Euras', '-A', ' continental', 'North', ' African', ' Oce', '北', '<think>', ' MEN', ' Southeast', '_A', '[A', ' Bắc', ' آسی', ' Antar', '南亚', '西亚', '-Saharan', ' 동아', '东北', '俑', '具体', ' Middle', 'Africa']

end-pass J-lens: lexical joint=True; own/partner ranks=8/24.

[' Arabia', 'Africa', ' Antarctica', ' Oce', ' Africa', 'Arab', ' Kazakhstan', '亚洲', ' Oman', ' Arabian', 'Europe', ' continents', ' Afghanistan', ' Europe', '大陆', ' Euras', 'China', ' Morocco', 'India', ' Islands', ' Somalia', 'continental', ' Australia', 'Australia', ' Portugal', ' Qatar', ' Pakistan', ' Madagascar', 'Indonesia', ' Bahrain', ' Yemen', ' Indonesia']

## Qatar (expected output Asia)

Input repr:
```text
'<|im_start|>user\nAnswer with only the continent name: On which continent is the country whose capital is Doha?<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Continuation (2 tokens; EOS=True), verbatim:
```text
Asia<|im_end|>
```

end-pass erased0.5 J-lens: lexical joint=True; own/partner ranks=4/131.

[' Antarctica', ' Arabia', ' Africa', ' Oce', ' Qatar', 'Africa', 'Arab', ' Kazakhstan', ' continents', ' Sahara', ' Arabian', '大陆', ' Afghanistan', ' Americas', ' Europe', ' Bahrain', ' Scandin', ' Egypt', ' Islands', ' Palestine', ' Morocco', ' Caribbean', ' Pakistan', 'continental', ' Greenland', 'Europe', ' Saudi', 'North', '非洲', ' Continental', ' Desert', ' Yemen']

end-pass erased0.5 plain24: lexical joint=False; own/partner ranks=599/41654.

['蹦', '叔叔', '玲玲', '教体', 'خلي', ' specifically', '_specific', 'specific', '散装', 'IRTH', 'Crime', ' peninsula', '神州', 'inį', '舌尖上的', ' desert', ' înt', ' caucus', 'влека', '岛屿', ' tiek', ' prezent', ' Oce', '君主', 'Birth', ' specif', ' Beacon', '岛', '伶', '一个个', 'ạm', ' Penis']

end-pass erased0.5 plain27: lexical joint=False; own/partner ranks=1337/89217.

[' North', '亚洲', '北美', ' Africa', '非洲', '北', 'North', ' Bắc', '美洲', '大洋', '-A', ' châu', '西亚', ' Antar', ' Arabian', '东南亚', ' continental', ' Euras', ' continents', ' Europe', ' African', '蹴', ' Middle', '茫茫', '<think>', '[A', 'ทวี', ' Oce', ' MEN', ' آسی', ' Latin', ' Arabia']

end-pass J-lens: lexical joint=True; own/partner ranks=8/164.

[' Arabia', 'Africa', ' Africa', ' Antarctica', ' Oce', 'Arab', ' continents', ' Kazakhstan', ' Qatar', 'Europe', '亚洲', ' Americas', ' Europe', ' Afghanistan', ' Arabian', ' Sahara', '大陆', ' africa', 'continental', ' Scandin', ' Palestine', ' Bahrain', 'Argentina', 'India', ' Hemisphere', ' Euras', 'China', ' Morocco', ' Egypt', ' Pakistan', ' Islands', 'North']

## Namibia (expected output Africa)

Input repr:
```text
'<|im_start|>user\nAnswer with only the continent name: On which continent is the country whose capital is Windhoek?<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Continuation (2 tokens; EOS=True), verbatim:
```text
Africa<|im_end|>
```

end-pass erased0.5 J-lens: lexical joint=False; own/partner ranks=121547/936.

[' Antarctica', ' Kazakhstan', ' Oce', '大陆', ' Asia', ' continents', 'Asia', ' Sahara', '南非', ' Zambia', ' Continental', '非洲', ' continental', 'continental', ' Europe', '南极', 'South', ' Zimbabwe', 'Europe', ' Desert', ' Afrika', '**', ' Americas', '<|endoftext|>', ' Scandin', ' Afghanistan', 'North', ' Ethiopia', ' Mongolia', ' Greenland', ' Arabia', ' South']

end-pass erased0.5 plain24: lexical joint=False; own/partner ranks=14503/30713.

['叔叔', '_specific', ' Bunda', 'ẹo', 'ạm', '散装', '冈', 'iền', '大陆', ' specifically', '蹦', '撒', '统计局', 'specific', '教体', '舌尖上的', ' slik', ' înt', '加工定制', ' FUCK', "').'", ' desert', ' pang', ' Lâm', 'Crime', ' sinking', 'ставка', '盾', ' technik', '中生', 'xia', 'IRTH']

end-pass erased0.5 plain27: lexical joint=False; own/partner ranks=26396/197.

['非洲', ' Afrika', ' continental', '南非', '洲', ' kont', ' África', ' continents', ' конт', ' Афри', '-Saharan', ' South', ' Antarctica', 'AF', ' 남아', '大洋', 'Afrique', ' continente', ' châu', 'ทวี', ' Af', ' North', ' apartheid', 'continental', ' Afro', '大陆', '-A', ' Kont', ' Afrique', ' continuum', '�', ' Asia']

end-pass J-lens: lexical joint=False; own/partner ranks=83562/1636.

[' Antarctica', 'Asia', '非洲', ' Kazakhstan', ' Asia', ' Oce', '南非', ' África', ' continents', '大陆', ' Afrika', ' Sahara', ' Zambia', 'Europe', 'continental', ' Afrique', ' Europe', ' Ethiopia', ' Arabia', 'frica', ' Zimbabwe', ' Americas', ' Mongolia', ' Morocco', ' Kenya', ' Continental', ' Tanzania', 'South', '南极', 'Afrique', ' Afghanistan', ' Somalia']

## Botswana (expected output Africa)

Input repr:
```text
'<|im_start|>user\nAnswer with only the continent name: On which continent is the country whose capital is Gaborone?<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Continuation (2 tokens; EOS=True), verbatim:
```text
Africa<|im_end|>
```

end-pass erased0.5 J-lens: lexical joint=False; own/partner ranks=766/142010.

[' Antarctica', 'Asia', ' Asia', ' Oce', ' Zimbabwe', '大陆', ' Nigeria', '非洲', ' Kazakhstan', ' Afghanistan', '**', 'Europe', ' Mongolia', ' Europe', ' Madagascar', ' continents', 'South', ' Zambia', ' Sahara', 'continental', ' Paraguay', ' Tanzania', '南非', 'asia', ' Americas', ' Ethiopia', ' Island', ' Caribbean', '<|endoftext|>', ' Afrika', ' Australia', ' Euras']

end-pass erased0.5 plain24: lexical joint=False; own/partner ranks=18665/46474.

[' Bunda', '叔叔', '_specific', '冈', 'xia', ' technik', 'ẹo', 'iền', '舌尖上的', ' specifically', 'ardia', ' tiek', '玲玲', ' FUCK', 'itic', ' Lâm', '变性', ' zza', '统计局', '伶', 'IRTH', '文明办', '教体', '颁奖', '辞', 'خلي', ' pagal', 'specific', '人民网', ' Lundi', '蹦', '大陆']

end-pass erased0.5 plain27: lexical joint=False; own/partner ranks=122/67049.

['非洲', '洲', ' continental', ' kont', ' Afrika', ' continents', ' конт', ' continente', ' África', '南非', ' Афри', '大陆', ' châu', '大洋', ' 남아', 'Afrique', '-Saharan', ' continuum', ' Kont', ' South', ' Rhodes', 'AF', '_CONT', 'continental', '-A', ' Af', ' North', 'ทวี', ' Antarctica', '北美', ',A', ' Afrique']

end-pass J-lens: lexical joint=False; own/partner ranks=1962/103668.

['Asia', ' Antarctica', '非洲', ' Asia', ' Oce', 'Europe', ' Nigeria', ' África', ' Zimbabwe', ' Afrika', ' Zambia', ' Mongolia', ' Kazakhstan', ' Ethiopia', ' Tanzania', '大陆', '南非', ' Afrique', ' Europe', ' Afghanistan', ' continents', 'continental', ' Madagascar', ' Sahara', 'India', 'Afrique', ' Arabia', ' Americas', 'asia', 'South', 'Argentina', 'frica']

