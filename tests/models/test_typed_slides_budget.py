"""Budget validation tests for TypedSlide @model_validator."""
import pytest
from pydantic import ValidationError

from decko_py.models.blocks import (
    CalloutBlock,
    CodeBlock,
    KineticTextBlock,
    ListBlock,
    MediaBlock,
    TextBlock,
)
from decko_py.models.rich_text import InlineNode, ListItem
from decko_py.models.typed_slides import (
    AgendaSlide,
    KineticHeroSlide,
    SectionBreakSlide,
    SingleColumnSlide,
    TitleSlide,
)


# ── _extract_text helpers ─────────────────────────────────────────────────────


class TestExtractText:
    def test_textblock_str(self):
        from decko_py.models.utils.text_utils import _extract_text

        assert _extract_text(TextBlock(content="hello world")) == "hello world"

    def test_textblock_inline_nodes(self):
        from decko_py.models.utils.text_utils import _extract_text

        block = TextBlock(content=[InlineNode(text="Hello"), InlineNode(text=" world")])
        assert _extract_text(block) == "Hello world"

    def test_calloutblock_body_only(self):
        from decko_py.models.utils.text_utils import _extract_text

        assert _extract_text(CalloutBlock(body="watch out")) == "watch out"

    def test_calloutblock_title_and_body(self):
        from decko_py.models.utils.text_utils import _extract_text

        block = CalloutBlock(title="Note", body="some body text")
        result = _extract_text(block)
        assert "Note" in result
        assert "some body text" in result

    def test_calloutblock_inline_title(self):
        from decko_py.models.utils.text_utils import _extract_text

        block = CalloutBlock(title=[InlineNode(text="Tip")], body="details")
        result = _extract_text(block)
        assert "Tip" in result
        assert "details" in result

    def test_kinetictextblock(self):
        from decko_py.models.utils.text_utils import _extract_text

        block = KineticTextBlock(content="IMPACT")
        assert _extract_text(block) == "IMPACT"

    def test_listblock_flat(self):
        from decko_py.models.utils.text_utils import _extract_text

        block = ListBlock(items=[ListItem(text="Alpha"), ListItem(text="Beta")])
        result = _extract_text(block)
        assert "Alpha" in result
        assert "Beta" in result

    def test_listblock_nested_children(self):
        from decko_py.models.utils.text_utils import _extract_text

        child = ListItem(text="child item")
        parent = ListItem(text="parent item", children=[child])
        block = ListBlock(items=[parent])
        result = _extract_text(block)
        assert "parent item" in result
        assert "child item" in result

    def test_listblock_inline_nodes(self):
        from decko_py.models.utils.text_utils import _extract_text

        block = ListBlock(items=[ListItem(text=[InlineNode(text="Bold item", bold=True)])])
        result = _extract_text(block)
        assert "Bold item" in result

    def test_non_text_block_returns_none(self):
        from decko_py.models.utils.text_utils import _extract_text

        assert _extract_text(MediaBlock(src="https://example.com/img.png")) is None
        assert _extract_text(CodeBlock(code="x = 1")) is None

    def test_unknown_object_returns_none(self):
        from decko_py.models.utils.text_utils import _extract_text

        assert _extract_text(object()) is None


# ── TitleSlide ────────────────────────────────────────────────────────────────


class TestTitleSlideBudget:
    def test_passes_within_budget(self):
        TitleSlide(headline="Short headline")  # no exception

    def test_headline_max_chars_violation(self):
        with pytest.raises(ValidationError, match="headline"):
            TitleSlide(headline="x" * 121)

    def test_headline_at_limit_passes(self):
        TitleSlide(headline="x" * 120)  # exactly at limit

    def test_subtitle_max_chars_violation(self):
        with pytest.raises(ValidationError, match="subtitle"):
            TitleSlide(headline="Valid", subtitle="y" * 201)

    def test_subtitle_within_budget_passes(self):
        TitleSlide(headline="Valid", subtitle="y" * 200)

    def test_eyebrow_max_chars_violation(self):
        with pytest.raises(ValidationError, match="eyebrow"):
            TitleSlide(headline="Valid", eyebrow="e" * 61)

    def test_optional_slot_omitted_passes(self):
        TitleSlide(headline="Valid")  # subtitle/eyebrow/logo all None

    def test_multiple_violations_reported(self):
        with pytest.raises(ValidationError) as exc_info:
            TitleSlide(headline="x" * 121, subtitle="y" * 201)
        msg = str(exc_info.value)
        assert "headline" in msg
        assert "subtitle" in msg

    def test_media_block_logo_skipped(self):
        # MediaBlock has no text budget — should not raise
        TitleSlide(
            headline="Valid",
            logo=MediaBlock(src="https://example.com/logo.png"),
        )


