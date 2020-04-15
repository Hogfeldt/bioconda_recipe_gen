.. _tutorial:

========
Tutorial
========

To show how BiRG works, we will create a recipe for a software called kallisto.
We will start with generating an initial recipe, with basic information about kallisto.
This recipe will then be given as input to BiRG, which will find the necessary dependencies required to build, test and run the software.

We assume that you are using the docker image that we provide, but if you have installed BiRG from source, the tutorial still applies, just go directly to `Recipe Initilization`_.

++++++++++++++++++++++++++
Using the Docker Container
++++++++++++++++++++++++++

The docker container should be called with the following settings, so that the container and the host system can communicate.

.. code-block:: console
    
    $ docker run -v /var/run/docker.sock:/var/run/docker.sock \
                 -v $PWD:/home \
                 --user $(id -u):$(id -g) \
                 -it perhogfeldt/birg:latest \
                 <birg-command>

In the rest of this tutorial you can just replace `birg` with the above command.

Here is a short explanation on what the settings are for, if you are not so familiar with docker.

The first volume we added, with `-v`, is the unix socket that the docker client uses to talk with the docker server. We need to add this socket, since the container will need to spin up more containers, when it tries to build the software.
The second volume will bind the containers home direcetory to the host systems current directory, this will make sure that files can be shared.
the `--user` option makes sure that files created on you system will be owned by your current user and `-it` just makes sure that you can communicate with the container directly in your current terminal.

If you prefer not to write all the settings every time you call birg, we recommend exporting the settings in an environment variable like this:

.. code-block:: console
    
    $ export BIRG="-v /var/run/docker.sock:/var/run/docker.sock \
                           -v $PWD:/home --user $(id -u):$(id -g) \
                           -it perhogfeldt/birg:latest"

Then you can just call birg with the environment variable:

.. code-block:: console
    
    $ docker run $BIRG <birg-command>

++++++++++++++++++++
Recipe Initilization
++++++++++++++++++++

First we will generate an initial recipe, this can be done by using the command `birg init`. 
BiRG will then ask for basic information about the software and create a directory named after the software,
which contains two files called `meta.yaml` and `build.sh`.
These files are the initial recipe, that we will transform into the final recipe.

The init command will ask for the following informations:

- Name
- Version
- Source url
- A build strategy to use

Here is the initialization of kallisto:

.. code-block:: console
    
    $ birg init
    Package name: kallisto
    Version: 0.46.2
    Url to download the code: https://github.com/pachterlab/kallisto/archive/v0.46.2.tar.gz
    Choose the strategy that you use to run your code
    ['cmake', 'python2', 'python3']: cmake

++++++++++
The Recipe
++++++++++

The basic recipe created by `init`, can be found in the newly created directory called `kallisto` and should look like this:

.. code-block:: yaml
   :caption: kallisto/meta.yaml

    package:
       name: kallisto
       version: 0.46.2
    source:
       url: https://github.com/pachterlab/kallisto/archive/v0.46.2.tar.gz
       md5: a6257231c6b16cac7fb8ccff1b7cb334
    build:
       number: 0


.. code-block::
   :caption: kallisto/build.sh

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

Before using the recipe for kallisto as input to BiRG, we will add some tests to the `meta.yaml` file.
By adding tests, we makes sure that BiRG will try and find run-time dependencies as well as build-time dependencies.

.. code-block:: yaml
   :caption: kallisto/meta.yaml

    package:
       name: kallisto
       version: 0.46.2
    source:
       url: https://github.com/pachterlab/kallisto/archive/v0.46.2.tar.gz
       md5: a6257231c6b16cac7fb8ccff1b7cb334
    build:
       number: 0
    test:
       commands:
          - kallisto cite


We will also edit the the `build.sh`, as kallisto requires us to run autoreconf and to set some flags for cmake:

.. code-block:: 
   :caption: kallisto/build.sh

    #!/bin/bash

    cd ext/htslib
    autoreconf
    cd ../..

    mkdir -p $PREFIX/bin
    mkdir -p build
    cd build
    cmake -DCMAKE_INSTALL_PREFIX:PATH=$PREFIX .. -DUSE_HDF5=ON
    make
    make install


.. note::

    The recipe for kallisto can be found in our github repo `here <https://github.com/Hogfeldt/bioconda_recipe_gen/tree/master/examples/cmake/input>`_

++++++++++++
Recipe Build
++++++++++++

We are now ready to give our inital recipe as input to BiRG. The build command takes two required arguments as shown below:

.. code-block:: console
    
    $ birg build --help
    usage: birg build [-h] [-d] recipe_path {cmake,python2,python3}

    positional arguments:
      recipe_path           Path to folder with meta.yaml and build.sh templates
      {cmake,python2,python3}
                            The ? that you used when creating the template with
                            'init'

    optional arguments:
      -h, --help            show this help message and exit
      -d, --debug           Set this flag if you want to activate the debug mode.
                            This creates an debug.log file that contains all debug
                            prints

recipe_path: Is the path to the recipe directory which was created by running `birg init`.

strategy: Here you must tell BiRG which building strategy to use. BiRG currently supports three strategies: cmake, python2 and python3.

Here is an example on how BiRG is called for building kallisto:

.. code-block:: console
    
    $ birg build kallisto/ cmake

When BiRG is running it will print out a lot of text, this is the output from it's building process.
BiRG will also, sometimes, ask for your help, to determine which version of a dependency it should use.

When BiRG is done running it will tell you if it was able to build and run your software, and the output recipe can be found in the directory which was created by the `init` command.

Here is the final recipe for kallisto:

.. code-block:: yaml
   :caption: kallisto/meta.yaml

    package:
      name: kallisto
      version: 0.46.2
    source:
      url: https://github.com/pachterlab/kallisto/archive/v0.46.2.tar.gz
      md5: a6257231c6b16cac7fb8ccff1b7cb334
    build:
      number: 2
    test:
      commands:
      - kallisto cite
    requirements:
      build:
      - cmake
      - make
      - automake
      - {{ compiler('cxx') }}
      host:
      - hdf5
      run:
      - hdf5
      - zlib

    
.. code-block:: 
   :caption: kallisto/build.sh

    #!/bin/bash

    cd ext/htslib
    autoreconf
    cd ../..

    mkdir -p $PREFIX/bin
    mkdir -p build
    cd build
    cmake -DCMAKE_INSTALL_PREFIX:PATH=$PREFIX .. -DUSE_HDF5=ON
    make
    make install

Congratulation you can now add your recipe to Bioconda and share your software.
