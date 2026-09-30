# All eight pursuit cases and equal-cardinality controls

Generated strings are reused eight-token cache entries. Alias scores are not semantic certification. — PI/OpenAI

## 0: December
Input: 'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'
Cached output: ' January.\nQuestion: What is the'

end-pass pursuit J24: alias_joint=False, AUROC=0.5, returned=31
['Months', 'ถัด', ' appelée', ".'.", ' Easter', '...*', ' kalt', ' Bia', '来过', '完全不', ' Moda', '＿＿', ' považ', '烟花', '。）', ' Spam', 'FOUND', ' Maxi', '朦', 'TRL', ' Ibu', '闰', ' Té', '蒜', '通常', ' Sleeve', ' Quello', 'APO', ' Fuji', '空', 'BEGIN']

end-pass unit-dot matched J24: alias_joint=True, AUROC=0.8563636541366577, returned=31
[' Months', ' December', '月份', ' February', 'Months', ' Januari', ' November', 'months', '-month', ' months', '(month', ' April', '月份的', ' bulan', ' tháng', 'เดือน', '_month', 'February', ' Tháng', 'December', ' Oktober', ' October', '.month', ' Februari', '次年', 'ในเดือน', '.Month', ' Ramadan', ' September', ' Marzo', 'calendar']

end-pass pursuit plain24: alias_joint=False, AUROC=0.5, returned=31
[' называется', 'رداد', ' preceded', 'ถัด', '...', ' usually', ' calendar', ' pove', ' regarded', ' наступ', '.', '/ap', '/', ' fools', '°', ' Cyber', '尾巴', '(name', '.getMonth', ' __________________', '眯眯', ' Numer', ' ули', ':', '—', '那个', ' Boxing', '担保', 'Y', ' in', ' qualit']

end-pass unit-dot matched plain24: alias_joint=False, AUROC=0.6945454478263855, returned=31
[' называется', ' called', ' termed', 'رداد', ' appelé', ' invariably', 'ถัด', ' preceded', ' považ', ' наступ', ' называют', '.getMonth', 'called', ' kolej', '眯眯', '紧接着', '志愿服务队', '・・・・', '_calendar', ' kalt', ' appelée', ' usually', ' указы', ' ули', '問わず', 'Called', ' calendar', ' Tháng', 'calendar', ' Folg', 'unie']

end-pass pursuit plain27: alias_joint=False, AUROC=0.5, returned=30
[' called', '_Dec', '____', ' Boxing', '展望', '...', 'usually', ' Ро', '资料来源', '.', ' Sap', ' theaters', '的那个人', '悟', '/j', '                               ', '{}.', ' comput', '水仙', '?', ' посл', ':', 'v', ' preceded', '动感', '手が', ' Δ', '\xa0', ' Reis', 'D']

end-pass unit-dot matched plain27: alias_joint=True, AUROC=0.9854545593261719, returned=30
[' December', ' called', '_Dec', 'December', 'called', ' называется', ' Januari', ' termed', ' Boxing', 'usually', ' appelé', ' usually', ' February', '\tJ', ' Ро', ' জান', 'Called', ' december', 'winter', 'February', '____', '称为', ' 일반적으로', ' typically', ' connu', '新的一年', ' معمول', ' __________________', 'typically', ' januari']

early-prefix at token12, consumed='Fact: The capital of Japan is Tokyo.\nFact: The'
Unmasked positive atoms: [' Ge', ' population', ' Queen', ' CIA', ' Tokyo', ' Lamb', ' Spa', '\\")', 'odore', ' Rocks', ' polo', ' Statue', ' baj', '正式', '氯乙烯', '毛利', '国歌', '公鸡', '最长的', ' Keb', ' رئ', ' роди', ' Austr', ' ausg', ' Flughafen', ' Sungai', '!“', ' Museu', ' Budi', '＿＿', ' Pase', ' Hauptstadt']
Post-mask: [' population', ' Statue', ' Hauptstadt', '最长的', ' CIA', '国歌', ' Budi', ' Queen', ' Austr', '\\")', ' Flughafen', ' Keb', ' رئ', 'odore', ' Museu', ' Ge', '正式', '氯乙烯', ' polo', ' роди', ' Sungai', '公鸡', '!“', ' Pase', '毛利', ' Spa', '＿＿', ' baj', ' Rocks', ' ausg', ' Lamb']

pre-clue at token18, consumed='Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing'
Unmasked positive atoms: ['\\<', ' January', '“The', ' Queen', ' Seat', ' HC', ' Rena', '"...', ' LeBron', ' Phillip', ' dinosaurs', ")').", '(curl', ' birthdays', '螺', '奥运', '最多的', '倒数', '大地震', '核电站', '你的名字', ' hiz', ' ausg', 'த்', '?“', ' Ponta', ' Feria', '페이', ' Azt', ' Ambas', ' Eiff', '本日']
Post-mask: [' January', ' birthdays', ' Eiff', '最多的', '核电站', ' LeBron', '“The', ' Ponta', ' dinosaurs', ")').", '페이', ' hiz', ' Queen', '倒数', '奥运', ' Ambas', '\\<', ' Phillip', '你的名字', ' HC', '本日', '"...', ' Azt', ' Rena', 'த்', '大地震', ' Seat', '(curl', ' ausg', ' Feria', '螺', '?“']

