import sys
import os

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))
sys.path.append(os.path.expandvars('$PYTHON_MODULES'))

import itv_shell
import itv_argparser
import mac_utils

### --- MAIN --- ###

parser = itv_argparser.parser(
os.path.dirname(__file__),
'Sets up this macs plist defaults for applications'
)
args = parser.parse_args(sys.argv[1:])

mac_utils.setup_defaults()
