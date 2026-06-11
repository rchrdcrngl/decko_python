from __future__ import annotations

from typing import TYPE_CHECKING

from decko_py.models.template import (
    AiHints,
    BaseTemplate,
    ContentBudget,
    TemplateSlot,
)

if TYPE_CHECKING:
    from decko_py.registry import TemplateRegistry

# ── Narrative ─────────────────────────────────────────────────────────────────


class TitleSlideTemplate(BaseTemplate):
    id: str = "title-slide"
    name: str = "Title Slide"
    category: str = "narrative"
    description: str = "Deck opener with hero headline, optional subtitle, eyebrow, and logo."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="headline",
            accepts=["text"],
            required=True,
            content_budget=ContentBudget(max_chars=120, recommended_chars=60),
        ),
        TemplateSlot(
            id="subtitle",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=200, recommended_chars=100),
        ),
        TemplateSlot(
            id="eyebrow",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=60),
        ),
        TemplateSlot(
            id="logo",
            accepts=["media"],
            required=False,
            content_budget=ContentBudget(),
        ),
    ]
    layout_modes: list[str] = ["auto", "centered"]
    ai_hints: AiHints = AiHints(
        when_to_use="First slide of a deck or major section opener.",
        good_for=["deck intro", "key statement", "brand moment"],
        avoid=["detailed data", "long bullet lists"],
        suggested_follow_up=["agenda", "section-break", "header-body"],
    )


class SectionBreakTemplate(BaseTemplate):
    id: str = "section-break"
    name: str = "Section Break"
    category: str = "narrative"
    description: str = "Visual divider between major sections."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="title",
            accepts=["text"],
            required=True,
            content_budget=ContentBudget(max_chars=100, recommended_chars=50),
        ),
        TemplateSlot(
            id="label",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=60),
        ),
        TemplateSlot(
            id="description",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=200),
        ),
    ]
    layout_modes: list[str] = ["auto", "centered"]
    ai_hints: AiHints = AiHints(
        when_to_use="Transition between major deck sections.",
        good_for=["pacing", "section numbering", "topic transitions"],
        avoid=["data", "detailed content"],
        suggested_follow_up=["header-body", "single-column", "title-slide"],
    )


class AgendaTemplate(BaseTemplate):
    id: str = "agenda"
    name: str = "Agenda"
    category: str = "narrative"
    description: str = "Ordered list of agenda items with optional title."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="items",
            accepts=["list"],
            required=True,
            content_budget=ContentBudget(max_words=80),
        ),
        TemplateSlot(
            id="title",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=80),
        ),
    ]
    layout_modes: list[str] = ["auto", "top-heavy"]
    ai_hints: AiHints = AiHints(
        when_to_use="Show the deck's agenda or a meeting's topics early on.",
        good_for=["meeting previews", "structured talks", "course outlines"],
        avoid=["more than 7 items", "nested sub-items"],
        suggested_follow_up=["section-break", "header-body"],
    )


class ClosingTemplate(BaseTemplate):
    id: str = "closing"
    name: str = "Closing"
    category: str = "narrative"
    description: str = "Final slide with headline, CTA, contact info, and logo."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="headline",
            accepts=["text"],
            required=True,
            content_budget=ContentBudget(max_chars=120),
        ),
        TemplateSlot(
            id="cta",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=80),
        ),
        TemplateSlot(
            id="contact",
            accepts=["text", "list"],
            required=False,
            content_budget=ContentBudget(max_chars=200),
        ),
        TemplateSlot(
            id="logo",
            accepts=["media"],
            required=False,
            content_budget=ContentBudget(),
        ),
    ]
    layout_modes: list[str] = ["auto", "centered"]
    ai_hints: AiHints = AiHints(
        when_to_use="Last slide — thank-you, next steps, or contact.",
        good_for=["Q&A prompt", "call to action", "contact details"],
        avoid=["new information", "complex data"],
        suggested_follow_up=[],
    )


