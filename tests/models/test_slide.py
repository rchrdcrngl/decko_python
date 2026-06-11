from decko_py.models.animation import BlockAnimation
from decko_py.models.blocks import TextBlock
from decko_py.models.composition import Composition
from decko_py.models.slide import (
    ColorBackground,
    Deck,
    DeckMeta,
    GradientBackground,
    ImageBackground,
    Slide,
    SlideAmbient,
    SlotStyle,
    ThemeBackground,
)
from decko_py.models.theme import DeckTheme
from decko_py.models.transition import FadeTransition


def test_slide_minimal(simple_slide):
    assert simple_slide.template_id == "title-slide"
    assert "headline" in simple_slide.slots


def test_slide_slot_single_block():
    b = TextBlock(content="Hello")
    s = Slide(template_id="t", slots={"main": b})
    assert s.slots["main"] == b


def test_slide_slot_list_of_blocks():
    blocks = [TextBlock(content="A"), TextBlock(content="B")]
    s = Slide(template_id="t", slots={"content": blocks})
    assert isinstance(s.slots["content"], list)
    assert len(s.slots["content"]) == 2


def test_slide_with_transition():
    s = Slide(
        template_id="t",
        slots={"main": TextBlock(content="x")},
        transition=FadeTransition(duration=0.3),
    )
    assert s.transition is not None
    assert s.transition.type == "fade"  # type: ignore[union-attr]


def test_slide_with_ambient():
    s = Slide(
        template_id="t",
        slots={"main": TextBlock(content="x")},
        ambient=SlideAmbient(type="particles", intensity="high"),
    )
    assert s.ambient is not None
    assert s.ambient.type == "particles"
    assert s.ambient.intensity == "high"


def test_slide_with_composition():
    s = Slide(
        template_id="t",
        slots={"main": TextBlock(content="x")},
        composition=Composition(density="dense", gravity="bottom"),
    )
    assert s.composition is not None
    assert s.composition.gravity == "bottom"


def test_slide_with_animations():
    b = TextBlock(content="animated", id="block-1")
    s = Slide(
        template_id="t",
        slots={"main": b},
        animations={"block-1": BlockAnimation(preset="slide-up")},
    )
    assert s.animations is not None
    assert "block-1" in s.animations


def test_slide_with_slot_styles():
    s = Slide(
        template_id="t",
        slots={"main": TextBlock(content="x")},
        slot_styles={"main": SlotStyle(position="absolute", top="10px", left="20px")},
    )
    d = s.model_dump(by_alias=True)
    assert d["slotStyles"]["main"]["top"] == "10px"


def test_slide_backgrounds():
    for bg in [
        ColorBackground(value="#000"),
        ImageBackground(src="https://example.com/img.png", overlay=0.5),
        GradientBackground(value="linear-gradient(#000, #fff)"),
        ThemeBackground(),
    ]:
        s = Slide(template_id="t", slots={"main": TextBlock(content="x")}, background=bg)
        assert s.background is not None
        assert s.background.type == bg.type


def test_deck_meta_defaults():
    m = DeckMeta(title="My Deck")
    assert m.aspect_ratio == "16:9"
    assert m.language == "en"
    assert m.author is None


def test_deck_meta_camel():
    m = DeckMeta(title="Test", aspect_ratio="4:3", author="Alice")
    d = m.model_dump(by_alias=True)
    assert d["aspectRatio"] == "4:3"
    assert d["author"] == "Alice"


def test_deck_version_default(simple_deck):
    assert simple_deck.version == "1"


def test_deck_serialization(simple_deck):
    json_str = simple_deck.model_dump_json(by_alias=True)
    assert '"version":"1"' in json_str
    assert '"templateId":"title-slide"' in json_str


def test_deck_variables():
    d = Deck(
        meta=DeckMeta(title="x"),
        theme=DeckTheme(name="nova"),
        slides=[Slide(template_id="t", slots={"m": TextBlock(content="x")})],
        variables={"brand": "Acme"},
    )
    assert d.variables is not None
    assert d.variables["brand"] == "Acme"
