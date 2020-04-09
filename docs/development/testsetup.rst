Test setup
==========

The way we have been developing BiRG is by taking a set of packages from `bioconda-recipes <https://github.com/bioconda/bioconda-recipes>`_ and then use our test pipeline which can be found in the repo `bioconda_recipe_gen_ci <https://github.com/birgorg/birg_ci>`_.
This pipeline runs BiRG on all the chosen packages and outputs for each package:

- a file with everything from stdout that was generated doing the build
- the generated meta.yaml
- the generated build.sh

Furthermore, it outputs a single overview file with each package name and whether or not it did build.

Exactly how to use the pipeline (or part of it) is explained in the the README of the `birg_ci <https://github.com/birgorg/birg_ci>`_ repo.



