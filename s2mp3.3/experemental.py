from urllib import parse, request
from bs4 import BeautifulSoup
from pytube import YouTube
from os import path, mkdir, getcwd, listdir
from pandas import read_csv
from mutagen.mp3 import MP3  
from mutagen.easyid3 import EasyID3  
import mutagen.id3  
from mutagen.id3 import ID3

# initialise variables
input_list = []
song_vector = []
artist_vector = []
album_vector = []
answer_check = False
name = ''

# create output folder
if not path.exists('output'):
    mkdir('output')

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
for x in range(0, len(input_list)):
    csv = read_csv(input_list[x])
    column = csv['Album Name']
    for y in range(0, len(column)):
        album_vector.append(column[y])
print(album_vector)

# combine song and lyric lists / main program loop
for x in range(0, len(song_vector)):
    print("downloading song " + str(x+1) + " of " + str(len(song_vector))+ ', '+ song_vector[x])
    if not song_vector[x].startswith('#'):
        if (setting_lyric == "y") | (setting_lyric == "Y"):
            song_vector[x] = song_vector[x] + " lyric video"

# search for the video on youtube
    query = parse.quote(song_vector[x])
    url = "https://www.youtube.com/results?search_query=" + query
    response = request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        if not vid['href'].startswith("https://googleads.g.doubleclick.net/"):
            if ("channel" not in vid['href']) & ("user" not in vid['href']):
                try:
                    yt = YouTube(vid['href'])
                    stream = yt.streams.filter(only_audio=True).first()
                    stream.download()
                except Exception as e:
                    print("failed to download " + artist_vector[x].split(',')[0] + " " + song_vector[x] + str(e))
                break
        try:
            mp3file = MP3('output/' + name + '.mp3', ID3=EasyID3)
            try:
                mp3file.add_tags(ID3=EasyID3)
            except mutagen.id3.error:
                print("has tags")
            mp3file['album'] = album_vector[x]
            mp3file['albumartist'] = album_vector[x]
            mp3file['artist'] = artist_vector[x]
            mp3file['title'] = song_vector[x]
            mp3file.save()  
        except (FileNotFoundError, mutagen.MutagenError):
            print("we could not add album metadata to " + name)

