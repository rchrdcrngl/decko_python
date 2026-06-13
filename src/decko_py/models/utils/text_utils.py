from __future__ import annotations

from typing import Union


def _richtext_to_str(rt: object) -> str:
    if isinstance(rt, str):
        return rt
    if isinstance(rt, list):
        return "".join(n.text for n in rt)
    return ""


def _extract_text(block: object) -> Union[str, None]:
    from decko_py.models.blocks import CalloutBlock, KineticTextBlock, ListBlock, TextBlock

    if isinstance(block, TextBlock):
        return _richtext_to_str(block.content)
    if isinstance(block, CalloutBlock):
        parts = []
        if block.title is not None:
            parts.append(_richtext_to_str(block.title))
        parts.append(_richtext_to_str(block.body))
        return " ".join(parts)
    if isinstance(block, KineticTextBlock):
        return block.content
    if isinstance(block, ListBlock):
        return _list_to_str(block)
    return None


def _list_to_str(block: object) -> str:
    from decko_py.models.blocks import ListBlock

    if not isinstance(block, ListBlock):
        return ""
    parts: list[str] = []
    for item in block.items:
        parts.append(_richtext_to_str(item.text))
        for child in item.children:
            parts.append(_richtext_to_str(child.text))
    return " ".join(parts)
