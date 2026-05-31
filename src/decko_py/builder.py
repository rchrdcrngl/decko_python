from __future__ import annotations

from pathlib import Path
from typing import Union

from decko_py.cdn import CdnConfig
from decko_py.models.slide import Deck, DeckMeta, Slide
from decko_py.models.theme import DeckTheme


class DeckBuilder:
    def __init__(self) -> None:
        self._meta = DeckMeta(title="Untitled")
        self._theme = DeckTheme(name="midnight")
        self._slides: list[Slide] = []
        self._variables: dict[str, str] = {}

    def meta(
        self,
        title: str,
        author: str | None = None,
        org: str | None = None,
        date: str | None = None,
        aspect_ratio: str = "16:9",
        language: str = "en",
    ) -> DeckBuilder:
        self._meta = DeckMeta(
            title=title,
            author=author,
            org=org,
            date=date,
            aspect_ratio=aspect_ratio,  # type: ignore[arg-type]
            language=language,
        )
        return self

    def theme(self, name: str, tokens: dict[str, str] | None = None) -> DeckBuilder:
        self._theme = DeckTheme(name=name, tokens=tokens)
        return self

    def var(self, key: str, value: str) -> DeckBuilder:
        self._variables[key] = value
        return self

    def slide(self, slide: Slide) -> DeckBuilder:
        self._slides.append(slide)
        return self

    def build(self) -> Deck:
        return Deck(
            meta=self._meta,
            theme=self._theme,
            variables=self._variables or None,
            slides=self._slides,
        )

    def render_html(
        self,
        cdn: CdnConfig | None = None,
        block_registry: object | None = None,
        **renderer_kwargs: object,
    ) -> str:
        from decko_py.renderer import HtmlRenderer

        return HtmlRenderer(cdn, block_registry, **renderer_kwargs).render(self.build())  # type: ignore[arg-type]

    def save(self, path: Union[str, Path], **renderer_kwargs: object) -> None:
        from decko_py.renderer import HtmlRenderer

        HtmlRenderer(**renderer_kwargs).save(self.build(), path)  # type: ignore[arg-type]
