import sys
import os

sys.path.append(os.path.expandvars('$PYTHON_SCRIPTS'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))

import itv_shell

loginHookPath = os.path.expandvars('$PYTHON_SCRIPTS') + "/login/loginHook.py"
itv_shell.run('python3 "%s"' % loginHookPath)
