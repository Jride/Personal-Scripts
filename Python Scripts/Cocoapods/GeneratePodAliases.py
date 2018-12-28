import sys
import os

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))

import itv_shell
import itv_argparser

### --- MAIN --- ###
def run(args = []):

    # Parse the arguments
    parser = itv_argparser.parser(
    os.path.dirname(__file__),
    '''Finds all cocoapod frameworks located in the Documents directory
    and exports each one by the name of the pod and it's corresponding path'''
    )
    args = parser.parse_args(args)

    swift_script = os.path.expandvars('$PYTHON_SCRIPTS') + "/Cocoapods/GeneratePodAliases.swift"
    itv_shell.run("swift '%s'" % swift_script)

if __name__ == "__main__":
    arguments = sys.argv[1:]
    run(arguments)
