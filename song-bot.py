#!/usr/bin/env python

#
# A Bot to download bollywood songs from the internet
# @author Kiran Gangadharan
#

import requests
import sys
from BeautifulSoup import BeautifulSoup

print "=" * 50
print "Song Bot"
print "=" * 50
movie_name = raw_input("Movie Name: ")
base_url = 'http://www.songspk.name/'
found = False

if not movie_name:
    print "Movie name cannot be empty"
    sys.exit(1)

movie_list_url = ''.join([base_url, movie_name[0], "_list.html"])
print 'Checking...'
response = requests.get(movie_list_url)
parser = BeautifulSoup(response.content)
links = parser.findAll('a')
possible_matches = []
for link in links:
    movie = link.text.replace("\n", "").replace("\t", "").replace("&nbsp;", "")
    movie_short_name = movie.split('-')[0].strip()
    if movie_name.lower() in movie_short_name.lower():
        possible_matches.append(link)
        found = True

if found:
    print 'Movie found'

    #Let user select a movie in case of multiple matches
    if len(possible_matches)>1:
        print 'We have found multiple matches...'
        for num, single_match in enumerate(possible_matches):
            print num+1, single_match.text.replace("\n", "").replace("\t", "").replace("&nbsp;", "")
        choice = int(raw_input("Enter which movie you want to proceed with: ")) - 1
        movie = possible_matches[choice]
    else:
        movie = possible_matches[0]

    #Getting songs page for selected movie
    print 'Querying movie page for songs...'
    link_attrs = movie.get('href')
    songs_url = ''.join([base_url, link_attrs])
    res = requests.get(songs_url)
    sparser = BeautifulSoup(res.content)
    songs = sparser.findAll('a')
    for link in songs[:]:
        if 'songid' not in unicode(link.get('href')):
            songs.remove(link)

    #Showing song list and asking user to select a song to download
    print 'Following songs found...'
    for num, song in enumerate(songs):
        print num+1, song.text
    track_no = int(raw_input("Enter the song number you want to download: ")) - 1

    #writing song to file
    print "Downloading {0}.mp3 Please wait...".format(songs[track_no].text)
    try:
        file = open(songs[track_no].text+'.mp3', 'wb')
    except Exception, e:
        print "Error occured:", e
        sys.exit(1)
    res = requests.get(songs[track_no].get('href'))
    from urllib import quote
    actual_url = quote(res.url, safe="%/:.")
    res = requests.get(actual_url, stream=True)
    for block in res.iter_content(1024):
        if not block:
            break
        file.write(block)
    print 'Download complete'

else:
    print "Movie not found"
