import sys
import os
import subprocess

subprocess.run('python3 "%s"' % loginHookPath, shell = True)

loginHookPath = os.path.expandvars('$PYTHON_SCRIPTS') + "/login/loginHook.py"
print(loginHookPath)

subprocess.run('python3 "%s"' % loginHookPath, shell = True)
