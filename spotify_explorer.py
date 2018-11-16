from secrets import client_id, secret
import spotipy

spotify = spotipy.Spotify()
name = 'Jason Molina'
results = spotify.search(q='artist:' + name, type='artist')
print(results)
