def test_metropole_population(towns):
    arles = next(towns.filter(depcom='13004'))
    assert arles.population == 52566


def test_arrondissements_population(towns):
    marseille_12_arrondissement = next(towns.filter(depcom='13212'))
    assert marseille_12_arrondissement.population == 57908


def test_dom_population(towns):
    basse_terre = next(towns.filter(depcom='97105'))
    assert basse_terre.population == 11150


def test_mortes_population(towns):
    bezonvaux = next(towns.filter(depcom='55050'))
    assert bezonvaux.population == 0


def test_unknown_population(towns):
    amareins = next(towns.filter(depcom='01003'))
    assert amareins.population == 'NULL'


def test_computed_population(towns):
    val_ocre = list(towns.filter(depcom='89334'))[1]
    assert val_ocre.population == 581
