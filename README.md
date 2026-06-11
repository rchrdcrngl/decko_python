# decko-py

Python wrapper for [Decko](https://github.com/rchrdcrngl/decko) — build, validate, and render presentations programmatically.

## Install

```bash
pip install decko-py
```

## Quick start

```python
from decko_py import DeckBuilder, TitleSlide

html = (
    DeckBuilder()
    .meta("My Presentation", author="Alice")
    .theme("midnight")
    .slide(TitleSlide(headline="Hello, World!"))
    .render_html()
)

# or save to file
DeckBuilder().meta("My Deck").theme("nova").slide(...).save("deck.html")
```

## Models

All Pydantic v2 models. Import from `decko_py` or `decko_py.models`:

```python
from decko_py import (
    Deck, DeckMeta, DeckTheme, Slide,
    TextBlock, CodeBlock, ListBlock, MediaBlock,
    MetricBlock, ChartBlock, ChartData, ChartDataset,
    TableBlock, CalloutBlock, DividerBlock, GroupBlock,
    XBlock, BlockAnimation, Composition,
    FadeTransition, PanTransition,
)
```

## Serialization

All models serialize to camelCase JSON (matching the TypeScript schema):

```python
block = TextBlock(content="Hello", display="heading")
block.model_dump(by_alias=True)
# {"type": "text", "display": "heading", "content": "Hello"}
```

## Custom blocks

Register server-side renderers for `x-*` blocks:

```python
from decko_py import BlockRegistry, XBlock

registry = BlockRegistry()

@registry.register("x-badge")
def render_badge(block: XBlock) -> str:
    return f'<span class="badge">{block.props["label"]}</span>'

html = DeckBuilder()...render_html(block_registry=registry)
```

## Templates

23 built-in templates across 5 categories. Each has a matching typed slide class:

| Category | Template ID | Typed slide class |
|---|---|---|
| narrative | `title-slide` | `TitleSlide` |
| narrative | `section-break` | `SectionBreakSlide` |
| narrative | `agenda` | `AgendaSlide` |
| narrative | `closing` | `ClosingSlide` |
| narrative | `quote` | `QuoteSlide` |
| content | `single-column` | `SingleColumnSlide` |
| content | `two-column` | `TwoColumnSlide` |
| content | `header-body` | `HeaderBodySlide` |
| content | `bullets-media` | `BulletsMediaSlide` |
| content | `three-up` | `ThreeUpSlide` |
| data | `big-metric` | `BigMetricSlide` |
| data | `metric-trio` | `MetricTrioSlide` |
| data | `chart-callout` | `ChartCalloutSlide` |
| data | `table-slide` | `TableSlide` |
| visual | `full-bleed-media` | `FullBleedMediaSlide` |
| visual | `media-caption` | `MediaCaptionSlide` |
| visual | `image-grid` | `ImageGridSlide` |
| visual | `comparison` | `ComparisonSlide` |
| visual | `kinetic-canvas` | `KineticCanvasSlide` |
| visual | `kinetic-hero` | `KineticHeroSlide` |
| technical | `code-walkthrough` | `CodeWalkthroughSlide` |
| technical | `architecture-diagram` | `ArchitectureDiagramSlide` |
| technical | `terminal` | `TerminalSlide` |

Typed slide classes expose named, typed slot fields — no raw `slots` dict required. Plain strings auto-coerce to `TextBlock`:

```python
from decko_py import TitleSlide, HeaderBodySlide, ListBlock
from decko_py.models.rich_text import ListItem

DeckBuilder()
    .slide(TitleSlide(
        headline="My Deck",          # str → TextBlock automatically
        subtitle="Subtitle here",
        notes="Speaker notes here",  # shown in presenter mode
    ))
    .slide(HeaderBodySlide(
        title="Why Decko?",
        body=ListBlock(display="bullets", items=[
            ListItem(text="Fully typed"),
            ListItem(text="23 built-in templates"),
        ]),
    ))
```

`DeckBuilder.slide()` accepts both typed slide classes and raw `Slide` objects.

Inspect slot requirements at the REPL:

```python
TitleSlide.slots_info()
# TitleSlide [title-slide]
#   headline             required   text  max_chars=120
#   subtitle             optional   text  max_chars=200
#   eyebrow              optional   text  max_chars=60
#   logo                 optional   media

TitleSlide.definition()  # returns the full BaseTemplate catalog entry
```

`DeckBuilder.build()` auto-validates content budgets by default. Pass `strict=False` to skip:

```python
deck = builder.build()               # raises ValueError on budget violations
deck = builder.build(strict=False)   # skip validation
```

Extend `BaseTemplate` to define custom templates:

```python
from decko_py import BaseTemplate, TemplateSlot, ContentBudget, AiHints

class SplitTemplate(BaseTemplate):
    id: str = "split"
    name: str = "Split Slide"
    category: str = "content"
    description: str = "Two-column layout."
    slots: list[TemplateSlot] = [
        TemplateSlot(id="left", accepts=["text", "list"], required=True,
                     content_budget=ContentBudget(max_chars=300)),
        TemplateSlot(id="right", accepts=["text", "media"], required=True,
                     content_budget=ContentBudget(max_chars=300)),
    ]
    layout_modes: list[str] = ["split"]
    ai_hints: AiHints = AiHints(
        when_to_use="Side-by-side comparison.",
        good_for=["comparisons", "text + image"],
        avoid=["charts", "tables"],
        suggested_follow_up=["header-body"],
    )
```

## Validation

Register templates before validating. `register_defaults` loads all 23 built-ins:

```python
from decko_py import validate_content, TemplateRegistry, register_defaults

reg = TemplateRegistry()
register_defaults(reg)

violations = validate_content(deck, reg)
for v in violations:
    print(f"Slide {v.slide_index}, slot '{v.slot_id}': {v.field} exceeded ({v.actual} > {v.budget})")
```

## CDN config

```python
from decko_py import CdnConfig, HtmlRenderer

cdn = CdnConfig(version="1.2.3")
renderer = HtmlRenderer(cdn=cdn)
html = renderer.render(deck)
```

## Development

```bash
git clone https://github.com/rchrdcrngl/decko_python.git
cd decko_python
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src/ tests/
mypy src/decko_py
```

## CI/CD

- **CI**: runs on every push/PR — lint (ruff), type check (mypy), tests (pytest) across Python 3.10–3.12
- **Publish**: triggers on GitHub release → builds wheel + sdist → publishes to PyPI via OIDC trusted publishing (no API key required)

## License

MIT
