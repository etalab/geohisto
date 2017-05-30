# History of counties (départements)

**The `departements.csv` file contains history for counties since 1790-03-04.**

The initial date (1860-07-01) has been chosen given that:

* we do not want to deal with the complexity of the Napoleonian period with a lot of annexation of european territories
* we want stable INSEE codes and as such the creation of Alpes-Maritimes as of 1860-06-23 and Haute-Savoie/Savoie as of 1860-06-15 are required

Recent (since 1946-03-19) overseas counties are listed too with their respective regions.


## Sources

* https://fr.wikipedia.org/wiki/Histoire_des_d%C3%A9partements_fran%C3%A7ais
* https://fr.wikipedia.org/wiki/Liste_des_d%C3%A9partements_fran%C3%A7ais
* https://fr.wikipedia.org/wiki/Liste_des_d%C3%A9partements_fran%C3%A7ais_de_1811


## Columns

* `id`: This is a [GeoID](https://github.com/etalab/geoids).
* `insee_code`: The 2-digits code delivered by INSEE.
* `start_datetime`: The effective start date + time for the current `id` using ISO format (`YYYY-MM-DD HH:MM:SS`).
* `end_datetime`: The effective end date + time for the current `id` using ISO format (`YYYY-MM-DD HH:MM:SS`).
* `name`: The name of the county.
* `successors`: List of `id`s separated by semicolons which are successors of the current `id`. Default is an empty string.
* `ancestors`: List of `id`s separated by semicolons which are ancestors of the current `id`. Default is an empty string.
* `chef_lieu`: List of `id`s separated by semicolons of the Chef-lieux for that county, as found in [communes.csv](../../exports/communes/). Default is an empty string.
* `parents`: List of `id`s separated by semicolons of the parents for that county, as found in [regions.csv](../../exports/regions/).

The `id` column is unique, the `insee_code` one is NOT. Arbitrarily, the far future end date has been set to `9999-12-31 23:59:59`.

A new entry/line is registered when the county `insee_code` or `name` is modified.


## Format

This is a regular CSV file with value separated by commas and a header line with previously described column names.

You can have a look at the file using Github preview if you click on it.
