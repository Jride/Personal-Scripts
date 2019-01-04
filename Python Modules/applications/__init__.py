import sys
import glob
import re
import os

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))

import itv_shell
import itv_logger

def open_textedit(file):
    itv_shell.run('open -a TextEdit "%s"' % file)

def open_sourcetree(path = None):
    if path:
        itv_shell.run('open -a SourceTree "%s"' % args.path)
    else:
        itv_shell.run('open -a SourceTree "."')
