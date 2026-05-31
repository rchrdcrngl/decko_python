from __future__ import annotations  # noqa: E402

# ruff: noqa: E402
# Import all model modules in dependency order to populate module cache
# before model_rebuild() calls resolve forward references
from decko_py.models import (
    animation,  # noqa: F401
    blocks,  # noqa: F401
    composition,  # noqa: F401
    rich_text,  # noqa: F401
    slide,  # noqa: F401
    template,  # noqa: F401
    theme,  # noqa: F401
    transition,  # noqa: F401
)

# Resolve forward references
from decko_py.models.blocks import GroupBlock
from decko_py.models.rich_text import ListItem

GroupBlock.model_rebuild()
ListItem.model_rebuild()

# ── Public API ────────────────────────────────────────────────────────────────

from decko_py.builder import DeckBuilder
from decko_py.cdn import CdnConfig
from decko_py.models.animation import AnimatableProps, BlockAnimation
from decko_py.models.blocks import (
    Block,
    CalloutBlock,
    ChartBlock,
    ChartData,
    ChartDataset,
    CodeBlock,
    DividerBlock,
    GroupBlock,
    KineticTextBlock,
    ListBlock,
    MediaBlock,
    MetricBlock,
    TableBlock,
    TextBlock,
    XBlock,
)
from decko_py.models.composition import Composition
from decko_py.models.rich_text import InlineAnimation, InlineLink, InlineNode, RichText
from decko_py.models.slide import (
    ColorBackground,
    Deck,
    DeckMeta,
    GradientBackground,
    ImageBackground,
    Slide,
    SlideAmbient,
    SlideBackground,
    SlotStyle,
    ThemeBackground,
)
from decko_py.models.template import (
    AiHints,
    ContentBudget,
    TemplateDefinition,
    TemplateSlot,
)
from decko_py.models.theme import DeckTheme, ThemeTokens
from decko_py.models.transition import (
    CutTransition,
    FadeTransition,
    MorphTransition,
    PanTransition,
    ParticleBurstTransition,
    SlideTransition,
    WipeTransition,
    ZoomOutTransition,
    ZoomThroughTransition,
)
from decko_py.registry import BlockRegistry, TemplateRegistry
from decko_py.renderer import HtmlRenderer
from decko_py.validator import ContentViolation, validate_content

__version__ = "0.1.0"

__all__ = [
    "__version__",
    # Builder
    "DeckBuilder",
    # CDN
    "CdnConfig",
    # Registry
    "BlockRegistry",
    "TemplateRegistry",
    # Renderer
    "HtmlRenderer",
    # Validator
    "ContentViolation",
    "validate_content",
    # Models — animation
    "AnimatableProps",
    "BlockAnimation",
    # Models — blocks
    "Block",
    "CalloutBlock",
    "ChartBlock",
    "ChartData",
    "ChartDataset",
    "CodeBlock",
    "DividerBlock",
    "GroupBlock",
    "KineticTextBlock",
    "ListBlock",
    "MediaBlock",
    "MetricBlock",
    "TableBlock",
    "TextBlock",
    "XBlock",
    # Models — composition
    "Composition",
    # Models — rich_text
    "InlineAnimation",
    "InlineLink",
    "InlineNode",
    "ListItem",
    "RichText",
    # Models — slide
    "ColorBackground",
    "Deck",
    "DeckMeta",
    "GradientBackground",
    "ImageBackground",
    "Slide",
    "SlideAmbient",
    "SlideBackground",
    "SlotStyle",
    "ThemeBackground",
    # Models — template
    "AiHints",
    "ContentBudget",
    "TemplateDefinition",
    "TemplateSlot",
    # Models — theme
    "DeckTheme",
    "ThemeTokens",
    # Models — transition
    "CutTransition",
    "FadeTransition",
    "MorphTransition",
    "PanTransition",
    "ParticleBurstTransition",
    "SlideTransition",
    "WipeTransition",
    "ZoomOutTransition",
    "ZoomThroughTransition",
]
