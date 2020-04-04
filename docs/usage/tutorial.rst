========
Tutorial
========

To show how BiRG works, we will create a recipe for a software called netReg.
We will start with generating an initial recipe, with basic information about netReg.
This recipe will then be given as input to BiRG, which will find the necessary dependencies required to build, test and run the software.

++++++++++++++++++++
Recipe Initilization
++++++++++++++++++++

First we will generate an initial recipe, this can be done by using the command `bioconda-recipe-gen init`. 
BiRG will then ask for basic information about the software and create a directory named after the software,
which contains two files called `meta.yaml` and `build.sh`.
These files are the initial recipe, that we will transform into the final recipe.

The init command will ask for the following informations:

- Name
- Version
- Source url
- A build strategy to use

Here is the initialization of netReg:

.. code-block:: console
    
    $ bioconda-recipe-gen init
    Package name: netreg
    Version: 1.8.0
    Url to download the code: https://github.com/dirmeier/netReg/archive/v1.8.0.tar.gz
    Choose the ? that you use to run your code
    ['cmake', 'python2', 'python3']: cmake

++++++++++
The recipe
++++++++++

The basic recipe create by `init` should look something like this:

.. code-block:: yaml
   :caption: netreg/meta.yaml

    package:
        name: netreg
        version: 1.8.0
    source:
        url: https://github.com/dirmeier/netReg/archive/v1.8.0.tar.gz
        md5: 0cd731c0b9a6902e37c1515858fb38f9
    build:
        number: 0

.. code-block::
   :caption: netreg/build.sh

    #!/bin/bash
    mkdir -p build
    cd build
    cmake ..
    make
    make install

This is the minimal initial recipe, that you can give as input to BiRG.
To make it easier for BiRG to find run-time dependencies it is important to add tests to the `meta.yaml` file.
If you have a patch or would like to add some additional meta data, feel free to do so. 
For information on what data and configuration you can add to a recipe, see the official Conda documentation `here <https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html>`_

Before using the recipe for netReg as input to BiRG, we will add some tests to the `meta.yaml` file.
By adding tests, we makes sure that BiRG will try and find run-time dependencies as well as build-time dependencies.

.. code-block:: yaml
   :caption: netReg/meta.yaml

    package:
        name: netreg
        version: 1.8.0
    source:
        url: https://github.com/dirmeier/netReg/archive/v1.8.0.tar.gz
        md5: 0cd731c0b9a6902e37c1515858fb38f9
    build:
        number: 0
    test:
        commands:
        - netReg -h

We will also edit the the `build.sh`, as netReg requires us to set some flags for cmake:

.. code-block:: 
   :caption: netReg/build.sh

    #!/bin/bash
    mkdir -p build
    cd build
    cmake -DCMAKE_INSTALL_PREFIX="${PREFIX}" -DBOOST_ROOT="${PREFIX}" -DCMAKE_CXX_COMPILER="${CXX}" ..
    make
    make install

.. note::

    The recipe for netReg can be found in our github repo `here <https://github.com/Hogfeldt/bioconda_recipe_gen/tree/master/examples/cmake/input>`_

++++++++++++
Recipe Build
++++++++++++

We are now ready to give our inital recipe as input to BiRG. The build command takes three required arguments as shown below:

.. code-block:: console
    
    $ bioconda-recipe-gen build --help
    usage: bioconda-recipe-gen build [-h] [-d]
                                     bioconda_recipe_path recipe_path
                                     {cmake,python2,python3}

    positional arguments:
      bioconda_recipe_path  Path to your local copy of the bioconda-recipe
                              repository
      recipe_path           Path to folder with meta.yaml and build.sh templates
      {cmake,python2,python3}
                            The ? that you used when creating the template with
                            'init'

    optional arguments:
      -h, --help            show this help message and exit
      -d, --debug           Set this flag if you want to activate the debug mode.
                            This creates an debug.log file that contains all debug
                            prints

bioconda_recipe_path: Is the path to you local version of the bioconda-recipes repository, which can be found `here <https://github.com/bioconda/bioconda-recipes>`_ .

recipe_path: Is the path to the recipe directory which was created by running `bioconda-recipe-gen init`.

Strategy: Here you must tell BiRG which building strategy to use, we currently supports three strategies cmake, python2 or python3.

Here is an example on how BiRG is called for building fuma:

.. code-block:: console
    
    $ bioconda-recipe-gen build bioconda-recipes/ netreg/ cmake

When BiRG is running it will print out a lot of text, this is the output from it's building process.
BiRG will also some times ask for your help, to determine which version of a dependency it should use.

When BiRG is done running (may take around 20 min for this specific package) it will tell you if it was able to build and run your software, and the output recipe can be found in the directory which was created by the `init` command.

Here is the final recipe for netReg:

.. code-block:: yaml
   :caption: netreg/meta.yaml

    package:
        name: netreg
        version: 1.8.0
    source:
        url: https://github.com/dirmeier/netReg/archive/v1.8.0.tar.gz
        md5: 0cd731c0b9a6902e37c1515858fb38f9
    build:
        number: 2
    test:
        commands:
        - netReg -h
    requirements:
        build:
        - cmake
        - make
        - {{ compiler('cxx') }}
        host:
        - armadillo
        - hdf5
        - boost
        run:
        - armadillo
        - hdf5
        - boost
    
.. code-block:: 
   :caption: netreg/build.sh

    #!/bin/bash
    mkdir -p build
    cd build
    cmake -DCMAKE_INSTALL_PREFIX="${PREFIX}" -DBOOST_ROOT="${PREFIX}" -DCMAKE_CXX_COMPILER="${CXX}" ..
    make
    make install

Congratulation you can now add your recipe to Bioconda and share your software.
