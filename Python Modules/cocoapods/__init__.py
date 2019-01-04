import sys
import glob
import re
import os

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))

import itv_shell
import itv_logger
import itv_filesystem

def generate_pod_aliases():
    swift_script = os.path.expandvars('$PYTHON_SCRIPTS') + "/Cocoapods/GeneratePodAliases.swift"
    itv_shell.run("swift '%s'" % swift_script)
