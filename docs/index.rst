.. BiRG documentation master file, created by
   sphinx-quickstart on Wed Feb 12 19:31:14 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============
Welcome to BiRG
===============

BiRG is an automation tool for generating Conda recipes for the Bioconda channel.
It is built on heuristics about how to find dependencies based on the error messages it gets from trying to build and run some given software.

BiRG achieves the same goal as conda skeleton, but instead of collecting the metadata from PyPI and building the
recipe based on that, BiRG finds a package's dependencies by trying to build the package, and based on the error
messages BiRG tries to detect the dependencies.

Therefore, BiRG is the choice if you don't have the software's metadata already available. However, in case you do
have a package on PyPI, we recommend to simply use conda skeleton.
A guide to this can be found `here <https://docs.conda.io/projects/conda-build/en/latest/user-guide/tutorials/build-pkgs-skeleton.html>`_.

User's guide
============

.. toctree::
  :maxdepth: 3

  usage/index

Development
===========

.. toctree::
  :maxdepth: 3

  development/index

