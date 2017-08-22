import pytest

from geohisto.intercommunalities import extract_name, extract_acronym

NAMES = (
    # Correct name is left unchanged
    ({'nature': 'CC', 'nom': 'Terre d\'Eaux'}, 'Terre d\'Eaux'),
    ({'nature': 'METRO', 'nom': 'Métropole Grenoble-Alpes-Métropole'}, 'Métropole Grenoble-Alpes-Métropole'),
    # Type du|de|de la|d'|des is inlined
    ({'nature': 'CC', 'nom': 'CC du Valromey'}, 'Communauté de Communes du Valromey'),  # noqa: E501
    ({'nature': 'CA', 'nom': 'CA de Bourg en Bresse'}, 'Communauté d\'Agglomération de Bourg en Bresse'),  # noqa: E501
    ({'nature': 'CC', 'nom': 'CC de la Vallière'}, 'Communauté de Communes de la Vallière'),  # noqa: E501
    ({'nature': 'CC', 'nom': 'CC d\'Oyonnax'}, 'Communauté de Communes d\'Oyonnax'),  # noqa: E501
    ({'nature': 'CC', 'nom': 'CC des Bords de Veyle'}, 'Communauté de Communes des Bords de Veyle'),  # noqa: E501
    # Missing type for du|de|de la|d'|des is added
    ({'nature': 'CC', 'nom': 'du Valromey'}, 'Communauté de Communes du Valromey'),  # noqa: E501
    ({'nature': 'CA', 'nom': 'de Bourg en Bresse'}, 'Communauté d\'Agglomération de Bourg en Bresse'),  # noqa: E501
    ({'nature': 'CC', 'nom': 'de la Vallière'}, 'Communauté de Communes de la Vallière'),  # noqa: E501
    ({'nature': 'CC', 'nom': 'd\'Oyonnax'}, 'Communauté de Communes d\'Oyonnax'),  # noqa: E501
    ({'nature': 'CC', 'nom': 'des Bords de Veyle'}, 'Communauté de Communes des Bords de Veyle'),  # noqa: E501
    # Type for names not including it is removed
    ({'nature': 'CC', 'nom': 'CC Terre d\'Eaux'}, 'Terre d\'Eaux'),
    # Fix casing
    ({'nature': 'CC', 'nom': 'CC TERRE D\'EAUX'}, 'Terre d\'Eaux'),
    ({'nature': 'CC', 'nom': 'CC DU VALROMEY'}, 'Communauté de Communes du Valromey'),  # noqa: E501
    ({'nature': 'CA', 'nom': 'CA DE BOURG EN BRESSE'}, 'Communauté d\'Agglomération de Bourg en Bresse'),  # noqa: E501
    ({'nature': 'CC', 'nom': 'CC DE LA VALLIÈRE'}, 'Communauté de Communes de la Vallière'),  # noqa: E501
    ({'nature': 'CC', 'nom': 'CC D\'OYONNAX'}, 'Communauté de Communes d\'Oyonnax'),  # noqa: E501
    ({'nature': 'CC', 'nom': 'CC DES BORDS DE VEYLE'}, 'Communauté de Communes des Bords de Veyle'),  # noqa: E501
    # Multiple spaces
    ({'nature': 'CC', 'nom': 'CC   Terre   d\'Eaux'}, 'Terre d\'Eaux'),
    # Special case for first char
    ({'nature': 'CC', 'nom': 'CC LES 2 VALLÉES'}, 'Les 2 Vallées'),
    # Special rules for initial mispelling (ie. C.C., C.U. ... )
    ({'nature': 'CC', 'nom': 'C.C. du Valromey'}, 'Communauté de Communes du Valromey'),  # noqa: E501
    # Special rules for old districts
    # Can be 'rural' or 'urbain' and can be contract as:
    # D.|DI|D.AGGLO|D.RURAL|DI RURAL (with or without spaces)
    ({'nature': 'DISTRICT', 'nom': 'D.RURAL MONTREVEL'}, 'Montrevel'),
    ({'nature': 'DISTRICT', 'nom': 'D.U D\'OYONNAX'}, 'District Urbain d\'Oyonnax'),  # noqa: E501
    ({'nature': 'DISTRICT', 'nom': 'D VALSEMINE'}, 'Valsemine'),
    ({'nature': 'DISTRICT', 'nom': 'D la Ferte sur Amance'}, 'La Ferte sur Amance'),  # noqa: E501
    ({'nature': 'DISTRICT', 'nom': 'D.de Gueux'}, 'District de Gueux'),
    ({'nature': 'DISTRICT', 'nom': 'Di Rural de la Region de Dou'}, 'District Rural de la Région de Dou'),  # noqa: E501
    ({'nature': 'DISTRICT', 'nom': 'D.u de Saumur'}, 'District Urbain de Saumur'),  # noqa: E501
    ({'nature': 'DISTRICT', 'nom': 'Di Urbain de Mouy'}, 'District Urbain de Mouy'),  # noqa: E501
    # Fix bad CSV formatting
    ({'nature': 'CC', 'nom': ':canton de Saint Agreve'}, 'Canton de Saint Agreve'),  # noqa: E501
    ({'nature': 'CC', 'nom': ':de l\'Albigeois'}, 'Communauté de Communes de l\'Albigeois'),  # noqa: E501
    ({'nature': 'CC', 'nom': ':delta Sevre Argent'}, 'Delta Sevre Argent'),
    ({'nature': 'CC', 'nom': 'C.C. :DU CHALABRAIS'}, 'Communauté de Communes du Chalabrais'),  # noqa: E501
    ({'nature': 'CA', 'nom': 'Communauté d\'agglomération "Vitré Communauté"'}, 'Communauté d\'agglomération Vitré Communauté'),  # noqa: E501
    ({'nature': 'CC', 'nom': '\'\'Ventoux-Sud\'\''}, 'Ventoux-Sud'),
    ({'nature': 'CC', 'nom': '"Ventoux-Sud"'}, 'Ventoux-Sud'),
    ({'nature': 'CA', 'nom': '"la Riviéra du Levant"'}, 'La Riviéra du Levant'),  # noqa: E501
    ({'nature': 'CA', 'nom': '.du Grand Rodez'}, 'Communauté d\'Agglomération du Grand Rodez'),  # noqa: E501
    ({'nature': 'CC', 'nom': 'Autour dAnduze'}, 'Autour d\'Anduze'),
    ({'nature': 'CC', 'nom': 'Terres de Cur'}, 'Terres de Cœur'),
    # Remove acronym between parenthesis or brackets
    ({'nature': 'CC', 'nom': 'Territoire de la Côte Ouest (TCO)'}, 'Territoire de la Côte Ouest'),  # noqa: E501
    ({'nature': 'CC', 'nom': 'CC Coeur d\'Ostrevent [c.C.C.O.]'}, 'Coeur d\'Ostrevent'),  # noqa: E501
    # Except for Tours
    ({'nature': 'CA', 'nom': 'Tour(s) Plus'}, 'Tour(s) Plus'),
    ({'nature': 'CA', 'nom': 'Tours (Plus)'}, 'Tours (Plus)'),
    # TODO
    # Replacements
    # Region -> Région
    # Reg -> Région
    # cant -> Canton
    # Vallee -> Vallée
    # Caux-fleur de Lin -> Caux - Fleur de Lin
    # ile/Ile -> Île
    # Seine-Eure
    # St-Etienne
    # Special rules for St/Ste/Saint/Sainte
    # Special rules for Hts/Ht/Hte/Hauts/Haut/Haute
    # Special rules for "interdepartementale", "interdépartementale", "interrégionale", "Intercommunale"  # noqa: E501
)


@pytest.mark.parametrize('line,expected', NAMES)
def test_extract_name(line, expected):
    assert extract_name(line) == expected


ACRONYMS = (
    ('Territoire de la Côte Ouest (tco)', 'TCO'),
    ('Territoire de la Côte Ouest', None),
    ('CC Coeur d\'Ostrevent [c.C.C.O.]', 'C.C.C.O.'),
    # Special cases for Tours (Plus)
    ('Tour(s) Plus', None),
    ('Tours (Plus)', None),
)


@pytest.mark.parametrize('name,expected', ACRONYMS)
def test_extract_acronym(name, expected):
    assert extract_acronym({'nom': name}) == expected
