# All eight development cases

Written by PI/OpenAI. Raw token lists, not semantic certification. GP means the new gradient-pursuit solver; MP means native matching pursuit.


## 0: December

Input: `'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing Christmas Day is'`

Cached output: `' January.\nQuestion: What is the'`

### end-pass gradient pursuit J24: alias pass=False, returned=31

[' Easter', '月份', ' kalt', 'Months', ' považ', '紧接着', '。）', '...*', '<u', '完全不', ' Januari', 'ถัด', '闰', ' Marzo', ' Oktober', ' Bia', ".'.", ' Té', ' Soup', ' appelée', '来过', '朦', 'BEGIN', '烟花', ' Ramadan', ' Moda', ' Adri', ' Caritas', ' Sleeve', 'YYY', ' Santa']

### end-pass gradient unit-dot matched J24: alias pass=True, returned=31

[' Months', ' December', '月份', ' February', 'Months', ' Januari', ' November', 'months', '-month', ' months', '(month', ' April', '月份的', ' bulan', ' tháng', 'เดือน', '_month', 'February', ' Tháng', 'December', ' Oktober', ' October', '.month', ' Februari', '次年', 'ในเดือน', '.Month', ' Ramadan', ' September', ' Marzo', 'calendar']

### end-pass pursuit J24: alias pass=False, returned=31

['Months', 'ถัด', ' appelée', ".'.", ' Easter', '...*', ' kalt', ' Bia', '来过', '完全不', ' Moda', '＿＿', ' považ', '烟花', '。）', ' Spam', 'FOUND', ' Maxi', '朦', 'TRL', ' Ibu', '闰', ' Té', '蒜', '通常', ' Sleeve', ' Quello', 'APO', ' Fuji', '空', 'BEGIN']

### end-pass gradient pursuit plain24: alias pass=False, returned=31

['.', '...', ' называется', 'رداد', ' calendar', ' regarded', ' наступ', 'ถัด', '.getMonth', ' preceded', '眯眯', ' fools', ' pove', ' usually', '/ap', '(name', ' Boxing', ' Numer', 'FIL', '尾巴', ' ___', ' qualit', ' Cait', ' الرب', '°', ' invariably', 'Y', '(M', '/', ' ули', ' [']

### end-pass gradient unit-dot matched plain24: alias pass=False, returned=31

[' называется', ' called', ' termed', 'رداد', ' appelé', ' invariably', 'ถัด', ' preceded', ' považ', ' наступ', ' называют', '.getMonth', 'called', ' kolej', '眯眯', '紧接着', '志愿服务队', '・・・・', '_calendar', ' kalt', ' appelée', ' usually', ' указы', ' ули', '問わず', 'Called', ' calendar', ' Tháng', 'calendar', ' Folg', 'unie']

### end-pass pursuit plain24: alias pass=False, returned=31

[' называется', 'رداد', ' preceded', 'ถัด', '...', ' usually', ' calendar', ' pove', ' regarded', ' наступ', '.', '/ap', '/', ' fools', '°', ' Cyber', '尾巴', '(name', '.getMonth', ' __________________', '眯眯', ' Numer', ' ули', ':', '—', '那个', ' Boxing', '担保', 'Y', ' in', ' qualit']

### end-pass gradient pursuit plain27: alias pass=False, returned=30

['.', ' called', '...', '____', '_Dec', ' Boxing', '展望', 'usually', ' Ро', '资料来源', ' Sap', 'ถัด', ' theaters', '/j', '动感', '的那个人', 'D', ' abbreviated', ' посл', '                               ', 'spy', '{}', ' ژ', '悟', ' nat', '新的一年', ' Δ', '\xa0', ' invariably', ':']

### end-pass gradient unit-dot matched plain27: alias pass=True, returned=30

[' December', ' called', '_Dec', 'December', 'called', ' называется', ' Januari', ' termed', ' Boxing', 'usually', ' appelé', ' usually', ' February', '\tJ', ' Ро', ' জান', 'Called', ' december', 'winter', 'February', '____', '称为', ' 일반적으로', ' typically', ' connu', '新的一年', ' معمول', ' __________________', 'typically', ' januari']

### end-pass pursuit plain27: alias pass=False, returned=30

[' called', '_Dec', '____', ' Boxing', '展望', '...', 'usually', ' Ро', '资料来源', '.', ' Sap', ' theaters', '的那个人', '悟', '/j', '                               ', '{}.', ' comput', '水仙', '?', ' посл', ':', 'v', ' preceded', '动感', '手が', ' Δ', '\xa0', ' Reis', 'D']

### Unmasked GP early-prefix

Consumed prefix: `'Fact: The capital of Japan is Tokyo.\nFact: The'`

[' Ge', ' population', 'Flag', ' Queen', ' CIA', ' Tokyo', ' Palace', ' hipp', ' airlines', ' Chin', ' Australians', '\\")', ' polo', ' Largest', ' mascot', ' Statue', '正式', '气候', '学制', '国歌', '最长的', '核电站', ' مُح', ' роди', ' Museo', ' rik', ' Cidade', ' Sungai', ' Budi', ' Pase', ' Hauptstadt', ' Eiff']

### Unmasked GP pre-clue

Consumed prefix: `'Fact: The capital of Japan is Tokyo.\nFact: The month immediately after the month containing'`

['\\<', ' April', ' January', ' Queen', ' Barack', ' Easter', ' Thanksgiving', ' Roma', '{name', ' Nombre', ' Phillip', ' dinosaurs', ' sushi', ' Leap', ' Oktober', '“.', ' JFK', ' birthdays', '日历', '奥运', '最多的', '倒数', '劳动节', '大地震', '核电站', ' hiz', ' Bulan', 'த்', ' Ponta', ' Ambas', ' Eiff', '本日']

