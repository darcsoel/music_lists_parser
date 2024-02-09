# pylint: disable=missing-function-docstring

from entities import SongEntity
from main import YouTubeMusicParser


def test_yt_music() -> None:
    parser = YouTubeMusicParser()

    result: SongEntity = next(parser.read())
    assert result == SongEntity(author="Johnny Cash", name="(Ghost) Riders in the Sky")
