# History of towns

**The `towns.csv` file contains mainly links between previous and current towns and their INSEE codes.**

Beware that the same INSEE code is recycled when towns are renamed and (sometimes!) merged.


## Columns

* `ID`: This is the hopefully unique combination of `INSEE_CODE` + `START_DATE` + `END_DATE`.
* `INSEE_CODE`: The INSEE code for the given town.
* `NAME`: The name of the town, including the article (`Le `, `La `, `L'` etc).
* `START_DATE`: The effective start date for the given `NAME` + `INSEE_CODE`.
* `END_DATE`: The effective end date for the given `NAME` + `INSEE_CODE`.
* `SUCCESSORS`: List of IDs separated by semicolons which are successors of the current `ID`. Default is an empty string.
* `ANCESTORS`: List of IDs separated by semicolons which are ancestors of the current `ID`. Default is an empty string.
* `POPULATION`: The population as of 2013, for merged towns since then it is the computed sum. In case of towns “mortes pour la France”, the population is set to `0` otherwise fallback on `NULL` to reflect that it is intentional.

Regarding dates, the initial date has been set as `1942-01-01` given that the first date in historical data is `1942-08-01`. Arbitrarily, the far future end date has been set to `9999-01-01`.


## Format

This is a regular CSV file with value separated by commas and a header line with previously described column names.

The `towns_head.csv` file contains the first 100 lines of the generated file for an easy preview within Github if you click on it.


## Examples

### Rename

```
010041955-03-319999-01-01,01004,Ambérieu-en-Bugey,1955-03-31,9999-01-01,,010041942-01-011955-03-31,14359,0
010041942-01-011955-03-31,01004,Ambérieu,1942-01-01,1955-03-31,010041955-03-319999-01-01,,NULL,100
```

As of `1955-03-31`, the town of `Ambérieu` has been renamed to `Ambérieu-en-Bugey`, keeping the same INSEE code (`01004`). It has a current population of `14359` inhabitants and an unknown previous population (`NULL`).


### Merge

```
010152016-01-019999-01-01,01015,Arboys en Bugey,2016-01-01,9999-01-01,,010151942-01-012016-01-01;013401942-01-012016-01-01,631,0
010151942-01-012016-01-01,01015,Arbignieu,1942-01-01,2016-01-01,010152016-01-019999-01-01,,495,331
013401942-01-012016-01-01,01340,Saint-Bois,1942-01-01,2016-01-01,010152016-01-019999-01-01,,136,331
```

As of `2016-01-01`, towns of `Arbignieu` and `Saint-Bois` has been merged to `Arboys en Bugey`, keeping the INSEE code of `Arbignieu` (`01015`). It has a computed (sum) population of `631` inhabitants.


### Move

```
2A0011976-01-019999-01-01,2A001,Afa,1976-01-01,9999-01-01,,200011942-01-011976-01-01,2955,0
200011942-01-011976-01-01,20001,Afa,1942-01-01,1976-01-01,2A0011976-01-019999-01-01,,NULL,410

```

As of `1976-01-01`, town of `Afa` has moved from `20001` to `2A001` (actually the code name for the county has changed but you get the point).

