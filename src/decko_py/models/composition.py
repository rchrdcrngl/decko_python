from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Composition(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    density: Union[Literal["sparse", "balanced", "dense"], None] = None
    rhythm: Union[Literal["tight", "normal", "loose"], None] = None
    gravity: Union[Literal["top", "center", "bottom"], None] = None
    accent: Union[str, None] = None