class QuoteTemplate(BaseTemplate):
    id: str = "quote"
    name: str = "Quote"
    category: str = "narrative"
    description: str = "Featured quote with attribution and optional avatar."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="quote",
            accepts=["text"],
            required=True,
            content_budget=ContentBudget(max_chars=300, recommended_chars=150),
        ),
        TemplateSlot(
            id="attribution",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=100),
        ),
        TemplateSlot(
            id="avatar",
            accepts=["media"],
            required=False,
            content_budget=ContentBudget(),
        ),
    ]
    layout_modes: list[str] = ["auto", "centered"]
    ai_hints: AiHints = AiHints(
        when_to_use="Highlight a key quote from a person or source.",
        good_for=["testimonials", "memorable statements", "social proof"],
        avoid=["long quotes over 50 words", "multiple quotes"],
        suggested_follow_up=["header-body", "single-column"],
    )


# ── Content ───────────────────────────────────────────────────────────────────


class SingleColumnTemplate(BaseTemplate):
    id: str = "single-column"
    name: str = "Single Column"
    category: str = "content"
    description: str = "Centered single-column layout with title and body."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="title",
            accepts=["text"],
            required=True,
            content_budget=ContentBudget(max_chars=80),
        ),
        TemplateSlot(
            id="body",
            accepts=["text", "list", "callout"],
            required=True,
            content_budget=ContentBudget(max_chars=600, max_words=100),
        ),
    ]
    layout_modes: list[str] = ["auto", "centered", "top-heavy"]
    ai_hints: AiHints = AiHints(
        when_to_use="Simple focused content — one idea, no media.",
        good_for=["short explanations", "key statements", "text + callout"],
        avoid=["media", "charts", "tables"],
        suggested_follow_up=["header-body", "two-column", "bullets-media"],
    )


class TwoColumnTemplate(BaseTemplate):
    id: str = "two-column"
    name: str = "Two Column"
    category: str = "content"
    description: str = "Side-by-side columns for comparison or parallel content."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="title",
            accepts=["text"],
            required=True,
            content_budget=ContentBudget(max_chars=80),
        ),
        TemplateSlot(
            id="left",
            accepts=["text", "list", "callout", "media"],
            required=True,
            content_budget=ContentBudget(max_chars=300),
        ),
        TemplateSlot(
            id="right",
            accepts=["text", "list", "callout", "media"],
            required=True,
            content_budget=ContentBudget(max_chars=300),
        ),
        TemplateSlot(
            id="left-label",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=60),
        ),
        TemplateSlot(
            id="right-label",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=60),
        ),
    ]
    layout_modes: list[str] = ["auto", "split"]
    ai_hints: AiHints = AiHints(
        when_to_use="Compare two ideas, before/after, or pros/cons.",
        good_for=["comparisons", "parallel arguments", "text + list pairs"],
        avoid=["more than 2 columns", "charts"],
        suggested_follow_up=["three-up", "comparison", "header-body"],
    )


class HeaderBodyTemplate(BaseTemplate):
    id: str = "header-body"
    name: str = "Header + Body"
    category: str = "content"
    description: str = "General-purpose slide with title, body, and optional subtitle."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="title",
            accepts=["text"],
            required=True,
            content_budget=ContentBudget(max_chars=80, recommended_chars=50),
        ),
        TemplateSlot(
            id="subtitle",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=120),
        ),
        TemplateSlot(
            id="body",
            accepts=["text", "list", "callout", "code", "table"],
            required=True,
            content_budget=ContentBudget(max_chars=600, max_words=100),
        ),
    ]
    layout_modes: list[str] = ["auto", "top-heavy", "bottom-heavy"]
    ai_hints: AiHints = AiHints(
        when_to_use="Most narrative slides — explanations, arguments, feature descriptions.",
        good_for=["bullet points", "code snippets", "text + callout combos"],
        avoid=["heavy data tables", "multiple charts"],
        suggested_follow_up=["header-body", "two-column", "chart-callout", "table-slide"],
    )


class BulletsMediaTemplate(BaseTemplate):
    id: str = "bullets-media"
    name: str = "Bullets + Media"
    category: str = "content"
    description: str = "Bullet list alongside a media asset."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="title",
            accepts=["text"],
            required=True,
            content_budget=ContentBudget(max_chars=80),
        ),
        TemplateSlot(
            id="bullets",
            accepts=["list"],
            required=True,
            content_budget=ContentBudget(max_words=80),
        ),
        TemplateSlot(
            id="media",
            accepts=["media"],
            required=True,
            content_budget=ContentBudget(),
        ),
        TemplateSlot(
            id="caption",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=120),
        ),
    ]
    layout_modes: list[str] = ["auto", "split"]
    ai_hints: AiHints = AiHints(
        when_to_use="Explain a concept with supporting visual.",
        good_for=["product features", "process steps with diagram", "text + screenshot"],
        avoid=["long bullet lists (>6 items)", "complex charts"],
        suggested_follow_up=["header-body", "two-column"],
    )


