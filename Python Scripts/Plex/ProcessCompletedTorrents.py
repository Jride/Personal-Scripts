import sys
import os
from os.path import expanduser
import re
import glob
from pprint import pprint

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))
sys.path.append(os.path.expandvars('$PYTHON_MODULES'))

import itv_argparser
import notifications
import torrents_utils

def normalize_show_name(show_name):
    """Apply custom normalization rules for specific show names."""
    # Convert to lowercase first
    show_name = show_name.lower()
    
    # Special case for Chicago PD
    show_name = re.sub(r'chicago\s+p\s+d', 'chicago pd', show_name)
    
    # Special case for 9-1-1 (original series)
    # Check if it's the original 9-1-1 (not Lone Star)
    if show_name == '9-1-1' or show_name == '911':
        show_name = '9-1-1 (2018)'
    
    # Add more special cases here as needed
    
    return show_name

def extract_show_info(filename):
    """Extract show name, season, and episode information from filename."""
    # Remove common prefixes and suffixes
    filename = re.sub(r'^www\.[^/]+/\s*-\s*', '', filename)
    filename = re.sub(r'\[.*?\]', '', filename)
    filename = re.sub(r'\(.*?\)', '', filename)
    
    # Try to match S##E## pattern
    season_ep_match = re.search(r'[Ss](\d{1,2})[Ee](\d{1,2})', filename)
    if not season_ep_match:
        return None, None, None
    
    season = season_ep_match.group(1)
    episode = season_ep_match.group(2)
    
    # Extract show name - everything before the season/episode pattern
    show_name = filename[:season_ep_match.start()].strip()
    # Clean up show name
    show_name = re.sub(r'[._]', ' ', show_name)
    show_name = re.sub(r'\s+', ' ', show_name)
    show_name = show_name.strip()
    
    # Apply custom normalization rules
    show_name = normalize_show_name(show_name)
    
    return show_name, season, episode

def process_tv_show_file(media_file, media_folder, dryrun=False):
    """Process a TV show file and move it to the appropriate show folder."""
    show_name, season, episode = extract_show_info(media_file.file_name)
    
    if not all([show_name, season, episode]):
        print(f"Could not extract show info from: {media_file.file_name}")
        return False
    
    # Create show folder if it doesn't exist
    show_folder = os.path.join(media_folder, show_name)
    if not os.path.exists(show_folder):
        if dryrun:
            print(f"[DRY RUN] Would create folder: {show_folder}")
        else:
            os.makedirs(show_folder)
    
    # Create new filename in format: show.name.s01e01.ext
    ext = os.path.splitext(media_file.file_name)[1].lower()
    new_filename = f"{show_name}.s{int(season):02d}e{int(episode):02d}{ext}"
    destination = os.path.join(show_folder, new_filename)
    
    if dryrun:
        print(f"\n[DRY RUN] Processing file: {media_file.file_name}")
        print(f"  Show Name: {show_name}")
        print(f"  Season: {season}")
        print(f"  Episode: {episode}")
        print(f"  Would move: {media_file.file_path}")
        print(f"  To: {destination}")
        return True
    
    # Move the file
    return torrents_utils.move_file(media_file.file_path, destination, dryrun)

### --- MAIN --- ###
parser = itv_argparser.parser(
    os.path.dirname(__file__),
    '''
    Checks for completed torrents, then renames and moves them into the correct plex media foldders
    '''
)
parser.add_argument('-mediaType', help='show, movie, kids_show, kids_movie')
parser.add_argument('--dryrun', help='Run the script to show what actions will happen first', action="store_true")
parser.add_argument('--skipcleanup', help='Skips deleting the torrent folder', action="store_true")
parser.add_argument('--single', help='Process only one torrent folder at a time', action="store_true")
args = parser.parse_args(sys.argv[1:])

TORRENT_MEDIA_FOLDER = "/hdd/torrents"
torrentFolderName = "tv_shows"

if args.mediaType == "movie":
    torrentFolderName = "movies"

if args.mediaType == "kids_show":
    torrentFolderName = "kids_shows"

if args.mediaType == "kids_movie":
    torrentFolderName = "kids_movies"

TORRENT_MEDIA_FOLDER = os.path.join(TORRENT_MEDIA_FOLDER, torrentFolderName)

MEDIA_FOLDER = os.path.join("/hdd", "Media")
# "TV Shows"

mediaFolderName = "TV_Shows"

if args.mediaType == "movie":
    mediaFolderName = "Movies"

if args.mediaType == "kids_show":
    mediaFolderName = "Kids/TV Shows"

if args.mediaType == "kids_movie":
    mediaFolderName = "Kids/Movies"

