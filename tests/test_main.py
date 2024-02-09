#  pylint:disable=missing-module-docstring
#  pylint:disable=missing-function-docstring

"""
Unit tests
"""

from entities import UnifiedSongModel
from main import SongsComparator


def test_comparator() -> None:
    comparator = SongsComparator()
    difference: set[UnifiedSongModel] = comparator.compare()
    assert difference


def test_get_artists_list() -> None:
    comparator = SongsComparator()
    artists = comparator.get_artists()
    assert artists
