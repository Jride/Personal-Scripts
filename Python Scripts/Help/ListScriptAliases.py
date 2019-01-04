import sys
import os
import re
import glob

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))

import itv_shell
import itv_logger
import itv_string_utils
import itv_argparser

def find_alias(line):
    return itv_string_utils.find_between_str("alias ", "=", line)

# Returns the parent directories name for the provided path
# /path/to/my/file.ext => my
def parent_dir_for_path(path):
    split_path = path.split('/')
    return split_path[len(split_path) - 2]

# Turns a flat array into a nested array with the given number of colums
# [1,2,3,4,5,6] => 3 cols => [[1,2,3],[4,5,6]]
def make_column_data(cols, arr):
    result = []
    row = []

    for item in arr:
        row.append(item)
        if len(row) == cols:
            result.append(row)
            row = []

    if len(row) > 0:
        result.append(row)

    return result

# Prints a nested array as colums
# [[1,2,3],[4,5,6]] =>
# 1  2  3
# 4  5  6
def print_column_data(data):
    # Find the max word length used to determine our column width
    col_width = max(len(word) for row in data for word in row) + 2  # padding
    for row in data:
        print("".join(word.ljust(col_width) for word in row))

# Gathers all the values (which are lists) of the dictionary and prints them
def print_dictionary_values(dict):
    all_values = []
    for values in dict.values():
        all_values = all_values + values

    col_data = make_column_data(3, all_values)
    print_column_data(col_data)

### --- MAIN --- ###

parser = itv_argparser.parser(
os.path.dirname(__file__),
'''
This script provides you with a list of all aliases for your Script repository
separated by category. It can be quite useful when there is large resource of
scripts and you forget how to call them and what they are for.
'''
)
args = parser.parse_args(sys.argv[1:])

data = {}

# Recursively finds all the alias files located in the Python Scripts folder
itv_logger.print_verbose("Aliases found in python scripts folder ---->")
for filename in glob.glob(os.path.expandvars('$PYTHON_SCRIPTS') + "/**/alias", recursive=True):
    itv_logger.print_verbose(filename)
    category = parent_dir_for_path(filename)
    data[category] = []

    alias = open(filename)
    for line in alias:
        if "alias" in line:
            data[category].append(find_alias(line))

script_categories = list(data.keys())
options = ["All"] + script_categories
choice = itv_shell.choose_from_list("Select a script category", options)

if choice == 0:
    print("********  All Scripts  ********")
    print_dictionary_values(data)
else:
    chosen_category = script_categories[choice-1]
    print("********  %s Scripts ********" % chosen_category)
    arr = make_column_data(3, data[chosen_category])
    print_column_data(arr)

print("")
