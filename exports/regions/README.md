# History of regions

**The `regions.csv` file contains mainly links between old (since 1970-01-09) and new regions (as of 2016-01-01).**

The initial date has been chosen given the latest modification (fusion of Corsica and Provence-Côte d'Azur) prior to the `2016-01-01` fusion:

> Le décret no 70-18 du 9 janvier 1970 porte à 22 (vingt-deux) le nombre des régions métropolitaines en séparant la Corse de la Provence-Côte d'Azur. — https://fr.wikipedia.org/wiki/R%C3%A9gion_fran%C3%A7aise#R.C3.A9gions.2C_.C3.A9tablissements_publics


## Columns

* `id`: This is the unique combination of `REG` + `insee_code` + `@` + `start_date` (using ISO format `YYYY-MM-DD`).
* `insee_code`: The 2-digits code delivered by INSEE.
* `start_datetime`: The effective start date + time for the current `id` using ISO format (`YYYY-MM-DD HH:MM:SS`).
* `end_datetime`: The effective end date + time for the current `id` using ISO format (`YYYY-MM-DD HH:MM:SS`).
* `name`: The name of the region.
* `successors`: List of `id`s separated by semicolons which are successors of the current `id`. Default is an empty string.
* `ancestors`: List of `id`s separated by semicolons which are ancestors of the current `id`. Default is an empty string.
* `population`: The population as of 2013.
* `surface`: The area in km2.
* `chef_lieu`: The `id` of the Chef-lieu for that region, as found in `towns.csv`.
* `nuts_code`: The 4-chars code delivered by Eurostat.
* `wikipedia`: The wikipedia page for that region (note that given how recent the change is, some links still redirect to temporary region names).

Given that regions have been merged, there is one line by current region and one line by ancestor. The `id` and `insee_code` columns are unique, the `nuts_code` one is NOT.

Regarding dates, the initial date + time has been set as `1970-01-09 00:00:00` given the date of the related [décret n° 70-18](https://fr.wikipedia.org/wiki/R%C3%A9gion_fran%C3%A7aise#R.C3.A9gions.2C_.C3.A9tablissements_publics). Arbitrarily, the far future end date has been set to `9999-12-31 23:59:59`.


## Format

This is a regular CSV file with value separated by commas and a header line with previously described column names.

You can have a look at the file using Github preview if you click on it.
