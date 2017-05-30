# History of overseas collectivities (Collectivités d’Outre-Mer)

**The `collectivites.csv` file contains history for overseas collectivities.**

The initial date has been chosen given their
[respective histories](https://insee.fr/fr/metadonnees/definition/c1842).


## Sources

* https://fr.wikipedia.org/wiki/France_d%27outre-mer
* https://insee.fr/fr/information/2028040


## Columns

* `id`: This is a [GeoID](https://github.com/etalab/geoids).
* `insee_code`: The 2-digits code delivered by INSEE.
* `start_datetime`: The effective start date + time for the current `id` using ISO format (`YYYY-MM-DD HH:MM:SS`).
* `end_datetime`: The effective end date + time for the current `id` using ISO format (`YYYY-MM-DD HH:MM:SS`).
* `name`: The name of the collectivite.
* `successors`: List of `id`s separated by semicolons which are successors of the current `id`. Default is an empty string.
* `ancestors`: List of `id`s separated by semicolons which are ancestors of the current `id`. Default is an empty string.
* `chef_lieu`: List of `id`s separated by semicolons of the Chef-lieux for that county, as found in [communes.csv](exports/communes/). Default is an empty string.
* `parents`: List of `id`s separated by semicolons of the parents for that county, as found in [regions.csv](exports/regions/).
* `iso2`: [ISO 3166-1 alpha-2 code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) for that overseas collectivity.

The `id` column is unique, the `insee_code` one is NOT. Arbitrarily, the far future end date has been set to `9999-12-31 23:59:59`.

A new entry/line is registered when the county `insee_code` or `name` is modified.


## Format

This is a regular CSV file with value separated by commas and a header line with previously described column names.

You can have a look at the file using Github preview if you click on it.
