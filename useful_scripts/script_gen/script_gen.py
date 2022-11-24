#!/usr/bin/env python3

import re
import json
import os
import sys
import argparse
from operator import itemgetter
from pathlib import Path
from collections import OrderedDict, defaultdict

PACKAGE_PARENT = "../run_burst"
script_dir = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(script_dir, PACKAGE_PARENT)))
from run_burst import parser as rb_parser
from options import options as rb_options


def read_json(file_path):
    """
    Reads json file and returns the dictionary that it returns
    :param file_path: path of json file to be read
    :return: json dictionary
    """
    try:
        with open(file_path) as db_file_handle:
            try:
                data = json.load(db_file_handle)
                return data
            except ValueError:
                print("ERROR: Invalid JSON file: " + str(file_path))
                exit(-1)
            except TypeError:  # NoneType
                print("WARN: Reading " + str(file_path) + " returned TypeErr")
                return None
    except IOError:
        print("Unable to open : " + str(file_path))
        return None


def write_json(file_path, data, sort=True):
    """
    Writes the json data to the specified file
    :param file_path: file path to write to
    :param data: json dictionary data input
    :param sort: Decides wether or not to sort the dictionary before writing
    :return:
    """
    try:
        with open(file_path, "w") as db_file_handle:
            json.dump(
                data, db_file_handle, sort_keys=sort, separators=(",", ": "), indent=4
            )
            db_file_handle.write(os.linesep)
    except IOError:
        print("Unable to open : " + str(file_path))
        return None


def list_db_template(base_dir, db_or_template="template", allow_print=True):
    """
    Function that lists valid regression templates, databases
    """
    _list = []
    valid_dbs = []
    file_extension = ".txt"
    if db_or_template == "database":
        file_extension = ".json"
        _list.append("all")
        db_repo_support_path = os.path.join(script_dir, "db_repo_support.json")
        valid_db_data = read_json(db_repo_support_path)
        try:
            repo = script_dir.split(os.sep)[-3]
        except IndexError:
            repo = None
        repo = repo if (repo == "burst" or repo == "mainline_burst") else None
        if valid_db_data and repo:
            valid_dbs = valid_db_data[repo]

    for filename in os.listdir(str(base_dir)):
        if filename.endswith(file_extension) and str(filename)[0] != "#":
            file_base, _ = os.path.splitext(filename)
            _list.append(file_base)
    if db_or_template == "database" and valid_dbs:
        _list = list(set(_list).intersection(set(valid_dbs)))
        _list.append("all")

    if allow_print:
        print("\nBase dir : " + base_dir)
        for item in _list:
            print(item)
        print("")
    return _list


# Global Settings
template_base_path = os.path.join(script_dir, "templates")
sub_temp_base = os.path.join(template_base_path, "sub_template")
template_list = list_db_template(template_base_path, "template", False)
sub_template_list = os.listdir(os.path.join(template_base_path, "sub_template"))
db_base_path = os.path.join(script_dir, "databases")
database_list = list_db_template(db_base_path, "database", False)
settings_file = os.path.join(script_dir, "settings_file.json")
outfile_path = os.path.join(script_dir, "outfile.json")
in_file_path = os.path.join(script_dir, "infile.json")

# Parse Arguments
parser = argparse.ArgumentParser(
    description="Script Generator",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    epilog="Queries Contact: burst_script_team@xilinx.com",
)

parser.add_argument(
    "--database",
    "-db",
    choices=database_list,
    default="test",
    help="Database to be used to generate cmd script",
)

parser.add_argument(
    "--database_path", "-dp", default=False, help="Custom base folder path for database"
)

parser.add_argument(
    "--cmd_path",
    "-cp",
    default=False,
    help="Custom base folder path for putting " "generated cmds files",
)

parser.add_argument(
    "--list_database", "-ld", action="store_true", help="List the existing databases "
)

parser.add_argument(
    "--list_template", "-lt", action="store_true", help="List the existing templates"
)

parser.add_argument(
    "--list_setup",
    "-ls",
    action="store_true",
    help="List the existing setups in " "user specified database",
)

parser.add_argument(
    "--create_form",
    "-cf",
    help="Create a form with user specified " "template list and inputs from infile",
)

parser.add_argument(
    "--print_form",
    "-pf",
    help="Print a form with user specified " "template list and inputs from infile",
)

parser.add_argument(
    "--add_setup",
    "-as",
    action="store_true",
    help="Adds the json data for a script " "form outfile to database",
)

