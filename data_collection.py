from datatypes import Playlist, Track
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dataclasses import dataclass

load_dotenv('creds.env')

client_credentials_manager = SpotifyClientCredentials(
    client_id=os.environ['SPOTIPY_CLIENT_ID'],
    client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_all_artists_from_person(uri):
    """Returns all the artists that a user has in their public playlists"""
    playlists = get_public_playlists(uri)
    all_playlist_objects = [get_playlist_tracks(
        playlist.uri) for playlist in playlists]
    all_artists = []
    for playlist in all_playlist_objects:
        for track in playlist:
            for artist in track.artists:
                all_artists.append(artist)
    return all_artists


def get_public_playlists(user: str) -> list:
    """Returns a user's public playlists"""
    playlists = sp.user_playlists(user)

    output = []
    while playlists:
        for playlist in playlists['items']:
            output.append(
                Playlist(name=playlist['name'], uri=playlist['uri'], tracks=[])
            )
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    return output


def get_playlist_tracks(pl_id: str):
    """Get all the tracks within a playlist"""
    tracks_paginated = []
    offset = 0
    while True:
        response = sp.playlist_items(pl_id,
                                     offset=offset,
                                     fields='items.track.id, items.track.name, items.track.artists, items.track.uri, total'
                                     )

        if len(response['items']) == 0:
            break

        tracks_paginated.append(response['items'])
        offset = offset + len(response['items'])

    output = []
    for page in tracks_paginated:
        for track in page:
            if track['track'] != None:
                output.append(
                    Track(name=track['track']['name'],
                          artists=get_all_artists_on_track(
                        track['track']['artists']),
                        uri=track['track']['uri'])
                )
    return output


def get_all_artists_on_track(artists: list) -> list:
    """Get all artists on a track"""
    return [artist['name'] for artist in artists]


def get_all_tracks_from_person(uri) -> list:
    """Returns all the tracks within all the user's public playlists"""
    playlists = get_public_playlists(uri)
    all_playlist_objects = [get_playlist_tracks(
        playlist.uri) for playlist in playlists]
    all_tracks = []
    for playlist in all_playlist_objects:
        for track in playlist:
            all_tracks.append(track.name)
    return all_tracks