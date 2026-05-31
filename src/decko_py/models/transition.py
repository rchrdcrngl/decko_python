from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing_extensions import Annotated

Direction = Literal["left", "right", "up", "down"]


class CutTransition(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    type: Literal["cut"] = "cut"


class FadeTransition(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    type: Literal["fade"] = "fade"
    duration: Union[float, None] = None


class ZoomThroughTransition(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    type: Literal["zoom-through"] = "zoom-through"
    target_id: str


class ZoomOutTransition(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    type: Literal["zoom-out"] = "zoom-out"
    origin_id: str


class PanTransition(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    type: Literal["pan"] = "pan"
    direction: Direction


class MorphTransition(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    type: Literal["morph"] = "morph"
    from_id: str
    to_id: str


class ParticleBurstTransition(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    type: Literal["particle-burst"] = "particle-burst"
    origin_id: str


class WipeTransition(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    type: Literal["wipe"] = "wipe"
    direction: Direction


SlideTransition = Annotated[
    Union[
        CutTransition,
        FadeTransition,
        ZoomThroughTransition,
        ZoomOutTransition,
        PanTransition,
        MorphTransition,
        ParticleBurstTransition,
        WipeTransition,
    ],
    Field(discriminator="type"),
]
