def test_metropole_population(towns):
    arles = towns.filter(depcom='13004')[0]
    assert arles.population == 52566


def test_arrondissements_population(towns):
    marseille_12_arrondissement = towns.filter(depcom='13212')[0]
    assert marseille_12_arrondissement.population == 57908


def test_dom_population(towns):
    basse_terre = towns.filter(depcom='97105')[0]
    assert basse_terre.population == 11150


def test_mortes_population(towns):
    bezonvaux = towns.filter(depcom='55050')[0]
    assert bezonvaux.population == 0


def test_unknown_population(towns):
    amareins = towns.filter(depcom='01003')[0]
    assert amareins.population == 'NULL'


def test_computed_population(towns):
    val_ocre = towns.filter(depcom='89334')[1]
    assert val_ocre.population == 581
