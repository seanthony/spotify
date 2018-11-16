from secrets import username, scope, client_id, secret, redirect
import spotipy
import spotipy.util as util

token = util.prompt_for_user_token(
    username, scope, client_id=client_id, client_secret=secret, redirect_uri=redirect)

spotify = spotipy.Spotify(auth=token)


name = 'Jason Molina'
artist = spotify.search(q='artist:' + name, type='artist')

# if artist.get('artists', False) and artist['artists'].get('items', False) and artist['artists']['items'][0].get('id', False):
id = artist['artists']['items'][0].get('id')
related = spotify.artist_related_artists(id)
name = artist['artists']['items'][0].get('name')
main_genres = artist['artists']['items'][0].get('genres')
genres = set(main_genres)
artists = [{'artist': name, 'genres': main_genres}]
for artist_dict in related.get('artists', []):
    artist_name = artist_dict.get('name')
    artist_genres = artist_dict.get('genres', [])
    for genre in artist_genres:
        genres.add(genre)
    artists.append({'artist': artist_name, 'genres': artist_genres})
