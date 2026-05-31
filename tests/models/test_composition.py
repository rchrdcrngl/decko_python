from decko_py.models.composition import Composition


def test_composition_empty():
    c = Composition()
    assert c.density is None
    assert c.rhythm is None
    assert c.gravity is None
    assert c.accent is None


def test_composition_full():
    c = Composition(density="balanced", rhythm="normal", gravity="center", accent="#ff0")
    assert c.density == "balanced"
    assert c.accent == "#ff0"


def test_composition_serialization():
    c = Composition(density="dense", gravity="top")
    d = c.model_dump(by_alias=True)
    assert d["density"] == "dense"
    assert d["gravity"] == "top"
    assert d["rhythm"] is None
