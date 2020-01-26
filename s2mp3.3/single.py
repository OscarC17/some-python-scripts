import urllib.request
from bs4 import BeautifulSoup
import youtube_dl
import os
import shutil
import time

directory = os.getcwd()

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
                time.sleep(3)
                break
    except Exception as e:
        print("failed to download " + str(e))
    break
