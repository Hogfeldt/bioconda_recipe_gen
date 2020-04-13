.. _tutorial:

========
Tutorial
========

To show how BiRG works, we will create a recipe for a software called netReg.
We will start with generating an initial recipe, with basic information about netReg.
This recipe will then be given as input to BiRG, which will find the necessary dependencies required to build, test and run the software.

We assume that you are using the docker image that we provide, but if you have installed BiRG from source, the tutorial still applies, just go directly to `Recipe Initilization`_.

++++++++++++++++++++++
Using the Docker Container
++++++++++++++++++++++

First we need to make sure that the docker container and the host system can communicate. This can be done by running `docker run`, with the following settings.

.. code-block:: console
    
    $ docker run -v /var/run/docker.sock:/var/run/docker.sock \
                 -v $PWD:/home \
                 -itd perhogfeldt/birg:latest

The first volume we added, with `-v`, is the unix socket that the docker client uses to talk with the docker server. We need to add this socket, since the container will need to spin up more containers, when it tries to build the software.
The second volume will bind the containers home direcetory to the host systems current directory, this will make sure that files can be shared.

The running container will spin up the container and detach, so that the container is running in the background. The command will return a container id, which we will use to send instructions to the container. The container id can also by found be running `docker ps`.

You can then run the BiRG commands mentioned in the rest of this tutorial with `docker exec`, the following way:

.. code-block:: console
    
    $ docker exec -it <container-id> <command>

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

Here is the initialization of netReg:

.. code-block:: console
    
    $ birg init
    Package name: netreg
    Version: 1.8.0
    Url to download the code: https://github.com/dirmeier/netReg/archive/v1.8.0.tar.gz
    Choose the strategy that you use to run your code
    ['cmake', 'python2', 'python3']: cmake

++++++++++
The Recipe
++++++++++

The basic recipe created by `init`, can be found in the newly created directory called `netreg` and should look like this:

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
   :caption: netreg/meta.yaml

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
   :caption: netreg/build.sh

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

Here is an example on how BiRG is called for building netreg:

.. code-block:: console
    
    $ birg build netreg/ cmake

When BiRG is running it will print out a lot of text, this is the output from it's building process.
BiRG will also, sometimes, ask for your help, to determine which version of a dependency it should use.

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
