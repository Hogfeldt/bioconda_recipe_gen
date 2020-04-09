from setuptools import setup, find_packages

# Package meta-data
NAME = "birg"
DESCRIPTION = "Bioconda Recipe Generator (BiRG) is an heuristic approach to automaticly generating recipes for Bioconda"

setup(
    name=NAME,
    description=DESCRIPTION,
    packages=find_packages("src"),
    package_dir={"": "src"},
    test_suite="test",
    install_requires=['docker>=2.0.0', 'gitdb2==2.0.5', 'validators', 'gitpython'],
    entry_points={
         'console_scripts': ['birg = birg.cli:start'],
    },
    include_package_data=True,
)

