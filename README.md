[![Build Status](https://travis-ci.org/Hogfeldt/bioconda_recipe_gen.svg?branch=master)](https://travis-ci.org/Hogfeldt/bioconda_recipe_gen)

# bioconda_recipe_gen
Recipe generator for Bioconda

## Getting Started
### Prerequisites
You need to install conda on your computer. This can be downloaded from: https://docs.conda.io/en/latest/miniconda.html
You should have a clone of the [bioconda-recipes](https://github.com/bioconda/bioconda-recipes.git) repo. 

#### Mac specific
Since we are using bioconda-utils, the program requires mac users to use the macOS 10.9 SDK. The reason for this is explained [here](https://docs.conda.io/projects/conda-build/en/latest/resources/compiler-tools.html). The link also tells how to set this up and where to download the SDK.

### Setup
After you have cloned this repo (bioconda_recipe_gen):
* Set channels:
	* `conda config --add channels conda-forge`
	* `conda config --add channels bioconda`
* Create a new conda environement with the following command: `conda create -n bioconda_recipe_gen python=3.6`
* Open the environment with: `conda activate bioconda_recipe_gen`
* Install bioconda-utils: `conda install bioconda-utils docker-py`

### How to run the script and tests as developer
* First, run the following command: `python setup.py develop`
* You can now run the program by calling: `bioconda-recipe-gen -h` to get an overview of the arguments needed to run the program.
* You can run the tests by calling: `python setup.py test`
