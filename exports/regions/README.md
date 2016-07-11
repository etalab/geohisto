# History of regions

**The `regions.csv` file contains mainly links between old (prior to 2016-01-01) and new regions and their INSEE codes.**

## Columns

* `INSEE_CODE`: The 2-digits code delivered by INSEE.
* `NUTS_CODE`: The 4-chars code delivered by Eurostat.
* `NAME`: The new name of the region.
* `WIKIPEDIA`: The wikipedia page for that new region (note that given how recent the change is, some links still redirect to temporary region names).
* `CHEF_LIEU`: The Chef-lieu for that new region.
* `START_DATE`: The date of effectiveness, in our case always 2016-01-01 for the moment.
* `PREV_INSEE_CODE`: The previous INSEE code for the parent region.
* `PREV_NUTS_CODE`: The previous NUTS code for the parent region.
* `PREV_NAME`: The name of the parent region.

Given that regions have been merged, there is one line by ancestor and the `INSEECODE` is not unique. The `PREVINSEECODE` is though.

## Format

This is a regular CSV file with value separated by commas and a header line with previously described column names.

You can have a look at the file using Github preview if you click on it.
