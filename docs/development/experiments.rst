===========
Experiments
===========

To see how well BiRG performs, we found all python (exclusively python, no other code like for example c)
and cmake (packages with a CMakeList.txt in the root folder) packages on `bioconda-recipes <https://github.com/bioconda/bioconda-recipes>`_.

We then tried to build the recipes for these packages with BiRG. We considered the recipe created successfully if
running `bioconda-utils build` with the recipe resulted in a successful build, as this is how a recipe should be used
to make a conda package.

Note: Before running the packages on BiRG, we filtered out all packages that didn't get a successful built with `bioconda-utils build` given its own recipe (E.g. blacklisted packages)

+++++++
Results
+++++++
- Python packages (both python2 and python3):
    - Date: 15/3/20
    - Total amount: 397
    - Successful builds: 256
    - Percentage of packages successfully built: 64%
- Cmake packages:
    - Date: 13/11/19
    - Total amount: 49
    - Successful builds: 28
    - Percentage of packages successfully built: 57%
