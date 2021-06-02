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
args = parser.parse_args(sys.argv[1:])

def run(command):
    itv_shell.run("ssh -t plex@plex-server.myddns.me \"transmission-remote --auth transmission:transmission %s\"" % (command))

media_types = {
    "TV Show": "tv_shows",
    "Movie": "movies"
}
media_options = list(media_types.keys())
selected_index = itv_shell.choose_from_list("What type of media?", media_options)
selected_media = media_options[selected_index]
folder_name = media_types[selected_media]

input("\nCopy magenet URL to clipboard and press enter")

magnet_link = pc.paste()

run("-w ~/torrents/%s/ -a '%s'" % (folder_name, magnet_link))
