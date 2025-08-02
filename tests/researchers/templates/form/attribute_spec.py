from jinjax import HTMLAttrs

def test_form_attribute_component_renders_div_with_attrs(catalog):
    rendered = catalog.render(
        "form.Attribute",
        _attrs=HTMLAttrs({"class": "flex flex-col gap-2"}),
        _content="<label>Label</label><input placeholder='Search' />",
    )

    assert '<div class="flex flex-col gap-2">' in rendered
    assert "<label>Label</label>" in rendered
    assert "<input placeholder='Search'" in rendered
    assert rendered.strip().endswith("</div>")
