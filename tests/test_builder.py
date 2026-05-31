from decko_py.builder import DeckBuilder
from decko_py.models.blocks import TextBlock
from decko_py.models.slide import Slide


def make_slide(content="Hello"):
    return Slide(template_id="title", slots={"headline": TextBlock(content=content)})


def test_builder_defaults():
    deck = DeckBuilder().slide(make_slide()).build()
    assert deck.meta.title == "Untitled"
    assert deck.theme.name == "midnight"
    assert len(deck.slides) == 1


def test_builder_meta():
    deck = (
        DeckBuilder()
        .meta("My Deck", author="Alice", org="Acme", date="2024-01-01")
        .slide(make_slide())
        .build()
    )
    assert deck.meta.title == "My Deck"
    assert deck.meta.author == "Alice"
    assert deck.meta.org == "Acme"
    assert deck.meta.date == "2024-01-01"


def test_builder_theme():
    deck = DeckBuilder().theme("nova").slide(make_slide()).build()
    assert deck.theme.name == "nova"


def test_builder_theme_with_tokens():
    deck = DeckBuilder().theme("custom", tokens={"colorAccent": "#abc"}).slide(make_slide()).build()
    assert deck.theme.tokens is not None
    assert deck.theme.tokens["colorAccent"] == "#abc"


def test_builder_variables():
    deck = DeckBuilder().var("brand", "Acme").var("year", "2024").slide(make_slide()).build()
    assert deck.variables is not None
    assert deck.variables["brand"] == "Acme"
    assert deck.variables["year"] == "2024"


def test_builder_multiple_slides():
    deck = (
        DeckBuilder()
        .slide(make_slide("Slide 1"))
        .slide(make_slide("Slide 2"))
        .slide(make_slide("Slide 3"))
        .build()
    )
    assert len(deck.slides) == 3


def test_builder_chaining_returns_self():
    builder = DeckBuilder()
    assert builder.meta("x") is builder
    assert builder.theme("midnight") is builder
    assert builder.var("k", "v") is builder
    assert builder.slide(make_slide()) is builder


def test_builder_render_html_returns_string():
    html = DeckBuilder().meta("Test").slide(make_slide()).render_html()
    assert isinstance(html, str)
    assert "<!DOCTYPE html>" in html


def test_builder_save(tmp_path):
    out = tmp_path / "output.html"
    DeckBuilder().meta("Saved").slide(make_slide()).save(out)
    assert out.exists()
    content = out.read_text()
    assert "<!DOCTYPE html>" in content


def test_builder_no_variables_if_empty():
    deck = DeckBuilder().slide(make_slide()).build()
    assert deck.variables is None


def test_builder_aspect_ratio():
    deck = DeckBuilder().meta("x", aspect_ratio="4:3").slide(make_slide()).build()
    assert deck.meta.aspect_ratio == "4:3"
