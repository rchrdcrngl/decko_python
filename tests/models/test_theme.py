from decko_py.models.theme import DeckTheme, ThemeTokens


def test_deck_theme_builtin():
    t = DeckTheme(name="midnight")
    assert t.name == "midnight"
    assert t.tokens is None


def test_deck_theme_with_tokens():
    t = DeckTheme(name="midnight", tokens={"colorAccent": "#ff0000"})
    assert t.tokens is not None
    assert t.tokens["colorAccent"] == "#ff0000"


def test_deck_theme_custom():
    t = DeckTheme(name="my-brand", tokens={"colorBackground": "#ffffff"})
    assert t.name == "my-brand"


def test_theme_tokens_full():
    tokens = ThemeTokens(
        color_accent="#ff0000",
        color_background="#000000",
        color_surface="#111111",
        color_text="#ffffff",
        color_text_muted="#aaaaaa",
        font_display="Inter",
        font_body="Inter",
        font_mono="JetBrains Mono",
        spacing_slide="48px",
        radius_card="8px",
        motion_intensity="moderate",
    )
    d = tokens.model_dump(by_alias=True)
    assert d["colorAccent"] == "#ff0000"
    assert d["motionIntensity"] == "moderate"
    assert d["fontMono"] == "JetBrains Mono"
