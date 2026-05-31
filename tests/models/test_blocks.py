import pytest
from pydantic import TypeAdapter

from decko_py.models.blocks import (
    Block,
    CalloutBlock,
    ChartBlock,
    ChartData,
    ChartDataset,
    CodeBlock,
    DividerBlock,
    GroupBlock,
    KineticTextBlock,
    ListBlock,
    MediaBlock,
    MetricBlock,
    TableBlock,
    TextBlock,
    XBlock,
)
from decko_py.models.rich_text import InlineNode, ListItem

block_adapter = TypeAdapter(Block)


def test_text_block_plain_string():
    b = TextBlock(content="hello")
    assert b.type == "text"
    assert b.content == "hello"


def test_text_block_inline_nodes():
    b = TextBlock(content=[InlineNode(text="bold", bold=True)])
    assert isinstance(b.content, list)
    assert b.content[0].bold is True


def test_text_block_camel_display():
    b = TextBlock(content="x", display="heading", id="h1")
    d = b.model_dump(by_alias=True)
    assert d["type"] == "text"
    assert d["display"] == "heading"


def test_kinetic_text_block():
    b = KineticTextBlock(content="KINETIC", font_size="4rem", ghost=True)
    d = b.model_dump(by_alias=True)
    assert d["type"] == "text-kinetic"
    assert d["fontSize"] == "4rem"
    assert d["ghost"] is True


def test_code_block():
    b = CodeBlock(code="x = 1", language="python", highlight=[1, 3])
    assert b.code == "x = 1"
    assert b.highlight == [1, 3]
    d = b.model_dump(by_alias=True)
    assert d["type"] == "code"


def test_list_block():
    b = ListBlock(
        items=[ListItem(text="a"), ListItem(text="b", checked=True)],
        display="checklist",
    )
    assert len(b.items) == 2
    assert b.items[1].checked is True


def test_media_block():
    b = MediaBlock(src="https://example.com/img.png", alt="test", display="image")
    assert b.src == "https://example.com/img.png"


def test_metric_block():
    b = MetricBlock(value=42, label="Users", delta="+5%", trend="up")
    assert b.value == 42
    d = b.model_dump(by_alias=True)
    assert d["trend"] == "up"


def test_chart_block():
    b = ChartBlock(
        chart_type="bar",
        data=ChartData(
            labels=["Q1", "Q2"],
            datasets=[ChartDataset(label="Revenue", values=[100.0, 200.0], color="#0f0")],
        ),
        title="Sales",
    )
    d = b.model_dump(by_alias=True)
    assert d["chartType"] == "bar"
    assert d["data"]["datasets"][0]["label"] == "Revenue"


def test_table_block():
    b = TableBlock(
        headers=["Name", "Score"],
        rows=[["Alice", "95"], ["Bob", "87"]],
        caption="Results",
    )
    assert b.headers == ["Name", "Score"]


def test_callout_block():
    b = CalloutBlock(body="Important!", display="warning", title="Note")
    d = b.model_dump(by_alias=True)
    assert d["type"] == "callout"
    assert d["display"] == "warning"


def test_divider_block():
    b = DividerBlock(display="line")
    assert b.type == "divider"


def test_group_block_nested():
    inner = TextBlock(content="nested")
    g = GroupBlock(blocks=[inner])
    assert g.blocks[0].type == "text"


def test_xblock_valid():
    b = XBlock(type="x-custom-widget", props={"color": "red"})
    assert b.type == "x-custom-widget"
    assert b.props["color"] == "red"


def test_xblock_invalid_type():
    with pytest.raises(Exception):  # noqa: B017
        XBlock(type="custom-widget")  # missing x- prefix


def test_xblock_invalid_type_uppercase():
    with pytest.raises(Exception):  # noqa: B017
        XBlock(type="x-Custom")  # uppercase not allowed


def test_block_discriminated_union_text():
    b = block_adapter.validate_python({"type": "text", "content": "hi"})
    assert isinstance(b, TextBlock)


def test_block_discriminated_union_chart():
    b = block_adapter.validate_python(
        {
            "type": "chart",
            "chartType": "pie",
            "data": {"labels": ["A"], "datasets": [{"values": [1.0]}]},
        }
    )
    assert isinstance(b, ChartBlock)


def test_block_discriminated_union_xblock():
    b = block_adapter.validate_python({"type": "x-foo", "props": {}})
    assert isinstance(b, XBlock)
