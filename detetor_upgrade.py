from datatypes import Playlist, Track
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dataclasses import dataclass


# client_credentials_manager = SpotifyClientCredentials(
#     client_id=os.environ['SPOTIPY_CLIENT_ID'],
#     client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
# )


client_credentials_manager = SpotifyClientCredentials(
    client_id='508c082ceebf41e18d65799a6ce0bc98',
    client_secret='1c1d1a2661d7402985d553edaa1fa6e1',
)


sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_public_playlists_uri(id: str) -> list:
    """Returns a list with all the user's playlists' URI."""
    playlists = sp.user_playlist(id)

    output = []
    while playlists:
        for playlist in playlists['items']:
            output.append(
                playlist['uri']
            )
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    return output

get_public_playlists_uri('chelseasoemitro')

def get_playlist_artists(pl_uri):
    """Returns the playlists' tracks"""
    track_paginated = []
    offset = 0
    while True:
        response = sp.playlist_items(pl_uri,
                                     offset=offset,
                                     fields='items.track.artists')
        if len(response['items']) == 0:
            break

    track_paginated.append(response['items'])
    offset += len(response['items'])

    output = []
    for page in track_paginated:
        for track in page:
            output.append(get_all_artists_on_track(track['track']['artists']))
    return output


def get_all_artists_on_track(artists: list) -> list:
    """Get all artists on a track"""
    return [artist['name'] for artist in artists]