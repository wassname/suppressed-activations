# Delayed readout

Config: patch residual L23 at the last 4 prompt positions. The
detector reads L23, L25, and L32. The Qwen template starts the
assistant thinking section in the input. Later states consume the same forced thought tokens with
no additional patch.

Forced continuation (`repr`):

```python
'Thinking Process:\n\n'
```

| condition   | state    | readout                                                                                   | source share   | donor share   |
|:------------|:---------|:------------------------------------------------------------------------------------------|:---------------|:--------------|
| base        | prompt   | [' DEM', '要先', '先把', '遨', 'onsor', 'ემ', '客人的', ' XM']                                    | 0.0362         | 0.0386        |
| base        | forced 1 | [' epidemi', 'æ', 'çon', ' histograms', ' пожалуй', '规章制度', ' sessions', 'ê']             | 0.0733         | 0.0676        |
| base        | forced 2 | [' Sullivan', ' 어울', 'olics', ' sembilan', ' cia', ' инвестиции', 'hrs', '.getUser']      | 0.0530         | 0.0496        |
| base        | forced 3 | ['MAL', ':[[', ' Elli', 'Paint', '姥爷', '_PICTURE', ' FALL', ' puerto']                    | 0.0690         | 0.0779        |
| base        | forced 4 | [' kennen', ' initial', ' Ej', ' Lig', ' Engineering', ' Meng', ' linguistic', ' legal']  | 0.0791         | 0.0784        |
| replace_C1  | prompt   | [' DEM', 'ittä', '先把', '要先', '客人的', '遨', 'gade', ' XM']                                   | 0.0363         | 0.0386        |
| replace_C1  | forced 1 | [' epidemi', 'æ', 'çon', ' histograms', ' пожалуй', '规章制度', ' sessions', 'UID']           | 0.0726         | 0.0673        |
| replace_C1  | forced 2 | [' Sullivan', ' 어울', 'olics', ' sembilan', ' инвестиции', ' cia', 'hrs', '.getUser']      | 0.0534         | 0.0496        |
| replace_C1  | forced 3 | [':[[', 'MAL', ' Elli', '姥爷', '_PICTURE', ' FALL', ' puerto', 'Paint']                    | 0.0693         | 0.0782        |
| replace_C1  | forced 4 | [' kennen', ' initial', ' Engineering', ' Ej', ' Meng', ' Lig', ' linguistic', ' Excell'] | 0.0792         | 0.0782        |
| replace_C4  | prompt   | ['ittä', '客人的', 'gade', '先把', ' DEM', '要先', '遨', ' XM']                                   | 0.0409         | 0.0385        |
| replace_C4  | forced 1 | [' epidemi', 'æ', 'çon', ' histograms', ' пожалуй', '规章制度', 'ê', 'UID']                   | 0.0716         | 0.0664        |
| replace_C4  | forced 2 | [' Sullivan', ' 어울', 'olics', ' sembilan', ' инвестиции', ' cia', 'hrs', '.getUser']      | 0.0539         | 0.0499        |
| replace_C4  | forced 3 | ['MAL', ':[[', ' Elli', '姥爷', ' FALL', '_PICTURE', ' puerto', 'Paint']                    | 0.0690         | 0.0782        |
| replace_C4  | forced 4 | [' kennen', ' initial', ' Lig', ' Ej', ' Engineering', ' Meng', ' linguistic', ' legal']  | 0.0780         | 0.0770        |

TODO validate: a donor-like delayed readout requires a change in the selected rows that persists
after identical continuation tokens. Projection shares alone do not establish semantic transfer.

Raw artifact: `result.json`.

-- Codex/gpt-5
