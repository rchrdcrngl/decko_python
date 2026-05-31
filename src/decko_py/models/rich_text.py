from __future__ import annotations

from typing import List, Literal, Union

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class InlineAnimation(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: Literal["fade-in", "slide-up", "typewriter"]
    delay: Union[float, None] = None
    duration: Union[float, None] = None


class InlineLink(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    href: str
    target: Union[Literal["_blank", "_self"], None] = None


class InlineNode(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    text: str
    bold: Union[bool, None] = None
    italic: Union[bool, None] = None
    underline: Union[bool, None] = None
    strike: Union[bool, None] = None
    code: Union[bool, None] = None
    color: Union[str, None] = None
    bg: Union[str, None] = None
    size: Union[Literal["sm", "md", "lg", "xl"], None] = None
    font: Union[Literal["display", "body", "mono"], None] = None
    link: Union[InlineLink, None] = None
    animate: Union[InlineAnimation, None] = None


RichText = Union[str, List[InlineNode]]


class ListItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    text: RichText
    checked: Union[bool, None] = None
    icon: Union[str, None] = None
    children: List["ListItem"] = []
