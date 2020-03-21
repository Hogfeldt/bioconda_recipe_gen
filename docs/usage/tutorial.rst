========
Tutorial
========

To show how BiRG works, we will create a recipe for a software called airr. First we will generate an initial recipe, with basic information about airr and then we will give this recipe as input to BiRG, which will find the necessary dependencies required to build, test and run the software.

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
    Package name: airr
    Version: 1.2.1
    Url to download the code: https://pypi.io/packages/source/a/airr/airr-1.2.1.tar.gz
    Choose the ? that you use to run your code
    ['cmake', 'python2', 'python3']: python3

++++++++++
The recipe
++++++++++

The basic recipe create by `init` should look something like this:

.. code-block:: 
   :caption: airr/meta.yaml

    package:
      name: airr
      version: 1.2.1
    source:
      url: https://pypi.io/packages/source/a/airr/airr-1.2.1.tar.gz
      md5: 66f13422ea75f9b40b86acf6fd521fdd
    build:
      number: 0

.. code-block:: 
   :caption: airr/build.sh

    #!/bin/bash
    $PYTHON setup.py install

This is the minimal initial recipe, that you can give as input to BiRG. To make it easier for BiRG to find run-time dependencies it is important to add tests to the `meta.yaml` file. 
If you have a patch or would like to add some additional meta data, feel free to do so. 
For information on what data and configuration you can add to a recipe, see the official Conda documentation `here <https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html>`_

Before using the recipe for airr as input to BiRG, we will add some tests to the `meta.yaml` file.
By adding tests, we makes sure that BiRG will try and find run-time dependencies as well as build-time dependencies.

.. code-block:: 
   :caption: airr/meta.yaml

    package:
      name: airr
      version: 1.2.1
    source:
      url: https://pypi.io/packages/source/a/airr/airr-1.2.1.tar.gz
      md5: 66f13422ea75f9b40b86acf6fd521fdd
    build:
      number: 0
    test:
      commands:
      - airr-tools --help
      imports:
      - airr
      - airr.specs
      - tests

We will also edit the the `build.sh`, since the developers of airr are preferring to use `pip`.

.. code-block:: 
   :caption: airr/build.sh

    #!/bin/bash
    $PYTHON -m pip install . --no-deps --ignore-installed --no-cache-dir -vvv 

.. note::

    The recipe for airr can be found in our github repo `here <https://github.com/Hogfeldt/bioconda_recipe_gen/tree/master/examples/python_builds_with_pip/input>`_

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
    
    $ bioconda-recipe-gen build bioconda-recipes/ airr/ python3

When BiRG is running it will print out a lot of text, this is the output from it's building process.
BiRG will also some times ask for your help, to determine which version of a dependency it should use.

When BiRG is done running it will tell you if it was able to build and run your software and the output recipe can be found in the directory which aws created by the `init` command. 

Here is the final recipe for airr:

.. code-block:: 
   :caption: airr/meta.yaml

    package:
      name: airr
      version: 1.2.1
    source:
      url: https://pypi.io/packages/source/a/airr/airr-1.2.1.tar.gz
      md5: 66f13422ea75f9b40b86acf6fd521fdd
    build:
      number: 0
    test:
      commands:
      - airr-tools --help
      imports:
      - airr
      - airr.specs
      - tests
    requirements:
      host:
      - python >=3
      run:
      - python >=3
      - pandas
      - pyyaml
      - yamlordereddictloader
      - setuptools
    
.. code-block:: 
   :caption: airr/build.sh

    #!/bin/bash
    $PYTHON -m pip install . --no-deps --ignore-installed --no-cache-dir -vvv 

Congratulation you can now add your recipe to Bioconda and share your software.