## 1: Thursday

Input: `'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after Thor is'`

Cached output: `' Friday.\nQuestion: What day of'`

### end-pass gradient pursuit J24: alias pass=True, returned=32

['称为', ' Iceland', ' Thurs', ' Halloween', '通宵', '北欧', ' غد', ' вторник', '____', ' Erz', '劳动节', ' Ragnar', ' monday', ' Budi', ' Marte', ' День', ' Mardi', ' Sky', ' Kolej', ' Thursday', '«.', '公', ').\\', '개가', '")!=', '今天是', '...”', '自由', ' Sanc', ' Thanksgiving', '对应的', ' Forge']

### end-pass gradient unit-dot matched J24: alias pass=True, returned=32

[' Thursday', ' Tuesday', ' Monday', ' Wednesday', ' Saturday', ' Sunday', ' Thurs', ' Tues', ' Mondays', ' Thanksgiving', 'Monday', 'Tuesday', 'Thursday', ' Halloween', ' Saturdays', ' monday', ' Christmas', ' Sundays', ' weekdays', ' вторник', 'Saturday', ' weekend', 'Wednesday', '星期三', ' weekends', '星期四', ' Days', '星期日', ' Iceland', ' tomorrow', ' Oktober', ' Easter']

### end-pass pursuit J24: alias pass=True, returned=32

[' Thursday', '北欧', ' Halloween', '称为', ' غد', '».**', ' День', ' Erz', '__)', ' Marte', ' Sanc', '通宵', ' Ragnar', '公', '개가', ' Budi', '...”', ' oslo', ' Kolej', '完全不', '劳动节', '对应的', '自由', ' Cha', ' ausg', '<w', ' isti', 'MI', ' paro', ' Maxi', ' Toujours', ' Ruh']

### end-pass gradient pursuit plain24: alias pass=False, returned=30

['...', '.', ' called', 'always', ' preceded', '____', '<|im_end|>', ' الني', '开放', '금', ' a', '表面上', ' Boxing', '现代的', '除恶', '动感', ' NOT', '少儿', ']].', '诞辰', ' информ', '树林', ' Labor', ' eig', ' нор', ' lands', 'le', ' ', ' lucr', '4']

### end-pass gradient unit-dot matched plain24: alias pass=False, returned=30

[' called', 'always', 'called', ' preceded', ' الني', ' называется', ' always', '现代的', ' информ', '诞辰', ' disebut', ' Boxing', 'IVERY', '除恶', ' lucr', '动感', ' Always', ' Dici', 'Always', '的名称', ' مرتبط', '少儿', ' 반드시', '금', '・・・・', ' нор', 'lands', ' Dzie', ' Lapangan', '呼び']

### end-pass pursuit plain24: alias pass=False, returned=30

[' called', 'always', '...', ' الني', ' preceded', '____', ' Boxing', '现代的', '<|im_end|>', '开放', '금', '表面上', ' eig', '除恶', ' a', '动感', ' нор', ' Labor', 'le', '.', ' NOT', ']].', '树林', '少儿', ' информ', '阳极', ' ', ' lands', ' colleg', '/']

### end-pass gradient pursuit plain27: alias pass=True, returned=30

['...', ' ', ' среда', 'called', ':', ' Чет', ' Thursday', 'FR', ' wed', 'always', ' pagan', '금', ']].', '瑞典', 'Thứ', '除恶', '动感', '<|im_end|>', ' spawns', 'NOT', ' Å', ' Mon', '推断', '________', 'bru', '主管', '又快', '-S', '$', ' Energ']

### end-pass gradient unit-dot matched plain27: alias pass=True, returned=30

[' Thursday', ' Wednesday', 'Monday', ' среда', ' Monday', 'Thursday', 'Wednesday', ' Thurs', ' среду', ' Чет', 'called', ' Tuesday', 'Tuesday', 'uesday', ' Thu', ' Saturday', '_FR', ' called', ' Wed', ' среды', ' wed', 'FR', 'Saturday', ' Þ', 'always', 'Thứ', '星期三', '瑞典', ' امروز', ' aujourd']

### end-pass pursuit plain27: alias pass=True, returned=31

[' Thursday', '...', 'called', ' среда', 'FR', ' Þ', ' wed', ' Чет', ' Mon', '금', ' pagan', ' ', 'always', ']].', '<|im_end|>', '除恶', ':', 'NOT', ' Boxing', '瑞典', '开放', 'Thứ', ' inaugur', '____', '.', '动感', 'bru', ' a', '-S', '推断', 'rides']

### Unmasked GP early-prefix

Consumed prefix: `'Fact: The capital of Japan is Tokyo.\nFact: The'`

[' Ge', ' population', 'Flag', ' Queen', ' CIA', ' Tokyo', ' Palace', ' hipp', ' airlines', ' Chin', ' Australians', '\\")', ' polo', ' Largest', ' mascot', ' Statue', '正式', '气候', '学制', '国歌', '最长的', '核电站', ' مُح', ' роди', ' Museo', ' rik', ' Cidade', ' Sungai', ' Budi', ' Pase', ' Hauptstadt', ' Eiff']

### Unmasked GP pre-clue

Consumed prefix: `'Fact: The capital of Japan is Tokyo.\nFact: The day immediately after the weekday named after'`

[' Queen', ' Cool', ' Tokyo', ' Pizza', ' Abraham', 'μ', ' hipp', '\\"",', ' dinosaurs', 'birds', ' Julius', ' Pax', ' Tolkien', ' Madonna', ' JFK', '顾', '人名', '希腊', '这个人', '源自', '谐音', ' kota', ' Padre', ' Samb', ' Alba', ' santi', '?“', ' Mustafa', ' Lundi', ' Hauptstadt', ' dran', ' Eiff']

