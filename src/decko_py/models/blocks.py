from __future__ import annotations

import re
from typing import Any, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel
from typing_extensions import Annotated

from decko_py.models.animation import BlockAnimation
from decko_py.models.rich_text import ListItem, RichText

# ── Display literals ──────────────────────────────────────────────────────────

TextDisplay = Literal[
    "heading",
    "subheading",
    "body",
    "label",
    "caption",
    "quote",
    "eyebrow",
    "hero",
]
CodeDisplay = Literal["block", "inline", "terminal"]
ListDisplay = Literal[
    "bullets",
    "numbered",
    "steps",
    "checklist",
    "timeline",
    "icon-row",
    "pill-row",
]
MediaDisplay = Literal["image", "video", "icon", "avatar", "logo"]
MetricDisplay = Literal["kpi", "stat-callout", "ring", "progress", "rating", "badge", "inline"]
ChartDisplay = Literal["minimal", "filled", "outlined", "gradient"]
TableDisplay = Literal["default", "compact", "striped", "borderless"]
GroupDisplay = Literal["columns", "cards", "comparison", "avatars", "icon-grid", "pricing"]
CalloutDisplay = Literal["info", "warning", "success", "danger", "neutral", "highlight"]
DividerDisplay = Literal["line", "dots", "space", "gradient"]


# ── Chart data ────────────────────────────────────────────────────────────────


class ChartDataset(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    label: Union[str, None] = None
    values: list[float]
    color: Union[str, None] = None


class ChartData(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    labels: list[str]
    datasets: list[ChartDataset]


# ── Block models ──────────────────────────────────────────────────────────────


class TextBlock(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: Literal["text"] = "text"
    display: Union[TextDisplay, None] = None
    content: RichText
    id: Union[str, None] = None
    animation: Union[BlockAnimation, None] = None


class KineticTextBlock(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: Literal["text-kinetic"] = "text-kinetic"
    content: str
    font_size: Union[str, None] = None
    color: Union[str, None] = None
    font_family: Union[str, None] = None
    font_weight: Union[str, int, None] = None
    letter_spacing: Union[str, None] = None
    ghost: Union[bool, None] = None
    id: Union[str, None] = None
    animation: Union[BlockAnimation, None] = None


class CodeBlock(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: Literal["code"] = "code"
    display: Union[CodeDisplay, None] = None
    code: str
    language: Union[str, None] = None
    filename: Union[str, None] = None
    highlight: Union[list[int], None] = None
    id: Union[str, None] = None
    animation: Union[BlockAnimation, None] = None


class ListBlock(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: Literal["list"] = "list"
    display: Union[ListDisplay, None] = None
    items: list[ListItem]
    id: Union[str, None] = None
    animation: Union[BlockAnimation, None] = None


class MediaBlock(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: Literal["media"] = "media"
    display: Union[MediaDisplay, None] = None
    src: str
    alt: Union[str, None] = None
    caption: Union[RichText, None] = None
    id: Union[str, None] = None
    animation: Union[BlockAnimation, None] = None


class MetricBlock(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: Literal["metric"] = "metric"
    display: Union[MetricDisplay, None] = None
    value: Union[str, int, float]
    label: RichText
    delta: Union[str, None] = None
    trend: Union[Literal["up", "down", "neutral"], None] = None
    id: Union[str, None] = None
    animation: Union[BlockAnimation, None] = None


class ChartBlock(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: Literal["chart"] = "chart"
    display: Union[ChartDisplay, None] = None
    chart_type: Literal["bar", "line", "pie", "donut", "scatter"]
    data: ChartData
    title: Union[str, None] = None
    id: Union[str, None] = None
    animation: Union[BlockAnimation, None] = None


class TableBlock(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: Literal["table"] = "table"
    display: Union[TableDisplay, None] = None
    headers: list[RichText]
    rows: list[list[RichText]]
    caption: Union[str, None] = None
    id: Union[str, None] = None
    animation: Union[BlockAnimation, None] = None


class CalloutBlock(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: Literal["callout"] = "callout"
    display: Union[CalloutDisplay, None] = None
    title: Union[RichText, None] = None
    body: RichText
    id: Union[str, None] = None
    animation: Union[BlockAnimation, None] = None


class DividerBlock(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: Literal["divider"] = "divider"
    display: Union[DividerDisplay, None] = None
    id: Union[str, None] = None
    animation: Union[BlockAnimation, None] = None


class GroupBlock(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: Literal["group"] = "group"
    display: Union[GroupDisplay, None] = None
    blocks: list[Block] = []
    id: Union[str, None] = None
    animation: Union[BlockAnimation, None] = None


class XBlock(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: str
    props: dict[str, Any] = {}
    id: Union[str, None] = None
    animation: Union[BlockAnimation, None] = None

    @field_validator("type")
    @classmethod
    def validate_x_prefix(cls, v: str) -> str:
        if not re.match(r"^x-[a-z][a-z0-9-]*$", v):
            raise ValueError("Custom block type must match x-{name} pattern")
        return v


# XBlock cannot be in the discriminated union (type: str, not Literal).
# Pydantic tries the discriminated union first, falls back to XBlock.
_KnownBlock = Annotated[
    Union[
        TextBlock,
        KineticTextBlock,
        CodeBlock,
        ListBlock,
        MediaBlock,
        MetricBlock,
        ChartBlock,
        TableBlock,
        CalloutBlock,
        DividerBlock,
        GroupBlock,
    ],
    Field(discriminator="type"),
]

Block = Union[_KnownBlock, XBlock]