## 1: Thursday
Input: 'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'
Cached output: ' Friday.\nQuestion: What day of'

end-pass pursuit J24: alias_joint=True, AUROC=0.550000011920929, returned=32
[' Thursday', '北欧', ' Halloween', '称为', ' غد', '».**', ' День', ' Erz', '__)', ' Marte', ' Sanc', '通宵', ' Ragnar', '公', '개가', ' Budi', '...”', ' oslo', ' Kolej', '完全不', '劳动节', '对应的', '自由', ' Cha', ' ausg', '<w', ' isti', 'MI', ' paro', ' Maxi', ' Toujours', ' Ruh']

end-pass unit-dot matched J24: alias_joint=True, AUROC=0.9320755004882812, returned=32
[' Thursday', ' Tuesday', ' Monday', ' Wednesday', ' Saturday', ' Sunday', ' Thurs', ' Tues', ' Mondays', ' Thanksgiving', 'Monday', 'Tuesday', 'Thursday', ' Halloween', ' Saturdays', ' monday', ' Christmas', ' Sundays', ' weekdays', ' вторник', 'Saturday', ' weekend', 'Wednesday', '星期三', ' weekends', '星期四', ' Days', '星期日', ' Iceland', ' tomorrow', ' Oktober', ' Easter']

end-pass pursuit plain24: alias_joint=False, AUROC=0.5, returned=30
[' called', 'always', '...', ' الني', ' preceded', '____', ' Boxing', '现代的', '<|im_end|>', '开放', '금', '表面上', ' eig', '除恶', ' a', '动感', ' нор', ' Labor', 'le', '.', ' NOT', ']].', '树林', '少儿', ' информ', '阳极', ' ', ' lands', ' colleg', '/']

end-pass unit-dot matched plain24: alias_joint=False, AUROC=0.9000000357627869, returned=30
[' called', 'always', 'called', ' preceded', ' الني', ' называется', ' always', '现代的', ' информ', '诞辰', ' disebut', ' Boxing', 'IVERY', '除恶', ' lucr', '动感', ' Always', ' Dici', 'Always', '的名称', ' مرتبط', '少儿', ' 반드시', '금', '・・・・', ' нор', 'lands', ' Dzie', ' Lapangan', '呼び']

end-pass pursuit plain27: alias_joint=True, AUROC=0.550000011920929, returned=31
[' Thursday', '...', 'called', ' среда', 'FR', ' Þ', ' wed', ' Чет', ' Mon', '금', ' pagan', ' ', 'always', ']].', '<|im_end|>', '除恶', ':', 'NOT', ' Boxing', '瑞典', '开放', 'Thứ', ' inaugur', '____', '.', '动感', 'bru', ' a', '-S', '推断', 'rides']

end-pass unit-dot matched plain27: alias_joint=True, AUROC=0.9358490705490112, returned=31
[' Thursday', ' Wednesday', 'Monday', ' среда', ' Monday', 'Thursday', 'Wednesday', ' Thurs', ' среду', ' Чет', 'called', ' Tuesday', 'Tuesday', 'uesday', ' Thu', ' Saturday', '_FR', ' called', ' Wed', ' среды', ' wed', 'FR', 'Saturday', ' Þ', 'always', 'Thứ', '星期三', '瑞典', ' امروز', ' aujourd', 'ุกร์']

early-prefix at token12, consumed='Fact: The capital of Japan is Tokyo.\nFact: The'
Unmasked positive atoms: [' Ge', ' population', ' Queen', ' CIA', ' Tokyo', ' Lamb', ' Spa', '\\")', 'odore', ' Rocks', ' polo', ' Statue', ' baj', '正式', '氯乙烯', '毛利', '国歌', '公鸡', '最长的', ' Keb', ' رئ', ' роди', ' Austr', ' ausg', ' Flughafen', ' Sungai', '!“', ' Museu', ' Budi', '＿＿', ' Pase', ' Hauptstadt']
Post-mask: [' population', ' Statue', ' Hauptstadt', '最长的', ' CIA', '国歌', ' Budi', ' Queen', ' Austr', '\\")', ' Flughafen', ' Keb', ' رئ', 'odore', ' Museu', ' Ge', '正式', '氯乙烯', ' polo', ' роди', ' Sungai', '公鸡', '!“', ' Pase', '毛利', ' Spa', '＿＿', ' baj', ' Rocks', ' ausg', ' Lamb']

pre-clue at token19, consumed='Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after'
Unmasked positive atoms: [' Cool', ' Tokyo', ' Pizza', ' Abraham', ' mue', '\\"",', ' dinosaurs', ' XK', 'birds', ' Julius', ' Madonna', '顾', '人名', '希腊', '这个人', '源自', '枫叶', '泰勒', '谐音', '取其', ' Capit', ' столиц', ' ausg', ' Padre', ' Samb', ' Alba', '?“', ' сэ', ' Lundi', ' Nuit', ' dran', ' shk']
Post-mask: [' Abraham', ' dinosaurs', '这个人', ' Madonna', ' Pizza', '人名', '?“', ' Padre', ' Julius', ' dran', '\\"",', ' столиц', ' Samb', '谐音', '源自', 'birds', ' Nuit', ' сэ', ' shk', ' Alba', ' Cool', ' ausg', '希腊', '取其', ' mue', ' XK', ' Lundi', '泰勒', '顾', '枫叶']

