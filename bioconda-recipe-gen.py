import subprocess
import os
import sys
from shutil import copyfile, rmtree

def main():
    # Setup variables
    name = 'kallisto2'
    src = 'https://github.com/pachterlab/kallisto/archive/v0.45.0.tar.gz'
    path = './bioconda-recipes/recipes/' + name
    os.mkdir(path)

    # Copy recipe to into Bioconda
    copyfile('./recipes/meta.yaml', path+'/meta.yaml')
    copyfile('./recipes/build.sh', path+'/build.sh')

    # Run Bioconda-utils
    subprocess.run(['ls','-l'])
    
    # clean up
    rmtree(path)

if __name__=='__main__':
    main()
