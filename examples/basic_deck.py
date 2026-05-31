"""Basic deck: title slide + content slide → deck.html"""

from decko_py import (
    DeckBuilder,
    Slide,
    TextBlock,
    ListBlock,
    CalloutBlock,
)
from decko_py.models.rich_text import ListItem

deck_html = (
    DeckBuilder()
    .meta(
        title="Getting Started with Decko",
        author="Alice",
        date="2024-01-01",
    )
    .theme("midnight")
    .slide(
        Slide(
            template_id="title",
            slots={
                "headline": TextBlock(
                    display="hero",
                    content="Getting Started with Decko",
                ),
                "subheading": TextBlock(
                    display="subheading",
                    content="Build beautiful presentations in Python",
                ),
            },
        )
    )
    .slide(
        Slide(
            template_id="content",
            slots={
                "headline": TextBlock(
                    display="heading",
                    content="Why Decko?",
                ),
                "body": ListBlock(
                    display="bullets",
                    items=[
                        ListItem(text="Compose decks from Python or data pipelines"),
                        ListItem(text="Pydantic models — fully typed and validated"),
                        ListItem(text="Render to static HTML with CDN runtime"),
                        ListItem(text="AI-friendly structured output"),
                    ],
                ),
                "callout": CalloutBlock(
                    display="info",
                    title="Tip",
                    body="Use DeckBuilder for a fluent API, or construct Deck directly.",
                ),
            },
        )
    )
    .render_html()
)

output = "deck.html"
with open(output, "w", encoding="utf-8") as f:
    f.write(deck_html)

print(f"Saved → {output}")