## 2: autumn
Input: 'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'
Cached output: ' winter.\nHypothesis: The'

end-pass pursuit J24: alias_joint=False, AUROC=0.5, returned=31
['干旱', '__.', '叫做', '紧接着', ' Tropical', ' begon', '樱花', 'PEAT', 'Months', '暖气', '。）', '充满活力', '造林', '相反的', ' Festiv', '<u', ' GREEN', '到来', ' Quali', '”…', '通常是', ' cic', ' Autre', ' Basketball', ' ausg', ' Compre', ' kalt', 'BEGIN', '马超', ' Té', '«.']

end-pass unit-dot matched J24: alias_joint=False, AUROC=0.8714596629142761, returned=31
[' autumn', ' primavera', ' summer', '冬季', '春季', ' rainy', ' printemps', ' seasons', ' зим', '雨季', 'summer', ' vinter', '冬天', ' Autumn', '季节', '春天', '夏季', ' spring', ' drought', 'ฤดู', ' summers', ' hiver', '春暖花开', ' Mùa', ' invierno', ' seasonal', '旺季', ' inverno', ' Summer', '秋季', ' warmer']

end-pass pursuit plain24: alias_joint=False, AUROC=0.5, returned=31
[' preceded', '.', ' called', ' наступ', '...', ' invariably', ' seasons', 'spring', '.navigationBar', '_the', "').'", '干旱', '/w', '名', ':', ' NOT', ' agriculture', '____', '到来', ' bore', '鸟语', '暖', ' a', ' rigor', '(s', 'dic', ' ', '冲刺', '\r', '另一种', 'beg']

end-pass unit-dot matched plain24: alias_joint=True, AUROC=0.8387799263000488, returned=31
[' preceded', ' наступ', ' называется', ' called', '紧接着', ' seasons', 'spring', ' invariably', '.navigationBar', ' termed', 'called', ' называют', ' forests', 'summer', '_the', '到来', ' agriculture', 'ฤดู', 'のことを', ' vinter', '温暖的', ' characterized', 'Spring', ' autumn', '鸟语', ' followed', ' springs', '是一年', '序幕', ' длится', ' bureaucracy']

end-pass pursuit plain27: alias_joint=True, AUROC=0.5294117331504822, returned=31
['Spring', ' called', ' summer', ' наступ', ' characterized', '...', '客机', 'ใบ', ' invariably', '(s', '上传者', ':', ' bore', '降水', ' hotter', '____', '园艺', 'unno', '_prim', '另一种', '/', '<|im_end|>', ' ', '全文数据库', ' Crédit', '紧接着', '.', 'nt', ' Boxing', 'Aut', '短袖']

end-pass unit-dot matched plain27: alias_joint=True, AUROC=0.9433550834655762, returned=31
['Spring', 'spring', ' spring', ' Spring', ' summer', ' autumn', 'pring', ' springs', 'summer', ' verano', ' primavera', ' Summer', 'Summer', '春', '春天', ' printemps', '.spring', '春意', ' Autumn', ' called', ' наступ', ' verão', '\tSpring', ' vinter', '.Spring', '春季', 'ฤดู', ' summers', '春的', ' characterized', ' preceded']

early-prefix at token12, consumed='Fact: The capital of Japan is Tokyo.\nFact: In'
Unmasked positive atoms: ['\\u', 'uz', ' Japan', ' Metro', ' Padding', '_<', ' WWII', ' Salman', ' Oktober', ' Cic', ' Ves', ' winters', 'habit', '排名', '中国共产党成立', '一般情况下', '公元前', '体育课', '鸟语', '抽水', ' Pari', ' Goi', ' Muit', 'estig', ' Sejak', '!“', '«,', ' demokrasi', ' бре', ' fyn', ' Traf', ' yık']
Post-mask: [' Oktober', ' WWII', '\\u', ' Metro', 'habit', ' demokrasi', ' winters', ' Padding', '中国共产党成立', 'uz', ' Muit', ' yık', '一般情况下', ' Pari', '!“', '排名', ' Cic', '体育课', '鸟语', '公元前', ' Traf', '抽水', ' Goi', 'estig', '«,', ' Salman', ' бре', ' Ves', ' fyn', '_<', ' Sejak']

pre-clue at token23, consumed='Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when'
Unmasked positive atoms: ['“', ' Christmas', ' Barack', ' QUE', ' Basketball', '\\"",', ' rains', ' Avg', ' sunrise', '#/', ' Polo', ' Nicol', ' KV', ' glaciers', ' Comet', '公', '调', '努', '树叶', '大多数人', '是一年', '最长的', '常驻', '追着', ' приме', '。**', ' Santi', ' Tierra', ' наблюдается', '＿＿', ' begon', '札幌']
Post-mask: [' sunrise', ' glaciers', ' Christmas', '最长的', '\\"",', ' rains', ' Barack', ' Avg', ' наблюдается', '大多数人', ' Comet', '＿＿', '札幌', '#/', ' Nicol', ' KV', '“', ' begon', '追着', ' Basketball', '是一年', '。**', '常驻', ' приме', ' Tierra', '努', '公', ' Polo', ' QUE', '树叶', ' Santi', '调']

