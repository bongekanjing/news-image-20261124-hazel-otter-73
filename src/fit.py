"""Text measurement for one printed page.

Every height and every wrap on the front page is decided here, against the
font that will actually draw the words. Nothing is estimated from a character
count: a caption is only ever given a height after the real face has been
asked how wide it is, which is what stops a deck being clipped or a row of
tiles falling out of alignment.

The three entry points are deliberately small:

    fit(m).lines(text, face, width)
    fit(m).block(x, y, text, face, width, fill, leading, limit=2)
    fit(m).one_line(text, kind, size, width)

where ``m`` is a :class:`Measure` built once around the page's draw handle.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Face:
    """A loaded font together with the leading the page uses for it."""

    font: object
    leading: int


class Measure:
    """Wraps Pillow's text metrics so the layout code reads as prose."""

    def __init__(self, draw, loader):
        self._draw = draw
        self._loader = loader
        self._loaded: dict = {}

    # -- fonts ------------------------------------------------------------
    def face(self, kind: str, size: int) -> object:
        """A font, cached: opening a TTF 400 times is most of a slow build."""
        key = (kind, size)
        if key not in self._loaded:
            self._loaded[key] = self._loader(kind, size)
        return self._loaded[key]

    def width(self, text: str, font) -> float:
        return self._draw.textlength(text, font=font)

    def fits(self, text: str, font, width: float) -> bool:
        return self.width(text, font) <= width

    # -- wrapping ---------------------------------------------------------
    def lines(self, text: str, font, width: float) -> list:
        """Greedy wrap. A single word wider than the measure still gets a line,
        so an unbreakable token can never loop or vanish."""
        out, current = [], ""
        for word in text.split():
            trial = word if not current else current + " " + word
            if self.width(trial, font) <= width:
                current = trial
            else:
                if current:
                    out.append(current)
                current = word
        if current:
            out.append(current)
        return out

    def count(self, text: str, font, width: float) -> int:
        return len(self.lines(text, font, width))

    # -- drawing ----------------------------------------------------------
    def block(self, x, y, text, font, width, fill, leading, limit=None):
        """Draw a wrapped paragraph and return the y the next element starts at."""
        rows = self.lines(text, font, width)
        if limit is not None:
            rows = rows[:limit]
        for row in rows:
            self._draw.text((x, y), row, font=font, fill=fill)
            y += leading
        return y

    def one_line(self, text: str, kind: str, size: int, width: float):
        """The largest size at or below ``size`` that keeps ``text`` on one line."""
        while size > 6:
            font = self.face(kind, size)
            if self.fits(text, font, width):
                return font
            size -= 1
        return self.face(kind, 6)

    # -- the page's own assertions ---------------------------------------
    def require(self, ok: bool, why: str) -> None:
        """A layout invariant. The build stops rather than print something wrong:
        a page with a caption cut in half is worse than no page at all."""
        if not ok:
            raise AssertionError(why)
