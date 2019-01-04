import sys
import os

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))
sys.path.append(os.path.expandvars('$PYTHON_MODULES'))

import itv_shell
import itv_argparser
import cocoapods

### --- MAIN --- ###

parser = itv_argparser.parser(
os.path.dirname(__file__),
'''Finds all cocoapod frameworks located in the Documents directory
and exports each one by the name of the pod and it's corresponding path'''
)
args = parser.parse_args(sys.argv[1:])

cocoapods.generate_pod_aliases()
