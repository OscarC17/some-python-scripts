import urllib.request
from bs4 import BeautifulSoup
import youtube_dl
import os
import shutil
import argparse

parser = argparse.ArgumentParser(description='-s [search] -f [format]')
parser.add_argument('-s', action="store", dest="search")
parser.add_argument('-f', action="store", dest="format")
parser.parse_args(['-s', '-f'])

oformat = 0
directory = os.getcwd()

opts, args = getopt.getopt(argv,"hi:o:",["format="])
for opt, arg in opts:
    if opt in ("-f", "--format"):
        if arg == webm:
            oformat = 1
        
textToSearch = input("Search: ")
query = urllib.parse.quote(textToSearch)
url = "https://www.youtube.com/results?search_query=" + query
response = urllib.request.urlopen(url)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
    print('downloading ' + 'https://www.youtube.com' + vid['href'])
    try:
        class MyLogger(object):
            def debug(self, msg):
                pass

            def warning(self, msg):
                pass

            def error(self, msg):
                print(msg)

        def my_hook(d):
            if d['status'] == 'finished':
                print('Done downloading now converting ...')
        if oformat == 1:
            ydl_opts = {}
        else:
            ydl_opts = {'format': 'bestaudio/best',
                        'noplaylist': True,
                        'outtmpl': os.path.join(directory, '%(title)s.%(ext)s'),
                        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3',
                                            'preferredquality': '128', }], 'logger': MyLogger(),
                        'progress_hooks': [my_hook], }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(
                'https://www.youtube.com' + vid['href'],
                download=False  # We just want to extract the info
            )
            print(result['duration'])
            if "channel" not in vid['href']:
                ydl.download(['https://www.youtube.com' + vid['href']])
            else:
                print("channel detected, cancelling.")
                break
    except Exception as e:
        print("failed to download " + str(e))
    break
