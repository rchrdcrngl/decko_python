from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from decko_py.models.blocks import Block

TemplateCategory = Literal["narrative", "content", "data", "visual", "technical"]
LayoutMode = Literal["auto", "top-heavy", "bottom-heavy", "centered", "split"]


class ContentBudget(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    max_chars: Union[int, None] = None
    max_words: Union[int, None] = None
    max_lines: Union[int, None] = None
    recommended_chars: Union[int, None] = None


class TemplateSlot(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str
    accepts: list[str]
    required: bool
    repeatable: Union[bool, None] = None
    content_budget: ContentBudget
    default: Union[Block, None] = None


class AiHints(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    when_to_use: str
    good_for: list[str]
    avoid: list[str]
    suggested_follow_up: list[str]


class TemplateDefinition(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str
    name: str
    category: TemplateCategory
    description: str
    slots: list[TemplateSlot]
    layout_modes: list[LayoutMode]
    ai_hints: AiHints


class BaseTemplate(TemplateDefinition):
    """Base for slide templates with hardcoded `id` defaults."""
