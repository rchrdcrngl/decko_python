from __future__ import annotations

import json
from typing import Callable

from decko_py.models.blocks import XBlock
from decko_py.models.template import TemplateDefinition


class BlockRegistry:
    def __init__(self) -> None:
        self._renderers: dict[str, Callable[[XBlock], str]] = {}

    def register(
        self, block_type: str
    ) -> Callable[[Callable[[XBlock], str]], Callable[[XBlock], str]]:
        def decorator(fn: Callable[[XBlock], str]) -> Callable[[XBlock], str]:
            self._renderers[block_type] = fn
            return fn

        return decorator

    def render(self, block: XBlock) -> str:
        fn = self._renderers.get(block.type)
        if fn:
            return fn(block)
        props_json = json.dumps(block.props)
        return (
            f'<div class="decko-block x-block" '
            f'data-block-type="{block.type}" '
            f"data-props='{props_json}'></div>"
        )


class TemplateRegistry:
    def __init__(self) -> None:
        self._templates: dict[str, TemplateDefinition] = {}

    def register(self, template: TemplateDefinition) -> None:
        self._templates[template.id] = template

    def get(self, id: str) -> TemplateDefinition | None:
        return self._templates.get(id)

    def all(self) -> list[TemplateDefinition]:
        return list(self._templates.values())