class ThreeUpTemplate(BaseTemplate):
    id: str = "three-up"
    name: str = "Three Up"
    category: str = "content"
    description: str = "Three equal columns for parallel points or pillars."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="title",
            accepts=["text"],
            required=True,
            content_budget=ContentBudget(max_chars=80),
        ),
        TemplateSlot(
            id="col-1",
            accepts=["text", "list", "callout", "metric"],
            required=True,
            content_budget=ContentBudget(max_chars=200),
        ),
        TemplateSlot(
            id="col-2",
            accepts=["text", "list", "callout", "metric"],
            required=True,
            content_budget=ContentBudget(max_chars=200),
        ),
        TemplateSlot(
            id="col-3",
            accepts=["text", "list", "callout", "metric"],
            required=True,
            content_budget=ContentBudget(max_chars=200),
        ),
        TemplateSlot(
            id="col-1-label",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=60),
        ),
        TemplateSlot(
            id="col-2-label",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=60),
        ),
        TemplateSlot(
            id="col-3-label",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=60),
        ),
    ]
    layout_modes: list[str] = ["auto", "centered"]
    ai_hints: AiHints = AiHints(
        when_to_use="Show three parallel ideas, pillars, or options.",
        good_for=["three-point frameworks", "feature trios", "metric + description"],
        avoid=["more than 3 columns", "long body text per column"],
        suggested_follow_up=["two-column", "metric-trio", "header-body"],
    )


# ── Data ──────────────────────────────────────────────────────────────────────


class BigMetricTemplate(BaseTemplate):
    id: str = "big-metric"
    name: str = "Big Metric"
    category: str = "data"
    description: str = "Single hero metric dominating the slide."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="metric",
            accepts=["metric"],
            required=True,
            content_budget=ContentBudget(),
        ),
        TemplateSlot(
            id="eyebrow",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=60),
        ),
        TemplateSlot(
            id="context",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=200),
        ),
    ]
    layout_modes: list[str] = ["auto", "centered"]
    ai_hints: AiHints = AiHints(
        when_to_use="Announce a single standout number.",
        good_for=["milestone numbers", "headline KPIs", "impact statements"],
        avoid=["multiple metrics (use metric-trio)", "detailed breakdowns"],
        suggested_follow_up=["metric-trio", "chart-callout", "header-body"],
    )


class MetricTrioTemplate(BaseTemplate):
    id: str = "metric-trio"
    name: str = "Metric Trio"
    category: str = "data"
    description: str = "Three KPI cards side by side."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="metric-1",
            accepts=["metric"],
            required=True,
            content_budget=ContentBudget(),
        ),
        TemplateSlot(
            id="metric-2",
            accepts=["metric"],
            required=True,
            content_budget=ContentBudget(),
        ),
        TemplateSlot(
            id="metric-3",
            accepts=["metric"],
            required=True,
            content_budget=ContentBudget(),
        ),
        TemplateSlot(
            id="title",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=80),
        ),
    ]
    layout_modes: list[str] = ["auto", "centered"]
    ai_hints: AiHints = AiHints(
        when_to_use="Show exactly 3 headline numbers together.",
        good_for=["KPI scorecard", "before/after/target triplet", "three-pillar metrics"],
        avoid=["more than 3 metrics (use header-body + group)", "single metric"],
        suggested_follow_up=["chart-callout", "table-slide", "header-body"],
    )


