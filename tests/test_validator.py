import pytest

from decko_py.models.blocks import CalloutBlock, CodeBlock, TextBlock
from decko_py.models.slide import Deck, DeckMeta, Slide
from decko_py.models.theme import DeckTheme
from decko_py.validator import ContentViolation, validate_content


def make_deck_with_block(block, template_registry):
    return (
        Deck(
            meta=DeckMeta(title="Test"),
            theme=DeckTheme(name="midnight"),
            slides=[Slide(template_id="title-slide", slots={"headline": block})],
        ),
        template_registry,
    )


def test_no_violations_short_text(template_registry):
    deck, reg = make_deck_with_block(TextBlock(content="Short"), template_registry)
    violations = validate_content(deck, reg)
    assert violations == []


def test_char_violation(template_registry):
    long_text = "x" * 101  # budget.max_chars = 100
    deck, reg = make_deck_with_block(TextBlock(content=long_text), template_registry)
    violations = validate_content(deck, reg)
    assert any(v.field == "maxChars" for v in violations)
    v = next(v for v in violations if v.field == "maxChars")
    assert v.actual == 101
    assert v.budget == 100


def test_word_violation(template_registry):
    long_text = " ".join(["word"] * 21)  # budget.max_words = 20
    deck, reg = make_deck_with_block(TextBlock(content=long_text), template_registry)
    violations = validate_content(deck, reg)
    assert any(v.field == "maxWords" for v in violations)


def test_line_violation(template_registry):
    from decko_py.models.template import (
        AiHints,
        ContentBudget,
        TemplateDefinition,
        TemplateSlot,
    )
    from decko_py.registry import TemplateRegistry

    reg = TemplateRegistry()
    reg.register(
        TemplateDefinition(
            id="title-slide",
            name="Title",
            category="narrative",
            description="x",
            slots=[
                TemplateSlot(
                    id="headline",
                    accepts=["text"],
                    required=True,
                    content_budget=ContentBudget(max_lines=2),
                )
            ],
            layout_modes=["auto"],
            ai_hints=AiHints(when_to_use="x", good_for=[], avoid=[], suggested_follow_up=[]),
        )
    )
    deck = Deck(
        meta=DeckMeta(title="x"),
        theme=DeckTheme(name="midnight"),
        slides=[Slide(template_id="title-slide", slots={"headline": TextBlock(content="a\nb\nc")})],
    )
    violations = validate_content(deck, reg)
    assert any(v.field == "maxLines" for v in violations)


def test_no_violation_non_text_block(template_registry):
    deck, reg = make_deck_with_block(CodeBlock(code="x = 1", language="python"), template_registry)
    violations = validate_content(deck, reg)
    assert violations == []


def test_callout_body_violation(template_registry):
    from decko_py.models.template import (
        AiHints,
        ContentBudget,
        TemplateDefinition,
        TemplateSlot,
    )
    from decko_py.registry import TemplateRegistry

    reg = TemplateRegistry()
    reg.register(
        TemplateDefinition(
            id="title-slide",
            name="Title",
            category="narrative",
            description="x",
            slots=[
                TemplateSlot(
                    id="headline",
                    accepts=["callout"],
                    required=True,
                    content_budget=ContentBudget(max_chars=5),
                )
            ],
            layout_modes=["auto"],
            ai_hints=AiHints(when_to_use="x", good_for=[], avoid=[], suggested_follow_up=[]),
        )
    )
    deck = Deck(
        meta=DeckMeta(title="x"),
        theme=DeckTheme(name="midnight"),
        slides=[Slide(template_id="title-slide", slots={"headline": CalloutBlock(body="too long text")})],
    )
    violations = validate_content(deck, reg)
    assert any(v.field == "maxChars" for v in violations)


def test_missing_template_no_violations(template_registry):
    deck = Deck(
        meta=DeckMeta(title="x"),
        theme=DeckTheme(name="midnight"),
        slides=[Slide(template_id="unknown-template", slots={"m": TextBlock(content="x" * 9999)})],
    )
    violations = validate_content(deck, template_registry)
    assert violations == []


def test_violation_dataclass_fields():
    v = ContentViolation(
        slide_index=0,
        slot_id="headline",
        block_index=0,
        field="maxChars",
        budget=100,
        actual=150,
    )
    assert v.slide_index == 0
    assert v.field == "maxChars"
    assert v.actual == 150


def test_wrong_registry_type_raises():
    with pytest.raises(TypeError):
        validate_content(
            Deck(
                meta=DeckMeta(title="x"),
                theme=DeckTheme(name="midnight"),
                slides=[Slide(template_id="t", slots={"m": TextBlock(content="x")})],
            ),
            object(),  # wrong type
        )
