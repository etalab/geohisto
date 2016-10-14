def test_metropole_population(result):
    arles = result.filter(depcom='13004')[0]
    assert arles.population == 52566


def test_arrondissements_population(result):
    marseille_12_arrondissement = result.filter(depcom='13212')[0]
    assert marseille_12_arrondissement.population == 57908


def test_dom_population(result):
    basse_terre = result.filter(depcom='97105')[0]
    assert basse_terre.population == 11150


def test_mortes_population(result):
    bezonvaux = result.filter(depcom='55050')[0]
    assert bezonvaux.population == 0


def test_unknown_population(result):
    amareins = result.filter(depcom='01003')[0]
    assert amareins.population == 'NULL'


def test_computed_population(result):
    val_ocre = result.filter(depcom='89334')[1]
    assert val_ocre.population == 581
