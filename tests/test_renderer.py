from decko_py.cdn import CdnConfig
from decko_py.models.blocks import TextBlock, XBlock
from decko_py.models.slide import Deck, DeckMeta, Slide, SlideAmbient
from decko_py.models.theme import DeckTheme
from decko_py.models.transition import FadeTransition
from decko_py.renderer import HtmlRenderer


def make_deck(theme_name="midnight", **slide_kwargs):
    slide = Slide(
        template_id="title-slide",
        slots={"headline": TextBlock(content="Hello")},
        **slide_kwargs,
    )
    return Deck(
        meta=DeckMeta(title="Test"),
        theme=DeckTheme(name=theme_name),
        slides=[slide],
    )


def test_render_returns_string(simple_deck):
    renderer = HtmlRenderer()
    html = renderer.render(simple_deck)
    assert isinstance(html, str)


def test_render_doctype(simple_deck):
    html = HtmlRenderer().render(simple_deck)
    assert html.startswith("<!DOCTYPE html>")


def test_render_title(simple_deck):
    html = HtmlRenderer().render(simple_deck)
    assert "<title>Test Deck</title>" in html


def test_render_deck_data_script(simple_deck):
    html = HtmlRenderer().render(simple_deck)
    assert 'id="deck-data"' in html
    assert 'type="application/json"' in html


def test_render_csr_mode(simple_deck):
    html = HtmlRenderer(mode="csr").render(simple_deck)
    assert 'data-render-mode="csr"' in html


def test_render_builtin_theme_has_theme_css():
    deck = make_deck(theme_name="midnight")
    html = HtmlRenderer().render(deck)
    assert "decko-theme-midnight.css" in html


def test_render_builtin_theme_no_css_vars():
    deck = make_deck(theme_name="midnight")
    html = HtmlRenderer().render(deck)
    assert ":root" not in html


def test_render_custom_theme_has_css_vars():
    deck = Deck(
        meta=DeckMeta(title="x"),
        theme=DeckTheme(name="custom", tokens={"colorAccent": "#ff0000"}),
        slides=[Slide(template_id="t", slots={"m": TextBlock(content="x")})],
    )
    html = HtmlRenderer().render(deck)
    assert ":root" in html
    assert "--decko-color-accent: #ff0000" in html


def test_render_builtin_theme_with_token_override_has_css_vars():
    deck = Deck(
        meta=DeckMeta(title="x"),
        theme=DeckTheme(name="midnight", tokens={"colorAccent": "#123456"}),
        slides=[Slide(template_id="t", slots={"m": TextBlock(content="x")})],
    )
    html = HtmlRenderer().render(deck)
    assert "--decko-color-accent: #123456" in html


def test_render_extra_css_url():
    deck = make_deck()
    html = HtmlRenderer(extra_css_urls=["https://example.com/custom.css"]).render(deck)
    assert "https://example.com/custom.css" in html


def test_render_extra_css_inline():
    deck = make_deck()
    html = HtmlRenderer(extra_css_inline=[".foo { color: red; }"]).render(deck)
    assert ".foo { color: red; }" in html


def test_render_extra_css_file(tmp_path):
    css_file = tmp_path / "custom.css"
    css_file.write_text(".bar { color: blue; }")
    deck = make_deck()
    html = HtmlRenderer(extra_css_files=[css_file]).render(deck)
    assert ".bar { color: blue; }" in html


def test_render_extra_script_url():
    deck = make_deck()
    html = HtmlRenderer(extra_script_urls=["https://example.com/plugin.js"]).render(deck)
    assert "https://example.com/plugin.js" in html


def test_render_critical_css(simple_deck):
    html = HtmlRenderer().render(simple_deck)
    assert "html,body{background:#000}" in html


def test_render_cdn_js_tag(simple_deck):
    cdn = CdnConfig(version="1.0.0")
    html = HtmlRenderer(cdn=cdn).render(simple_deck)
    assert "dist/browser/index.global.js" in html


def test_render_nav(simple_deck):
    html = HtmlRenderer().render(simple_deck)
    assert 'id="decko-nav"' in html
    assert 'id="decko-prev"' in html
    assert 'id="decko-next"' in html


def test_render_ssr_mode():
    deck = make_deck()
    html = HtmlRenderer(mode="ssr").render(deck)
    assert 'data-render-mode="csr"' not in html
    assert 'class="decko-slide"' in html
    assert 'data-template-id="title-slide"' in html


def test_render_ssr_transition():
    deck = make_deck(transition=FadeTransition(duration=0.4))
    html = HtmlRenderer(mode="ssr").render(deck)
    assert "data-transition" in html
    assert '"fade"' in html


def test_render_ssr_ambient():
    deck = make_deck(ambient=SlideAmbient(type="particles", intensity="medium"))
    html = HtmlRenderer(mode="ssr").render(deck)
    assert 'data-ambient="particles"' in html
    assert 'data-ambient-intensity="medium"' in html


def test_render_ssr_xblock():
    from decko_py.registry import BlockRegistry

    reg = BlockRegistry()

    @reg.register("x-badge")
    def render_badge(block: XBlock) -> str:
        return '<span class="badge">X</span>'

    deck = Deck(
        meta=DeckMeta(title="x"),
        theme=DeckTheme(name="midnight"),
        slides=[Slide(template_id="t", slots={"m": XBlock(type="x-badge", props={})})],
    )
    html = HtmlRenderer(mode="ssr", block_registry=reg).render(deck)
    assert 'class="badge"' in html


def test_save_creates_file(simple_deck, tmp_path):
    out = tmp_path / "deck.html"
    HtmlRenderer().save(simple_deck, out)
    assert out.exists()
    assert "<!DOCTYPE html>" in out.read_text()
