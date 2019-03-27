# bioconda_recipe_gen
Recipe generator for Bioconda

## Getting Started
### Prerequisites
You need to install conda on your computer. This can be downloaded from: https://docs.conda.io/en/latest/miniconda.html

### Setup
After if have cloned this repo (bioconda_recipe_gen):
* cd into bioconda_recipe_gen, and clone the [bioconda-recipes](https://github.com/bioconda/bioconda-recipes.git) repo 
* Create a new conda environement with the following command: conda create -n bioconda_recipe_gen python=3.6
* Open the environment with: conda activate bioconda_recipe_gen
* Set channels:
	* conda config --add channels conda-forge
	* conda config --add channels bioconda
* Install bioconda-utils: conda install bioconda-utils=0.15.10
* You can now run the script: python3 bioconda_recipe_gen.py

### How to run the script
First, run the following command: python3 setup.py develop
You can now run the program by calling: bioconda-recipe-gen
And you can run the tests by calling: python3 setup.py test
