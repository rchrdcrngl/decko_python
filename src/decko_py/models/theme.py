from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ThemeTokens(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    color_accent: str
    color_background: str
    color_surface: str
    color_text: str
    color_text_muted: str
    font_display: str
    font_body: str
    font_mono: str
    spacing_slide: str
    radius_card: str
    motion_intensity: Literal["none", "subtle", "moderate", "expressive"]


class DeckTheme(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    name: str
    tokens: Union[dict[str, str], None] = None
