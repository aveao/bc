#/bin/python3
import requests
import re
import argparse
import subprocess
import sys

# Let's initialize argparse
parser = argparse.ArgumentParser(description='Downloads all songs from bandcamp authors,'\
    'needs bandcamp-dl (pip install bandcamp_downloader) to function outside --dry-run.')
parser.add_argument('url', metavar='url', type=str, nargs='+',
                    help='Artist\'s url')
parser.add_argument('--dry-run', dest='dryrun', action='store_true',
                    help='makes a dry run (just lists albums and tracks, doesn\'t download)')
args = parser.parse_args()

regex = r"<a href=\"/((album|track)/[a-zA-Z0-9-]*)\">"
url_num = 0

for url in args.url:
    url_num += 1
    print(f"Now working on {url} ({url_num}/{len(args.url)})")
    artist_html = requests.get(f"{url}/music").text
    matches = re.findall(regex, artist_html, re.MULTILINE)
    matches = list(set(matches)) # removes duplicates
    match_num = 0
    for match in matches:
        match_num += 1
        
        final_url = f"{url}/{match[0]}"
        print(f"\n{match_num}/{len(matches)}: {final_url}") # starts with \n because fucking stderr
        if not args.dryrun:
            p1 = subprocess.Popen(["echo", "y"], stdout=subprocess.PIPE)
            subprocess.call(f"bandcamp-dl {final_url}", stdin=p1.stdout, shell=True)