MEDIA_FOLDER = os.path.join(MEDIA_FOLDER, mediaFolderName)

IS_MOVIE = False
if args.mediaType == "movie" or args.mediaType == "kids_movie":
    IS_MOVIE = True

completed_torrents = []
all_torrents = torrents_utils.torrent_folders(TORRENT_MEDIA_FOLDER)
response = torrents_utils.result("-l")
lines = response.splitlines()

if args.verbose:
    print(all_torrents)

# Removes header and footer from the printed table
del lines[0]
del lines[-1]

for index, line in enumerate(lines):
    text = line.strip()
    text = re.sub('(.) (.)', r'\1>>>space<<<\2', text)
    text = re.sub(' +', ' ', text)
    properties = text.split(' ')

    torrent = torrents_utils.Torrent(
        properties[0].strip().replace('>>>space<<<', ' '),
        properties[-1].strip().replace('>>>space<<<', ' '),
        properties[2].strip().replace('>>>space<<<', ' '),
        properties[1].strip().replace('>>>space<<<', ' ')
    )

    if args.verbose:
        torrent.print_desc()

    folder = torrent.folder.lower()
    torrent.name = torrents_utils.get_title(folder)

    # Only add the completed ones
    if torrent.is_done:
        completed_torrents.append(torrent)

    # Remove any processed torrent from the all torrents list
    if torrent.folder in all_torrents:
        all_torrents.remove(torrent.folder)

# Add any untracked completed torrents to the list
for torrent_folder in all_torrents:

    torrent = torrents_utils.Torrent(
        None,
        torrent_folder,
        None,
        None
    )

    folder = torrent_folder.lower()
    torrent.name = torrents_utils.get_title(folder)
    completed_torrents.append(torrent)

# Get all media files from torrents folder
types = ('*.avi', '*.mp4', '*.mkv', '*.flv', '*.mov', '*.wmv')
media_files = []
for files in types:
    search = os.path.join(TORRENT_MEDIA_FOLDER, "**")
    search = os.path.join(search, files)
    media_files.extend(glob.glob(search, recursive=True))

if args.verbose:
    pprint(media_files)

# Build up media files info
for torrent in completed_torrents:
    found_media = []
    for file_path in media_files:
        if torrent.folder in file_path:

            # print(file_path)
            # print(torrent_folder)
            file_name_chunks = file_path.split("/")
            file_name = file_name_chunks[-1]

            # print(file_name)
            media = torrents_utils.Media(file_path, file_name)
            found_media.append(media)

    torrent.media_list = found_media

    if args.verbose:
        torrent.print_media_list()

# Print summary of what will be processed
print(f"\nFound {len(completed_torrents)} completed torrents to process")
if args.single:
    print("Single torrent mode: Will process only the first torrent folder")

# Process Completed Torrents Only
processed_count = 0
for torrent in completed_torrents:
    if not torrent.media_list:
        print("No media for torrent")
        continue

    print(f"\nProcessing torrent: {torrent.folder}")
    
    if torrent.identifier is not None:
        if args.dryrun:
            print(f"[DRY RUN] Would remove torrent: {torrent.identifier}")
        else:
            torrents_utils.remove_torrent(torrent.identifier, args.dryrun)

    new_media = False
    for media_file in torrent.media(args.mediaType):
        if IS_MOVIE:
            destination = os.path.join(MEDIA_FOLDER, media_file.file_name)
            if args.dryrun:
                print(f"[DRY RUN] Would move movie:")
                print(f"  From: {media_file.file_path}")
                print(f"  To: {destination}")
            new_media = torrents_utils.move_file(media_file.file_path, destination, args.dryrun)
        else:
            # Process TV shows with the new function
            new_media = process_tv_show_file(media_file, MEDIA_FOLDER, args.dryrun)

    if new_media:
        if IS_MOVIE:
            message = "Movie finished downloading: " + torrent.name
            if args.dryrun:
                print(f"[DRY RUN] Would send notification: {message}")
            else:
                notifications.send("Movie Download Complete", message)
        else:
            message = "New episode(s) available for " + torrent.name
            if args.dryrun:
                print(f"[DRY RUN] Would send notification: {message}")
            else:
                notifications.send("New Episode Available", message)

    torrent_folder = os.path.join(TORRENT_MEDIA_FOLDER, torrent.folder)
    if args.dryrun:
        print(f"[DRY RUN] Would delete folder: {torrent_folder}")
    else:
        torrents_utils.delete_folder(torrent_folder, args.dryrun, args.skipcleanup)
    
    processed_count += 1
    if args.single and processed_count >= 1:
        print("\nSingle torrent processed. Stopping.")
        break
