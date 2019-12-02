import tempfile
import docker
import os

from bioconda_recipe_gen.utils import download_and_unpack_source
from bioconda_recipe_gen.filesystem import Filesystem


def run_setup_sdist(source_path, python_version, setup_filepath):
    client = docker.from_env()
    try:
        container = client.containers.run(
            "python:%s" % python_version,
            "python setup.py sdist",
            volumes={source_path: {"bind": "/mnt/source", "mode": "rw"}},
            working_dir=os.path.join("/mnt/source", setup_filepath),
            detach=True,
            user=os.getuid(),
        )
        result = container.wait()
        return True if result["StatusCode"] == 0 else False
    finally:
        container.remove()


def find_python_setup_directory(root_path):
    filesystem = Filesystem(root_path)
    setup_file_paths = filesystem.where_is_file_in_filesystem("setup.py")
    if setup_file_paths == []:
        return None
    setup_file_dir = setup_file_paths[0].replace("setup.py", "")
    if setup_file_dir.startswith("/"):
        setup_file_dir = setup_file_dir[1:]
    return setup_file_dir


def find_python_requirement_file(root_path):
    filesystem = Filesystem(root_path)
    requires_file_paths = filesystem.where_is_file_in_filesystem("requires.txt")
    if requires_file_paths == []:
        return None
    # TODO: Consider if there could be more than one requires.txt and how to
    #       choose the correct one.
    requires_path = requires_file_paths[0]
    if requires_path.startswith("/"):
        requires_path = requires_path[1:]
    return os.path.join(root_path, requires_path)


def add_requirements_from_file(recipe, requires_path):
    # TODO: Use conda to search if package exists
    requirements = list()
    with open(requires_path) as f:
        requirements = [req.replace("\n", "") for req in f.readlines()]
    print(requirements)
    for req in requirements:
        recipe.add_requirement(req, "run")
    recipe.write_recipe_to_meta_file()


def sdist_optimization(recipe):
    with tempfile.TemporaryDirectory() as tmpdir:
        source_path = download_and_unpack_source(recipe.url, tmpdir)
        setup_dir = find_python_setup_directory(source_path)
        if setup_dir != None:
            # TODO: Be smarter with python version
            run_setup_sdist(source_path, "3.5", setup_dir)
            requires_path = find_python_requirement_file(source_path)
            if requires_path != None:
                add_requirements_from_file(recipe, requires_path)
