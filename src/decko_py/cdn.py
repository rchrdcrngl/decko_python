from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

CDN_BASE = "https://unpkg.com/@deckohq/decko"


class CdnConfig(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    version: str = "latest"
    base: str = CDN_BASE

    @property
    def js(self) -> str:
        return f"{self.base}@{self.version}/dist/browser/index.global.js"

    @property
    def base_css(self) -> str:
        return f"{self.base}@{self.version}/dist/css/decko-base.css"

    @property
    def templates_css(self) -> str:
        return f"{self.base}@{self.version}/dist/css/decko-templates.css"

    def theme_css(self, theme_name: str) -> str:
        return f"{self.base}@{self.version}/dist/css/decko-theme-{theme_name}.css"