parser.add_argument(
    "--renum_db", "-rn", action="store_true", help="Renumber a given database"
)

parser.add_argument(
    "--remove_setup",
    "-rs",
    type=int,
    help="Removes the json data for a script " "specified by setup number",
)

parser.add_argument(
    "--clean",
    "-cl",
    action="store_true",
    help="Remove the $SCRIPTS/cmd_scripts or $PWD/cmd_script" " dir",
)

parser.add_argument(
    "--apply_format",
    "-af",
    action="store_true",
    help="Format all the generated python script using black",
)

parser.add_argument(
    "--generate_profile",
    "-gp",
    choices=["all", "preempt", "non-preempt"],
    default=None,
    help="generates the regression profile for specified database (when script_gen.py"
    " is imported from another python script, it returns a dictionary of generated "
    "output with key = script path (relative) and value = command to run the script)",
)


class Setup(object):
    """
    Class that stores general setup and database information.
    """

    def __init__(self, args):
        if args.cmd_path:
            self.script_base_path = os.path.join(args.cmd_path, "cmd_scripts")
        elif os.getenv("SCRIPTS"):
            self.script_base_path = os.path.join(os.getenv("SCRIPTS"), "cmd_scripts")
        else:
            self.script_base_path = os.path.join(os.getcwd(), "cmd_scripts")
        try:
            if Path(args.database_path).is_dir():
                global db_base_path
                global database_list
                db_base_path = args.database_path
                database_list = list_db_template(db_base_path, "database", False)
        except TypeError:
            pass
        if (not Path(self.script_base_path).is_dir()) and self.script_base_path:
            mk_cmd = "mkdir --parents " + str(self.script_base_path)
            os.system(mk_cmd)
        self.db_name_list = []
        self.db_next_index = 0
        if args.database == "all":
            _database_list = database_list
            _database_list.remove("all")
            self.db_name_list = _database_list
        else:
            self.db_name_list.append(str(args.database))
        self.db_name = None
        self.db_file = None
        self.update_db_name()

    def update_db_name(self):
        self.db_name = self.db_name_list[self.db_next_index]
        self.db_file = os.path.join(db_base_path, (self.db_name + ".json"))
        self.db_next_index = self.db_next_index + 1

    def set_db_name(self, db_name):
        self.db_name = db_name
        self.db_file = os.path.join(db_base_path, (self.db_name + ".json"))
        self.db_next_index = self.db_name_list.index(self.db_name) + 1


class Script(object):
    """
    class equivalent to one cmd file information in database file
    """

    def __init__(self):
        self.num = None
        self.name = None
        self.script_location = None
        self.template_list = []
        self.db_name = None
        self.run_cmd = None


class Infile(object):
    """
    class with contents of infile.
    """

    def __init__(self):
        self.setup_name = None
        self.board = None
        self.dc = None
        self.si = None
        self.board_revision = None
        self.root_complex = None
        self.end_point = None
        self.lane_count = None
        self.proc = None
        self.project = None
        self.clk = None
        self.dp = None
        self.be = None
        self.ecc = None
        self.pre_empt = None

    def read_set(self):
        """
        Read the infile and set the equivalent database
        This function will need modification if new class of scripts are added.
        :return:
        """
        valid_setups = ["normal_setup", "pcie_setup"]
        d = read_json(in_file_path)
        self.setup_name = str(d["setup_name"]).lower()
        if not (self.setup_name in valid_setups):
            setups_string = ""
            for item in valid_setups:
                setups_string = setups_string + item + ", "
            print(
                "Error: Invalid value for setup_name in infile"
                "valid values are: \n" + setups_string
            )
            exit(-1)
        # common items
        self.project = check_input(d[self.setup_name]["project"])
        self.si = check_input(d[self.setup_name]["si"])
        self.proc = check_input(d[self.setup_name]["processor"])
        self.pre_empt = check_input(d[self.setup_name]["pre-emptable"])
        # normal setup
        if self.setup_name == "normal_setup":
            self.board = check_input(d[self.setup_name]["board"])
            self.board_revision = check_input(d[self.setup_name]["board_" "revision"])
            self.dc = check_input(d[self.setup_name]["daughter_card"])
            self.clk = check_input(d[self.setup_name]["clock"])
            self.dp = check_input(d[self.setup_name]["display_port"])
            self.be = check_input(d[self.setup_name]["big-endian"])
            self.ecc = check_input(d[self.setup_name]["ecc"])
        # pcie setup
        elif self.setup_name == "pcie_setup":
            self.root_complex = check_input(d[self.setup_name]["root_complex"])
            self.end_point = check_input(d[self.setup_name]["end_point"])
            self.lane_count = check_input(d[self.setup_name]["lane_count"])