class ChartCalloutTemplate(BaseTemplate):
    id: str = "chart-callout"
    name: str = "Chart + Callout"
    category: str = "data"
    description: str = "Chart with optional callout annotation."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="title",
            accepts=["text"],
            required=True,
            content_budget=ContentBudget(max_chars=80),
        ),
        TemplateSlot(
            id="chart",
            accepts=["chart"],
            required=True,
            content_budget=ContentBudget(),
        ),
        TemplateSlot(
            id="callout",
            accepts=["callout"],
            required=False,
            content_budget=ContentBudget(max_chars=200),
        ),
    ]
    layout_modes: list[str] = ["auto", "top-heavy"]
    ai_hints: AiHints = AiHints(
        when_to_use="Show a chart and highlight one key insight.",
        good_for=["bar/line/area charts with insight callout", "trend + annotation"],
        avoid=["multiple charts", "complex tables"],
        suggested_follow_up=["table-slide", "metric-trio", "header-body"],
    )


class TableSlideTemplate(BaseTemplate):
    id: str = "table-slide"
    name: str = "Table Slide"
    category: str = "data"
    description: str = "Tabular data with title and optional footnote."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="title",
            accepts=["text"],
            required=True,
            content_budget=ContentBudget(max_chars=80),
        ),
        TemplateSlot(
            id="table",
            accepts=["table"],
            required=True,
            content_budget=ContentBudget(),
        ),
        TemplateSlot(
            id="footnote",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=150),
        ),
    ]
    layout_modes: list[str] = ["auto", "top-heavy"]
    ai_hints: AiHints = AiHints(
        when_to_use="Show structured tabular data — rankings, comparisons, breakdowns.",
        good_for=["leaderboards", "product comparisons", "multi-column data"],
        avoid=["charts", "narrative text", "more than 8 columns"],
        suggested_follow_up=["chart-callout", "header-body"],
    )


# ── Visual ────────────────────────────────────────────────────────────────────


class FullBleedMediaTemplate(BaseTemplate):
    id: str = "full-bleed-media"
    name: str = "Full Bleed Media"
    category: str = "visual"
    description: str = "Edge-to-edge media fill with optional overlay text and caption."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="media",
            accepts=["media"],
            required=True,
            content_budget=ContentBudget(),
        ),
        TemplateSlot(
            id="overlay-text",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=150),
        ),
        TemplateSlot(
            id="caption",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=120),
        ),
    ]
    layout_modes: list[str] = ["auto", "centered"]
    ai_hints: AiHints = AiHints(
        when_to_use="Visual impact slide — photo, video, or illustration dominates.",
        good_for=["emotional moments", "product photography", "scene-setting"],
        avoid=["data", "long text overlay"],
        suggested_follow_up=["header-body", "quote", "section-break"],
    )


class MediaCaptionTemplate(BaseTemplate):
    id: str = "media-caption"
    name: str = "Media + Caption"
    category: str = "visual"
    description: str = "Media asset with title and caption below."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="media",
            accepts=["media"],
            required=True,
            content_budget=ContentBudget(),
        ),
        TemplateSlot(
            id="title",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=80),
        ),
        TemplateSlot(
            id="caption",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=200),
        ),
    ]
    layout_modes: list[str] = ["auto", "top-heavy", "bottom-heavy"]
    ai_hints: AiHints = AiHints(
        when_to_use="Show a single visual with explanatory context.",
        good_for=["screenshots with annotation", "diagram walkthrough", "before/after"],
        avoid=["text-heavy explanations", "multiple media"],
        suggested_follow_up=["header-body", "bullets-media"],
    )


class ImageGridTemplate(BaseTemplate):
    id: str = "image-grid"
    name: str = "Image Grid"
    category: str = "visual"
    description: str = "2–4 image grid with optional title."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="image-1",
            accepts=["media"],
            required=True,
            content_budget=ContentBudget(),
        ),
        TemplateSlot(
            id="image-2",
            accepts=["media"],
            required=True,
            content_budget=ContentBudget(),
        ),
        TemplateSlot(
            id="title",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=80),
        ),
        TemplateSlot(
            id="image-3",
            accepts=["media"],
            required=False,
            content_budget=ContentBudget(),
        ),
        TemplateSlot(
            id="image-4",
            accepts=["media"],
            required=False,
            content_budget=ContentBudget(),
        ),
    ]
    layout_modes: list[str] = ["auto", "centered"]
    ai_hints: AiHints = AiHints(
        when_to_use="Show multiple visuals in a grid layout.",
        good_for=["portfolio showcase", "team photos", "product gallery"],
        avoid=["more than 4 images", "images with different aspect ratios"],
        suggested_follow_up=["media-caption", "full-bleed-media"],
    )


