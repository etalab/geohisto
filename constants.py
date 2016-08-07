from datetime import date

# The first date in history records is 1942-08-01. We need these
# boundaries to deal with ranges related to renamed towns
# with the same INSEE (DEP+COM) codes.
START_DATE = date(1942, 1, 1)
END_DATE = date(2020, 1, 1)