## 2: autumn

Input: `'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when deciduous trees shed their leaves is'`

Cached output: `' winter.\nHypothesis: The'`

### end-pass gradient pursuit J24: alias pass=False, returned=31

['紧接着', ' Tropical', ' primavera', '叫做', ' rainy', ' kalt', '__.', '<u', '供暖', '干旱', 'PEAT', ' begon', '夏季', ' Seasons', ' cic', '到来', '.»', ' Basketball', '樱花', '造林', ' vinter', '”…', '惰', 'BEGIN', '充满活力', '相反的', ' Ano', '。\\', ' ALWAYS', ' Oktober', ' hoor']

### end-pass gradient unit-dot matched J24: alias pass=False, returned=31

[' autumn', ' primavera', ' summer', '冬季', '春季', ' rainy', ' printemps', ' seasons', ' зим', '雨季', 'summer', ' vinter', '冬天', ' Autumn', '季节', '春天', '夏季', ' spring', ' drought', 'ฤดู', ' summers', ' hiver', '春暖花开', ' Mùa', ' invierno', ' seasonal', '旺季', ' inverno', ' Summer', '秋季', ' warmer']

### end-pass pursuit J24: alias pass=False, returned=31

['干旱', '__.', '叫做', '紧接着', ' Tropical', ' begon', '樱花', 'PEAT', 'Months', '暖气', '。）', '充满活力', '造林', '相反的', ' Festiv', '<u', ' GREEN', '到来', ' Quali', '”…', '通常是', ' cic', ' Autre', ' Basketball', ' ausg', ' Compre', ' kalt', 'BEGIN', '马超', ' Té', '«.']

### end-pass gradient pursuit plain24: alias pass=False, returned=32

['.', '...', ' called', ' наступ', "').'", ' invariably', 'spring', '.navigationBar', ' preceded', ' seasons', ' a', '____', '名', '到来', '干旱', '紧接着', '温暖的', ' agriculture', '鸟语', ' NOT', '短袖', '幕', '_the', ' forests', '休止', ' rigor', '/w', ' bore', '(s', '是一年', ' ', ' тури']

### end-pass gradient unit-dot matched plain24: alias pass=True, returned=32

[' preceded', ' наступ', ' называется', ' called', '紧接着', ' seasons', 'spring', ' invariably', '.navigationBar', ' termed', 'called', ' называют', ' forests', 'summer', '_the', '到来', ' agriculture', 'ฤดู', 'のことを', ' vinter', '温暖的', ' characterized', 'Spring', ' autumn', '鸟语', ' followed', ' springs', '是一年', '序幕', ' длится', ' bureaucracy', ' typically']

### end-pass pursuit plain24: alias pass=False, returned=31

[' preceded', '.', ' called', ' наступ', '...', ' invariably', ' seasons', 'spring', '.navigationBar', '_the', "').'", '干旱', '/w', '名', ':', ' NOT', ' agriculture', '____', '到来', ' bore', '鸟语', '暖', ' a', ' rigor', '(s', 'dic', ' ', '冲刺', '\r', '另一种', 'beg']

### end-pass gradient pursuit plain27: alias pass=True, returned=31

['Spring', ' summer', ' called', ' наступ', ' ', '...', '/', ':', ' characterized', '客机', '_prim', ' hotter', 'ใบ', ' invariably', '上传者', '(s', ' bore', 'unno', '<|im_end|>', '____', '另一种', '园艺', '降水', ' Crédit', '全文数据库', ' вес', 'nt', 'ớm', 'Aut', ' preceded', '紧接着']

### end-pass gradient unit-dot matched plain27: alias pass=True, returned=31

['Spring', 'spring', ' spring', ' Spring', ' summer', ' autumn', 'pring', ' springs', 'summer', ' verano', ' primavera', ' Summer', 'Summer', '春', '春天', ' printemps', '.spring', '春意', ' Autumn', ' called', ' наступ', ' verão', '\tSpring', ' vinter', '.Spring', '春季', 'ฤดู', ' summers', '春的', ' characterized', ' preceded']

### end-pass pursuit plain27: alias pass=True, returned=31

['Spring', ' called', ' summer', ' наступ', ' characterized', '...', '客机', 'ใบ', ' invariably', '(s', '上传者', ':', ' bore', '降水', ' hotter', '____', '园艺', 'unno', '_prim', '另一种', '/', '<|im_end|>', ' ', '全文数据库', ' Crédit', '紧接着', '.', 'nt', ' Boxing', 'Aut', '短袖']

### Unmasked GP early-prefix

Consumed prefix: `'Fact: The capital of Japan is Tokyo.\nFact: In'`

['struct', '\\u', 'uz', ' Japan', ' Jose', '_year', ' Italy', ' Queen', ' Metro', ' Padding', ' WWII', ' Canberra', ' Oktober', ' Cic', ' winters', 'habit', '排名', '中国共产党成立', '一般情况下', '西游记', '体育课', '抽水', ' Amerika', ' Pari', ' Muit', ' XXI', ' Sejak', '!“', ' demokrasi', ' Traf', ' Sushi', ' yık']

### Unmasked GP pre-clue

Consumed prefix: `'Fact: The capital of Japan is Tokyo.\nFact: In the Northern Hemisphere, the season immediately after the season when'`

['“', ' Christmas', ' Prince', ' Barack', ' GN', ' daylight', ' Maxim', '\\"",', ' whales', '()?.', ' rains', ' skiing', ' Avg', ' sunrise', '#/', ' Ramadan', ' Nicol', ' Hurricanes', ' glaciers', ' Comet', '太阳', '气温', '树叶', '大多数人', '是一年', '最长的', '常驻', ' наблюдается', '＿＿', ' Paling', ' begon', '札幌']

## 3: apple

