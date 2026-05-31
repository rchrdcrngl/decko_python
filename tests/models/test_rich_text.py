import pytest

from decko_py.models.rich_text import InlineAnimation, InlineLink, InlineNode, ListItem


def test_inline_node_minimal():
    node = InlineNode(text="hello")
    assert node.text == "hello"
    assert node.bold is None


def test_inline_node_full():
    node = InlineNode(
        text="styled",
        bold=True,
        italic=True,
        underline=True,
        strike=False,
        code=False,
        color="#ff0000",
        bg="#000000",
        size="lg",
        font="mono",
        link=InlineLink(href="https://example.com", target="_blank"),
        animate=InlineAnimation(type="fade-in", delay=0.5, duration=1.0),
    )
    assert node.size == "lg"
    assert node.link is not None
    assert node.link.target == "_blank"
    assert node.animate is not None
    assert node.animate.type == "fade-in"


def test_inline_node_camel_serialization():
    node = InlineNode(text="x", font="display")
    d = node.model_dump(by_alias=True)
    assert "font" in d


def test_inline_animation_invalid_type():
    with pytest.raises(Exception):  # noqa: B017
        InlineAnimation(type="unknown-type")  # type: ignore[arg-type]


def test_list_item_nested():
    child = ListItem(text="child")
    parent = ListItem(text="parent", children=[child])
    assert len(parent.children) == 1
    assert parent.children[0].text == "child"


def test_list_item_deep_nesting():
    grandchild = ListItem(text="gc")
    child = ListItem(text="c", children=[grandchild])
    root = ListItem(text="r", children=[child])
    assert root.children[0].children[0].text == "gc"


def test_list_item_default_children():
    item = ListItem(text="solo")
    assert item.children == []


def test_inline_link_minimal():
    link = InlineLink(href="https://example.com")
    assert link.target is None