def check_input(input_var):
    """
    Check if the input values in infile is valid and not empty.
    """
    if not input_var:
        return None
    elif str(input_var).lower() == "":
        return None
    else:
        return str(input_var)


def str_dict(in_dict_list):
    """
    Function that converts a dictionary to string based dictionary
    :param in_dict_list: input dictionary list
    :return: out dict - string dict with all objects converted to string
    """
    out_dict = {}
    for in_dict in in_dict_list:
        _sorted_items = sorted(in_dict.items(), key=itemgetter(0))
        for key, value in _sorted_items:
            out_dict[str(key)] = str(value)
    return out_dict

# Gopi - function to fill the keywords in the template files
def form_fill(rd_file_path, wr_file, db_keys, script):
    """
    Function that replaces the template key values with database values
    and writes it to the cmd file
    :param rd_file_path: template file
    :param wr_file: cmd file object
    :param db_keys:
    :param script: script class object
    """
    try:
        with open(rd_file_path, "r") as rd_file:
            for line in rd_file:
                matches_list = re.findall(r"<::.*::>", line)
                if matches_list:
                    for match_item in matches_list:
                        match_key, match_default = find_match_default(match_item)
                        sub_template_file = is_sub_template(match_key)
                        if sub_template_file:
                            try:
                                print_subtemplate(
                                    sub_template_file, wr_file, db_keys[match_key]
                                )
                            except KeyError:
                                continue
                        else:
                            try:
                                # Todo Check other special characters
                                if "$" in match_item:
                                    match_item_old = match_item
                                    match_item = re.sub("\$", "", match_item)
                                    line = line.replace(match_item_old, match_item)
                                line = re.sub(match_item, db_keys[match_key], line)
                            except KeyError:
                                if match_default:
                                    line = re.sub(match_item, match_default, line)
                                else:
                                    print(
                                        "Index Error:\n 1) No value for key "
                                        "'{}' in database \n 2) No default "
                                        "value for '{}' in template".format(
                                            match_key, match_key
                                        )
                                    )
                            wr_file.write(line)
                else:
                    wr_file.write(line)
    except IOError:
        print("Unable to open : " + str(rd_file_path))

# Gopi - if in the subtemplate <::.*::> exists then replace them with actual values otherwise write as it is into cmd_Script
def print_subtemplate(sub_template_file, wr_file, value):
    """
    Writes the given sub-template to the cmd file (wr_file). It can also replace
    parameters defined in the sub-template.
    :param sub_template_file: sub template file object
    :param wr_file: cmd file
    :param value: yes/no, or dictionary
    :return:
    """
    use_subtemplete = 0
    if type(value) == dict:
        use_subtemplete = 1
    elif type(value) == str:
        if value.lower() == "yes":
            use_subtemplete = 1
    if use_subtemplete:
        try:
            with open(sub_template_file) as rd_file:
                for line in rd_file:
                    matches_list = re.findall(r"<::.*::>", line)
                    if matches_list:
                        for match_item in matches_list:
                            match_key, match_default = find_match_default(match_item)
                            if type(value) == dict:
                                try:
                                    line = re.sub(match_item, value[match_key], line)
                                except KeyError:
                                    if match_default:
                                        line = re.sub(match_item, match_default, line)
                                    else:
                                        print(
                                            "Index Error:\n 1) No value for "
                                            "key '{}' in database \n 2) No "
                                            "default value for '{}' in "
                                            "subtemplate".format(match_key, match_key)
                                        )
                            elif type(value) == str:
                                if match_default:
                                    line = re.sub(match_item, match_default, line)
                                else:
                                    print(
                                        "ERROR: Subtemplate {} doesn't"
                                        " have default value".format(sub_template_file)
                                    )
                            wr_file.write(line)
                    else:
                        wr_file.write(line)
        except IOError:
            print("ERROR: Unable to open {}".format(sub_template_file))
            exit(-1)


def is_sub_template(match_key):
    """
    Checks if the match is a sub template and returns sub template path or None
    :param match_key:
    :return:
    """
    sub_template_file = None
    if "__SUB_TEMPLATE__" in match_key:
        sub_string = match_key.rstrip("__").lstrip("__")
        sub_template_file = sub_string.split("__")[1]
        sub_template_file = os.path.join(sub_temp_base, (sub_template_file + ".txt"))
        # print(match_key + ' : ' + sub_template_file)
    return sub_template_file


