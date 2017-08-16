# History of intercommunalities (EPCI)

**The `epci.csv` file contains history for intercommunalities since 1999-01-01.**

## Sources

* https://fr.wikipedia.org/wiki/%C3%89tablissement_public_de_coop%C3%A9ration_intercommunale
* https://www.collectivites-locales.gouv.fr/liste-et-composition-des-epci-a-fiscalite-propre


## Columns

* `id`: This is a [GeoID](https://github.com/etalab/geoids).
* `siren`: The 9-digits code delivered by INSEE.
* `name`: The name of the intercommunality.
* `acronym`: An optionnal known acronym or short name.
* `kind`: The legal form of the intercommunality.
* `taxmodel`: The tax model under which the intercommunality is.
* `towns`: List of component towns `id`s separated by semicolons.
* `start_date`: The effective start date for the current `id` using ISO format (`YYYY-MM-DD`).
* `end_date`: The effective end date for the current `id` using ISO format (`YYYY-MM-DD`).
* `end_reason`: The reason explaining the end of this intercommunality.
* `successors`: List of `id`s separated by semicolons which are successors of the current `id`.
* `ancestors`: List of `id`s separated by semicolons which are ancestors of the current `id`.
* `population`: The legal population from last census.

The `id` column is unique, the `siren` one is NOT.
Arbitrarily, the far future end date has been set to `9999-12-31 23:59:59`.

A new entry/line is registered when the intercommunality changed one of its:
- `siren`
- `name`
- `taxmodel`
- `kind`
- conponent `towns`


## Format

This is a regular CSV file with value separated by commas and a header line with previously described column names.

You can have a look at the file using Github preview if you click on it.
