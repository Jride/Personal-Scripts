import sys
import os
from os.path import expanduser

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))

import itv_argparser
import itv_filesystem

### --- MAIN --- ###

parser = itv_argparser.parser(
    os.path.dirname(__file__),
    '''
    Checks for new episodes to all your shows
    '''
)
args = parser.parse_args(sys.argv[1:])


home = expanduser("~")
download_show_cache = os.path.join(home, "cron_test.txt")
itv_filesystem.write_text_to_file("Running Cron...\n", download_show_cache, "a+")