def find_match_default(match_item):
    """
    Check for default value of a parameter.
    :param match_item:
    :return:
    """
    match_key = match_item.lstrip("<::").rstrip("::>")
    match_default = None
    if len(match_key.split(":=:")) == 2:
        match_pair = match_key.split(":=:")
        match_key = match_pair[0]
        match_default = match_pair[1]
    return match_key, match_default


def create_setup_file(_script, _script_file, do_format=False):
    """
    Function that generates a cmd script using script class object loaded
    with a script json entry from database file
    :param _script: script class object
    :param _script_file: output file path to generate cmd file
    :param do_format: Boolean to decide wether to format the generated script
    :return: None
    """
    try:
        with open(_script_file, "w") as wr_file:
            for item in _script.template_list:
                template_path = os.path.join(template_base_path, item["template_file"])
                form_fill(template_path, wr_file, item["keys"], _script)
    except IOError:
        print("Unable to open : " + str(_script_file))
    # Apply black format formatting for the generated python scripts
    _, ext = os.path.splitext(_script_file)
    os.chmod(_script_file,0o755)
    if ext == ".py" and do_format:
        os.system(f"black {_script_file}")
    return


def reset_infile():
    """
    Reset the infile to default values and create a file if it does not exist.
    :return:
    """
    if os.path.exists(settings_file):
        settings = read_json(settings_file)
        settings_data = settings["infile_defaults"]
        if os.path.exists(in_file_path):
            in_data = read_json(in_file_path)
            for key in settings_data:
                try:
                    in_data[key] = settings_data[key]
                except KeyError:
                    print(
                        "setting file and infile key mismatch"
                        "\nDelete the infile and try again"
                    )
        else:
            in_data = settings_data
        write_json(in_file_path, in_data, False)
    else:
        print("ERROR: settings file missing \n {}".format(settings_file))
        exit(-1)
    return


def read_infile():
    """
    Function that reads the infile and returns the script name and folder path.
    This function will need modification if new class of scripts are added.
    :return:
    """
    folder_string = ""
    file_string = ""
    x = Infile()
    x.read_set()
    # Create folder path
    if x.project:
        folder_string = folder_string + x.project
    if x.si:
        folder_string = folder_string + "/" + x.si
    if x.setup_name == "pcie_setup":
        folder_string = folder_string + "/pcie"
    elif x.board:
        folder_string = folder_string + "/" + x.board
        if x.board_revision:
            folder_string = folder_string + "_" + x.board_revision
        if x.dc:
            folder_string = folder_string + "_" + x.dc
    # Create file path
    if x.setup_name == "pcie_setup":
        if x.root_complex:
            file_string = file_string + "_" + x.root_complex
        if x.end_point:
            file_string = file_string + "_" + x.end_point
        if x.lane_count:
            file_string = file_string + "_" + x.lane_count
        if x.proc:
            file_string = file_string + "_" + x.proc
        if x.pre_empt:
            file_string = file_string + "_preempt"
    elif x.setup_name == "normal_setup":
        if x.board:
            file_string = file_string + x.board
        if x.board_revision:
            file_string = file_string + "_" + x.board_revision
        if x.dc:
            file_string = file_string + "_" + x.dc
        if x.proc:
            file_string = file_string + "_" + x.proc
        if x.be:
            file_string = file_string + "_be"
        if x.ecc:
            file_string = file_string + "_ecc"
        if x.dp:
            file_string = file_string + "_dp"
        if x.clk:
            file_string = file_string + "_" + x.clk
        if x.pre_empt:
            file_string = file_string + "_preempt"
    return [folder_string, file_string]


def print_db_form(
    template_file_path, sorted_keys, match_dict, last, space, print_write=print
):
    """
    Function that prints/ writes json template for one template file
    :param template_file_path: template_file_path location
    :param sorted_keys: list of identified keys from template
    :param match_dict: dictionary of defaults with keys in sorted_keys list
    :param last: Boolean: last template or not
    :param space: space string
    :param print_write: print or write function
    :return: None
    """
    print_write(
        space
        + "{\n"
        + space
        + " " * 1
        + '"template_file" : "'
        + os.path.split(template_file_path)[1]
        + '",\n'
    )
    print_write(space + " " * 1 + '"keys" : {\n')
    for item in sorted_keys:
        default_val = "INPUT"
        if match_dict[item]:
            default_val = match_dict[item]
        if sorted_keys.index(item) == len(sorted_keys) - 1:
            print_write(
                space + " " * 5 + '"' + item + '"' + ' : "' + str(default_val) + '"\n'
            )
        else:
            print_write(
                space + " " * 5 + '"' + item + '"' + ' : "' + str(default_val) + '",\n'
            )
    print_write(space + " " * 4 + "}\n")
    if last:
        print_write(space + "}\n")
    else:
        print_write(space + "},\n")

