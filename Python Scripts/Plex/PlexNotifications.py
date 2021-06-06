import sys
import os

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))
sys.path.append(os.path.expandvars('$PYTHON_MODULES'))

import itv_argparser
import itv_filesystem
import notifications

### --- MAIN --- ###
parser = itv_argparser.parser(
    os.path.dirname(__file__),
    '''
    Sends push notifications for newly downloaded episodes
    '''
)
args = parser.parse_args(sys.argv[1:])

home = expanduser("~")
download_show_cache = os.path.join(home, "torrents/.show_cache")

notifications.send("My custom title", "Line one\nLine two")

if itv_filesystem.does_file_exist(download_show_cache):
    file = open(download_show_cache, "r")
    show_cache = file.readlines()