Input: `'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit poisoned in the story of Snow White is'`

Cached output: `' red.\nHypothesis: The'`

### end-pass gradient pursuit J24: alias pass=False, returned=31

['红色', ' BLACK', '。\\', ' strawberries', ' Apfel', ' blau', '白雪', ' Candy', ' ined', '描述', '在德国', '|.', ' witches', ' Granny', ' Daisy', ' lipstick', ' ivory', ' Garlic', ' dran', '�', 'MC', ' LENG', '红颜', ' Toujours', ' cinnamon', '薇', ' Karls', '*/)', ' pink', '...”', ' Schaden']

### end-pass gradient unit-dot matched J24: alias pass=False, returned=31

[' pink', ' purple', '红色', ' strawberry', 'pink', ' красный', ' rossa', ' strawberries', ' rojo', 'purple', ' rouge', ' poisonous', ' blonde', ' rosso', ' berries', '(red', ' violet', ' orange', ' Purple', '红色的', ' blue', ' Pink', '粉红色', ' crimson', ' Strawberry', '_red', '紅色', ':red', ' rouges', ' yellow', '蓝色']

### end-pass pursuit J24: alias pass=False, returned=31

[' pink', ' strawberries', '红色', '。\\', ' BLACK', ' Apfel', '|.', '在德国', ' Granny', '描述', ' ined', ' Candy', '貂', ' Bái', 'MC', ' LENG', '*/)', 'FALSE', ' dran', ' güz', ' Alba', '薇', '··', ' Interna', ' Toujours', ' Sya', ' Erz', ' bbc', ' berüh', '�', 'ریان']

### end-pass gradient pursuit plain24: alias pass=False, returned=32

['.', '_', '红色', ' лечению', ' depicted', '全文数据库', ' organs', ' diam', ' a', '/w', '....', '史蒂', 'シャー', '�', ' poisoning', '红颜', ' утвер', '惨叫', 'MC', ' Бел', '<|im_end|>', ' spo', ' (', '_integration', ' iCloud', '_interfaces', 'Ford', '通常是', ' эксперти', 'u', ' berries', '守']

### end-pass gradient unit-dot matched plain24: alias pass=False, returned=32

['红颜', ':red', ' красный', '_red', ' лечению', '红色', '全文数据库', ' rojo', ' depicted', ' эксперти', ' Eventi', '红了', '빨', '史蒂', '_integration', ' poisoning', ' poisonous', ' 레드', '分享到朋友圈', ' czerw', '惨叫', '红红的', ' thème', ' červen', '粉红色', ' organs', '_cores', "').'", '眯眯', ' iCloud', ' jdbc', 'シャー']

### end-pass pursuit plain24: alias pass=False, returned=32

['红颜', ' лечению', ' depicted', '红色', ' organs', '....', '全文数据库', '_', ' poisoning', '/w', ' diam', '.', 'シャー', '史蒂', ' a', 'MC', ' утвер', ' бел', '�', '变电', '<|im_end|>', '_integration', 'Ford', 'related', ' (', '惨叫', ' berries', ' spo', 'B', '通常是', ' antagon', '拐']

### end-pass gradient pursuit plain27: alias pass=False, returned=30

[' apple', ' poisoning', '.', ':', ' depicted', '全文数据库', ' бел', ' rů', '...', ' упомина', '致命', ' лечению', '{}".', '\xa0\xa0\xa0\xa0', ' Plum', '<|im_end|>', ' Applies', ' cyan', '纯洁', '_RE', '应有尽有', ' (', 'M', '白雪', '红色', '这首歌', '的不是', '_', ' Johann', 'nw']

### end-pass gradient unit-dot matched plain27: alias pass=False, returned=30

[' poisoning', '_red', ' красный', '红色', ' rojo', ' poisonous', ':red', '紅色', ' červen', '紅', ' đỏ', '.red', ' apple', ' красного', '(red', '中毒', 'สีแดง', ' 레드', ' rouge', ' الأحمر', '红', ' vermelho', '红色的', '-red', 'Apple', '红了', ' apples', ' czerw', '红红的', '红线']

### end-pass pursuit plain27: alias pass=False, returned=31

['红色', ' apple', ' бел', ' depicted', ' rů', '全文数据库', '_RE', '...', ' cyan', ' упомина', ' Applies', ':', '<|im_end|>', '纯洁', ' Plum', '{}".', '\xa0\xa0\xa0\xa0', '.', ' deadly', '分红', 'M', '的不是', '应有尽有', ' a', ' spo', ' (', ' лечению', '_', '白雪', ' WW', '中毒']

### Unmasked GP early-prefix

Consumed prefix: `'Fact: The capital of Japan is Tokyo.\nFact: The'`

[' Ge', ' population', 'Flag', ' Queen', ' CIA', ' Tokyo', ' Palace', ' hipp', ' airlines', ' Chin', ' Australians', '\\")', ' polo', ' Largest', ' mascot', ' Statue', '正式', '气候', '学制', '国歌', '最长的', '核电站', ' مُح', ' роди', ' Museo', ' rik', ' Cidade', ' Sungai', ' Budi', ' Pase', ' Hauptstadt', ' Eiff']

### Unmasked GP pre-clue

Consumed prefix: `'Fact: The capital of Japan is Tokyo.\nFact: The usual color of the fruit'`

['?”', '「', ' salad', ' Basket', ' tomatoes', 'alsa', ' Fruit', ' banana', 'cake', ' pis', ' berries', '/apple', ' Scarlet', ' Zika', ' APPLE', ' Mango', ' Peanut', ' raspberry', '称为', '颜色', '脐', '的水果', '猕猴桃', '和蔬菜', '产自', ' Samb', ' Gour', ' Pob', ' spad', ' thun', ' رضا', ' Dior']

## 4: violin

