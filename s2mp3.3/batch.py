from urllib import parse, request
from bs4 import BeautifulSoup
from youtube_dl import YoutubeDL
from os import path, mkdir, getcwd, listdir
from pandas import read_csv

# initialise variables
input_list = []
song_vector = []
artist_vector = []
answer_check = False

# scan for csv files in input directory
for file in listdir('input'):
    if file.endswith(".csv"):
        input_list.append(path.join('input', file))
if not input_list:
    print("no .csv files were found in the input folder, closing")
    exit()

# let user set preferences for download
setting_lyric = input("append lyric to search term? (y/n): ")
max_seconds = int(input("max seconds for song, default 600: ") or "600")

# read Track Name and Artist Name columns from csv and put them in a list
for x in range(0, len(input_list)):
    csv = read_csv(input_list[x])
    column = csv['Track Name']
    for y in range(0, len(column)):
        song_vector.append(column[y])
    print(song_vector)
for x in range(0, len(input_list)):
    csv = read_csv(input_list[x])
    column = csv['Artist Name']
    for y in range(0, len(column)):
        artist_vector.append(column[y])
    print(artist_vector)

# combine song and lyric lists
for x in range(0, len(song_vector)):
    if not song_vector[x].startswith('#'):
        if (setting_lyric == "y") | (setting_lyric == "Y"):
            song_vector[x] = song_vector[x] + " lyrics"
        song_vector[x] = artist_vector[x].split(',')[0] + " " + song_vector[x]

# search for the video on youtube
    query = parse.quote(song_vector[x])
    url = "https://www.youtube.com/results?search_query=" + query
    response = request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        if ("channel" not in vid['href']) & ("user" not in vid['href']):
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
                        print('Done downloading ' + song_vector[x] + ', now converting ...')


                ydl_opts = {'format': 'bestaudio/best',
                            'noplaylist': True,
                            'outtmpl': path.join('output', '%(title)s.%(ext)s'),
                            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3',
                                                'preferredquality': '128', }], 'logger': MyLogger(),
                            'progress_hooks': [my_hook], }
                with YoutubeDL(ydl_opts) as ydl:
                    result = ydl.extract_info(
                        'https://www.youtube.com' + vid['href'],
                        download=False  # We just want to extract the info
                    )
                    print('downloading ' + 'https://www.youtube.com' + vid['href'])
                    print(result['duration'])
                    if result['duration'] <= max_seconds:
                        ydl.download(['https://www.youtube.com' + vid['href']])
                    else:
                        print('video too long, skipping')
            except Exception as e:
                print("failed to download " + song_vector[x] + str(e))
            break
