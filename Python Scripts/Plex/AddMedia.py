import sys
import os
import pyperclip as pc

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))

import itv_shell
import itv_argparser

### --- MAIN --- ###

parser = itv_argparser.parser(
    os.path.dirname(__file__),
    '''
    Start download a torrent via a magnet url
    '''
)
parser.add_argument('--show', help='Adds tv show', action="store_true")
parser.add_argument('--movie', help='Adds move', action="store_true")
parser.add_argument('--magnet', help='magnet link')
args = parser.parse_args(sys.argv[1:])

def run(command):
    itv_shell.run("ssh -t plex@plex-server.myddns.me -p 8888 \"transmission-remote --auth transmission:transmission %s\"" % (command))

if args.show:
    folder_name = "tv_show"
elif args.movie:
    folder_name = "movies"
else:
    media_types = {
        "TV Show": "tv_shows",
        "Movie": "movies"
    }
    media_options = list(media_types.keys())
    selected_index = itv_shell.choose_from_list("What type of media?", media_options)
    selected_media = media_options[selected_index]
    folder_name = media_types[selected_media]

if args.magnet:
    magnet_link = args.magnet
else:
    input("\nCopy magenet URL to clipboard and press enter")
    magnet_link = pc.paste()

run("-w ~/torrents/%s/ -a '%s'" % (folder_name, magnet_link))
