import sys
import os
import untangle
import re
from os.path import expanduser

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))

import itv_shell
import itv_argparser
import itv_filesystem

def run(command):
    itv_shell.run("transmission-remote --auth transmission:transmission -w /hdd/torrents/tv_shows %s" % (command))

class Torrent:
    name = None
    season_episode = None
    magnet_720 = None
    magnet_1080 = None

    @property
    def id(self):
        if self.season_episode is None:
            return self.name
        else:
            return self.name + "-" + self.season_episode

    def print_desc(self):
        print(self.name)
        print(self.season_episode)
        if self.magnet_720 is None:
            print("720: False")
        else:
            print("720: True")
        if self.magnet_1080 is None:
            print("1080: False")
        else:
            print("1080: True")

    def cache_name(self):
        if self.season_episode is None:
            return self.name + "\n"
        else:
            return self.name + " - " + self.season_episode + "\n"

### --- MAIN --- ###

parser = itv_argparser.parser(
    os.path.dirname(__file__),
    '''
    Checks for new episodes to all your shows
    '''
)
args = parser.parse_args(sys.argv[1:])


download_show_cache = "/hdd/torrents/.show_cache"
show_cache = []

if itv_filesystem.does_file_exist(download_show_cache):
    file = open(download_show_cache, "r")
    show_cache = file.readlines()
    # print(show_cache)

url = 'http://showrss.info/user/255222.rss?magnets=true&namespaces=true&name=null&quality=null&re=null'

o = untangle.parse(url)
torrents = {}
for item in o.rss.channel.item:
    title = item.title.cdata.lower().replace("'", "")
    link = item.link.cdata
    if link:
        torrent = Torrent()

        season_search = re.search(r"(s\d\de\d\d)", title)
        if season_search is not None:
            title_search = re.split(r"(s\d\de\d\d)", title)
            torrent.name = title_search[0].strip()
            torrent.season_episode = season_search.group()

        if "720p" in title:
            torrent.magnet_720 = link
            if season_search is None:
                title_search = title.split("720p")
        elif "1080p" in title:
            torrent.magnet_1080 = link
            if season_search is None:
                title_search = title.split("1080p")
        else:
            continue

        torrent.name = title_search[0].strip()

        if torrent.id in torrents:
            if torrent.magnet_1080 is None:
                torrents[torrent.id].magnet_720 = link
            else:
                torrents[torrent.id].magnet_1080 = link
        else:
            torrents[torrent.id] = torrent

new_shows = []
for key in torrents.keys():
    torrent = torrents[key]
    # torrent.print_desc()

    if torrent.cache_name() in show_cache:
        continue

    if torrent.magnet_1080 is None:
        print("Downloading 720p >> " + torrent.id)
        run("-a '%s'" % (torrent.magnet_720))
    else:
        print("Downloading 1080p >> " + torrent.id)
        run("-a '%s'" % (torrent.magnet_1080))

    new_shows.append(torrent.cache_name())

write_show_cache = "".join(new_shows)
itv_filesystem.write_text_to_file(write_show_cache, download_show_cache, "a+")
