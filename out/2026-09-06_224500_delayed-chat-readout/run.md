# Delayed readout

Config: patch residual L23 at the last 4 prompt positions. The
detector reads L23, L25, and L32. Later states consume the same
forced tokens with no additional patch.

Forced continuation (`repr`):

```python
'8<|im_end|>\n<|endoftext|>'
```

| condition   | state    | readout                                                                        | source share   | donor share   |
|:------------|:---------|:-------------------------------------------------------------------------------|:---------------|:--------------|
| base        | prompt   | [' PDO', ' laba', '爬到', ' Silk', ' embroidery', ' WEB', '前车', '-web']          | 0.0802         | 0.0504        |
| base        | forced 1 | [' فول', '居委会', ' MANUAL', 'вши', ' dokon', '.setAuto', 'MBER', ' Deployment'] | 0.0570         | 0.0259        |
| base        | forced 2 | [' коде', '_REAL', ' официаль', ' لاست', '厚的', ' COMUN', '证明文件', 'UCCIÓN']     | 0.0380         | 0.0522        |
| base        | forced 3 | ['ান্ত', ' nacht', '认证的', '抵押贷款', 'みた', 'ANDROID', '毅然', ' Пита']              | 0.0247         | 0.0409        |
| base        | forced 4 | ['闘', '_small', ' Imper', 'witz', ' Luigi', '\')">', '缰', ' hut']              | 0.0498         | 0.0593        |
| replace_C1  | prompt   | ['前车', ' PDO', ' embroidery', ' bite', '刺绣', ' Ủy', ' 장치', ' عمران']           | 0.0802         | 0.0504        |
| replace_C1  | forced 1 | [' فول', '居委会', 'вши', ' MANUAL', ' dokon', '.setAuto', 'MBER', ' Deployment'] | 0.0570         | 0.0259        |
| replace_C1  | forced 2 | [' коде', '_REAL', ' официаль', ' لاست', ' COMUN', '证明文件', '_Min', '厚的']       | 0.0380         | 0.0522        |
| replace_C1  | forced 3 | ['ান্ত', ' nacht', '抵押贷款', '认证的', 'みた', 'ANDROID', '毅然', ' Пита']              | 0.0247         | 0.0409        |
| replace_C1  | forced 4 | ['闘', '_small', ' Imper', 'witz', ' Luigi', '\')">', '缰', ' hut']              | 0.0498         | 0.0593        |
| replace_C4  | prompt   | ['前车', ' unleashed', ' Sirius', '수의', ' พัน', '수에', ' PDO', '狗粮']              | 0.0802         | 0.0504        |
| replace_C4  | forced 1 | [' فول', 'вши', ' dokon', ' Vater', ' MANUAL', '居委会', ' setzen', ' učink']     | 0.0570         | 0.0259        |
| replace_C4  | forced 2 | [' коде', '_REAL', ' официаль', ' COMUN', '证明文件', '_Min', 'UCCIÓN', ' لاست']   | 0.0380         | 0.0522        |
| replace_C4  | forced 3 | [' nacht', 'ান্ত', '抵押贷款', '认证的', '毅然', 'みた', 'yb', ' Пита']                   | 0.0247         | 0.0409        |
| replace_C4  | forced 4 | ['闘', '_small', ' Imper', 'witz', ' Luigi', '\')">', '缰', '过多的']               | 0.0498         | 0.0593        |

TODO validate: a donor-like delayed readout requires a change in the selected rows that persists
after identical continuation tokens. Projection shares alone do not establish semantic transfer.

Raw artifact: `result.json`.

-- Codex/gpt-5
