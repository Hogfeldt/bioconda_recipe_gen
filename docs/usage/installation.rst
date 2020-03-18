.. _installation:

============
Installation
============

This is a quick guide on how to start generating recipes with BiRG.
BiRG is simply installed using the following conda commands:

.. code-block:: console

    $ conda config --add channels ???
    $ conda create -n myproject python=3.5 ???
    $ source activate myproject

.. note::

    It's important that you read the next section, if Docker is not installed and working on your system.

++++++++++++
Dependencies
++++++++++++

BiRG depends on a various set of packages, which will be installed alongside BiRG, 
if you install it with conda. With one exception! 

To run BiRG you will need to have Docker installed and working. We use Docker to ensure that the
environment, which we are building and testing in is clean an reproducible.

We recommend that you follow the Docker installation guide which can be found at the following link:
`Docker installation guide <https://docs.docker.com/install/>`_

When Docker is installed, we recommend following the post-installation step "Manage Docker as a non-root user", the linux guide kan be found `here <https://docs.docker.com/install/linux/linux-postinstall/>`_ .
Setting up Docker to be used as non-root, will make it possible to run BiRG without escalated privileges.

