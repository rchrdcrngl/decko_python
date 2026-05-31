from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing_extensions import Annotated

from decko_py.models.animation import BlockAnimation
from decko_py.models.blocks import Block
from decko_py.models.composition import Composition
from decko_py.models.theme import DeckTheme
from decko_py.models.transition import SlideTransition

# ── SlideBackground ───────────────────────────────────────────────────────────


class ColorBackground(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    type: Literal["color"] = "color"
    value: str


class ImageBackground(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    type: Literal["image"] = "image"
    src: str
    overlay: Union[float, None] = None


class GradientBackground(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    type: Literal["gradient"] = "gradient"
    value: str


class ThemeBackground(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    type: Literal["theme"] = "theme"


SlideBackground = Annotated[
    Union[ColorBackground, ImageBackground, GradientBackground, ThemeBackground],
    Field(discriminator="type"),
]

# ── SlideAmbient ──────────────────────────────────────────────────────────────


class SlideAmbient(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: Literal["particles", "gradient-shift", "aurora", "constellation", "ripple", "orbs"]
    intensity: Union[Literal["low", "medium", "high"], None] = None


# ── SlotStyle ─────────────────────────────────────────────────────────────────


class SlotStyle(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    position: Union[Literal["absolute", "relative", "fixed"], None] = None
    top: Union[str, None] = None
    left: Union[str, None] = None
    right: Union[str, None] = None
    bottom: Union[str, None] = None
    width: Union[str, None] = None
    height: Union[str, None] = None
    z_index: Union[int, None] = None
    transform_origin: Union[str, None] = None


LayoutMode = Literal["auto", "top-heavy", "bottom-heavy", "centered", "split"]

# ── Slide ─────────────────────────────────────────────────────────────────────


class Slide(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: Union[str, None] = None
    template_id: str
    layout_mode: Union[LayoutMode, None] = None
    background: Union[SlideBackground, None] = None
    slots: dict[str, Union[Block, list[Block]]]
    composition: Union[Composition, None] = None
    transition: Union[SlideTransition, None] = None
    ambient: Union[SlideAmbient, None] = None
    animations: Union[dict[str, BlockAnimation], None] = None
    slot_styles: Union[dict[str, SlotStyle], None] = None
    notes: Union[str, None] = None


# ── DeckMeta ──────────────────────────────────────────────────────────────────

AspectRatio = Literal["16:9", "4:3", "1:1"]


class DeckMeta(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    title: str
    author: Union[str, None] = None
    org: Union[str, None] = None
    date: Union[str, None] = None
    aspect_ratio: AspectRatio = "16:9"
    language: str = "en"


# ── Deck ──────────────────────────────────────────────────────────────────────


class Deck(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    version: Literal["1"] = "1"
    meta: DeckMeta
    theme: DeckTheme
    variables: Union[dict[str, str], None] = None
    slides: list[Slide]
