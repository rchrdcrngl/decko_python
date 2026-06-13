from __future__ import annotations

from dataclasses import dataclass

from decko_py.models.slide import Deck
from decko_py.models.utils.text_utils import _extract_text


@dataclass
class ContentViolation:
    slide_index: int
    slot_id: str
    block_index: int
    field: str
    budget: int
    actual: int


def validate_content(deck: Deck, registry: object) -> list[ContentViolation]:
    """Check ContentBudget constraints for text/callout blocks per slot."""
    from decko_py.registry import TemplateRegistry

    if not isinstance(registry, TemplateRegistry):
        raise TypeError("registry must be a TemplateRegistry instance")

    violations: list[ContentViolation] = []

    for si, slide in enumerate(deck.slides):
        tmpl = registry.get(slide.template_id)
        if not tmpl:
            continue

        for slot_def in tmpl.slots:
            raw = slide.slots.get(slot_def.id, [])
            blocks = raw if isinstance(raw, list) else [raw]
            budget = slot_def.content_budget

            for bi, block in enumerate(blocks):
                text = _extract_text(block)
                if text is None:
                    continue

                if budget.max_chars and len(text) > budget.max_chars:
                    violations.append(
                        ContentViolation(
                            si, slot_def.id, bi, "maxChars", budget.max_chars, len(text)
                        )
                    )
                if budget.max_words and len(text.split()) > budget.max_words:
                    violations.append(
                        ContentViolation(
                            si, slot_def.id, bi, "maxWords", budget.max_words, len(text.split())
                        )
                    )
                if budget.max_lines and text.count("\n") + 1 > budget.max_lines:
                    line_count = text.count("\n") + 1
                    violations.append(
                        ContentViolation(
                            si, slot_def.id, bi, "maxLines", budget.max_lines, line_count
                        )
                    )

    return violations