class ComparisonTemplate(BaseTemplate):
    id: str = "comparison"
    name: str = "Comparison"
    category: str = "visual"
    description: str = "Side-by-side visual comparison with optional labels."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="left",
            accepts=["media", "text", "list"],
            required=True,
            content_budget=ContentBudget(max_chars=300),
        ),
        TemplateSlot(
            id="right",
            accepts=["media", "text", "list"],
            required=True,
            content_budget=ContentBudget(max_chars=300),
        ),
        TemplateSlot(
            id="title",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=80),
        ),
        TemplateSlot(
            id="left-label",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=60),
        ),
        TemplateSlot(
            id="right-label",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=60),
        ),
    ]
    layout_modes: list[str] = ["auto", "split"]
    ai_hints: AiHints = AiHints(
        when_to_use="Visual before/after, option A vs B, or two competing approaches.",
        good_for=["before/after media", "design variants", "product comparison"],
        avoid=["data tables", "code blocks"],
        suggested_follow_up=["two-column", "header-body"],
    )


class KineticCanvasTemplate(BaseTemplate):
    id: str = "kinetic-canvas"
    name: str = "Kinetic Canvas"
    category: str = "visual"
    description: str = "Free-form canvas for kinetic typography with up to 5 words."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="word-1",
            accepts=["text-kinetic", "text"],
            required=True,
            content_budget=ContentBudget(max_chars=30),
        ),
        TemplateSlot(
            id="bg",
            accepts=["text-kinetic", "media"],
            required=False,
            content_budget=ContentBudget(),
        ),
        TemplateSlot(
            id="word-2",
            accepts=["text-kinetic", "text"],
            required=False,
            content_budget=ContentBudget(max_chars=30),
        ),
        TemplateSlot(
            id="word-3",
            accepts=["text-kinetic", "text"],
            required=False,
            content_budget=ContentBudget(max_chars=30),
        ),
        TemplateSlot(
            id="word-4",
            accepts=["text-kinetic", "text"],
            required=False,
            content_budget=ContentBudget(max_chars=30),
        ),
        TemplateSlot(
            id="word-5",
            accepts=["text-kinetic", "text"],
            required=False,
            content_budget=ContentBudget(max_chars=30),
        ),
        TemplateSlot(
            id="caption",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=120),
        ),
        TemplateSlot(
            id="accent",
            accepts=["divider", "text-kinetic"],
            required=False,
            content_budget=ContentBudget(),
        ),
    ]
    layout_modes: list[str] = ["auto"]
    ai_hints: AiHints = AiHints(
        when_to_use="Expressive typographic moment — motion-forward, high-impact.",
        good_for=["theme words", "brand slogans", "kinetic intros"],
        avoid=["data", "long sentences", "static text-heavy content"],
        suggested_follow_up=["kinetic-hero", "title-slide", "section-break"],
    )


class KineticHeroTemplate(BaseTemplate):
    id: str = "kinetic-hero"
    name: str = "Kinetic Hero"
    category: str = "visual"
    description: str = "Stacked kinetic words (top/mid/bottom) for bold typographic impact."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="word-top",
            accepts=["text-kinetic", "text"],
            required=True,
            content_budget=ContentBudget(max_chars=30),
        ),
        TemplateSlot(
            id="word-mid",
            accepts=["text-kinetic", "text"],
            required=True,
            content_budget=ContentBudget(max_chars=30),
        ),
        TemplateSlot(
            id="word-bottom",
            accepts=["text-kinetic", "text"],
            required=True,
            content_budget=ContentBudget(max_chars=30),
        ),
        TemplateSlot(
            id="ghost-bg",
            accepts=["text-kinetic"],
            required=False,
            content_budget=ContentBudget(),
        ),
        TemplateSlot(
            id="label-top",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=80),
        ),
        TemplateSlot(
            id="label-bottom",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=80),
        ),
        TemplateSlot(
            id="tagline",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=120),
        ),
    ]
    layout_modes: list[str] = ["auto", "centered"]
    ai_hints: AiHints = AiHints(
        when_to_use="Three-word stacked typography for maximum visual punch.",
        good_for=["brand reveals", "three-word mantras", "motion-forward openers"],
        avoid=["data", "sentences longer than 3 words per row"],
        suggested_follow_up=["kinetic-canvas", "title-slide"],
    )


