# History of towns

**The `towns.csv` file contains mainly links between previous and current towns and their INSEE codes.**

Beware that the same INSEE code is recycled when towns are renamed and (sometimes!) merged.


## Columns

* `DIRECTION`: Either `--`, `<-` or `->` if the town is unchanged, has been renamed or merged respectively.
* `INSEE_CODE`: The INSEE code for the given town.
* `NAME`: The name of the town, including the article (`Le `, `La `, `L'` etc).
* `START_DATE`: The effective start date for the given `NAME` + `INSEE_CODE`.
* `END_DATE`: The effective end date for the given `NAME` + `INSEE_CODE`.
* `POPULATION`: The population as of 2013, for merged towns since then it is the computed sum. In case of towns “mortes pour la France”, the population is set to `0` otherwise fallback on `NULL` to reflect that it is intentional.

Regarding dates, the initial date has been set as `1943-01-01` given that the first date in historical data is `1943-08-12`. Arbitrarily, the far future end date has been set to `2020-01-01`.


## Format

This is a regular CSV file with value separated by commas and a header line with previously described column names.

The `towns_head.csv` file contains the first 100 lines of the generated file for an easy preview within Github if you click on it.


## Examples

### Rename

```
--,01004,Ambérieu-en-Bugey,1955-03-31,2020-01-01,14359
<-,01004,Ambérieu,1943-01-01,1955-03-31,NULL
```

As of `1955-03-31`, the town of `Ambérieu` has been renamed to `Ambérieu-en-Bugey`, keeping the same INSEE code (`01004`). It has a current population of `14359` inhabitants and an unknown previous population (`NULL`).


### Merge

```
--,01015,Arboys en Bugey,2016-01-01,2020-01-01,631
<-,01015,Arbignieu,1943-01-01,2016-01-01,495
->,01340,Saint-Bois,1943-01-01,2016-01-01,136
```

As of `2016-01-01`, towns of `Arbignieu` and `Saint-Bois` has been merged to `Arboys en Bugey`, keeping the INSEE code of `Arbignieu` (`01015`). It has a computed (sum) population of `631` inhabitants.