## 3: apple
Input: 'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'
Cached output: ' red.\nHypothesis: The'

end-pass pursuit J24: alias_joint=False, AUROC=0.47727271914482117, returned=31
[' pink', ' strawberries', '红色', '。\\', ' BLACK', ' Apfel', '|.', '在德国', ' Granny', '描述', ' ined', ' Candy', '貂', ' Bái', 'MC', ' LENG', '*/)', 'FALSE', ' dran', ' güz', ' Alba', '薇', '··', ' Interna', ' Toujours', ' Sya', ' Erz', ' bbc', ' berüh', '�', 'ریان']

end-pass unit-dot matched J24: alias_joint=False, AUROC=0.8181818127632141, returned=31
[' pink', ' purple', '红色', ' strawberry', 'pink', ' красный', ' rossa', ' strawberries', ' rojo', 'purple', ' rouge', ' poisonous', ' blonde', ' rosso', ' berries', '(red', ' violet', ' orange', ' Purple', '红色的', ' blue', ' Pink', '粉红色', ' crimson', ' Strawberry', '_red', '紅色', ':red', ' rouges', ' yellow', '蓝色']

end-pass pursuit plain24: alias_joint=False, AUROC=0.47727271914482117, returned=32
['红颜', ' лечению', ' depicted', '红色', ' organs', '....', '全文数据库', '_', ' poisoning', '/w', ' diam', '.', 'シャー', '史蒂', ' a', 'MC', ' утвер', ' бел', '�', '变电', '<|im_end|>', '_integration', 'Ford', 'related', ' (', '惨叫', ' berries', ' spo', 'B', '通常是', ' antagon', '拐']

end-pass unit-dot matched plain24: alias_joint=False, AUROC=0.9040403962135315, returned=32
['红颜', ':red', ' красный', '_red', ' лечению', '红色', '全文数据库', ' rojo', ' depicted', ' эксперти', ' Eventi', '红了', '빨', '史蒂', '_integration', ' poisoning', ' poisonous', ' 레드', '分享到朋友圈', ' czerw', '惨叫', '红红的', ' thème', ' červen', '粉红色', ' organs', '_cores', "').'", '眯眯', ' iCloud', ' jdbc', 'シャー']

end-pass pursuit plain27: alias_joint=False, AUROC=0.5037878751754761, returned=31
['红色', ' apple', ' бел', ' depicted', ' rů', '全文数据库', '_RE', '...', ' cyan', ' упомина', ' Applies', ':', '<|im_end|>', '纯洁', ' Plum', '{}".', '\xa0\xa0\xa0\xa0', '.', ' deadly', '分红', 'M', '的不是', '应有尽有', ' a', ' spo', ' (', ' лечению', '_', '白雪', ' WW', '中毒']

end-pass unit-dot matched plain27: alias_joint=False, AUROC=0.9116161465644836, returned=31
[' poisoning', '_red', ' красный', '红色', ' rojo', ' poisonous', ':red', '紅色', ' červen', '紅', ' đỏ', '.red', ' apple', ' красного', '(red', '中毒', 'สีแดง', ' 레드', ' rouge', ' الأحمر', '红', ' vermelho', '红色的', '-red', 'Apple', '红了', ' apples', ' czerw', '红红的', '红线', ' крас']

early-prefix at token12, consumed='Fact: The capital of Japan is Tokyo.\nFact: The'
Unmasked positive atoms: [' Ge', ' population', ' Queen', ' CIA', ' Tokyo', ' Lamb', ' Spa', '\\")', 'odore', ' Rocks', ' polo', ' Statue', ' baj', '正式', '氯乙烯', '毛利', '国歌', '公鸡', '最长的', ' Keb', ' رئ', ' роди', ' Austr', ' ausg', ' Flughafen', ' Sungai', '!“', ' Museu', ' Budi', '＿＿', ' Pase', ' Hauptstadt']
Post-mask: [' population', ' Statue', ' Hauptstadt', '最长的', ' CIA', '国歌', ' Budi', ' Queen', ' Austr', '\\")', ' Flughafen', ' Keb', ' رئ', 'odore', ' Museu', ' Ge', '正式', '氯乙烯', ' polo', ' роди', ' Sungai', '公鸡', '!“', ' Pase', '毛利', ' Spa', '＿＿', ' baj', ' Rocks', ' ausg', ' Lamb']

pre-clue at token17, consumed='Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit'
Unmasked positive atoms: ['................', '\\">', '「', ' Pir', ' Maz', ' Fruit', ' banana', 'cake', ' pis', ' Scarlet', ' raspberry', '供', '契', '称为', '种类', '颜色', '脐', '摘下', '和蔬菜', '产自', ' Samb', ' Neymar', '?“', '❤️', ' Pob', ' spad', ' thun', ' رضا', ' margar', ' Sauv', ' Tokio', ' doves']
Post-mask: [' banana', 'cake', '称为', ' raspberry', '「', '产自', ' Scarlet', ' Neymar', '?“', '颜色', ' spad', '和蔬菜', ' Samb', ' thun', '❤️', ' Pir', '契', ' margar', ' Pob', '................', ' doves', ' رضا', ' Sauv', ' Tokio', '\\">', '脐', ' Maz', '种类', ' pis', '供', '摘下']

## 4: violin
Input: 'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'
Cached output: ' the woodwind family.\nQuestion:'

