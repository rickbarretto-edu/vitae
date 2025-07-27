"""Abstract Related value objects."""

from typing import Final

import attrs


@attrs.frozen
class Abstract:
    """Curriculum's Abstract."""

    _text: str
    _brief_limit: Final[int] = 50

    @property
    def full(self) -> str:
        """Full abstract."""
        return self._text

    @property
    def brief(self) -> str:
        """Brief abstract."""
        limit = self._brief_limit

        words = self._text.split()
        brief_text = " ".join(words[:limit])

        if len(words) > limit:
            return f"{brief_text}..."

        return brief_text
