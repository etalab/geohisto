from datetime import date

# The first date in history records is 1943-08-12. We need these
# boundaries to deal with ranges related to renamed towns
# with the same INSEE (DEP+COM) codes.
START_DATE = date(1943, 1, 1)
END_DATE = date(2020, 1, 1)
