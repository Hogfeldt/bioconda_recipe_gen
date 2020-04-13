.. _installation:

============
Installation
============

BiRG is heavily dependent on Docker, therefore make sure that you have Docker installed and working. We use Docker to ensure that the environment, which we are building and testing in, is clean and reproducible.

If you don't have Docker installed, we recommend that you follow the Docker installation guide which can be found at the following link:
`Docker installation guide <https://docs.docker.com/install/>`_

When Docker is installed, we recommend following the post-installation step "Manage Docker as a non-root user", the linux guide can be found `here <https://docs.docker.com/install/linux/linux-postinstall/>`_ .
Setting up Docker to be used as non-root, will make it possible to run BiRG without escalated privileges.

+++++++++++++++
From Docker Hub
+++++++++++++++

We have prepared a docker image for running BiRG, the docker image can be downloaded from Docker Hub, by running the following command:

.. code-block:: console

    $ docker pull perhogfeldt/birg:latest

That's it you can now proceed to the tutorial, for instructions on how to use the docker image.

:ref:`tutorial`

+++++++++++
From Source
+++++++++++

First clone the BiRG recipe from github with the following command:

.. code-block:: console

    $ git clone https://github.com/birgorg/birg.git



Next up is to create a conda environment from the environment.yml file in the BiRG repo folder:

.. code-block:: console

    $ cd birg
    $ conda env create -f environment.yml
    $ conda activate birg

.. note::

    There might be problems with creating an environment from the environment.yml file, if you are on a mac.
    A solution is to run the following commands instead:

    .. code-block::

        conda create -n birg python=3.6
        conda activate birg
        conda install bioconda-utils docker-py gitdb2=2.0.5



Install it with the setup.py and check if BiRG is installed correctly by running -h:

.. code-block:: console

    $ python setup.py install
    $ birg -h
