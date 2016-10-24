# GeoHisto

**Historic information for French regions and towns based on INSEE data, exported as a (re)usable CSV file.**

It might be useful if you have to deal with redirections and is in use by the [geozones](https://github.com/etalab/geozones) project to feed [data.gouv.fr](http://www.data.gouv.fr/fr/).


## Usage

If you’re only interested in generated data, check out the `exports` folder which contains CSV files related to [regions](exports/regions/) and [towns](exports/towns/). There is a dedicated documentation at these places.


## Sources

Source files are coming from the [INSEE downloads page](http://www.insee.fr/fr/methodes/nomenclatures/cog/telechargement.asp) which allows to retrieve information related to the “Code officiel géographique”. We’re using the list of existing towns and their history which are both available within the `sources` folder.

Additionaly, files containing the population for almost all towns has been computed too in the `sources` folder. They are coming from [a XLS dataset](http://www.insee.fr/fr/ppp/bases-de-donnees/recensement/populations-legales/pages2015/zip/HIST_POP_COM_RP13.zip) provided by  [INSEE](http://www.insee.fr/fr/ppp/bases-de-donnees/recensement/populations-legales/), manually completed with Wikipedia data for [Lyon](https://fr.wikipedia.org/wiki/Arrondissements_de_Lyon) and [Marseille](https://fr.wikipedia.org/wiki/Secteurs_et_arrondissements_de_Marseille) districts, and converted into CSV.


## Development

The project doesn’t require any dependency, you have to run it with Python 3:

    $ python3 -m geohisto

Note that it takes about 4 minutes to generate the towns export.


## Tests

If you plan to contribute, you have to install [pytest](http://doc.pytest.org/en/latest/) and launch the test suite:

    $ python -m pytest tests

Note that the duration of the whole test suite run is about 5 minutes.

That's why you would probably prefer to run a particular test:

    $ python -m pytest tests/test_actions.py::test_change_name



## TODO

* Make the export configurable through command-line options?
* Collect feedback from reusers
