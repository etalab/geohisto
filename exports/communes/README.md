# History of towns

**The `communes.csv` file contains mainly links between previous and current towns and their INSEE codes.**

Beware that the same INSEE code is recycled when towns are renamed and (sometimes!) merged.


## Columns

* `id`: This is the unique combination of `COM` + `insee_code` + `@` + `start_date` (using ISO format `YYYY-MM-DD`).
* `insee_code`: The INSEE code for the given town which is county code (two-letters digit except for Corsica) + town code (3-letters digits). As a result it's a 5-letters string.
* `start_datetime`: The effective start date + time for the current `id` using ISO format (`YYYY-MM-DD HH:MM:SS`).
* `end_datetime`: The effective end date + time for the current `id` using ISO format (`YYYY-MM-DD HH:MM:SS`).
* `name`: The name of the town, including the article (`Le `, `La `, `L'` etc).
* `successors`: List of `id`s separated by semicolons which are successors of the current `id`. Default is an empty string.
* `ancestors`: List of `id`s separated by semicolons which are ancestors of the current `id`. Default is an empty string.
* `parents`: List of `id`s separated by semicolons of the parents for that town, as found in `counties.csv`.
* `population`: The population as of 2013, for merged towns since then it is the computed sum. In case of towns “mortes pour la France”, the population is set to `0` otherwise fallback on `NULL` to reflect that it is intentional.
* `insee_modification`: Indicate the [INSEE modification](https://www.insee.fr/fr/information/2114773#mod) performed on the town.

Regarding dates, the initial date + time has been set as `1942-01-01 00:00:00` given that the first date in historical data is `1942-08-01`. Arbitrarily, the far future end date has been set to `9999-12-31 23:59:59`.


## Format

This is a regular CSV file with value separated by commas and a header line with previously described column names.

The `communes_head.csv` file contains the first 100 lines of the generated file for an easy preview within Github if you click on it.

The `communes_{date}.csv` files contain towns valid at the given date.


## Examples

### Rename

```
COM01004@1942-01-01,01004,Ambérieu,1942-01-01 00:00:00,1955-03-30 23:59:59,COM01004@1955-03-31,,NULL,100
COM01004@1955-03-31,01004,Ambérieu-en-Bugey,1955-03-31 00:00:00,9999-12-31 23:59:59,,COM01004@1942-01-01,14359,0
```

As of `1955-03-31`, the town of `Ambérieu` has been renamed to `Ambérieu-en-Bugey`, keeping the same INSEE code (`01004`). It has a current population of `14359` inhabitants and an unknown previous population (`NULL`).


### Merge

```
COM01015@2016-01-01,01015,Arboys en Bugey,2016-01-01 00:00:00,9999-12-31 23:59:59,,COM01015@1942-01-01;COM01340@1942-01-01,631,0
COM01015@1942-01-01,01015,Arbignieu,1942-01-01 00:00:00,2015-12-31 23:59:59,COM01015@2016-01-01,,495,331
COM01340@1942-01-01,01340,Saint-Bois,1942-01-01 00:00:00,2015-12-31 23:59:59,COM01015@2016-01-01,,136,331
```

As of `2016-01-01`, towns of `Arbignieu` and `Saint-Bois` has been merged to `Arboys en Bugey`, keeping the INSEE code of `Arbignieu` (`01015`). It has a computed (sum) population of `631` inhabitants.


### Move

```
COM20001@1942-01-01,20001,Afa,1942-01-01 00:00:00,1975-12-31 23:59:59,COM2A001@1976-01-01,,NULL,410
COM2A001@1976-01-01,2A001,Afa,1976-01-01 00:00:00,9999-12-31 23:59:59,,COM20001@1942-01-01,2955,0
```

As of `1976-01-01`, town of `Afa` has moved from `20001` to `2A001` (actually the code name for the county has changed but you get the point).
