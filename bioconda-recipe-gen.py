import subprocess
import os
import sys
from shutil import copyfile, rmtree

def add_pack_to_host(recipe_path, pack_name):
    with open(recipe_path, 'r') as meta_file:
        in_file = meta_file.readlines()

    out_file = []
    for line in in_file:
        out_file.append(line)
        if('host' in line):
            out_file.append('       - ' + pack_name)
    
    with open(recipe_path, 'w') as meta_file:
        meta_file.writelines(out_file)


def bioconda_utils_build(name, wd):
    os.chdir('./bioconda-recipes')
    proc = subprocess.run(['bioconda-utils', 'build', 'recipes/', 'config.yml', '--packages', 'kallisto2'], encoding='utf-8', stdout=subprocess.PIPE )
    
    os.chdir(wd)
    return proc


def main():
    # Setup variables
    name = 'kallisto2'
    src = 'https://github.com/pachterlab/kallisto/archive/v0.45.0.tar.gz'
    path = './bioconda-recipes/recipes/' + name
    wd = os.getcwd()
    os.mkdir(path)

    # Copy recipe to into Bioconda
    copyfile('./recipes/meta.yaml', path+'/meta.yaml')
    copyfile('./recipes/build.sh', path+'/build.sh')

    proc = bioconda_utils_build(name, wd)
    print("return code: " + str(proc.returncode)+'\n')
    if(proc.returncode != 0):
        # Check for dependencies
        for line in proc.stdout.split('\n'):
            line_norma = line.lower()
            if 'missing' in line_norma:
                print(line_norma)
                if 'hdf5' in line_norma: 
                    add_pack_to_host(path+'/meta.yaml', 'hdf5')
    else:
        print('Build succeded')
        sys.exit(0)
    
    proc = bioconda_utils_build(name, wd)
    for line in proc.stdout.split('\n'):
        print(line)

    # clean up
    rmtree(path)

if __name__=='__main__':
    main()
