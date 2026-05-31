from decko_py.models.blocks import XBlock
from decko_py.models.template import (
    AiHints,
    ContentBudget,
    TemplateDefinition,
    TemplateSlot,
)
from decko_py.registry import BlockRegistry, TemplateRegistry


def test_block_registry_passthrough():
    reg = BlockRegistry()
    block = XBlock(type="x-unknown", props={"k": "v"})
    html = reg.render(block)
    assert 'data-block-type="x-unknown"' in html
    assert "x-block" in html


def test_block_registry_custom_renderer():
    reg = BlockRegistry()

    @reg.register("x-badge")
    def render_badge(block: XBlock) -> str:
        return f'<span class="badge">{block.props.get("label", "")}</span>'

    block = XBlock(type="x-badge", props={"label": "New"})
    html = reg.render(block)
    assert "<span" in html
    assert "New" in html


def test_block_registry_decorator_returns_fn():
    reg = BlockRegistry()

    @reg.register("x-pill")
    def render_pill(block: XBlock) -> str:
        return "<span>pill</span>"

    assert callable(render_pill)


def test_template_registry_register_get():
    reg = TemplateRegistry()
    tmpl = TemplateDefinition(
        id="t1",
        name="T1",
        category="content",
        description="A template",
        slots=[
            TemplateSlot(
                id="main",
                accepts=["text"],
                required=True,
                content_budget=ContentBudget(),
            )
        ],
        layout_modes=["auto"],
        ai_hints=AiHints(
            when_to_use="content",
            good_for=["body"],
            avoid=[],
            suggested_follow_up=[],
        ),
    )
    reg.register(tmpl)
    assert reg.get("t1") is tmpl


def test_template_registry_get_missing():
    reg = TemplateRegistry()
    assert reg.get("nonexistent") is None


def test_template_registry_all():
    reg = TemplateRegistry()
    for i in range(3):
        reg.register(
            TemplateDefinition(
                id=f"t{i}",
                name=f"T{i}",
                category="content",
                description="x",
                slots=[
                    TemplateSlot(
                        id="m",
                        accepts=["text"],
                        required=True,
                        content_budget=ContentBudget(),
                    )
                ],
                layout_modes=["auto"],
                ai_hints=AiHints(when_to_use="x", good_for=[], avoid=[], suggested_follow_up=[]),
            )
        )
    assert len(reg.all()) == 3