end-pass pursuit J24: alias_joint=True, AUROC=0.5714285969734192, returned=31
[' violin', ' comprised', ' Brass', '。\\', ' مرتبط', ' Trees', '«.', ' عائلة', '目瞪口呆', ' Polo', ' tamb', ' SAME', '暖气', ' kling', ':X', ' γνω', ' Cuc', '存在', ' Lamborghini', ' Rotary', ' berüh', ' HARD', ' Austr', '缺失', '【', ' Serif', '锤子', ' dran', ':...', ' TECN', ' Columb']

end-pass unit-dot matched J24: alias_joint=True, AUROC=0.8598901033401489, returned=31
[' violin', ' Piano', ' piano', ' guitar', ' Guitar', '钢琴', ' guitars', 'ดนตรี', ' percussion', ' flute', '乐器', ' comprised', ' trumpet', ' Mozart', '古筝', ' jazz', ' composed', ' musicians', ' Jazz', '古琴', ' auditory', ' музыка', '提琴', '的音乐', '小提琴', ' 음악', ' الموسيقى', ' instrumental', ' pian', '声乐', ' musician']

end-pass pursuit plain24: alias_joint=False, AUROC=0.49038463830947876, returned=30
[' comprised', ' percussion', ' NOT', 'dataProvider', ' called', '_the', '_pipe', ':', '<|im_end|>', ' closely', '吵闹', 'ходу', ' ...', ' auditor', 'A', ' wood', '错误的是', '键盘', "').'", '{{', 'ro', '.', ' descended', ' a', 'INVALID', '/', '很好奇', ' disb', '..', 'WK']

end-pass unit-dot matched plain24: alias_joint=True, AUROC=0.8736264109611511, returned=30
[' comprised', ' percussion', ' descended', '_pipe', ' keluarga', ' المكان', '吵闹', '_family', 'っていました', 'dataProvider', ' responsabilità', ' violin', ' عائلة', ' vocals', "').'", '_the', ' dbo', ' العائلة', 'INVALID', ' خانواده', '很好奇', '_valid', ' verantwortlich', 'ходу', 'members', ' jsonResponse', '教体', ' guitars', '木有', ' ALSO']

end-pass pursuit plain27: alias_joint=False, AUROC=0.5631868243217468, returned=29
[' violin', ' instruments', '键盘', ' brass', ':', ' percussion', 'wind', ' called', '_pipe', ' NOT', ' ...', ' uk', 'STRING', '类比', ' a', '{{', ' descended', '壮大', '=', '没钱', '错误的是', ' wood', '忧心', 'Based', ' c', 'axes', '????', 'W', ' ']

end-pass unit-dot matched plain27: alias_joint=True, AUROC=0.9697802662849426, returned=29
[' violin', ' instruments', ' percussion', ' instrumentos', '键盘', ' piano', ' guitars', ' Instruments', ' flute', 'Viol', ' instrumental', ' Piano', ' trumpet', ' drums', ' sax', '小提琴', ' viol', 'keyboard', ' guitar', ' instrumentation', ' Viol', '-viol', ' инструментов', ' keyboards', '钢琴', ' viola', ' brass', '弦', ' instrumento']

early-prefix at token12, consumed='Fact: The capital of Japan is Tokyo.\nFact: The'
Unmasked positive atoms: [' Ge', ' population', ' Queen', ' CIA', ' Tokyo', ' Lamb', ' Spa', '\\")', 'odore', ' Rocks', ' polo', ' Statue', ' baj', '正式', '氯乙烯', '毛利', '国歌', '公鸡', '最长的', ' Keb', ' رئ', ' роди', ' Austr', ' ausg', ' Flughafen', ' Sungai', '!“', ' Museu', ' Budi', '＿＿', ' Pase', ' Hauptstadt']
Post-mask: [' population', ' Statue', ' Hauptstadt', '最长的', ' CIA', '国歌', ' Budi', ' Queen', ' Austr', '\\")', ' Flughafen', ' Keb', ' رئ', 'odore', ' Museu', ' Ge', '正式', '氯乙烯', ' polo', ' роди', ' Sungai', '公鸡', '!“', ' Pase', '毛利', ' Spa', '＿＿', ' baj', ' Rocks', ' ausg', ' Lamb']

pre-clue at token19, consumed='Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument'
Unmasked positive atoms: ['\\"', ' category', '【', ' Pist', ' Trent', '>b', ' Musical', ' violin', ' Gloves', '*/)', ' keyboards', ' Pang', '螺', '称为', '琉', '古董', '家族的', '下表', '海鸥', ' çe', ' lapis', '∙', 'த்', ' HUM', ' kū', ' Cib', ' Suri', 'টির', ' Mannheim', ' INSTR', 'komb', ' Coro']
Post-mask: [' violin', '称为', ' category', ' Pist', '\\"', ' kū', '古董', '琉', ' çe', ' Trent', '*/)', ' Pang', '家族的', ' keyboards', ' lapis', '【', ' Cib', 'টির', 'த்', ' Gloves', ' Mannheim', '∙', '螺', '下表', ' Coro', 'komb', '海鸥', '>b', ' Suri', ' HUM']

## 5: Hamlet
Input: "Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"
Cached output: ' William Shakespeare.\nQuestion: Who wrote'

