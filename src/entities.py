# pylint: disable=missing-function-docstring, missing-class-docstring

import re
from dataclasses import dataclass


@dataclass
class SongEntity:
    author: str
    name: str


class UnifiedSongModel:
    """
    Comparable class. Reformat song and author to unified format.
    Idea to compare songs without any redundant characters.

    """

    def __init__(self, author: str, name: str) -> None:
        self._author = self.unification(author)
        self._song_name = self.unification(name)

    @property
    def author(self) -> str:
        return self._author

    @staticmethod
    def unification(value: str) -> str:
        # dropping all text inside () and () themselves
        value = re.sub(r"\((.*?)\)", "", value)

        value = value.replace("  ", " ")
        value = value.replace("--", "-")

        return value.lower().strip()

    def __hash__(self) -> int:
        return hash((self._author, self._song_name))

    def __eq__(self, value: "UnifiedSongModel") -> bool:  # type: ignore
        return self._author == value._author and self._song_name == value._song_name

    def __str__(self) -> str:
        return f"{self._author} - {self._song_name}"
