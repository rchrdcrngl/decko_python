from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from decko_py.models.animation import BlockAnimation
from decko_py.models.blocks import (
    Block,
    CalloutBlock,
    ChartBlock,
    CodeBlock,
    DividerBlock,
    KineticTextBlock,
    ListBlock,
    MediaBlock,
    MetricBlock,
    TableBlock,
    TextBlock,
)
from decko_py.models.composition import Composition
from decko_py.models.slide import Slide, SlideAmbient, SlideBackground, SlotStyle
from decko_py.models.transition import SlideTransition

# ── Base ──────────────────────────────────────────────────────────────────────


class TypedSlide(BaseModel):
    """Strongly-typed slide. Subclasses expose slot fields as kwargs. Call .to_slide() for the renderer."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    template_id: str
    id: Union[str, None] = None
    layout_mode: Union[str, None] = None
    background: Union[SlideBackground, None] = None
    composition: Union[Composition, None] = None
    transition: Union[SlideTransition, None] = None
    ambient: Union[SlideAmbient, None] = None
    animations: Union[dict[str, BlockAnimation], None] = None
    slot_styles: Union[dict[str, SlotStyle], None] = None
    speaker_notes: Union[str, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        raise NotImplementedError

    def to_slide(self) -> Slide:
        return Slide(
            id=self.id,
            template_id=self.template_id,
            layout_mode=self.layout_mode,
            background=self.background,
            slots=self._build_slots(),
            composition=self.composition,
            transition=self.transition,
            ambient=self.ambient,
            animations=self.animations,
            slot_styles=self.slot_styles,
            notes=self.speaker_notes,
        )


# ── Narrative ─────────────────────────────────────────────────────────────────


class TitleSlide(TypedSlide):
    template_id: Literal["title-slide"] = "title-slide"
    headline: TextBlock
    subtitle: Union[TextBlock, None] = None
    eyebrow: Union[TextBlock, None] = None
    logo: Union[MediaBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {"headline": self.headline}
        if self.subtitle is not None:
            s["subtitle"] = self.subtitle
        if self.eyebrow is not None:
            s["eyebrow"] = self.eyebrow
        if self.logo is not None:
            s["logo"] = self.logo
        return s


class SectionBreakSlide(TypedSlide):
    template_id: Literal["section-break"] = "section-break"
    title: TextBlock
    label: Union[TextBlock, None] = None
    description: Union[TextBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {"title": self.title}
        if self.label is not None:
            s["label"] = self.label
        if self.description is not None:
            s["description"] = self.description
        return s


class AgendaSlide(TypedSlide):
    template_id: Literal["agenda"] = "agenda"
    items: ListBlock
    title: Union[TextBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {"items": self.items}
        if self.title is not None:
            s["title"] = self.title
        return s


class ClosingSlide(TypedSlide):
    template_id: Literal["closing"] = "closing"
    headline: TextBlock
    cta: Union[TextBlock, None] = None
    contact: Union[TextBlock, ListBlock, None] = None
    logo: Union[MediaBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {"headline": self.headline}
        if self.cta is not None:
            s["cta"] = self.cta
        if self.contact is not None:
            s["contact"] = self.contact
        if self.logo is not None:
            s["logo"] = self.logo
        return s


class QuoteSlide(TypedSlide):
    template_id: Literal["quote"] = "quote"
    quote: TextBlock
    attribution: Union[TextBlock, None] = None
    avatar: Union[MediaBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {"quote": self.quote}
        if self.attribution is not None:
            s["attribution"] = self.attribution
        if self.avatar is not None:
            s["avatar"] = self.avatar
        return s


# ── Content ───────────────────────────────────────────────────────────────────

SingleColumnBody = Union[TextBlock, ListBlock, CalloutBlock]
TwoColumnContent = Union[TextBlock, ListBlock, CalloutBlock, MediaBlock]
HeaderBodyContent = Union[TextBlock, ListBlock, CalloutBlock, CodeBlock, TableBlock]
ThreeUpContent = Union[TextBlock, ListBlock, CalloutBlock, MetricBlock]


class SingleColumnSlide(TypedSlide):
    template_id: Literal["single-column"] = "single-column"
    title: TextBlock
    body: SingleColumnBody

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        return {"title": self.title, "body": self.body}


class TwoColumnSlide(TypedSlide):
    template_id: Literal["two-column"] = "two-column"
    title: TextBlock
    left: TwoColumnContent
    right: TwoColumnContent
    left_label: Union[TextBlock, None] = None
    right_label: Union[TextBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {
            "title": self.title,
            "left": self.left,
            "right": self.right,
        }
        if self.left_label is not None:
            s["left-label"] = self.left_label
        if self.right_label is not None:
            s["right-label"] = self.right_label
        return s


class HeaderBodySlide(TypedSlide):
    template_id: Literal["header-body"] = "header-body"
    title: TextBlock
    body: HeaderBodyContent
    subtitle: Union[TextBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {"title": self.title, "body": self.body}
        if self.subtitle is not None:
            s["subtitle"] = self.subtitle
        return s


class BulletsMediaSlide(TypedSlide):
    template_id: Literal["bullets-media"] = "bullets-media"
    title: TextBlock
    bullets: ListBlock
    media: MediaBlock
    caption: Union[TextBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {
            "title": self.title,
            "bullets": self.bullets,
            "media": self.media,
        }
        if self.caption is not None:
            s["caption"] = self.caption
        return s


class ThreeUpSlide(TypedSlide):
    template_id: Literal["three-up"] = "three-up"
    title: TextBlock
    col_1: ThreeUpContent
    col_2: ThreeUpContent
    col_3: ThreeUpContent
    col_1_label: Union[TextBlock, None] = None
    col_2_label: Union[TextBlock, None] = None
    col_3_label: Union[TextBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {
            "title": self.title,
            "col-1": self.col_1,
            "col-2": self.col_2,
            "col-3": self.col_3,
        }
        if self.col_1_label is not None:
            s["col-1-label"] = self.col_1_label
        if self.col_2_label is not None:
            s["col-2-label"] = self.col_2_label
        if self.col_3_label is not None:
            s["col-3-label"] = self.col_3_label
        return s


# ── Data ──────────────────────────────────────────────────────────────────────


class BigMetricSlide(TypedSlide):
    template_id: Literal["big-metric"] = "big-metric"
    metric: MetricBlock
    eyebrow: Union[TextBlock, None] = None
    context: Union[TextBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {"metric": self.metric}
        if self.eyebrow is not None:
            s["eyebrow"] = self.eyebrow
        if self.context is not None:
            s["context"] = self.context
        return s


class MetricTrioSlide(TypedSlide):
    template_id: Literal["metric-trio"] = "metric-trio"
    metric_1: MetricBlock
    metric_2: MetricBlock
    metric_3: MetricBlock
    title: Union[TextBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {
            "metric-1": self.metric_1,
            "metric-2": self.metric_2,
            "metric-3": self.metric_3,
        }
        if self.title is not None:
            s["title"] = self.title
        return s


class ChartCalloutSlide(TypedSlide):
    template_id: Literal["chart-callout"] = "chart-callout"
    title: TextBlock
    chart: ChartBlock
    callout: Union[CalloutBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {
            "title": self.title,
            "chart": self.chart,
        }
        if self.callout is not None:
            s["callout"] = self.callout
        return s


class TableSlide(TypedSlide):
    template_id: Literal["table-slide"] = "table-slide"
    title: TextBlock
    table: TableBlock
    footnote: Union[TextBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {
            "title": self.title,
            "table": self.table,
        }
        if self.footnote is not None:
            s["footnote"] = self.footnote
        return s


# ── Visual ────────────────────────────────────────────────────────────────────

KineticWord = Union[KineticTextBlock, TextBlock]
ComparisonContent = Union[MediaBlock, TextBlock, ListBlock]


class FullBleedMediaSlide(TypedSlide):
    template_id: Literal["full-bleed-media"] = "full-bleed-media"
    media: MediaBlock
    overlay_text: Union[TextBlock, None] = None
    caption: Union[TextBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {"media": self.media}
        if self.overlay_text is not None:
            s["overlay-text"] = self.overlay_text
        if self.caption is not None:
            s["caption"] = self.caption
        return s


class MediaCaptionSlide(TypedSlide):
    template_id: Literal["media-caption"] = "media-caption"
    media: MediaBlock
    title: Union[TextBlock, None] = None
    caption: Union[TextBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {"media": self.media}
        if self.title is not None:
            s["title"] = self.title
        if self.caption is not None:
            s["caption"] = self.caption
        return s


class ImageGridSlide(TypedSlide):
    template_id: Literal["image-grid"] = "image-grid"
    image_1: MediaBlock
    image_2: MediaBlock
    title: Union[TextBlock, None] = None
    image_3: Union[MediaBlock, None] = None
    image_4: Union[MediaBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {
            "image-1": self.image_1,
            "image-2": self.image_2,
        }
        if self.title is not None:
            s["title"] = self.title
        if self.image_3 is not None:
            s["image-3"] = self.image_3
        if self.image_4 is not None:
            s["image-4"] = self.image_4
        return s


class ComparisonSlide(TypedSlide):
    template_id: Literal["comparison"] = "comparison"
    left: ComparisonContent
    right: ComparisonContent
    title: Union[TextBlock, None] = None
    left_label: Union[TextBlock, None] = None
    right_label: Union[TextBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {
            "left": self.left,
            "right": self.right,
        }
        if self.title is not None:
            s["title"] = self.title
        if self.left_label is not None:
            s["left-label"] = self.left_label
        if self.right_label is not None:
            s["right-label"] = self.right_label
        return s


class KineticCanvasSlide(TypedSlide):
    template_id: Literal["kinetic-canvas"] = "kinetic-canvas"
    word_1: KineticWord
    bg: Union[KineticTextBlock, MediaBlock, None] = None
    word_2: Union[KineticWord, None] = None
    word_3: Union[KineticWord, None] = None
    word_4: Union[KineticWord, None] = None
    word_5: Union[KineticWord, None] = None
    caption: Union[TextBlock, None] = None
    accent: Union[DividerBlock, KineticTextBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {"word-1": self.word_1}
        if self.bg is not None:
            s["bg"] = self.bg
        if self.word_2 is not None:
            s["word-2"] = self.word_2
        if self.word_3 is not None:
            s["word-3"] = self.word_3
        if self.word_4 is not None:
            s["word-4"] = self.word_4
        if self.word_5 is not None:
            s["word-5"] = self.word_5
        if self.caption is not None:
            s["caption"] = self.caption
        if self.accent is not None:
            s["accent"] = self.accent
        return s


class KineticHeroSlide(TypedSlide):
    template_id: Literal["kinetic-hero"] = "kinetic-hero"
    word_top: KineticWord
    word_mid: KineticWord
    word_bottom: KineticWord
    ghost_bg: Union[KineticTextBlock, None] = None
    label_top: Union[TextBlock, None] = None
    label_bottom: Union[TextBlock, None] = None
    tagline: Union[TextBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {
            "word-top": self.word_top,
            "word-mid": self.word_mid,
            "word-bottom": self.word_bottom,
        }
        if self.ghost_bg is not None:
            s["ghost-bg"] = self.ghost_bg
        if self.label_top is not None:
            s["label-top"] = self.label_top
        if self.label_bottom is not None:
            s["label-bottom"] = self.label_bottom
        if self.tagline is not None:
            s["tagline"] = self.tagline
        return s


# ── Technical ─────────────────────────────────────────────────────────────────

CodeAnnotation = Union[TextBlock, ListBlock, CalloutBlock]


class CodeWalkthroughSlide(TypedSlide):
    template_id: Literal["code-walkthrough"] = "code-walkthrough"
    title: TextBlock
    code: CodeBlock
    annotation: Union[CodeAnnotation, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {
            "title": self.title,
            "code": self.code,
        }
        if self.annotation is not None:
            s["annotation"] = self.annotation
        return s


class ArchitectureDiagramSlide(TypedSlide):
    template_id: Literal["architecture-diagram"] = "architecture-diagram"
    title: TextBlock
    diagram: MediaBlock
    notes: Union[ListBlock, TextBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {
            "title": self.title,
            "diagram": self.diagram,
        }
        if self.notes is not None:
            s["notes"] = self.notes
        return s


class TerminalSlide(TypedSlide):
    template_id: Literal["terminal"] = "terminal"
    code: CodeBlock
    title: Union[TextBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {"code": self.code}
        if self.title is not None:
            s["title"] = self.title
        return s