end-pass pursuit J24: alias_joint=False, AUROC=0.4910714328289032, returned=32
[' Shakespeare', ' Robert', '丹麦', 'unknown', ' playwright', '。\\', ' Mort', '笔名', ' Jorn', ' Budi', '__)', ' mcc', '«.', '虚构', '毛', ' Claud', '(Func', ' Elis', ' gondol', '离世', ' Charl', '")!=', ' Manz', '吊', '冷气', '为王', ' Urs', ' chamb', '忙碌', '由高', ' Haf', '萧']

end-pass unit-dot matched J24: alias_joint=False, AUROC=0.8928571343421936, returned=32
[' Shakespeare', '莎士比亚', ' Robert', ' Elizabeth', ' playwright', ' Dickens', 'akespeare', ' Henry', ' Richard', ' Aristotle', ' John', ' Charles', ' Shakespe', ' Margaret', ' George', ' Tolkien', ' Henrik', ' Jane', ' Romeo', ' Edward', ' Christopher', ' Julius', ' Dumbledore', ' Harry', ' Stephen', ' Emily', ' Samuel', ' Matthew', ' novelist', ' Edmund', ' Daniel', ' Arthur']

end-pass pursuit plain24: alias_joint=False, AUROC=0.4910714328289032, returned=31
[' Shakespeare', ' credited', '虚构', '____', ' usually', ' mortality', ' unknown', ' corpus', '推理', ' canon', '屠', '...', ' Haf', ' a', 'Ghost', ' مسرح', '.', '鲁', '除掉', ' ', ' Th', ' السير', ' sco', 'Works', '/w', ' bullying', '佚', '港', '-', ' mad', '<|im_end|>']

end-pass unit-dot matched plain24: alias_joint=False, AUROC=0.7351190447807312, returned=31
[' Shakespeare', ' credited', '虚构', ' fictional', ' playwright', 'akespeare', ' fiction', ' مسرح', '莎士比亚', ' السير', '佚', ' corpus', ' breastfeeding', ' unbek', ' UNKNOWN', ' supposed', ' deceased', ' mortality', '丹麦', '推理', ' greve', '谋杀', '異なります', ' murdered', ' autoria', '伟大的', ' Unknown', '.......', ' unknown', ' tragedia', ' المسرح']

end-pass pursuit plain27: alias_joint=False, AUROC=0.4821428656578064, returned=31
[' Shakespeare', ' playwright', ' credited', ' lago', ' shakes', '屠', ' unknown', ':', ' mortality', '丹麦', '____', '舞台上', 'Ghost', ' ', ' dram', ' eit', '/w', ' Strat', '-', ' revenge', ' topping', ' Sen', '       ', 'ælde', '.', '搬', ' thou', '5', ' Hol', '迷雾', 'Pub']

end-pass unit-dot matched plain27: alias_joint=False, AUROC=0.7976190447807312, returned=31
[' Shakespeare', ' playwright', 'akespeare', '莎士比亚', ' مسرح', ' Shakespe', ' dramat', '舞台上', ' المسرح', ' credited', ' 셰', ' théâtre', ' teatro', ' شك', '-play', ' shakes', ' Plays', ' dram', ' plays', ' lago', '莎士', ' театра', '/play', ' teatrale', ' tragedies', '_play', ' theatrical', ' Théâtre', ' onstage', ' tragedia', 'akespe']

early-prefix at token12, consumed='Fact: The capital of Japan is Tokyo.\nFact: The'
Unmasked positive atoms: [' Ge', ' population', ' Queen', ' CIA', ' Tokyo', ' Lamb', ' Spa', '\\")', 'odore', ' Rocks', ' polo', ' Statue', ' baj', '正式', '氯乙烯', '毛利', '国歌', '公鸡', '最长的', ' Keb', ' رئ', ' роди', ' Austr', ' ausg', ' Flughafen', ' Sungai', '!“', ' Museu', ' Budi', '＿＿', ' Pase', ' Hauptstadt']
Post-mask: [' population', ' Statue', ' Hauptstadt', '最长的', ' CIA', '国歌', ' Budi', ' Queen', ' Austr', '\\")', ' Flughafen', ' Keb', ' رئ', 'odore', ' Museu', ' Ge', '正式', '氯乙烯', ' polo', ' роди', ' Sungai', '公鸡', '!“', ' Pase', '毛利', ' Spa', '＿＿', ' baj', ' Rocks', ' ausg', ' Lamb']

pre-clue at token17, consumed='Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose'
Unmasked positive atoms: [' title', 'WW', ' lyrics', 'Contains', '(_.', ' protagonist', ' McD', '\\"",', ' Spo', '_rm', ' Edgar', 'MV', ' Dram', ' premiered', ' Jas', ' Staten', '灵感', '导致了', '蒙特', '篡改', ' wund', ' Fuer', ' Gedung', ' Poli', '■■', ' cujo', ' konusu', '?“', ' Siti', ' adı', ' Shakespe', ' Tratt']
Post-mask: [' protagonist', ' lyrics', '\\"",', ' adı', '(_.', ' Gedung', 'Contains', ' Edgar', '灵感', '?“', ' Dram', ' cujo', '蒙特', ' wund', ' Spo', '_rm', ' premiered', ' Fuer', ' Staten', 'MV', ' Jas', '■■', ' Shakespe', '导致了', ' Siti', ' Tratt', ' McD', ' Poli', '篡改', 'WW', ' konusu']

