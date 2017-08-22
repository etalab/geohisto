# Documentation des sources des EPCI

Ces fichiers sont la consolidation des [Listes et compositions des EPCI à fiscalité propre publiées par la Direction Générale des collectivités locales][download].

Chaque fichier (un par année) est encodé en UTF-8,
contient une ligne par commune constituante d'un EPCI
et possède les colonnes suivantes:

| Nom          | Nom complet                         | Référence                                 |
|--------------|-------------------------------------|-------------------------------------------|
| `siren`      | Numéro de SIREN de l'EPCI           |                                           |
| `nom`        | Nom de l'EPCI                       | [Règles de nommage](#regles-de-nommage)   |
| `nature`     | Nature juridique de l'EPCI          | [Natures juridiques](#natures-juridiques) |
| `fiscalite`  | Fiscalité de l'ECPI                 | [Fiscalités](#fiscalites)                 |
| `nb_com`     | Nombre de communes de l'EPCI        |                                           |
| `ptot`       | Population totale de l'EPCI         | [Population](#population)                 |
| `insee`      | Code INSEE de la commune            |                                           |
| `nom_com`    | Nom de la commune                   |                                           |
| `ptot_com`   | Population totale de la commune     | [Population](#population)                 |
| `pmun_com`   | Population municipale de la commune | [Population](#population)                 |

Certains fichiers peuvent contenir les colonnes supplémentaires suivantes:

| Nom          | Nom complet                             | Référence                 |
|--------------|-----------------------------------------|---------------------------|
| `pmun`       | Population municipale de l'EPCI         | [Population](#population) |
| `pcap`       | Population comptée à part de l'EPCI     | [Population](#population) |
| `siren_com`  | Numéro SIREN de la commune              |                           |
| `pcap_com`   | Population comptée à part de la commune | [Population](#population) |


## Natures juridiques

| Code     | Nom                                 |
|----------|-------------------------------------|
| CC       | Communauté de Communes              |
| CA       | Communauté d’Agglomérations         |
| CU       | Communauté Urbaine                  |
| CV       | Communauté de Villes                |
| DISTRICT | District  (urbain ou rural)         |
| METRO    | Métropole                           |
| MET69    | Métropole de Lyon (cas particulier) |
| METRO69  | Métropole de Lyon (cas particulier) |
| SAN      | Syndicat d’Agglomération Nouvelle   |


## Fiscalités

| Code | Nom                                                 |
|------|-----------------------------------------------------|
| 4TX  | Régime fiscal à 4 TauX pour la taxe professionnelle |
| TPU  | Régime de la Taxe Professionnelle Unique            |
| FA   | Régime de la Fiscalité Additionnelle                |
| FPU  | Régime de la Fiscalité Professionnelle Unique       |


## Population

La population exprimée correspond toujours à la population légale au dernier recensement.
La population de l'EPCI est la somme des populations de communes constituantes.

On distingue 3 types de populations:
- La population municipale (`pmun`) comprend les personnes ayant leur résidence habituelle sur le territoire de la commune.
- La population comptée à part (`pcap`) comprend certaines personnes dont la résidence habituelle est dans une autre commune mais qui gardent un lien de résidence avec la commune (étudiants, prisonniers...).
- la population totale (`ptot`) est la somme de la population municipale et de la population comptée à part.

Elles sont **calculées** au moyen du recensement de la population de façon cyclique (de 5 à 9 ans suivant les années et la méthode).

**Références:**
- [Populations légales 2014](https://www.insee.fr/fr/statistiques/2525755)
- [Définition des "Populations légales"](https://www.insee.fr/fr/metadonnees/definition/c1999)
- [Définition de la "Population totale"](https://www.insee.fr/fr/metadonnees/definition/c1270)
- [Définition de la "Population municipale"](https://www.insee.fr/fr/metadonnees/definition/c1932)
- [Définition de la "Population comptée à part"](https://www.insee.fr/fr/metadonnees/definition/c1650)
- [Définition du "Recensement de la population"](https://www.insee.fr/fr/metadonnees/definition/c1486)


## Règles de nommage

D'une année sur l'autre, la colonne `nom` peut changer de règle de nommage.

Les règles observées sont les suivantes:
TODO

## Ajout d'un nouveau fichier

- Télécharger le nouveau fichier depuis [la page correspondante][download].
- Ne conserver que les colonnes documentées ci-dessus en utilisant les noms fournis.
- Trier sur la colonne `siren`.
- Encoder en UTF-8 avec ';' comme séparateur de champ.
- Nommer le fichier `{année}.csv`

Pour faciliter la procédure, il est possible d'utiliser le fichier `EPCI.ods` du [jeu de données "Liste et composition des EPCI à fiscalité propre"](https://www.data.gouv.fr/fr/datasets/liste-et-composition-des-epci-a-fiscalite-propre/). Il contient les années,
les fusions et les références dans des feuilles séparées.


[download]: https://www.collectivites-locales.gouv.fr/liste-et-composition-des-epci-a-fiscalite-propre
