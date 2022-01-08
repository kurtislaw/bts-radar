from os import stat
import re
import data_collection

def bts_radar(user_uri) -> bool:
    """Returns whether a user listen to the South Korean boy band, BTS (Bangtan Boys)."""
    return 'BTS' in data_collection.get_all_artists_from_person(user_uri)


def stats(user_uri) -> tuple:
    artists = data_collection.get_all_artists_from_person(user_uri)
    bts_count = artists.count('BTS')
    total_count = len(data_collection.get_all_tracks_from_person(user_uri))

    percentage = round((bts_count/total_count) * 100, 2)

    return (bts_count, total_count, percentage)
