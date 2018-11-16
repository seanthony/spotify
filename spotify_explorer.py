from secrets import username, scope, client_id, secret, redirect
import spotipy
import spotipy.util as util

import numpy as np
from bokeh.plotting import figure, show, output_file

token = util.prompt_for_user_token(
    username, scope, client_id=client_id, client_secret=secret, redirect_uri=redirect)

spotify = spotipy.Spotify(auth=token)


name = 'The National'
artist = spotify.search(q='artist:' + name, type='artist')

# if artist.get('artists', False) and artist['artists'].get('items', False) and artist['artists']['items'][0].get('id', False):
id = artist['artists']['items'][0].get('id')
related = spotify.artist_related_artists(id)
name = artist['artists']['items'][0].get('name')
main_genres = artist['artists']['items'][0].get('genres')
genre_set = set(main_genres)
artists = [{'artist': name, 'genres': main_genres}]
for artist_dict in related.get('artists', [])[:8]:
    artist_name = artist_dict.get('name')
    artist_genres = artist_dict.get('genres', [])
    for genre in artist_genres:
        genre_set.add(genre)
    artists.append({'artist': artist_name, 'genres': artist_genres})

genres = sorted(list(genre_set))
names = [artist['artist'] for artist in artists]

colors = ['#ffffff', '#1db954']
xname = []
yname = []
color = []
alpha = []

for genre in genres:
    for artist in artists:
        xname.append(genre)
        yname.append(artist['artist'])
        alpha.append(1)
        if genre in artist.get('genres', []):
            color.append(colors[1])
        else:
            color.append(colors[0])


data = dict(
    xname=xname,
    yname=yname,
    colors=color,
    alphas=alpha,
    # count=counts.flatten(),
)

title = 'Related Artists for {} on Spotify'.format(name)
p = figure(title=title,
           x_axis_location="above", tools="hover,save",
           x_range=genres, y_range=list(reversed(names)),)
#    tooltips=[('names', '@yname, @xname'), ('count', '@count')])

# p.plot_width = 800
# p.plot_height = 800
p.sizing_mode = "stretch_both"
p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "10pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = np.pi / 3

# p.rect('xname', 'yname', 0.9, 0.9, source=data,
#        color='colors', alpha='alphas', line_color=None,
#        hover_line_color='black', hover_color='colors')
p.circle('xname', 'yname', source=data, size=15,
         color='colors', alpha='alphas', line_color=None,
         hover_line_color='black', hover_color='colors')


output_file("index.html", title=title)

show(p)  # show the plot