## 6: hydrogen
Input: 'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'
Cached output: ' a gas.\nHypothesis:'

end-pass pursuit J24: alias_joint=False, AUROC=0.5, returned=31
['液态', ' vapor', '__.', ' Lightweight', ' invariably', ' jelly', ' Homo', '破冰', ' Ruh', ' STO', '各不相同', '？”', '固体', ' bombe', ' Ging', '«.', ' eit', ' Pizza', '青松', '猜想', ':...', '桌子', ' Samb', '<u', ' Emas', ' abhängig', ' анги', ' Unknown', ' лёг', ' mdi', ' berüh']

end-pass unit-dot matched J24: alias_joint=False, AUROC=0.6728395223617554, returned=31
['液态', ' liquids', 'liquid', ' liquid', ' vapor', ' Liquid', ' lique', ' Vapor', '液体', ' gases', ' liquide', '常温', '气体', ' liquido', 'Liquid', '的气体', ' Liqu', '液化', ' fluids', ' vap', '_gas', '固态', ' líquido', ' Gas', ' gas', '固体', ' magma', ' жидкости', ' solids', 'gas', '液体的']

end-pass pursuit plain24: alias_joint=False, AUROC=0.5, returned=31
['สถานะ', '...', '液态', 'usually', ' exhibited', 'फल', ' not', 'graph', ' quyển', ':', ' something', '卜', '吸气', ' dibattito', ' kwest', '_pred', '<|im_end|>', '常温', '\xa0', ' namely', ' unle', '�', '.', '_', '/w', '观光', '................', 'โปร่ง', ',', ' представляет', 'ั']

end-pass unit-dot matched plain24: alias_joint=False, AUROC=0.5679012537002563, returned=31
['สถานะ', ' الحالة', '液态', 'usually', '固态', '常温', ' liquids', ' состояния', '的状态', '................', '的气体', '.......', '状态的', ' usually', ' 항상', '工作状态', '_state', '.....', '[state', '固体', ' estado', 'फल', '........', ' quyển', ' состояние', ' invariably', ' gases', ' газо', ' состоянию', '液体', 'ั']

end-pass pursuit plain27: alias_joint=False, AUROC=0.472222238779068, returned=31
[' gas', '固态', 'usually', '...', ' liquids', ' الحالة', ':', ' dibattito', ' determined', ' __________________', '(g', '_predict', '附录', ' what', '�', '/w', ' NOT', 'blogs', ' boils', '<|im_end|>', '\xa0', 'graph', '其中之一', ' paperback', '$', ' gaze', '吸气', ' -', 'PAR', ' Britann', ' errone']

end-pass unit-dot matched plain27: alias_joint=False, AUROC=0.5925925970077515, returned=31
[' gas', ' gases', '气体', '的气体', '气体的', ' Gas', '_gas', 'gas', 'Gas', ' газ', ' газа', '固态', ' газо', '固体', '气', ' gás', ' GAS', ' الغاز', ' liquids', 'liquid', '液态', 'ก๊าซ', ' liquid', ' solids', '氣體', 'solid', ' газов', '液体', ' غاز', ' rắn', ' گاز']

early-prefix at token12, consumed='Fact: The capital of Japan is Tokyo.\nFact: The'
Unmasked positive atoms: [' Ge', ' population', ' Queen', ' CIA', ' Tokyo', ' Lamb', ' Spa', '\\")', 'odore', ' Rocks', ' polo', ' Statue', ' baj', '正式', '氯乙烯', '毛利', '国歌', '公鸡', '最长的', ' Keb', ' رئ', ' роди', ' Austr', ' ausg', ' Flughafen', ' Sungai', '!“', ' Museu', ' Budi', '＿＿', ' Pase', ' Hauptstadt']
Post-mask: [' population', ' Statue', ' Hauptstadt', '最长的', ' CIA', '国歌', ' Budi', ' Queen', ' Austr', '\\")', ' Flughafen', ' Keb', ' رئ', 'odore', ' Museu', ' Ge', '正式', '氯乙烯', ' polo', ' роди', ' Sungai', '公鸡', '!“', ' Pase', '毛利', ' Spa', '＿＿', ' baj', ' Rocks', ' ausg', ' Lamb']

pre-clue at token19, consumed='Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the'
Unmasked positive atoms: [' city', 'α', ' substance', ' Mol', ' hottest', ' Liquid', ' MED', '。\\', ' Kurds', ')")', ' unicorn', ' Statue', ' Belize', ' Pasta', '化学', '馒', '溶解', '国旗', '最常用的', ' Kön', ' Đồng', ' rik', '）」', ' гипо', ' pala', ' Vedi', ' بري', ' сэ', ' austr', ' vorgen', ' kling', ' Eiff']
Post-mask: [' substance', ' hottest', ' Statue', ' Liquid', ' unicorn', ' Belize', '国旗', '。\\', ' city', '最常用的', ' Pasta', '溶解', ' Kurds', 'α', ' rik', ' MED', ')")', '化学', ' Vedi', ' Kön', ' сэ', ' austr', '馒', ' vorgen', ' Mol', ' гипо', ' Eiff', '）」', ' Đồng', ' pala', ' بري', ' kling']

