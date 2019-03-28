import jinja2
import ruamel_yaml
import re
import os

compilers_in_build = set()

def make_meta_file_from_dict(recipe_dict, path_to_meta_file):
    with open(path_to_meta_file, "w") as meta_file:
        ruamel_yaml.round_trip_dump(recipe_dict, meta_file)


def make_dict_from_meta_file(path):
    try:
        document = dynamic_jinja_to_static_ruamel_yaml(path)
        recipe_dict = ruamel_yaml.safe_load(document)
        # add compilers to the dict
        for comp in compilers_in_build:
            recipe_dict["requirements"]["build"].append(comp)
        
        return recipe_dict
    except ruamel_yaml.YAMLError as exc:
        print("Couldn't create a dictionary from the meta.ruamel_yaml. Error: {}".format(exc))


def convert_line(line, jinja_configs):
    """helper function: converts {% to #% and {{ to <{.

    'greedy' check that seems to be enough
    (there might still be some other elements
    in the line that has {{ ... }} or {% ... %} around it) """

    if any(conf in line for conf in jinja_configs):
        line = line.replace("{{", "<{")
        line = line.replace("}}", "}>")
        line = line.replace("{%", "#%")
        line = line.replace("%}", "%#")

    return line


def convert_jinja_syntax(file_to_convert):
    """ Converts the jinja syntax in a ruamel_yaml file,
    into a syntax that can be used by ruamel"""

    new_file = ""
    jinja_configs = {"compilter"}

    with open(file_to_convert, 'r') as fp:
        for line in fp:
            if "{%" in line:
                result = re.search('{% set (.*)=', line)
                jinja_configs.add(result.group(1).strip())

            converted_line = convert_line(line, jinja_configs)
            if re.search('{{ compiler(.*)}}', converted_line):
                # violates jinja2's syntax and is therefore saved
                # to be added after the dict is made.
                cleaned_line = converted_line.strip()[2:]
                compilers_in_build.add(cleaned_line)
            else:
                new_file += converted_line
            
    
    with open(file_to_convert, 'w') as fp:
        fp.write(new_file)
    

def dynamic_jinja_to_static_ruamel_yaml(filename):
    tmp_file = 'tmp.ruamel_yaml'

    convert_jinja_syntax(filename)
    
    data = ruamel_yaml.round_trip_load(open(filename))
    with open(tmp_file, 'w') as fp:
        ruamel_yaml.round_trip_dump(data, fp)

    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath='.'),
        trim_blocks=True,
        block_start_string='#%', block_end_string='%#',
        variable_start_string='<{', variable_end_string='}>')

    try:
        recipe_dict = environment.get_template(tmp_file).render()
        os.remove("tmp.ruamel_yaml")
        return recipe_dict
    except:
        print("ERROR in dynamic_jinja_to_static_ruamel_yaml")
        return ""