Input: `'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument played by Sherlock Holmes is'`

Cached output: `' the woodwind family.\nQuestion:'`

### end-pass gradient pursuit J24: alias pass=True, returned=30

[' comprised', '。\\', ' violin', ' Brass', '«.', ' guitars', ' TREE', ' Piano', ' tamb', '目瞪口呆', '暖气', '相同的', ' مرتبط', ' kling', ' Rotary', ' Lamborghini', ' Polo', ' Cuc', ' trumpet', ' Serif', ' называется', ' Missing', ':x', ' berasal', '存在', ' berüh', 'เดียวกับ', ' flute', ' HARD', ' elephants']

### end-pass gradient unit-dot matched J24: alias pass=True, returned=30

[' violin', ' Piano', ' piano', ' guitar', ' Guitar', '钢琴', ' guitars', 'ดนตรี', ' percussion', ' flute', '乐器', ' comprised', ' trumpet', ' Mozart', '古筝', ' jazz', ' composed', ' musicians', ' Jazz', '古琴', ' auditory', ' музыка', '提琴', '的音乐', '小提琴', ' 음악', ' الموسيقى', ' instrumental', ' pian', '声乐']

### end-pass pursuit J24: alias pass=True, returned=31

[' violin', ' comprised', ' Brass', '。\\', ' مرتبط', ' Trees', '«.', ' عائلة', '目瞪口呆', ' Polo', ' tamb', ' SAME', '暖气', ' kling', ':X', ' γνω', ' Cuc', '存在', ' Lamborghini', ' Rotary', ' berüh', ' HARD', ' Austr', '缺失', '【', ' Serif', '锤子', ' dran', ':...', ' TECN', ' Columb']

### end-pass gradient pursuit plain24: alias pass=False, returned=31

[':', ' percussion', '_pipe', ' NOT', 'A', 'dataProvider', ' a', ' comprised', '吵闹', '很好奇', '<|im_end|>', "').'", ' auditor', ' descended', 'ходу', '错误的是', ' wood', '键盘', '_the', ' المكان', ' called', ' closely', '{{', ' ...', 'ro', '壮大', '................', ' violin', '/w', ' housed', ' ']

### end-pass gradient unit-dot matched plain24: alias pass=True, returned=31

[' comprised', ' percussion', ' descended', '_pipe', ' keluarga', ' المكان', '吵闹', '_family', 'っていました', 'dataProvider', ' responsabilità', ' violin', ' عائلة', ' vocals', "').'", '_the', ' dbo', ' العائلة', 'INVALID', ' خانواده', '很好奇', '_valid', ' verantwortlich', 'ходу', 'members', ' jsonResponse', '教体', ' guitars', '木有', ' ALSO', '键盘']

### end-pass pursuit plain24: alias pass=False, returned=30

[' comprised', ' percussion', ' NOT', 'dataProvider', ' called', '_the', '_pipe', ':', '<|im_end|>', ' closely', '吵闹', 'ходу', ' ...', ' auditor', 'A', ' wood', '错误的是', '键盘', "').'", '{{', 'ro', '.', ' descended', ' a', 'INVALID', '/', '很好奇', ' disb', '..', 'WK']

### end-pass gradient pursuit plain27: alias pass=False, returned=29

[':', ' violin', ' instruments', '键盘', ' percussion', ' ...', 'wind', ' a', ' uk', '_pipe', ' NOT', 'strings', '{{', ' called', ' descended', ' metais', ' sax', '没钱', ' brass', ' wood', ' trump', '类比', ' Clar', '=', '其中之一', 'W', ' c', ' basa', ' bears']

### end-pass gradient unit-dot matched plain27: alias pass=True, returned=29

[' violin', ' instruments', ' percussion', ' instrumentos', '键盘', ' piano', ' guitars', ' Instruments', ' flute', 'Viol', ' instrumental', ' Piano', ' trumpet', ' drums', ' sax', '小提琴', ' viol', 'keyboard', ' guitar', ' instrumentation', ' Viol', '-viol', ' инструментов', ' keyboards', '钢琴', ' viola', ' brass', '弦', ' instrumento']

### end-pass pursuit plain27: alias pass=False, returned=29

[' violin', ' instruments', '键盘', ' brass', ':', ' percussion', 'wind', ' called', '_pipe', ' NOT', ' ...', ' uk', 'STRING', '类比', ' a', '{{', ' descended', '壮大', '=', '没钱', '错误的是', ' wood', '忧心', 'Based', ' c', 'axes', '????', 'W', ' ']

### Unmasked GP early-prefix

Consumed prefix: `'Fact: The capital of Japan is Tokyo.\nFact: The'`

[' Ge', ' population', 'Flag', ' Queen', ' CIA', ' Tokyo', ' Palace', ' hipp', ' airlines', ' Chin', ' Australians', '\\")', ' polo', ' Largest', ' mascot', ' Statue', '正式', '气候', '学制', '国歌', '最长的', '核电站', ' مُح', ' роди', ' Museo', ' rik', ' Cidade', ' Sungai', ' Budi', ' Pase', ' Hauptstadt', ' Eiff']

### Unmasked GP pre-clue

Consumed prefix: `'Fact: The capital of Japan is Tokyo.\nFact: The orchestral family of the musical instrument'`

['\\"', ' category', '【', ' Pist', ' Trent', ' Piano', ' Musical', ' violin', ' cuck', '*/)', ' keyboards', ' Polo', ' bamb', ' percussion', ' TELE', '称为', '琉', '洗衣机', '古董', '家族的', '是一把', ' çe', '∙', ' terdiri', 'த்', ' kū', ' Cib', ' Suri', ' sınıf', ' INSTR', ' Lamborghini', ' klingt']

## 5: Hamlet

