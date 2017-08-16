# Intercommunalities sources documentation

These files are consolidation of "[Listes et compositions des EPCI à fiscalité propre publiées par la Direction Générale des collectivités locales][download]".

Each file (one by year) is UTF-8 encoded,
contains a line by component town from an intercommunality
and has the following fields:

| Name         | Full name                           | Reference                                 |
|--------------|-------------------------------------|-------------------------------------------|
| `siren`      | Intercommunality's SIREN number     |                                           |
| `nom`        | Intercommunality's name             | [Naming rules](#naming-rules)             |
| `nature`     | Intercommunality's legal form       | [Legal forms](#legal-forms)               |
| `fiscalite`  | Intercommunality's tax model        | [Tax models](#tax-models)                 |
| `nb_com`     | Number of component towns           |                                           |
| `ptot`       | Intercommunality's total population | [Population](#population)                 |
| `insee`      | Town's INSEE Code                   |                                           |
| `nom_com`    | Town's nameommune                   |                                           |
| `ptot_com`   | Town's total population             | [Population](#population)                 |
| `pmun_com`   | Town's municipal population         | [Population](#population)                 |

Some files may contains these additionnal fields:

| Name         | Full name                               | Reference                 |
|--------------|-----------------------------------------|---------------------------|
| `pmun`       | Intercommunality's municipal population | [Population](#population) |
| `pcap`       | Intercommunality's aside population     | [Population](#population) |
| `siren_com`  | Town's SIREN number                     |                           |
| `pcap_com`   | Town's aside population                 | [Population](#population) |


## Legal forms

**TODO**

| Code     | French name                         |
|----------|-------------------------------------|
| CC       | Communauté de Communes              |
| CA       | Communauté d’Agglomérations         |
| CU       | Communauté Urbaine                  |
| CV       | Communauté de Villes                |
| DISTRICT | District (urbain ou rural)          |
| METRO    | Métropole                           |
| MET69    | Métropole de Lyon (special case)    |
| METRO69  | Métropole de Lyon (special case)    |
| SAN      | Syndicat d’Agglomération Nouvelle   |


## Tax models

**TODO**

| Code | Name |
|------|------|
| 4TX  |      |
| TPU  |      |
| FA   |      |
| FPU  |      |


## Population

The population always express the legal population from the last census.
The intercommunality's population is the sum of its component town's population.

We distinguish 3 types of populations:
- the municipal population (`pmun`) includes people with their main residence on the town's territory.
- the aside population (`pcap`) includes some people having their main residence in another town but keeping a residential link in this town (students, prisonners...).
- the total population (`ptot`) is the sum of the municipal population and the aside population.

They are **computed** using the population census which is cyclic (from 5 to 9 depending on the year and the method).

**References (french):**
- ["Populations légales 2014"](https://www.insee.fr/fr/statistiques/2525755)
- [Definition of "Populations légales"](https://www.insee.fr/fr/metadonnees/definition/c1999)
- [Definition of "Population totale"](https://www.insee.fr/fr/metadonnees/definition/c1270)
- [Definition of "Population municipale"](https://www.insee.fr/fr/metadonnees/definition/c1932)
- [Definition of "Population comptée à part"](https://www.insee.fr/fr/metadonnees/definition/c1650)
- [Definition of "Recensement de la population"](https://www.insee.fr/fr/metadonnees/definition/c1486)


## Naming rules

From one year to another the `nom` fields can change its naming rule.

The rules observed are as follows:
TODO

## Adding a new file

- Download the new file from [the corresponding page][download].
- Only keep the documented fields above using the provided names.
- Sort on the `siren` field.
- Encode in UTF-8 with ';' as field separator.
- Name the file `{year}.csv`

To help the process, there is a `EPCI.ods` with all years, merges and references as sheets.
You can use it to add an extra year from the original CSV (`Sheets > Insert Sheet from File...`)
and then format and sort it.
This document contains a macro to automate the export of the sheets to CSV in the right format
(you can safely ignore the warning message when you open the document).
You can execute it from the menu `Tools > Macros > Run macro...`
and then select `EPCI.ods > export_as_csv` in the left column and `export_sheets_to_csv` in the right one
and then click on `Run`.


[download]: https://www.collectivites-locales.gouv.fr/liste-et-composition-des-epci-a-fiscalite-propre
