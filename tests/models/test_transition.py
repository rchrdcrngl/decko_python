import pytest
from pydantic import TypeAdapter

from decko_py.models.transition import (
    CutTransition,
    FadeTransition,
    MorphTransition,
    PanTransition,
    ParticleBurstTransition,
    SlideTransition,
    WipeTransition,
    ZoomOutTransition,
    ZoomThroughTransition,
)

adapter = TypeAdapter(SlideTransition)


def test_cut():
    t = CutTransition()
    assert t.type == "cut"


def test_fade_with_duration():
    t = FadeTransition(duration=0.5)
    assert t.duration == 0.5


def test_zoom_through():
    t = ZoomThroughTransition(target_id="hero-img")
    d = t.model_dump(by_alias=True)
    assert d["targetId"] == "hero-img"


def test_zoom_out():
    t = ZoomOutTransition(origin_id="logo")
    d = t.model_dump(by_alias=True)
    assert d["originId"] == "logo"


def test_pan_directions():
    for direction in ("left", "right", "up", "down"):
        t = PanTransition(direction=direction)  # type: ignore[arg-type]
        assert t.direction == direction


def test_morph():
    t = MorphTransition(from_id="slide-a-img", to_id="slide-b-img")
    d = t.model_dump(by_alias=True)
    assert d["fromId"] == "slide-a-img"
    assert d["toId"] == "slide-b-img"


def test_particle_burst():
    t = ParticleBurstTransition(origin_id="star")
    d = t.model_dump(by_alias=True)
    assert d["originId"] == "star"


def test_wipe():
    t = WipeTransition(direction="right")
    assert t.direction == "right"


def test_discriminated_union_cut():
    t = adapter.validate_python({"type": "cut"})
    assert isinstance(t, CutTransition)


def test_discriminated_union_pan():
    t = adapter.validate_python({"type": "pan", "direction": "up"})
    assert isinstance(t, PanTransition)
    assert t.direction == "up"


def test_discriminated_union_invalid():
    with pytest.raises(Exception):  # noqa: B017
        adapter.validate_python({"type": "teleport"})
