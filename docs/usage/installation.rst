.. _installation:

============
Installation
============

This is a quick guide on how to start generating recipes with BiRG.

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


.. note::

    It's important that you read the next section, if Docker is not installed and working on your system.

++++++++++++
Dependencies
++++++++++++

To run BiRG you also to have Docker installed and working. We use Docker to ensure that the
environment, which we are building and testing in is clean an reproducible.

We recommend that you follow the Docker installation guide which can be found at the following link:
`Docker installation guide <https://docs.docker.com/install/>`_

When Docker is installed, we recommend following the post-installation step "Manage Docker as a non-root user", the linux guide kan be found `here <https://docs.docker.com/install/linux/linux-postinstall/>`_ .
Setting up Docker to be used as non-root, will make it possible to run BiRG without escalated privileges.

