from datetime import date

# The first date in history records is 1942-08-01. We need these
# boundaries to deal with ranges related to renamed towns
# with the same INSEE (DEP+COM) codes.
START_DATE = date(1942, 1, 1)
END_DATE = date(9999, 1, 1)

# Modification keys from INSEE/COG:
# http://www.insee.fr/fr/methodes/nomenclatures/cog/documentation.asp↩
# ?page=telechargement/2016/doc/doc_variables.htm#mod
RENAME_SIMPLE = 100
RENAME_FUSION_LEADER = 110
FUSION_FOLLOWER = 330
SPLIT_LEADER = 120
SPLIT_FOLLOWER = 210
FUSION_TO_NEW_LEADER = (321, 341)
FUSION_TO_NEW_FOLLOWER = (311, 331)
CHANGE_COUNTY = 410
DELETION = 300
OBSOLETE = 990
