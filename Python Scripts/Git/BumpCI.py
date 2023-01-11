import sys
import os

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))

import itv_shell
import itv_argparser

### --- MAIN --- ###

parser = itv_argparser.parser(
os.path.dirname(__file__),
'''
Pushes an empty commit in an attempt to trigger something on the CI integration
'''
)
args = parser.parse_args(sys.argv[1:])

itv_shell.run('git commit --allow-empty -m "Bump CI"')
itv_shell.run('git push')
