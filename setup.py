from setuptools import setup, find_packages

# Package meta-data
NAME = "bioconda_recipe_gen"
DESCRIPTION = "Recipe generator for Bioconda"

# What packages are required for this module to be executed
REQUIRED = []

setup(
    name=NAME,
    description=DESCRIPTION,
    packages=find_packages("src"),
    package_dir={"": "src"},
    test_suite="test",
    install_requires=REQUIRED,
    entry_points={
         'console_scripts': ['bioconda-recipe-gen = bioconda_recipe_gen.bioconda_recipe_gen:main'],
    },
)

