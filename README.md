# decko-py

Python wrapper for [Decko](https://github.com/rchrdcrngl/decko) — build, validate, and render presentations programmatically.

## Install

```bash
pip install decko-py
```

## Quick start

```python
from decko_py import DeckBuilder, TextBlock, Slide

html = (
    DeckBuilder()
    .meta("My Presentation", author="Alice")
    .theme("midnight")
    .slide(
        Slide(
            template_id="title",
            slots={"headline": TextBlock(content="Hello, World!", display="hero")},
        )
    )
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

## Validation

```python
from decko_py import validate_content, TemplateRegistry, TemplateDefinition

reg = TemplateRegistry()
reg.register(TemplateDefinition(...))

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
