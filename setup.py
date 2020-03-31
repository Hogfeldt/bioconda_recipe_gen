from setuptools import setup, find_packages

# Package meta-data
NAME = "bioconda_recipe_gen"
DESCRIPTION = "Recipe generator for Bioconda"

setup(
    name=NAME,
    description=DESCRIPTION,
    packages=find_packages("src"),
    package_dir={"": "src"},
    test_suite="test",
    install_requires=['docker-py', 'gitdb2==2.0.5'],
    entry_points={
         'console_scripts': ['bioconda-recipe-gen = bioconda_recipe_gen.cli:start'],
    },
    include_package_data=True,
)