# Gopi read the template and store in dictionary
#
def process_db_form(rd_file_path, print_write, tabs=1, last=False):
    """
    Function that read the template file and prints or writes json entry to file
    :param rd_file_path: template file path to read
    :param print_write: print or write function
    :param tabs: Number of tabs = 4 x space
    :param last: Boolean: last template or not
    :return: None
    """
    space = " " * (tabs * 4)
    match_dict = {}
    try:
        with open(rd_file_path, "r") as rd_file:
            key_set = set()
            for line in rd_file:
                matches_list = re.findall(r"<::.*::>", line)
                if matches_list:
                    for match_item in matches_list:
                        match_key, match_default = find_match_default(match_item)
                        # print(match_key + " : " + str(match_default))
                        key_set.add(match_key)
                        # Gopi - this is equivalent to .get()
                        if not (match_key in match_dict):
                            match_dict[match_key] = match_default
                        elif not match_dict[match_key]:  # None
                            match_dict[match_key] = match_default
            if key_set:
                sorted_keys = []
                for item in key_set:
                    sorted_keys.append(item)
                sorted_keys.sort()
                if print_write != print:
                    print_db_form(
                        rd_file_path, sorted_keys, match_dict, last, space, print_write
                    )
                else:
                    print_db_form(rd_file_path, sorted_keys, match_dict, last, space)
    except IOError:
        print("Unable to open : " + str(rd_file_path))

# Gopi - prints the template form if no template is mentioned otherwise it will create new one based outline.json
def print_template_form(print_template_list, print_write=print):
    """
    Function that prints to console or writes json data required for database
    :param print_template_list: list of template names
    :param print_write: print or write to file function
    :return: None
    """
    [script_loc, script_title] = read_infile()
    script_num = "99999"
    space_index = 1
    space = " " * (space_index * 4)
    if print_write != print:
        print_write("{\n")
    print_write('"' + script_title + '": {\n')
    print_write(space + '"form" : [\n')
    for item in print_template_list:
        template_path = os.path.join(template_base_path, item + ".txt")
        last = False
        if item == print_template_list[-1]:
            last = True
        process_db_form(template_path, print_write, space_index + 1, last)
    print_write(space + "],\n")
    print_write(space + '"script_location" : "' + script_loc + '",\n')
    print_write(space + '"script_num" : "' + script_num + '"\n')
    print_write("}\n")
    if print_write != print:
        print_write("}\n")


def print_setup_numbers(setup):
    """
    Function that lists the setup numbers in a given database file
    :param setup:
    :return:
    """
    db_data = read_json(setup.db_file)
    print("Database : " + setup.db_name)
    print("Setup Num : Setup Name")
    sorted_items = sorted(db_data.items(), key=itemgetter(0))
    for key, value in sorted_items:
        print("{:9} : {}".format(str(value["script_num"]), key))
    print("")


def get_user_approval(string):
    signature = input(string + "yes(y)/no(n):")
    if signature.lower() == "yes" or signature.lower() == "y":
        return True
    else:
        return False


def re_number_setups(data):
    """
    Function that reorders the setup numbers
    :param data: database json file data
    :return:
    """
    setup_number = 1
    sorted_data = OrderedDict(sorted(data.items()))
    for item in sorted_data:
        sorted_data[item]["script_num"] = setup_number
        setup_number = setup_number + 1
    return sorted_data


def create_print_form(args, print_create="print"):
    """
    Create/ Print the database form entry for adding a new cmd script.
    :param args:
    :param print_create:
    :return:
    """
    if print_create == "create":
        templates = args.create_form.split(",")
    else:
        templates = args.print_form.split(",")
    if all(item in template_list for item in templates):
        if print_create == "print":
            print_template_form(templates)
        if print_create == "create":
            try:
                with open(outfile_path, "w", newline="\n") as outfile:
                    print_template_form(templates, outfile.write)
            except IOError:
                print("Error: Unable to open file" + str(outfile_path))
        exit(0)
    else:
        print("Invalid syntax/input for --create_form/-pf option")
        print(
            "Syntax:\n"
            "-pf <template1>,<template2>... \nOR\n"
            "-create_form <template1>,<template2>... "
        )
        print("To list available templates:\n --list_template OR -lt")
        exit(-1)


