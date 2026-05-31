from __future__ import annotations

from pathlib import Path
from typing import Union

from decko_py.cdn import CdnConfig
from decko_py.models.blocks import XBlock
from decko_py.models.slide import Deck, Slide

BUILTIN_THEMES = {"nova", "midnight", "kinetic"}


def _escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


class HtmlRenderer:
    def __init__(
        self,
        cdn: Union[CdnConfig, None] = None,
        block_registry: Union[_BlockRegistry, None] = None,
        extra_css_urls: Union[list[str], None] = None,
        extra_css_files: Union[list[Path], None] = None,
        extra_css_inline: Union[list[str], None] = None,
        extra_script_urls: Union[list[str], None] = None,
        mode: str = "csr",
    ) -> None:
        from decko_py.registry import BlockRegistry

        self.cdn = cdn or CdnConfig()
        self.blocks = block_registry or BlockRegistry()
        self.extra_css_urls = extra_css_urls or []
        self.extra_css_files = extra_css_files or []
        self.extra_css_inline = extra_css_inline or []
        self.extra_script_urls = extra_script_urls or []
        self.mode = mode

    def render(self, deck: Deck) -> str:
        title = _escape(deck.meta.title)
        lang = deck.meta.language
        aspect_ratio = deck.meta.aspect_ratio

        deck_json = deck.model_dump_json(by_alias=True)

        css_urls = self._build_css_urls(deck)
        link_tags = "\n".join(f'  <link rel="stylesheet" href="{u}">' for u in css_urls)

        inline_css = self._build_inline_css(deck)

        critical = "  <style>html,body{background:#000}</style>"
        style_tag = f"  <style>\n{inline_css}\n  </style>" if inline_css else ""

        head_extras = "\n".join(filter(None, [critical, link_tags, style_tag]))

        all_scripts = [self.cdn.js] + self.extra_script_urls
        script_tags = "\n".join(f'  <script src="{u}"></script>' for u in all_scripts)

        root_mode_attr = ' data-render-mode="csr"' if self.mode == "csr" else ""
        root_content = "" if self.mode == "csr" else self._render_slides(deck)

        return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
{head_extras}
</head>
<body>
  <div id="decko-root" data-aspect-ratio="{aspect_ratio}"{root_mode_attr}>{root_content}</div>
  <nav id="decko-nav">
    <button id="decko-prev" aria-label="Previous slide">&#8592;</button>
    <span id="decko-counter"></span>
    <button id="decko-next" aria-label="Next slide">&#8594;</button>
  </nav>
  <script id="deck-data" type="application/json">{deck_json}</script>
{script_tags}
</body>
</html>"""

    def _build_css_urls(self, deck: Deck) -> list[str]:
        urls = [self.cdn.base_css, self.cdn.templates_css]
        if deck.theme.name in BUILTIN_THEMES:
            urls.append(self.cdn.theme_css(deck.theme.name))
        urls.extend(self.extra_css_urls)
        return urls

    def _build_inline_css(self, deck: Deck) -> str:
        parts = []
        if deck.theme.name not in BUILTIN_THEMES or deck.theme.tokens:
            parts.append(self._tokens_to_css_vars(deck.theme.tokens or {}))
        for p in self.extra_css_files:
            parts.append(p.read_text())
        parts.extend(self.extra_css_inline)
        return "\n".join(filter(None, parts))

    def _tokens_to_css_vars(self, tokens: dict) -> str:  # type: ignore[type-arg]
        mapping = {
            "colorAccent": "--decko-accent",
            "colorBackground": "--decko-bg",
            "colorSurface": "--decko-surface",
            "colorText": "--decko-text",
            "colorTextMuted": "--decko-text-muted",
            "fontDisplay": "--decko-font-display",
            "fontBody": "--decko-font-body",
            "fontMono": "--decko-font-mono",
            "spacingSlide": "--decko-spacing-slide",
            "radiusCard": "--decko-radius-card",
            "motionIntensity": "--decko-motion",
        }
        vars_str = "\n".join(
            f"  {css_var}: {tokens[ts_key]};"
            for ts_key, css_var in mapping.items()
            if ts_key in tokens
        )
        return f":root {{\n{vars_str}\n}}" if vars_str else ""

    def _render_slides(self, deck: Deck) -> str:
        return "\n    ".join(self._render_slide(s) for s in deck.slides)

    def _render_slide(self, slide: Slide) -> str:
        attrs = [f'data-template-id="{slide.template_id}"']
        if slide.transition:
            attrs.append(
                f"data-transition='{slide.transition.model_dump_json(by_alias=True)}'"  # type: ignore[union-attr]
            )
        if slide.ambient:
            attrs.append(f'data-ambient="{slide.ambient.type}"')
            if slide.ambient.intensity:
                attrs.append(f'data-ambient-intensity="{slide.ambient.intensity}"')
        if slide.notes:
            attrs.append(f"data-notes='{_escape(slide.notes)}'")
        if slide.id:
            attrs.append(f'id="{slide.id}"')

        attrs_str = " ".join(attrs)
        slots_html = "\n".join(
            self._render_slot(slot_id, blocks, slide) for slot_id, blocks in slide.slots.items()
        )
        return f'<section class="decko-slide" {attrs_str}>\n{slots_html}\n</section>'

    def _render_slot(self, slot_id: str, blocks: object, slide: Slide) -> str:
        style = ""
        if slide.slot_styles and slot_id in slide.slot_styles:
            style = (
                f" data-slot-style='{slide.slot_styles[slot_id].model_dump_json(by_alias=True)}'"
            )

        block_list = blocks if isinstance(blocks, list) else [blocks]
        blocks_html = "".join(
            self._render_block_entry(b, slide)
            for b in block_list  # type: ignore[union-attr]
        )
        return f'  <div class="decko-slot" data-slot="{slot_id}"{style}>{blocks_html}</div>'

    def _render_block_entry(self, block: object, slide: Slide) -> str:
        anim = ""
        if (
            slide.animations
            and hasattr(block, "id")
            and block.id  # type: ignore[union-attr]
            and block.id in slide.animations  # type: ignore[union-attr]
        ):
            anim_json = slide.animations[block.id].model_dump_json(by_alias=True)  # type: ignore[union-attr]
            anim = f" data-animate='{anim_json}'"

        if isinstance(block, XBlock):
            inner = self.blocks.render(block)
        else:
            block_json = block.model_dump_json(by_alias=True)  # type: ignore[union-attr]
            inner = (
                f'<div class="decko-block" '
                f'data-block-type="{block.type}" '  # type: ignore[union-attr]
                f"data-block='{block_json}'></div>"
            )
        return f'<div class="decko-block-wrapper"{anim}>{inner}</div>'

    def save(self, deck: Deck, path: Union[str, Path]) -> None:
        Path(path).write_text(self.render(deck), encoding="utf-8")


# type alias for type hint in __init__
_BlockRegistry = object
