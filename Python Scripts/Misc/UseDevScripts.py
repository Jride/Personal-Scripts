import sys
import os
import glob

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))

import itv_shell
import itv_argparser

### --- MAIN --- ###

parser = itv_argparser.parser(
os.path.dirname(__file__),
'''
Changes the current terminal window to use the development scripts (both personal and ITV)
'''
)
args = parser.parse_args(sys.argv[1:])

dev_scripts = os.path.expandvars('$DEV_SCRIPTS')
itv_dev_scripts = os.path.expandvars('$ITV_DEV_SCRIPTS')

itv_shell.run('export PYTHON_SCRIPTS="%s/Python Scripts"' % dev_scripts)
itv_shell.run('export PYTHON_MODULES="%s/Python Modules"' % dev_scripts)
itv_shell.run('export PYTHON_CORE_MODULES="%s/Python Core Modules"' % dev_scripts)
itv_shell.run('export PYTHON_SUPPORTING_SCRIPTS="%s/Supporting Scripts"' % dev_scripts)

itv_shell.run('export ITV_PYTHON_SCRIPTS="%s/Python Scripts"' % itv_dev_scripts)
itv_shell.run('export ITV_PYTHON_MODULES="%s/Python Modules"' % itv_dev_scripts)
itv_shell.run('export ITV_PYTHON_CORE_MODULES="%s/Python Core Modules"' % itv_dev_scripts)
itv_shell.run('export ITV_PYTHON_SUPPORTING_SCRIPTS="%s/Supporting Scripts"' % itv_dev_scripts)

for alias in glob.glob(os.path.expandvars('$PYTHON_SCRIPTS') + "/**/alias", recursive=True):
    itv_shell.run('source "%s"' % alias)

for alias in glob.glob(os.path.expandvars('$ITV_PYTHON_SCRIPTS') + "/**/alias", recursive=True):
    itv_shell.run('source "%s"' % alias)

print("Personal and ITV scripts now pointing to development...\n")
