import pytest

from decko_py.models.blocks import (
    CalloutBlock,
    ChartBlock,
    ChartData,
    ChartDataset,
    CodeBlock,
    ListBlock,
    TextBlock,
)
from decko_py.models.rich_text import InlineNode, ListItem
from decko_py.models.slide import Deck, DeckMeta, Slide
from decko_py.models.template import (
    AiHints,
    ContentBudget,
    TemplateDefinition,
    TemplateSlot,
)
from decko_py.models.theme import DeckTheme


@pytest.fixture
def text_block():
    return TextBlock(content="Hello world")


@pytest.fixture
def inline_text_block():
    return TextBlock(content=[InlineNode(text="Hello", bold=True)])


@pytest.fixture
def callout_block():
    return CalloutBlock(body="Watch out!", display="warning")


@pytest.fixture
def list_block():
    return ListBlock(items=[ListItem(text="Item 1"), ListItem(text="Item 2")])


@pytest.fixture
def code_block():
    return CodeBlock(code="print('hello')", language="python")


@pytest.fixture
def chart_block():
    return ChartBlock(
        chart_type="bar",
        data=ChartData(
            labels=["A", "B"],
            datasets=[ChartDataset(values=[1.0, 2.0])],
        ),
    )


@pytest.fixture
def simple_slide(text_block):
    return Slide(template_id="title", slots={"headline": text_block})


@pytest.fixture
def simple_deck(simple_slide):
    return Deck(
        meta=DeckMeta(title="Test Deck"),
        theme=DeckTheme(name="midnight"),
        slides=[simple_slide],
    )


@pytest.fixture
def template_registry():
    from decko_py.registry import TemplateRegistry

    reg = TemplateRegistry()
    reg.register(
        TemplateDefinition(
            id="title",
            name="Title",
            category="narrative",
            description="A title slide",
            slots=[
                TemplateSlot(
                    id="headline",
                    accepts=["text"],
                    required=True,
                    content_budget=ContentBudget(max_chars=100, max_words=20),
                )
            ],
            layout_modes=["auto"],
            ai_hints=AiHints(
                when_to_use="Opening slide",
                good_for=["intros"],
                avoid=["data-heavy content"],
                suggested_follow_up=["content"],
            ),
        )
    )
    return reg