# ── Technical ─────────────────────────────────────────────────────────────────


class CodeWalkthroughTemplate(BaseTemplate):
    id: str = "code-walkthrough"
    name: str = "Code Walkthrough"
    category: str = "technical"
    description: str = "Code block with title and optional annotation."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="title",
            accepts=["text"],
            required=True,
            content_budget=ContentBudget(max_chars=80),
        ),
        TemplateSlot(
            id="code",
            accepts=["code"],
            required=True,
            content_budget=ContentBudget(),
        ),
        TemplateSlot(
            id="annotation",
            accepts=["text", "list", "callout"],
            required=False,
            content_budget=ContentBudget(max_chars=300),
        ),
    ]
    layout_modes: list[str] = ["auto", "split"]
    ai_hints: AiHints = AiHints(
        when_to_use="Walk through a code snippet with optional explanation.",
        good_for=["API examples", "implementation demos", "before/after code"],
        avoid=["code over 30 lines", "multiple code blocks"],
        suggested_follow_up=["terminal", "architecture-diagram", "header-body"],
    )


class ArchitectureDiagramTemplate(BaseTemplate):
    id: str = "architecture-diagram"
    name: str = "Architecture Diagram"
    category: str = "technical"
    description: str = "System diagram with title and optional notes."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="title",
            accepts=["text"],
            required=True,
            content_budget=ContentBudget(max_chars=80),
        ),
        TemplateSlot(
            id="diagram",
            accepts=["media"],
            required=True,
            content_budget=ContentBudget(),
        ),
        TemplateSlot(
            id="notes",
            accepts=["list", "text"],
            required=False,
            content_budget=ContentBudget(max_chars=300),
        ),
    ]
    layout_modes: list[str] = ["auto", "top-heavy"]
    ai_hints: AiHints = AiHints(
        when_to_use="Show a system, infrastructure, or data flow diagram.",
        good_for=["system architecture", "data pipelines", "network diagrams"],
        avoid=["text-heavy explanations (use header-body)", "multiple diagrams"],
        suggested_follow_up=["code-walkthrough", "header-body"],
    )


class TerminalTemplate(BaseTemplate):
    id: str = "terminal"
    name: str = "Terminal"
    category: str = "technical"
    description: str = "Full-bleed terminal/CLI code block with optional title."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="code",
            accepts=["code"],
            required=True,
            content_budget=ContentBudget(),
        ),
        TemplateSlot(
            id="title",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=80),
        ),
    ]
    layout_modes: list[str] = ["auto", "centered"]
    ai_hints: AiHints = AiHints(
        when_to_use="Show a CLI session, shell commands, or terminal output.",
        good_for=["installation steps", "command demos", "log output"],
        avoid=["application code (use code-walkthrough)", "non-monospace content"],
        suggested_follow_up=["code-walkthrough", "header-body"],
    )


# ── Registry ──────────────────────────────────────────────────────────────────

DEFAULT_TEMPLATES: list[BaseTemplate] = [
    # narrative
    TitleSlideTemplate(),
    SectionBreakTemplate(),
    AgendaTemplate(),
    ClosingTemplate(),
    QuoteTemplate(),
    # content
    SingleColumnTemplate(),
    TwoColumnTemplate(),
    HeaderBodyTemplate(),
    BulletsMediaTemplate(),
    ThreeUpTemplate(),
    # data
    BigMetricTemplate(),
    MetricTrioTemplate(),
    ChartCalloutTemplate(),
    TableSlideTemplate(),
    # visual
    FullBleedMediaTemplate(),
    MediaCaptionTemplate(),
    ImageGridTemplate(),
    ComparisonTemplate(),
    KineticCanvasTemplate(),
    KineticHeroTemplate(),
    # technical
    CodeWalkthroughTemplate(),
    ArchitectureDiagramTemplate(),
    TerminalTemplate(),
]


def register_defaults(registry: TemplateRegistry) -> None:
    """Register all 23 default catalog templates into a TemplateRegistry."""
    for template in DEFAULT_TEMPLATES:
        registry.register(template)