def create_runcmd(script_name, s_data):
    """Generate the run_burst.py command to launch the script

    Args:
        script_name (str): Name of the script being generated
        s_data (dict): single script data from database
    return cmd (str): run-burst.py cmd to launch the script
    """
    dir_list = s_data["script_location"].split("/")
    name_list = script_name.split("_")
    is_python = False
    try:
        project, silicon, _ = dir_list
    except ValueError:
        is_python, project, silicon, _ = dir_list

    # Reverse the 1:n run_burst parser options to a n:1 dictionary
    cmd_key_dict_inv = {}
    for key, val in rb_options.items():
        for item in val:
            cmd_key_dict_inv[item] = key

    cmd = f"-pj {project} -si {silicon}"
    if "rc" in name_list and "pcie" in dir_list:  # PCIe script
        cmd += f" -rc {name_list[0]}"
        name_list = name_list[2:]
        ep_index = name_list.index("ep")
        if ep_index == 1:  #  Everest SPP and silicon
            cmd += f" -ep {name_list[0]}"
            name_list = name_list[2:]
        elif ep_index == 2:  # pcie legacy
            if name_list[0] in rb_options["bridge_rc"]:
                cmd += f" --bridge_rc {name_list[0]}"
            elif name_list[0] in rb_options["config_rc"]:
                cmd += f" --config_rc {name_list[0]}"
            cmd += f" -ep {name_list[1]}"
            if name_list[3] in rb_options["bridge_ep"]:
                cmd += f" --bridge_ep {name_list[3]}"
                name_list = name_list[4:]
            else:
                name_list = name_list[3:]
        elif ep_index == 3:  # General PCIe
            cmd += f" --bridge_rc {name_list[0]}"
            cmd += f" --config_rc {name_list[1]}"
            cmd += f" -ep {name_list[2]}"
            cmd += f" --bridge_ep {name_list[4]}"
            name_list = name_list[5:]
        else:  # Non pcie script
            raise Exception(f"Unexpected script name :{script_name}")
        cmd_key_dict_inv_keys = cmd_key_dict_inv.keys()
        name_list_tmp = [x for x in name_list]
        for item in name_list:
            if item in cmd_key_dict_inv_keys:
                cmd += f" --{cmd_key_dict_inv[item]} {item}"
                name_list_tmp.remove(item)
        name_list = name_list_tmp
    else:
        board = name_list[0] if name_list[0] != "remus" else "ep108"
        name_list = name_list[1:]
        cmd += f" -b {board}"
        name_list_tmp = [x for x in name_list]
        cmd_key_dict_inv_keys = cmd_key_dict_inv.keys()
        for item in name_list:
            if item in cmd_key_dict_inv_keys:
                cmd += f" --{cmd_key_dict_inv[item]} {item}"
                name_list_tmp.remove(item)
        name_list = name_list_tmp
    switch_list = ["be", "ospi", "ecc", "dp", "bup", "bupcoh"]
    for switch in switch_list:
        if switch in name_list:
            cmd += f" -{switch}"
            name_list.remove(switch)
    if "preempt" in name_list:
        cmd += " -pm 1"
        name_list.remove("preempt")
    if is_python:
        cmd += " -py"

    # Makes sure that the cmd files generated are recognizable by run_burst
    if len(name_list):
        print("Illegal name: {script_name} : {name_list} unrecognized!")
    return cmd


def list_unused_templates():
    template_use_count = defaultdict(lambda: 0)
    sub_template_use_count = defaultdict(lambda: 0)
    unused_templates, unused_sub_templates = [], []
    db_files = [f for f in database_list if f != "all"]
    for db in db_files:
        db_path = os.path.join(db_base_path, db + ".json")
        db_data = read_json(db_path)
        for script in db_data:
            for i, entry in enumerate(db_data[script]["form"]):
                template = db_data[script]["form"][i]["template_file"]
                template_use_count[template] += 1
                for key, value in entry["keys"].items():
                    if "__SUB_TEMPLATE__" in key and (
                        str(value).lower() == "yes" or type(value) == dict
                    ):
                        mod_key = key.replace("__SUB_TEMPLATE__", "")
                        sub_template = mod_key.replace("__", "")
                        sub_template_use_count[sub_template + ".txt"] += 1
    warn_str1, warn_str2 = "", ""
    for template in template_list:
        if not template_use_count[template + ".txt"]:
            unused_templates.append(template)
            warn_str1 += f"{template}.txt "
    for sub_template in sub_template_list:
        if not sub_template_use_count[sub_template]:
            unused_sub_templates.append(sub_template.replace(".txt", ""))
            warn_str2 += f"{sub_template} "
    if warn_str1:
        print(f"WARN: Unused template(s): {warn_str1}")
    if warn_str2:
        print(f"WARN: Unused sub-template(s): {warn_str2}")
    return unused_templates, unused_sub_templates


