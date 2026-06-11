"""Basic deck: title slide + content slide → deck.html"""

from decko_py import (
    DeckBuilder,
    HeaderBodySlide,
    ListBlock,
    TextBlock,
    TitleSlide,
    TemplateRegistry,
    register_defaults,
)
from decko_py.models.rich_text import ListItem

registry = TemplateRegistry()
register_defaults(registry)

deck_html = (
    DeckBuilder()
    .meta(
        title="Getting Started with Decko",
        author="Alice",
        date="2024-01-01",
    )
    .theme("midnight")
    .slide(
        TitleSlide(
            headline=TextBlock(
                display="hero",
                content="Getting Started with Decko",
            ),
            subtitle=TextBlock(
                display="subheading",
                content="Build beautiful presentations in Python",
            ),
        )
    )
    .slide(
        HeaderBodySlide(
            title=TextBlock(
                display="heading",
                content="Why Decko?",
            ),
            body=ListBlock(
                display="bullets",
                items=[
                    ListItem(text="Compose decks from Python or data pipelines"),
                    ListItem(text="Pydantic models — fully typed and validated"),
                    ListItem(text="Render to static HTML with CDN runtime"),
                    ListItem(text="AI-friendly structured output"),
                ],
            ),
        )
    )
    .render_html()
)

output = "deck.html"
with open(output, "w", encoding="utf-8") as f:
    f.write(deck_html)

print(f"Saved → {output}")