Input: `"Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose Danish prince asks 'To be, or not to be' is"`

Cached output: `' William Shakespeare.\nQuestion: Who wrote'`

### end-pass gradient pursuit J24: alias pass=False, returned=32

[' Shakespeare', ' playwright', '丹麦', 'unknown', '。\\', ' Robert', ' Claud', '__)', '«.', ' Charl', '毛', '虚构', '佚名', ' Snape', ' Budi', '鲁', ' Margaret', ' Jorn', 'MC', ' Urs', ' gondol', ' Died', ' Elias', '笔名', ' Manz', '为王', '写过', ' Laure', ' chamb', '?...', ' Mort', ' HAM']

### end-pass gradient unit-dot matched J24: alias pass=False, returned=32

[' Shakespeare', '莎士比亚', ' Robert', ' Elizabeth', ' playwright', ' Dickens', 'akespeare', ' Henry', ' Richard', ' Aristotle', ' John', ' Charles', ' Shakespe', ' Margaret', ' George', ' Tolkien', ' Henrik', ' Jane', ' Romeo', ' Edward', ' Christopher', ' Julius', ' Dumbledore', ' Harry', ' Stephen', ' Emily', ' Samuel', ' Matthew', ' novelist', ' Edmund', ' Daniel', ' Arthur']

### end-pass pursuit J24: alias pass=False, returned=32

[' Shakespeare', ' Robert', '丹麦', 'unknown', ' playwright', '。\\', ' Mort', '笔名', ' Jorn', ' Budi', '__)', ' mcc', '«.', '虚构', '毛', ' Claud', '(Func', ' Elis', ' gondol', '离世', ' Charl', '")!=', ' Manz', '吊', '冷气', '为王', ' Urs', ' chamb', '忙碌', '由高', ' Haf', '萧']

### end-pass gradient pursuit plain24: alias pass=False, returned=32

[' Shakespeare', ' credited', '____', '.', ' a', '虚构', ' corpus', '推理', ' unknown', ' canon', ' مسرح', ' breastfeeding', ' usually', '-', ' mortality', '除掉', '屠', '.......', ' Flem', 'Works', ' sco', '鲁', ' Haf', '迷雾', 'Ghost', ' Th', '满', ' dbo', '/w', ' <', '伟大的', ' ']

### end-pass gradient unit-dot matched plain24: alias pass=False, returned=32

[' Shakespeare', ' credited', '虚构', ' fictional', ' playwright', 'akespeare', ' fiction', ' مسرح', '莎士比亚', ' السير', '佚', ' corpus', ' breastfeeding', ' unbek', ' UNKNOWN', ' supposed', ' deceased', ' mortality', '丹麦', '推理', ' greve', '谋杀', '異なります', ' murdered', ' autoria', '伟大的', ' Unknown', '.......', ' unknown', ' tragedia', ' المسرح', 'usually']

### end-pass pursuit plain24: alias pass=False, returned=31

[' Shakespeare', ' credited', '虚构', '____', ' usually', ' mortality', ' unknown', ' corpus', '推理', ' canon', '屠', '...', ' Haf', ' a', 'Ghost', ' مسرح', '.', '鲁', '除掉', ' ', ' Th', ' السير', ' sco', 'Works', '/w', ' bullying', '佚', '港', '-', ' mad', '<|im_end|>']

### end-pass gradient pursuit plain27: alias pass=False, returned=31

[' Shakespeare', ' playwright', ' ', ' lago', ' credited', ':', ' shakes', '屠', ' unknown', 'ælde', ' dram', '舞台上', ' revenge', ' mortality', '丹麦', '____', ' Strat', ' eit', ' fiction', '迷雾', ' Prosper', ' Sen', '/w', '羽', '       ', '—', '搬', '飘香', '-', ' Hol', ' stabbed']

### end-pass gradient unit-dot matched plain27: alias pass=False, returned=31

[' Shakespeare', ' playwright', 'akespeare', '莎士比亚', ' مسرح', ' Shakespe', ' dramat', '舞台上', ' المسرح', ' credited', ' 셰', ' théâtre', ' teatro', ' شك', '-play', ' shakes', ' Plays', ' dram', ' plays', ' lago', '莎士', ' театра', '/play', ' teatrale', ' tragedies', '_play', ' theatrical', ' Théâtre', ' onstage', ' tragedia', 'akespe']

### end-pass pursuit plain27: alias pass=False, returned=31

[' Shakespeare', ' playwright', ' credited', ' lago', ' shakes', '屠', ' unknown', ':', ' mortality', '丹麦', '____', '舞台上', 'Ghost', ' ', ' dram', ' eit', '/w', ' Strat', '-', ' revenge', ' topping', ' Sen', '       ', 'ælde', '.', '搬', ' thou', '5', ' Hol', '迷雾', 'Pub']

### Unmasked GP early-prefix

Consumed prefix: `'Fact: The capital of Japan is Tokyo.\nFact: The'`

[' Ge', ' population', 'Flag', ' Queen', ' CIA', ' Tokyo', ' Palace', ' hipp', ' airlines', ' Chin', ' Australians', '\\")', ' polo', ' Largest', ' mascot', ' Statue', '正式', '气候', '学制', '国歌', '最长的', '核电站', ' مُح', ' роди', ' Museo', ' rik', ' Cidade', ' Sungai', ' Budi', ' Pase', ' Hauptstadt', ' Eiff']

### Unmasked GP pre-clue

Consumed prefix: `'Fact: The capital of Japan is Tokyo.\nFact: The author of the play whose'`

[' title', ' lyrics', 'Contains', ' Castle', ' Shakespeare', ' protagonist', '\\"",', ' Spo', 'MV', ' Edmund', '":"\'', ' ilk', '_____', ' premiered', ' mascot', ' screenplay', ' Jas', ' actresses', ' Staten', '结局', '灵感', '主题是', ' Pia', ' wund', ' Fuer', '■■', ' cujo', ' verdens', '?“', ' مقت', ' adı', ' siedz']

