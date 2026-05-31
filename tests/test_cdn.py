from decko_py.cdn import CDN_BASE, CdnConfig


def test_cdn_defaults():
    cdn = CdnConfig()
    assert cdn.version == "latest"
    assert cdn.base == CDN_BASE


def test_cdn_js_url():
    cdn = CdnConfig(version="1.2.3")
    assert cdn.js == f"{CDN_BASE}@1.2.3/dist/browser/index.global.js"


def test_cdn_base_css_url():
    cdn = CdnConfig(version="1.0.0")
    assert cdn.base_css == f"{CDN_BASE}@1.0.0/dist/css/decko-base.css"


def test_cdn_templates_css_url():
    cdn = CdnConfig(version="2.0.0")
    assert cdn.templates_css == f"{CDN_BASE}@2.0.0/dist/css/decko-templates.css"


def test_cdn_theme_css_url():
    cdn = CdnConfig(version="1.0.0")
    assert cdn.theme_css("midnight") == f"{CDN_BASE}@1.0.0/dist/css/decko-theme-midnight.css"
    assert cdn.theme_css("nova") == f"{CDN_BASE}@1.0.0/dist/css/decko-theme-nova.css"


def test_cdn_latest_urls_contain_latest():
    cdn = CdnConfig()
    assert "@latest/" in cdn.js
    assert "@latest/" in cdn.base_css
