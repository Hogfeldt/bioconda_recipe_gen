from . import make_dict

build_tools = ['cmake', 'make', 'autoconf']
libs = ['hdf5', 'zlib']

class Recipe:
    """ Represents a meta.yaml recipe file """

    def __init__(self, path_to_meta_file):
        self.path_to_meta_file = path_to_meta_file
        self.recipe_dict = make_dict.make_dict_from_meta_file(path_to_meta_file)

    def write_recipe_to_meta_file(self):
        """ Writes the current recipe_dict into the meta.yaml file """
        make_dict.make_meta_file_from_dict(self.recipe_dict, self.path_to_meta_file)

    def add_requirement(self, pack_name, type_of_requirement):
        """ Adds a package to the list of requirements in the recipe

        Args:
            pack_name: Name of the package to add
            type_of_requirement: Specify were you want to add the package "host", "build" or "run"
        """
        if type_of_requirement == 'build' and pack_name in libs:
            return
        elif type_of_requirement == 'host' and pack_name in build_tools:
            return
        curr_list = self.recipe_dict["requirements"].setdefault(type_of_requirement, [])
        if pack_name not in curr_list:
            curr_list.append(pack_name)
