import jinja2
from ruamel import yaml
import re
import os


def make_meta_file_from_dict(recipe_dict, path_to_meta_file):
    with open(path_to_meta_file, "w") as meta_file:
        yaml.round_trip_dump(recipe_dict, meta_file)


def make_dict_from_meta_file(path):
    try:
        document = dynamic_jinja_to_static_yaml(path)
        return yaml.safe_load(document)
    except yaml.YAMLError as exc:
        print("Couldn't create a dictionary from the meta.yaml. Error: {}".format(exc))


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

    # remove conda's own 'compiler' syntax (that the yaml parser wont accept)
    # TODO: This code is reuse from some older code. Seems like there were a bug with the 'result' not being used
    if "{{" in line:
        result = re.search('{{ compiler(.*)}}', line)
        line = ""

    return line


def convert_jinja_syntax(file_to_convert):
    """ Converts the jinja syntax in a yaml file,
    into a syntax that can be used by ruamel"""

    new_file = ""
    jinja_configs = set()

    with open(file_to_convert, 'r') as fp:
        for line in fp:
            if "{%" in line:
                result = re.search('{% set (.*)=', line)
                jinja_configs.add(result.group(1).strip())

            new_file += convert_line(line, jinja_configs)
    
    with open(file_to_convert, 'w') as fp:
        fp.write(new_file)
    

def dynamic_jinja_to_static_yaml(filename):
    tmp_file = 'tmp.yaml'

    convert_jinja_syntax(filename)
    
    data = yaml.round_trip_load(open(filename))
    with open(tmp_file, 'w') as fp:
        yaml.round_trip_dump(data, fp)

    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath='.'),
        trim_blocks=True,
        block_start_string='#%', block_end_string='%#',
        variable_start_string='<{', variable_end_string='}>')

    try:
        recipe_dict = environment.get_template(tmp_file).render()
        os.remove("tmp.yaml")
        return recipe_dict
    except:
        print("ERROR in dynamic_jinja_to_static_yaml")
        return ""
