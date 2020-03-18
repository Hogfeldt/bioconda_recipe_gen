========
Tutorial
========

To show how BiRG works, we will create a recipe for a software called fuma. First we will generate an initial recipe, with basic information about fuma and then we will give this recipe as input to BiRG, which will find the necessary dependencies required to build, test and run fuma.

++++++++++++++++++++
Recipe Initilization
++++++++++++++++++++

First we will generate an initial recipe, this can be done by using the command `bioconda-recipe-gen init`. 
BiRG will then ask for basic information about the software and create a directory named after the software, which contains two files called `meta.yaml` and `build.sh`, thees files are the initial recipe, that we will transform into the final recipe. 

The init command will ask for the following informations:

- Name
- Version
- Source url
- A strategy to use

Here is the initialization of fuma:

.. code-block:: console
    
    $ bioconda-recipe-gen init
    Package name: fuma
    Version: 3.0.5
    Url to download the code: https://github.com/yhoogstrate/fuma/archive/v3.0.5.tar.gz
    Choose the ? that you use to run your code
    ['cmake', 'python2', 'python3']: python3

++++++++++
The recipe
++++++++++

The basic recipe create by `init` should look something like this:

.. code-block:: 
   :caption: fuma/meta.yaml

    package:
      name: fuma
      version: 3.0.5
    source:
      url: https://github.com/yhoogstrate/fuma/archive/v3.0.5.tar.gz
      md5: 4dabc4af48b73ce30cd43f8320dadcea
    build:
      number: 0

.. code-block:: 
   :caption: fuma/build.sh

    #!/bin/bash
    $PYTHON setup.py install

This is the minimal initial recipe, that you can give as input to BiRG. To make it easier for BiRG to find run time dependencies it is important to add tests to the `meta.yaml` file. 
If you have a patch or would like to add some additional meta data, feel free to do so. 
For information on what data and configuration you can add to a recipe, see the official Conda documentation `here <https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html>`_

Before using the recipe for fuma as input to BiRG we make some alterations to the `meta.yaml` file.

.. code-block:: 
   :caption: fuma/meta.yaml

    package:
      name: fuma
      version: 3.0.5
    source:
      url: https://github.com/yhoogstrate/fuma/archive/v3.0.5.tar.gz
      md5: 4dabc4af48b73ce30cd43f8320dadcea
      patches:
        - remove-nose-dep.patch
    build:
      number: 0
    test:
      imports:
        - fuma
      commands:
        - fuma --help
        - fuma --version

    about:
      home: https://github.com/yhoogstrate/fuma/
      license:  GNU General Public License v3 or later (GPLv3+)
      summary: 'FuMa: reporting overlap in RNA-seq detected fusion genes'


.. note::

    We added a patch called `remove-nose-dep.patch` in the `meta.yaml` file, this patch can be downloaded `here <https://raw.githubusercontent.com/bioconda/bioconda-recipes/master/recipes/fuma/remove-nose-dep.patch>`_ , this file should be placed in the recipe directory.


++++++++++++
Recipe Build
++++++++++++