## 6: hydrogen

Input: `'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the lightest chemical element is'`

Cached output: `' a gas.\nHypothesis:'`

### end-pass gradient pursuit J24: alias pass=False, returned=30

['液态', ' jelly', '固体', '«.', ' Lightweight', ' bombe', '通常为', ' Gas', ' vapor', '破冰', '。\\', '？”', ' Miz', ' eit', ' berüh', ' Homo', ' Ruh', '青松', ' NOTA', ' Ging', '__.', '不断地', ':...', ' unk', ' translucent', ' Stanis', '各不相同', '桌子', ' LV', ' физического']

### end-pass gradient unit-dot matched J24: alias pass=False, returned=30

['液态', ' liquids', 'liquid', ' liquid', ' vapor', ' Liquid', ' lique', ' Vapor', '液体', ' gases', ' liquide', '常温', '气体', ' liquido', 'Liquid', '的气体', ' Liqu', '液化', ' fluids', ' vap', '_gas', '固态', ' líquido', ' Gas', ' gas', '固体', ' magma', ' жидкости', ' solids', 'gas']

### end-pass pursuit J24: alias pass=False, returned=31

['液态', ' vapor', '__.', ' Lightweight', ' invariably', ' jelly', ' Homo', '破冰', ' Ruh', ' STO', '各不相同', '？”', '固体', ' bombe', ' Ging', '«.', ' eit', ' Pizza', '青松', '猜想', ':...', '桌子', ' Samb', '<u', ' Emas', ' abhängig', ' анги', ' Unknown', ' лёг', ' mdi', ' berüh']

### end-pass gradient pursuit plain24: alias pass=False, returned=31

['...', '.', 'สถานะ', '液态', 'usually', ' not', ' exhibited', '<|im_end|>', ' quyển', 'फल', 'graph', '\xa0', '的气体', ' kwest', '_', '�', '英文名称', '_predict', 'ั', ' лёг', 'โปร่ง', '各不相同', ' staring', ' الحالة', ' donating', '/w', ' namely', ' known', '破冰', ' unle', '观光']

### end-pass gradient unit-dot matched plain24: alias pass=False, returned=31

['สถานะ', ' الحالة', '液态', 'usually', '固态', '常温', ' liquids', ' состояния', '的状态', '................', '的气体', '.......', '状态的', ' usually', ' 항상', '工作状态', '_state', '.....', '[state', '固体', ' estado', 'फल', '........', ' quyển', ' состояние', ' invariably', ' gases', ' газо', ' состоянию', '液体', 'ั']

### end-pass pursuit plain24: alias pass=False, returned=31

['สถานะ', '...', '液态', 'usually', ' exhibited', 'फल', ' not', 'graph', ' quyển', ':', ' something', '卜', '吸气', ' dibattito', ' kwest', '_pred', '<|im_end|>', '常温', '\xa0', ' namely', ' unle', '�', '.', '_', '/w', '观光', '................', 'โปร่ง', ',', ' представляет', 'ั']

### end-pass gradient pursuit plain27: alias pass=False, returned=31

[' gas', ':', '固态', '...', 'usually', ' liquids', ' газо', ' dibattito', '气', ' rắn', '_predict', ' الحالة', ' quyển', ' determined', 'graph', '<|im_end|>', '附录', '(states', '(g', '其中之一', '\xa0', ' NOT', ' bothering', ' __________________', '熔点', '�', ' what', '$', '                                 ', '/w', '吸气']

### end-pass gradient unit-dot matched plain27: alias pass=False, returned=31

[' gas', ' gases', '气体', '的气体', '气体的', ' Gas', '_gas', 'gas', 'Gas', ' газ', ' газа', '固态', ' газо', '固体', '气', ' gás', ' GAS', ' الغاز', ' liquids', 'liquid', '液态', 'ก๊าซ', ' liquid', ' solids', '氣體', 'solid', ' газов', '液体', ' غاز', ' rắn', ' گاز']

### end-pass pursuit plain27: alias pass=False, returned=31

[' gas', '固态', 'usually', '...', ' liquids', ' الحالة', ':', ' dibattito', ' determined', ' __________________', '(g', '_predict', '附录', ' what', '�', '/w', ' NOT', 'blogs', ' boils', '<|im_end|>', '\xa0', 'graph', '其中之一', ' paperback', '$', ' gaze', '吸气', ' -', 'PAR', ' Britann', ' errone']

### Unmasked GP early-prefix

Consumed prefix: `'Fact: The capital of Japan is Tokyo.\nFact: The'`

[' Ge', ' population', 'Flag', ' Queen', ' CIA', ' Tokyo', ' Palace', ' hipp', ' airlines', ' Chin', ' Australians', '\\")', ' polo', ' Largest', ' mascot', ' Statue', '正式', '气候', '学制', '国歌', '最长的', '核电站', ' مُح', ' роди', ' Museo', ' rik', ' Cidade', ' Sungai', ' Budi', ' Pase', ' Hauptstadt', ' Eiff']

### Unmasked GP pre-clue

Consumed prefix: `'Fact: The capital of Japan is Tokyo.\nFact: The physical state at room temperature of the'`

['state', ' city', 'α', ' substance', ' Mol', ' hottest', ' Liquid', ' Mineral', ' jelly', ' MED', '\\")', ' Kurds', ' unicorn', ' Largest', ' mascot', ' Statue', ' Belize', ' Pasta', '化学', '氯乙烯', '产物', '溶解', '国旗', '的物品', '最常用的', ' rik', ' pala', ' Sungai', ' Hauptstadt', ' cuire', ' kling', ' Eiff']