## 7: triangle
Input: 'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'
Cached output: ' 3.\nFact: The number'

end-pass pursuit J24: alias_joint=True, AUROC=0.5333333015441895, returned=32
[' ALWAYS', ' triangle', '(number', '固定的', '等于', '.\\', ' Polygon', ' drie', '取决于', ' Undefined', '.addEdge', ':...', ' Bia', '_ge', ' kaki', '«.', ' 다양', ' Sasha', '至少有', '愚', ' Evang', '>|', '六', ' Spor', '满脸', ' kū', ' Mosc', '鲁班', ' indé', 'zf', ' isti', ' Bake']

end-pass unit-dot matched J24: alias_joint=True, AUROC=0.9999999403953552, returned=32
[' ALWAYS', ' triangle', 'always', ' triangles', ' always', ' polygon', '三角形的', '三角形', ' polygons', ' triangular', '(number', ' دائمًا', ' invariably', ' zawsze', ' دائماً', ' triang', ' Always', ' selalu', 'Always', ' 항상', ' Triangle', ' vždy', ' beträgt', ' всегда', '必ず', 'Triangle', '总是', 'Triangles', ':number', 'triangle', ' треуго', ' Polygon']

end-pass pursuit plain24: alias_joint=False, AUROC=0.4893616735935211, returned=31
['always', '三角形的', ' indetermin', ' greater', ' exactly', '____', '...', 'फल', 'aner', ':number', 'FACE', '取决于', ' <', 'n', '<|im_end|>', '{}".', '恒心', ' waved', ' uniquely', ':', '3', 'ฤษฎ', '在这种情况下', '/is', ' liable', '幻', '..', ' Lob', ' Gegen', '所大学', 'ge']

end-pass unit-dot matched plain24: alias_joint=True, AUROC=0.9999999403953552, returned=31
['always', ' always', '三角形的', ' triangles', ' Always', ' selalu', 'Always', 'फल', ' zawsze', ' ALWAYS', ' polygons', ' indetermin', ' دائمًا', ' invariably', ' всегда', '所大学', ' دائماً', ' 항상', ' Siempre', ' greater', '必ず', '.........', '(number', 'usually', ' зависеть', ' uniquely', 'ilateral', ' exactly', '異なります', '永远不会', 'depends']

end-pass pursuit plain27: alias_joint=False, AUROC=0.5234042406082153, returned=29
[' always', ' triangles', ' determined', '____', 'ilateral', '依赖于', ' ?.', '(n', ' exactly', ' impres', ' Anzahl', '...', ' greater', 'aner', ':', ' gonna', '{}".', '.edges', 'फल', '恒心', '除非', '3', '<|im_end|>', '\xa0', 'poly', ' называется', 'S', 'vor', '固定']

end-pass unit-dot matched plain27: alias_joint=True, AUROC=0.9985815286636353, returned=29
[' always', 'always', ' triangles', '三角形的', ' Always', 'Always', ' triangle', '三角形', ' всегда', ' sempre', ' 항상', ' selalu', ' ALWAYS', ' zawsze', ' دائمًا', '常に', ' alltid', '总是', ' altijd', 'Triangle', 'triangle', ' luôn', ' треуго', ' siempre', ' toujours', '必ず', ' determined', ' Всегда', ' invariably']

early-prefix at token12, consumed='Fact: The capital of Japan is Tokyo.\nFact: The'
Unmasked positive atoms: [' Ge', ' population', ' Queen', ' CIA', ' Tokyo', ' Lamb', ' Spa', '\\")', 'odore', ' Rocks', ' polo', ' Statue', ' baj', '正式', '氯乙烯', '毛利', '国歌', '公鸡', '最长的', ' Keb', ' رئ', ' роди', ' Austr', ' ausg', ' Flughafen', ' Sungai', '!“', ' Museu', ' Budi', '＿＿', ' Pase', ' Hauptstadt']
Post-mask: [' population', ' Statue', ' Hauptstadt', '最长的', ' CIA', '国歌', ' Budi', ' Queen', ' Austr', '\\")', ' Flughafen', ' Keb', ' رئ', 'odore', ' Museu', ' Ge', '正式', '氯乙烯', ' polo', ' роди', ' Sungai', '公鸡', '!“', ' Pase', '毛利', ' Spa', '＿＿', ' baj', ' Rocks', ' ausg', ' Lamb']

pre-clue at token18, consumed='Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape'
Unmasked positive atoms: ['“', ' formed', ' Shape', ' QUE', ' Pizza', '/angular', ' pictured', ' кл', 'iran', 'ABCDE', ' polygons', '"is', ' RECT', ' nale', ' Rosie', ' bola', '三角', '喘', '在水', '太极', '以下的', '叫做', '至少有', ' Kön', ' رئ', ' крат', ' berüh', '♡', ' Giardia', ' dependen', ' Luka', ' Eiff']
Post-mask: [' pictured', '叫做', ' polygons', '♡', ' Pizza', 'ABCDE', '"is', 'iran', ' Eiff', ' Giardia', ' bola', ' RECT', '在水', ' formed', '以下的', ' رئ', ' Luka', '/angular', ' QUE', '太极', ' dependen', ' Rosie', ' кл', '至少有', ' nale', '三角', ' berüh', ' Kön', '“', ' крат', '喘']

