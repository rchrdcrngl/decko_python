from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class AnimatableProps(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    x: Union[float, None] = None
    y: Union[float, None] = None
    z: Union[float, None] = None
    opacity: Union[float, None] = None
    scale: Union[float, None] = None
    scale_x: Union[float, None] = None
    scale_y: Union[float, None] = None
    rotate_x: Union[float, None] = None
    rotate_y: Union[float, None] = None
    rotate_z: Union[float, None] = None
    skew_x: Union[float, None] = None
    width: Union[float, None] = None


class BlockAnimation(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    preset: Union[str, None] = None
    duration: Union[float, None] = None
    delay: Union[float, None] = None
    easing: Union[str, None] = None
    mode: Union[Literal["js", "css"], None] = None
    from_props: Union[AnimatableProps, None] = None
    to_props: Union[AnimatableProps, None] = None
    target: Union[Literal["block", "chars", "words", "lines"], None] = None
    stagger: Union[float, None] = None
    scatter: Union[bool, None] = None
