#!/usr/bin/env python

#
# A Bot to download bollywood songs from the internet
# @author Kiran Gangadharan
#

import requests
import sys
from BeautifulSoup import BeautifulSoup

print "==" * 30
print "Song Bot"
print "==" * 30
movie_name = raw_input("Movie Name: ")
starting_letter = movie_name[0]
base_url = 'http://www.songspk.info/indian_movie/'
found = False

movie_list_url = ''.join([base_url, starting_letter.upper(), "_List.html"])
response = requests.get(movie_list_url)
parser = BeautifulSoup(response.content)
table = parser.findAll('table')[8]
rows = table.findAll('tr')
for row in rows:
    movie = row.find('td', {'width': '315'})
    name = movie.text.split('-')[0].strip()
    if movie_name.lower() == name.lower():
        found = True
        break

if found:
    #print "Movie found"
    link_attrs = movie.find('a').get('href')
    #temp = [value for (key, value) in link_attrs if key == 'href']
    songs_url = ''.join([base_url, link_attrs])
    res = requests.get(songs_url)
    sparser = BeautifulSoup(res.content)
    table = sparser.findAll('table')[8]
    rows = table.findAll('tr')
    song_names = []
    song_urls = []
    for row in rows:
        songs = row.find('td', {'width': '440'})
        if songs:
            song_names.append(songs.text)
            song_urls.append(songs.find('a').get('href'))
    print "=" * 30
    for i in range(0, len(song_names)):
        print '{0}. {1}'.format(i, song_names[i])
    print "=" * 30
    print "\n"
    track_no = raw_input("Select the song you want to download: ")
    path = raw_input("Enter download destination(full path): ")
    try:
        file = open(path + "/" + song_names[int(track_no)] + ".mp3", 'w')
    except Exception, e:
        print "Enter a valid path"
        sys.exit(1)
    print "Downloading {0}.mp3...Please wait".format(song_names[int(track_no)])
    res = requests.get(song_urls[int(track_no)])
    if res.ok:
        try:
            file.write(res.content)
            print "Download Completed."
        except Exception, e:
            print "Download failed"
            sys.exit(1)

else:
    print "Movie not found"
