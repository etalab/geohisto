# History of towns

**The `towns.csv` file contains mainly links between previous and current towns and their INSEE codes.**

Beware that the same INSEE code is recycled when towns are renamed and (sometimes!) merged.


## Columns

* `id`: This is the hopefully unique combination of `insee_code` + `@` `start_date`.
* `insee_code`: The INSEE code for the given town.
* `name`: The name of the town, including the article (`Le `, `La `, `L'` etc).
* `start_datetime`: The effective start date + time for the given `name` + `insee_code`.
* `end_datetime`: The effective end date + time for the given `name` + `insee_code`.
* `successors`: List of IDs separated by semicolons which are successors of the current `id`. Default is an empty string.
* `ancestors`: List of IDs separated by semicolons which are ancestors of the current `id`. Default is an empty string.
* `population`: The population as of 2013, for merged towns since then it is the computed sum. In case of towns “mortes pour la France”, the population is set to `0` otherwise fallback on `NULL` to reflect that it is intentional.
* `insee_modification`: Indicate the [INSEE modification](http://www.insee.fr/fr/methodes/nomenclatures/cog/documentation.asp?page=telechargement/2016/doc/doc_variables.htm#mod) performed on the town.

Regarding dates, the initial date + time has been set as `1942-01-01 00:00:00` given that the first date in historical data is `1942-08-01`. Arbitrarily, the far future end date has been set to `9999-12-31 23:59:59`.


## Format

This is a regular CSV file with value separated by commas and a header line with previously described column names.

The `towns_head.csv` file contains the first 100 lines of the generated file for an easy preview within Github if you click on it.


## Examples

### Rename

```
01004@1942-01-01,01004,Ambérieu,1942-01-01 00:00:00,1955-03-30 23:59:59,01004@1955-03-31,,NULL,100
01004@1955-03-31,01004,Ambérieu-en-Bugey,1955-03-31 00:00:00,9999-12-31 23:59:59,,01004@1942-01-01,14359,0
```

As of `1955-03-31`, the town of `Ambérieu` has been renamed to `Ambérieu-en-Bugey`, keeping the same INSEE code (`01004`). It has a current population of `14359` inhabitants and an unknown previous population (`NULL`).


### Merge

```
01015@2016-01-01,01015,Arboys en Bugey,2016-01-01 00:00:00,9999-12-31 23:59:59,,01015@1942-01-01;01340@1942-01-01,631,0
01015@1942-01-01,01015,Arbignieu,1942-01-01 00:00:00,2015-12-31 23:59:59,01015@2016-01-01,,495,331
01340@1942-01-01,01340,Saint-Bois,1942-01-01 00:00:00,2015-12-31 23:59:59,01015@2016-01-01,,136,331
```

As of `2016-01-01`, towns of `Arbignieu` and `Saint-Bois` has been merged to `Arboys en Bugey`, keeping the INSEE code of `Arbignieu` (`01015`). It has a computed (sum) population of `631` inhabitants.


### Move

```
20001@1942-01-01,20001,Afa,1942-01-01 00:00:00,1975-12-31 23:59:59,2A001@1976-01-01,,NULL,410
2A001@1976-01-01,2A001,Afa,1976-01-01 00:00:00,9999-12-31 23:59:59,,20001@1942-01-01,2955,0
```

As of `1976-01-01`, town of `Afa` has moved from `20001` to `2A001` (actually the code name for the county has changed but you get the point).