## 7: triangle

Input: `'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape formed by joining three non-collinear points is'`

Cached output: `' 3.\nFact: The number'`

### end-pass gradient pursuit J24: alias pass=True, returned=32

[' ALWAYS', '固定的', ' drie', ' Polygon', '等于', '(number', '取决于', '.\\', ' triangle', '<u', '«.', ' kaki', ' indé', ':...', '不少于', ' Bia', '二十三', '五角', ' Euler', ' 다양', '_ge', ' Mystic', '_edges', ' Undefined', '必然会', ' NOTA', ' Sasha', ' chiam', ' Js', '要么是', ' taky', '.|']

### end-pass gradient unit-dot matched J24: alias pass=True, returned=32

[' ALWAYS', ' triangle', 'always', ' triangles', ' always', ' polygon', '三角形的', '三角形', ' polygons', ' triangular', '(number', ' دائمًا', ' invariably', ' zawsze', ' دائماً', ' triang', ' Always', ' selalu', 'Always', ' 항상', ' Triangle', ' vždy', ' beträgt', ' всегда', '必ず', 'Triangle', '总是', 'Triangles', ':number', 'triangle', ' треуго', ' Polygon']

### end-pass pursuit J24: alias pass=True, returned=32

[' ALWAYS', ' triangle', '(number', '固定的', '等于', '.\\', ' Polygon', ' drie', '取决于', ' Undefined', '.addEdge', ':...', ' Bia', '_ge', ' kaki', '«.', ' 다양', ' Sasha', '至少有', '愚', ' Evang', '>|', '六', ' Spor', '满脸', ' kū', ' Mosc', '鲁班', ' indé', 'zf', ' isti', ' Bake']

### end-pass gradient pursuit plain24: alias pass=False, returned=31

['always', '...', 'फल', '三角形的', ' indetermin', '3', 'aner', ' greater', 'n', ' exactly', ' <', '<|im_end|>', ':number', '所大学', ':', '脸的', ' hereby', ' polygons', '/is', '異なります', '除非', '____', ' depend', '四个自信', '{}".', ' Madame', '偶', '恒心', ' uniquely', ' Proj', ' Lob']

### end-pass gradient unit-dot matched plain24: alias pass=True, returned=31

['always', ' always', '三角形的', ' triangles', ' Always', ' selalu', 'Always', 'फल', ' zawsze', ' ALWAYS', ' polygons', ' indetermin', ' دائمًا', ' invariably', ' всегда', '所大学', ' دائماً', ' 항상', ' Siempre', ' greater', '必ず', '.........', '(number', 'usually', ' зависеть', ' uniquely', 'ilateral', ' exactly', '異なります', '永远不会', 'depends']

### end-pass pursuit plain24: alias pass=False, returned=31

['always', '三角形的', ' indetermin', ' greater', ' exactly', '____', '...', 'फल', 'aner', ':number', 'FACE', '取决于', ' <', 'n', '<|im_end|>', '{}".', '恒心', ' waved', ' uniquely', ':', '3', 'ฤษฎ', '在这种情况下', '/is', ' liable', '幻', '..', ' Lob', ' Gegen', '所大学', 'ge']

### end-pass gradient pursuit plain27: alias pass=False, returned=29

[' always', ' triangles', ':', '3', '____', ' determined', '(n', ' exactly', '依赖于', ' greater', '{}".', ' ?.', 'aner', ' impres', ' gonna', 'फल', 'ilateral', '.edges', '.....', '<|im_end|>', ' называется', 'さまざま', ' Anzahl', '除非', 'poly', '恒心', '固定', '所大学', '\xa0']

### end-pass gradient unit-dot matched plain27: alias pass=True, returned=29

[' always', 'always', ' triangles', '三角形的', ' Always', 'Always', ' triangle', '三角形', ' всегда', ' sempre', ' 항상', ' selalu', ' ALWAYS', ' zawsze', ' دائمًا', '常に', ' alltid', '总是', ' altijd', 'Triangle', 'triangle', ' luôn', ' треуго', ' siempre', ' toujours', '必ず', ' determined', ' Всегда', ' invariably']

### end-pass pursuit plain27: alias pass=False, returned=29

[' always', ' triangles', ' determined', '____', 'ilateral', '依赖于', ' ?.', '(n', ' exactly', ' impres', ' Anzahl', '...', ' greater', 'aner', ':', ' gonna', '{}".', '.edges', 'फल', '恒心', '除非', '3', '<|im_end|>', '\xa0', 'poly', ' называется', 'S', 'vor', '固定']

### Unmasked GP early-prefix

Consumed prefix: `'Fact: The capital of Japan is Tokyo.\nFact: The'`

[' Ge', ' population', 'Flag', ' Queen', ' CIA', ' Tokyo', ' Palace', ' hipp', ' airlines', ' Chin', ' Australians', '\\")', ' polo', ' Largest', ' mascot', ' Statue', '正式', '气候', '学制', '国歌', '最长的', '核电站', ' مُح', ' роди', ' Museo', ' rik', ' Cidade', ' Sungai', ' Budi', ' Pase', ' Hauptstadt', ' Eiff']

### Unmasked GP pre-clue

Consumed prefix: `'Fact: The capital of Japan is Tokyo.\nFact: The number of sides of the shape'`

['“', ' formed', '.svg', ' Shape', ' QUE', ' Pizza', ' Triangle', '/angular', ' pictured', 'iran', 'ABCDE', ' Leonardo', ' polygons', '"is', ' Morph', ' RECT', '.Circle', ' Rosie', ' bola', '描述', '在水', '太极', '以下的', '叫做', ' رئ', '♡', ' Giardia', ' приведен', ' pepe', ' Luka', ' Eiff', '多いです']
