from decko_py.models.blocks import TextBlock
from decko_py.models.template import (
    AiHints,
    ContentBudget,
    TemplateDefinition,
    TemplateSlot,
)


def test_content_budget_defaults():
    b = ContentBudget()
    assert b.max_chars is None
    assert b.max_words is None


def test_content_budget_camel():
    b = ContentBudget(max_chars=200, max_words=50, recommended_chars=150)
    d = b.model_dump(by_alias=True)
    assert d["maxChars"] == 200
    assert d["maxWords"] == 50
    assert d["recommendedChars"] == 150


def test_template_slot_minimal():
    slot = TemplateSlot(
        id="headline",
        accepts=["text"],
        required=True,
        content_budget=ContentBudget(max_chars=100),
    )
    assert slot.id == "headline"
    assert slot.required is True
    assert slot.default is None


def test_template_slot_with_default():
    slot = TemplateSlot(
        id="body",
        accepts=["text", "callout"],
        required=False,
        content_budget=ContentBudget(max_words=30),
        default=TextBlock(content="Default text"),
    )
    assert slot.default is not None
    assert slot.default.type == "text"  # type: ignore[union-attr]


def test_template_definition():
    tmpl = TemplateDefinition(
        id="title",
        name="Title Slide",
        category="narrative",
        description="Opening slide with large headline",
        slots=[
            TemplateSlot(
                id="headline",
                accepts=["text"],
                required=True,
                content_budget=ContentBudget(max_chars=80),
            )
        ],
        layout_modes=["auto", "centered"],
        ai_hints=AiHints(
            when_to_use="Start of presentation",
            good_for=["intros", "chapter breaks"],
            avoid=["data tables"],
            suggested_follow_up=["content", "data"],
        ),
    )
    d = tmpl.model_dump(by_alias=True)
    assert d["id"] == "title"
    assert d["aiHints"]["whenToUse"] == "Start of presentation"
    assert d["layoutModes"] == ["auto", "centered"]
