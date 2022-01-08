from dataclasses import dataclass


@dataclass
class Track:
    """Class for a track's useful Spotify data."""
    name: str
    uri: str
    artists: list


@dataclass
class Playlist:
    """Class for a playlists' useful information"""
    name: str
    uri: str
    tracks: list
