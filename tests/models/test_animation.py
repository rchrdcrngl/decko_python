from decko_py.models.animation import AnimatableProps, BlockAnimation


def test_block_animation_minimal():
    anim = BlockAnimation(preset="fade-in")
    assert anim.preset == "fade-in"
    assert anim.delay is None


def test_block_animation_from_to():
    anim = BlockAnimation(
        duration=0.5,
        delay=0.1,
        from_props=AnimatableProps(opacity=0.0, y=20.0),
        to_props=AnimatableProps(opacity=1.0, y=0.0),
    )
    assert anim.from_props is not None
    assert anim.from_props.opacity == 0.0
    assert anim.to_props is not None
    assert anim.to_props.y == 0.0


def test_block_animation_camel_alias():
    anim = BlockAnimation(
        from_props=AnimatableProps(scale_x=1.5),
        to_props=AnimatableProps(scale_x=1.0),
    )
    d = anim.model_dump(by_alias=True)
    assert "fromProps" in d
    assert "toProps" in d


def test_animatable_props_camel():
    props = AnimatableProps(rotate_z=45.0, skew_x=10.0)
    d = props.model_dump(by_alias=True)
    assert "rotateZ" in d
    assert "skewX" in d


def test_block_animation_target_modes():
    for target in ("block", "chars", "words", "lines"):
        anim = BlockAnimation(target=target)  # type: ignore[arg-type]
        assert anim.target == target


def test_block_animation_css_mode():
    anim = BlockAnimation(mode="css")
    assert anim.mode == "css"