# ── SectionBreakSlide ─────────────────────────────────────────────────────────


class TestSectionBreakSlideBudget:
    def test_passes_within_budget(self):
        SectionBreakSlide(title="Section One")

    def test_title_violation(self):
        with pytest.raises(ValidationError, match="title"):
            SectionBreakSlide(title="t" * 101)

    def test_label_violation(self):
        with pytest.raises(ValidationError, match="label"):
            SectionBreakSlide(title="Valid", label="l" * 61)

    def test_description_violation(self):
        with pytest.raises(ValidationError, match="description"):
            SectionBreakSlide(title="Valid", description="d" * 201)


# ── AgendaSlide ───────────────────────────────────────────────────────────────


class TestAgendaSlideBudget:
    def test_passes_within_budget(self):
        AgendaSlide(items=ListBlock(items=[ListItem(text="Item one"), ListItem(text="Item two")]))

    def test_list_aggregate_word_violation(self):
        with pytest.raises(ValidationError, match="items"):
            AgendaSlide(items=ListBlock(items=[ListItem(text="word " * 81)]))

    def test_list_aggregate_at_limit_passes(self):
        words = " ".join(["w"] * 80)
        AgendaSlide(items=ListBlock(items=[ListItem(text=words)]))

    def test_title_violation(self):
        with pytest.raises(ValidationError, match="title"):
            AgendaSlide(
                items=ListBlock(items=[ListItem(text="ok")]),
                title="t" * 81,
            )


# ── SingleColumnSlide ─────────────────────────────────────────────────────────


class TestSingleColumnSlideBudget:
    def test_passes_within_budget(self):
        SingleColumnSlide(title="Title", body="Short body text")

    def test_body_max_chars_violation(self):
        with pytest.raises(ValidationError, match="body"):
            SingleColumnSlide(title="Title", body="x" * 601)

    def test_body_max_words_violation(self):
        with pytest.raises(ValidationError, match="body"):
            SingleColumnSlide(title="Title", body=" ".join(["word"] * 101))

    def test_callout_body_budget_checked(self):
        with pytest.raises(ValidationError, match="body"):
            SingleColumnSlide(
                title="Title",
                body=CalloutBlock(body="w " * 101),
            )


# ── KineticHeroSlide (KineticTextBlock) ───────────────────────────────────────


class TestKineticHeroSlideBudget:
    def test_passes_within_budget(self):
        KineticHeroSlide(word_top="SCALE", word_mid="FAST", word_bottom="NOW")

    def test_word_top_violation(self):
        with pytest.raises(ValidationError, match="word-top"):
            KineticHeroSlide(word_top="x" * 31, word_mid="OK", word_bottom="OK")

    def test_word_mid_violation(self):
        with pytest.raises(ValidationError, match="word-mid"):
            KineticHeroSlide(word_top="OK", word_mid="x" * 31, word_bottom="OK")

    def test_word_bottom_at_limit_passes(self):
        KineticHeroSlide(word_top="OK", word_mid="OK", word_bottom="x" * 30)


# ── Unknown template (no definition) ─────────────────────────────────────────


class TestNoDefinitionSkipsValidation:
    def test_custom_template_id_skips_budget_check(self):
        from decko_py.models.typed_slides import TypedSlide
        from typing import Literal

        class CustomSlide(TypedSlide):
            template_id: Literal["x-unknown"] = "x-unknown"

            def _build_slots(self):
                return {}

        CustomSlide()  # definition() returns None — should not raise