def remove_unused_subtemplate_refs(unused_subs):
    sub_string_list = [f"__SUB_TEMPLATE__{sub}__" for sub in unused_subs]
    db_files = [f for f in database_list if f != "all"]
    for db in db_files:
        db_path = os.path.join(db_base_path, db + ".json")
        db_data = read_json(db_path)
        for script in db_data:
            for i, key_data in enumerate(db_data[script]["form"]):
                data_tmp = dict(key_data["keys"])
                for key, _ in key_data["keys"].items():
                    if key in sub_string_list:
                        data_tmp.pop(key)
                db_data[script]["form"][i]["keys"] = data_tmp
        write_json(db_path, db_data)
    return


def main(args):
    """
    Main function that runs when the script is executed.
    :param args: user input
    :return: Script's base path.
    """
    # Gopi - Setup() basically will set the database name and it's path
    setup = Setup(args)
    script = Script()
    # Create infile if it does not exist
    # Gopi - overwrites infile based on settings.json if infile.json already exists otherwise just create with the content inside the settings.json
    if not os.path.exists(in_file_path):
        reset_infile()
    # Remove the cmd_scripts folder if required
    if args.clean:
        clean_cmd = "rm -rf " + str(setup.script_base_path)
        os.system(clean_cmd)
        exit(0)
    # List the available templates and/or databases
    if args.list_template or args.list_database:
        if args.list_template:
            list_db_template(template_base_path, "template", True)
        if args.list_database:
            list_db_template(db_base_path, "database", True)
        exit(0)
    if args.list_setup:
        for db_item in setup.db_name_list:
            setup.set_db_name(db_item)
            print_setup_numbers(setup)
        exit(0)

    # Gopi - We are re-numbering the setup_num mentioned in database
    # Doubt
    if args.renum_db:
        if os.path.exists(setup.db_file):
            db_data = read_json(setup.db_file)
            db_data = re_number_setups(db_data)
            write_json(setup.db_file, db_data)
        else:
            print("ERROR! No database specified to renumber")
            exit(-1)
        exit(0)
    # Generate json entry for creating a script using list of user specified
    # templates
    # Gopi - basically it will create a JSON file for us if we specify
    elif args.print_form:
        create_print_form(args)
    elif args.create_form:
        create_print_form(args, "create")
    # Add setup data from outfile to specified database
    elif args.add_setup:
        if os.path.exists(outfile_path) and os.path.exists(setup.db_file):
            outfile_data = read_json(outfile_path)
            db_data = read_json(setup.db_file)
            if outfile_data != {}:
                db_data.update(outfile_data)
            db_data = re_number_setups(db_data)
            write_json(setup.db_file, db_data)
            write_json(outfile_path, {})
            exit(0)
        else:
            print("Error: database or outfile missing")
            exit(-1)
    # Gopi - Give setup number to delete the particular setup
    elif args.remove_setup:
        if not os.path.exists(setup.db_file):
            print("ERROR: database file missing: " + setup.db_file)
            exit(-1)
        else:
            db_data = read_json(setup.db_file)
            exit_flag = False
            for item in db_data:
                if db_data[item]["script_num"] == args.remove_setup:
                    user_string = (
                        "Remove setup {}={} from database '{}'."
                        "\nImportant Warn! Cannot be undone!!"
                        "\nIt is advisable to create a backup of "
                        "database '{}.json'"
                        "\nDo you agree to proceed ? ".format(
                            args.remove_setup, item, setup.db_name, setup.db_name
                        )
                    )
                    user_approval = get_user_approval(user_string)
                    if user_approval:
                        del db_data[item]
                        _db_data = db_data
                        _db_data = re_number_setups(_db_data)
                        write_json(setup.db_file, _db_data)
                        exit_flag = 1
                        break
                    else:
                        print(
                            "User declined permission"
                            " to remove setup {} from"
                            " database {}".format(args.remove_setup, setup.db_name)
                        )
            if exit_flag:
                exit(0)
            else:
                print(
                    "Setup Number: {} not present "
                    "in database: {}".format(args.remove_setup, setup.db_name)
                )
            exit(-1)
    # Gopi - We can generate profiles along with JSON files also
    if args.generate_profile:
        gp = args.generate_profile
        for db_item in setup.db_name_list:
            setup.set_db_name(db_item)
            if args.database == "all":
                profile_name = "all.profile"
                file_mode = "w" if setup.db_name_list.index(db_item) == 0 else "a+"
            else:
                if not os.path.exists(setup.db_file):
                    print("ERROR: database file missing: " + setup.db_file)
                    continue
                profile_name = db_item + ".profile"
                file_mode = "w"
            db_data = read_json(setup.db_file)
            if not db_data:  # Empty json data, skip it.
                continue
            # Create the scripts cmd required to run the .cmd file
            script_cmd_dict = {}
            script_cmd_list = []
            for script_name in db_data:
                script_num = db_data[script_name]["script_num"]
                script_loc1 = db_data[script_name]["script_location"]
                # Gopi - name should be in the options.py
                run_cmd = create_runcmd(script_name, db_data[script_name])
                # Gopi - if we give -ve number then it will comment out the cmd generated
                if script_num < 0:
                    run_cmd = "# " + run_cmd
                else:
                    extension = ".py" if ("bf2/" in script_loc1) else ".cmd"
                    script_path = os.path.join(script_loc1, script_name) + extension
                if (gp == "all" or gp == "preempt") and ("-pm " in run_cmd):
                    script_cmd_list.append(run_cmd)
                    script_cmd_dict[f"{script_path}"] = run_cmd
                elif (gp == "all" or gp == "non-preempt") and ("-pm " not in run_cmd):
                    script_cmd_list.append(run_cmd)
                    script_cmd_dict[f"{script_path}"] = run_cmd
        # If imported from another script return dict, and if called directly as script
        # generate a profile file.
        if __name__ == "script_gen":
            return script_cmd_dict
        else:
            with open(profile_name, file_mode) as pfile:
                for line in script_cmd_list:
                    pfile.write(f"{line}\n")
            print(f"Generated : {profile_name}")
            exit(0)
    # Find un-used templates and subtemplates files, remove unused subtemplate references
    _, unused_subs = list_unused_templates()
    if unused_subs:
        remove_unused_subtemplate_refs(unused_subs)

    # Add a run_burst parser choices validity check
    parser_dict = vars(rb_parser.parse_args(args=[]))
    parser_dict_keys = set(parser_dict.keys())
    rb_option_keys = set(rb_options.keys())
    is_superset = parser_dict_keys.issuperset(rb_option_keys)
    if not is_superset:
        raise Exception("options.py->options has illegal keys")
    # Check if the database file exist
    if not os.path.exists(setup.db_file):
        print("ERROR: database file missing: " + setup.db_file)
        exit(-1)
    # Create the scripts for the specified database
    # Gopi - Actual script creation?
    for db_item in setup.db_name_list:
        setup.set_db_name(db_item)
        db_data = read_json(setup.db_file)
        if not db_data:  # Empty json data, skip it.
            continue
        # Create the scripts specified in the database file
        for script_name in db_data:
            script.db_name = db_item
            script.name = script_name
            script.template_list = db_data[script_name]["form"]
            script.num = db_data[script_name]["script_num"]
            script.script_location = os.path.join(
                setup.script_base_path, db_data[script_name]["script_location"]
            )
            script.run_cmd = create_runcmd(script_name, db_data[script_name])
            db_data[script_name]["cmd"] = script.run_cmd
            is_dir = Path(script.script_location).is_dir()
            if not is_dir:
                mk_cmd = "mkdir --parents " + str(script.script_location)
                os.system(mk_cmd)
            extension = ".py" if ("bf2/" in script.script_location) else ".cmd"
            script_file = os.path.join(script.script_location, script_name) + extension
            if script.num > 0:  # Add -(minus) in script_num to not generate it
                # Gopi - Core logic to generate the cmd script
                create_setup_file(script, script_file, args.apply_format)
        write_json(setup.db_file, db_data, False)
    print(f"Generated scripts in : {setup.script_base_path}")
    return setup.script_base_path


if __name__ == "__main__":
    try:
        usr_args = parser.parse_args()
        main(usr_args)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        exit(0)
