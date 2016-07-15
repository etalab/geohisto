# History of regions

**The `regions.csv` file contains mainly links between old (since 1970-01-09) and new regions (as of 2016-01-01).**

The initial date has been chosen given the latest modification (fusion of Corsica and Provence-Côte d'Azur) prior to the `2016-01-01` fusion:

> Le décret no 70-18 du 9 janvier 1970 porte à 22 (vingt-deux) le nombre des régions métropolitaines en séparant la Corse de la Provence-Côte d'Azur. — https://fr.wikipedia.org/wiki/R%C3%A9gion_fran%C3%A7aise#R.C3.A9gions.2C_.C3.A9tablissements_publics


## Columns

* `DIRECTION`: Either `--`, `<-` or `->` if the region is unchanged, has been renamed or merged respectively.
* `INSEE_CODE`: The 2-digits code delivered by INSEE.
* `NAME`: The new name of the region.
* `START_DATE`: The start date of existence, in our case either `1970-01-09` or `2016-01-01`.
* `END_DATE`: The end date of existence, in our case always `2016-01-01` or `2020-01-01`.
* `POPULATION`: The population as of 2013.
* `SURFACE`: The area in km2.
* `CHEF_LIEU`: The Chef-lieu for that new region.
* `NUTS_CODE`: The 4-chars code delivered by Eurostat.
* `WIKIPEDIA`: The wikipedia page for that new region (note that given how recent the change is, some links still redirect to temporary region names).

Given that regions have been merged, there is one line by current region and one line by ancestor. The `INSEE_CODE` column is unique, the `NUTS_CODE` one is NOT.

## Format

This is a regular CSV file with value separated by commas and a header line with previously described column names.

You can have a look at the file using Github preview if you click on it.
