# pylint: disable=missing-function-docstring, missing-class-docstring

import csv
import xml.etree.ElementTree as ET
from dataclasses import asdict
from typing import Any, Generator

from entities import SongEntity, UnifiedSongModel  # type: ignore


class AppleMusicParser:
    file_name: str = "apple_music.xml"

    def __init__(self) -> None:
        tree: ET.ElementTree = ET.parse(self.file_name)
        self.root: ET.Element | Any = tree.getroot()

    def parse_xml(self) -> Generator[list[Any], Any, None]:
        # pylint: disable=too-many-nested-blocks
        for child in self.root:
            if child.tag == "dict":
                for key in child:
                    if key.tag == "dict":
                        for track_key in key:
                            row: list[dict[str, Any]] = []
                            for track_key_child in track_key:
                                row.append({track_key_child.tag: track_key_child.text or -1})

                            if row:
                                yield row

    @staticmethod
    def parse_xml_raw_as_song(raw: list[dict[str, str | None]]) -> dict[str, str]:
        keys: list[str] = []
        values: list[str] = []

        for item in raw:
            if key := item.get("key"):
                keys.append(key)
            elif value := item.get("integer"):
                values.append(value)
            elif value := item.get("string"):
                values.append(value)
            elif value := item.get("date"):
                values.append(value)
            elif "true" in item:
                values.append(item.get("true") or "false")
            else:
                raise RuntimeError(f"can not parse {item}")

        result: dict[str, str] = {}

        for key, value in zip(keys, values):
            result[key] = value

        return result

    def read(self) -> Generator[SongEntity, Any, None]:
        for raw in self.parse_xml():
            parsed: dict[str, str] = self.parse_xml_raw_as_song(raw)
            yield SongEntity(author=parsed["Artist"], name=parsed["Name"])


class YouTubeMusicParser:
    file_name: str = "yt_music.csv"

    def read(self) -> Generator[SongEntity, Any, None]:
        with open(file=self.file_name, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header

            for row in reader:
                _, song_name, _, artist_name = row
                yield SongEntity(author=artist_name, name=song_name)


class SongsComparator:
    def __init__(self) -> None:
        self._apple_songs = AppleMusicParser()
        self._youtube_songs = YouTubeMusicParser()

    def read_apple_music_songs(self) -> set[UnifiedSongModel]:
        return set(UnifiedSongModel(**asdict(song)) for song in self._apple_songs.read())

    def read_youtube_music_songs(self) -> set[UnifiedSongModel]:
        return set(UnifiedSongModel(**asdict(song)) for song in self._youtube_songs.read())

    def compare(self) -> set[UnifiedSongModel]:
        apple: set[UnifiedSongModel] = self.read_apple_music_songs()
        yt: set[UnifiedSongModel] = self.read_youtube_music_songs()

        diff: set[UnifiedSongModel] = yt - apple
        return diff

    def get_artists(self, source: str = "yt") -> set[str]:
        songs: set[UnifiedSongModel]

        if source == "yt":
            songs = self.read_youtube_music_songs()
        elif source == "apple":
            songs = self.read_apple_music_songs()

        return set(song.author for song in songs)


def save_difference_to_file(difference: set[UnifiedSongModel]) -> None:
    with open("difference.txt", mode="w+") as file:
        file.writelines(f"{song}\n" for song in difference)


if __name__ == "__main__":
    comparator = SongsComparator()
    difference: set[UnifiedSongModel] = comparator.compare()
    save_difference_to_file(difference)
