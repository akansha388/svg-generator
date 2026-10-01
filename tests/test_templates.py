"""
Unit tests verifying all 10 layout templates render clean, valid SVGs.
"""
import pytest
from engine.models import BannerRequest
from engine.ai_generator import AIGenerator
from engine.templates import TEMPLATE_REGISTRY, render_template
from engine.validator import SVGValidator


@pytest.fixture
def ai_gen():
    return AIGenerator()


@pytest.fixture
def validator():
    return SVGValidator()


@pytest.mark.parametrize("template_name", list(TEMPLATE_REGISTRY.keys()))
def test_all_templates_render_valid_svg(ai_gen, validator, template_name):
    req = BannerRequest(
        category="Technology and AI",
        topic="Scalable Vector Graphics for Modern Interfaces",
        template=template_name,
        design_type="Infographic" if "infographic" in template_name else "Banner",
    )
    content = ai_gen.generate_content(req, item_id=f"test_{template_name}")
    svg_str = render_template(template_name, content)
    
    # Assert string has XML header and SVG tags
    assert "<?xml version=" in svg_str
    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "viewBox=" in svg_str
    
    # Validate with validator
    res = validator.validate(svg_str, f"test_{template_name}.svg", f"test_{template_name}")
    assert res.is_valid is True
    assert res.status == "passed"
    assert res.quality_score >= 85.0
    assert len(res.errors) == 0
