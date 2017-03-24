from datetime import date, datetime, timedelta

# In use to concatenate ids.
SEPARATOR = '@'

# The first date in history records is 1942-08-01. We need these
# boundaries to deal with ranges related to renamed towns
# with the same INSEE (DEP+COM) codes.
START_DATE = date(1942, 1, 1)
START_DATETIME = datetime.combine(START_DATE, datetime.min.time())
END_DATE = date(9999, 12, 31)
END_DATETIME = datetime.combine(END_DATE, datetime.max.time())
DELTA = timedelta.resolution

# Conversion required because historiq file does not contain `ARTMIN`.
TNCC2ARTICLE = {
    0: '',
    1: '',
    2: 'Le',
    3: 'La',
    4: 'Les',
    5: "L'",
    6: 'Aux',
    7: 'Las',
    8: 'Los',
}

# Modification keys from INSEE/COG:
# https://www.insee.fr/fr/information/2114773#mod
CHANGE_NAME = 100
CHANGE_NAME_FUSION = 110
CHANGE_NAME_CREATION = 111
CHANGE_NAME_REINSTATEMENT = 120
CHANGE_NAME_CHANGE_ADMINISTRATIVE_CENTRE = 130  # Do not handle that case.
CHANGE_NAME_TRANSFERT_CANTON = 140  # Do not handle that case.
CHANGE_NAME_TRANSFERT_ADMINISTRATIVE_CENTRE = 150  # Do not handle that case.

CREATION = 200
REINSTATEMENT = 210
GIVING_PARCELS = 220  # Do not handle that case.
SPLITING = 230
CREATION_NEW_FRACTION = 240  # Do not handle that case.

DELETION_PARTITION = 300
DELETION_FUSION = 310
CREATION_NOT_DELEGATED = 311
FUSION_ABSORPTION = 320  # Already done with DELETION_FUSION.
CREATION_NOT_DELEGATED_POLE = 321  # Already done with CREATION_NOT_DELEGATED.
FUSION_ASSOCIATION_ASSOCIATED = 330
CREATION_DELEGATED = 331
CREATION_PREEXISTING_ASSOCIATED = 332
# Already done with CREATION_DELEGATED.
CREATION_PREEXISTING_DELEGATED = 333
FUSION_ASSOCIATION_ABSORBER = 340  # Already done with CHANGE_NAME_FUSION?
CREATION_DELEGATED_POLE = 341
# Already done with FUSION_ASSOCIATION_ASSOCIATED
FUSION_ASSOCIATION_SIMPLE_ABSORBER = 350
# Already done with CREATION_DELEGATED
CREATION_DELETION = 351
# Already done with FUSION_ASSOCIATION_ABSORBER
FUSION_ASSOCIATION_SIMPLE_POLE = 360
DELETION_FRACTION = 370  # Do not handle that case.
RECEPTION_PARCELS = 390  # Do not handle that case.

CHANGE_REGION = 400  # Never happened.
CHANGE_COUNTY = 410
CHANGE_COUNTY_CREATION = 411
CHANGE_DISTRICT = 420  # Do not handle that case.
CHANGE_DISTRICT_CREATION = 421  # Do not handle that case.
CHANGE_CANTON = 430  # Do not handle that case.
CHANGE_CANTON_CREATION = 431  # Do not handle that case.

TRANSFERT_ADMINISTRATIVE_CENTRE = 500  # Do not handle that case.
TRANSFERT_ADMINISTRATIVE_CENTRE_CANTON = 510  # Do not handle that case.
TRANSFERT_ADMINISTRATIVE_CENTRE_ARRONDISSEMENT = 520  # Do not handle that case
TRANSFERT_ADMINISTRATIVE_CENTRE_COUNTY = 530  # Do not handle that case.
TRANSFERT_ADMINISTRATIVE_CENTRE_REGION = 540  # Do not handle that case.

CEASING_PARCELS_WITH_DEMO = 600  # Do not handle that case.
CEASING_PARCELS_WITHOUT_DEMO = 610  # Do not handle that case.
RECEIVING_PARCELS_WITH_DEMO = 620  # Do not handle that case.
RECEIVING_PARCELS_WITHOUT_DEMO = 630  # Do not handle that case.

ASSOCIATED_BECOMING_DELEGATED = 700  # Do not handle that case.

OBSOLETE = 990
