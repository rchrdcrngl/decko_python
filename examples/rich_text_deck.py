"""Rich text, animations, transitions, custom theme tokens → rich_deck.html"""

from decko_py import (
    CodeBlock,
    DeckBuilder,
    HeaderBodySlide,
    TemplateRegistry,
    TextBlock,
    TitleSlide,
    register_defaults,
)
from decko_py.models.animation import AnimatableProps, BlockAnimation
from decko_py.models.rich_text import InlineAnimation, InlineLink, InlineNode
from decko_py.models.slide import SlideAmbient
from decko_py.models.transition import FadeTransition, PanTransition

registry = TemplateRegistry()
register_defaults(registry)

deck_html = (
    DeckBuilder()
    .meta(title="Rich Text & Animations", author="Carol")
    .theme(
        "midnight",
        tokens={
            "colorAccent": "#a78bfa",
            "motionIntensity": "expressive",
        },
    )
    .slide(
        TitleSlide(
            ambient=SlideAmbient(type="particles", intensity="medium"),
            headline=TextBlock(
                display="hero",
                content=[
                    InlineNode(text="Rich Text ", bold=True),
                    InlineNode(text="& ", color="#a78bfa"),
                    InlineNode(
                        text="Animations",
                        bold=True,
                        animate=InlineAnimation(type="typewriter", delay=0.5),
                    ),
                ],
                animation=BlockAnimation(
                    preset="fade-in",
                    duration=0.8,
                    delay=0.2,
                ),
            ),
            transition=FadeTransition(duration=0.4),
        )
    )
    .slide(
        HeaderBodySlide(
            title=TextBlock(
                display="heading",
                content=[
                    InlineNode(text="Inline formatting: "),
                    InlineNode(text="bold", bold=True),
                    InlineNode(text=", "),
                    InlineNode(text="italic", italic=True),
                    InlineNode(text=", "),
                    InlineNode(text="code", code=True),
                    InlineNode(text=", "),
                    InlineNode(
                        text="link",
                        link=InlineLink(href="https://example.com", target="_blank"),
                    ),
                ],
            ),
            body=CodeBlock(
                display="block",
                language="python",
                filename="example.py",
                highlight=[1, 4],
                code=(
                    "from decko_py import DeckBuilder, TextBlock, TitleSlide\n"
                    "\n"
                    "html = (\n"
                    "    DeckBuilder()\n"
                    '    .meta("My Deck")\n'
                    '    .theme("midnight")\n'
                    "    .slide(TitleSlide(\n"
                    '        headline=TextBlock(content="Hello!"),\n'
                    "    ))\n"
                    "    .render_html()\n"
                    ")"
                ),
                animation=BlockAnimation(
                    from_props=AnimatableProps(opacity=0.0, y=30.0),
                    to_props=AnimatableProps(opacity=1.0, y=0.0),
                    duration=0.6,
                    delay=0.3,
                ),
            ),
            transition=PanTransition(direction="left"),
        )
    )
    .render_html()
)

output = "rich_deck.html"
with open(output, "w", encoding="utf-8") as f:
    f.write(deck_html)

print(f"Saved → {output}")
