"""
Unit tests for the SVG quality and validation engine.
"""
from engine.validator import SVGValidator


def test_validator_detects_malformed_xml():
    validator = SVGValidator()
    malformed_svg = "<svg><rect width='100' height='100'></svg"
    res = validator.validate(malformed_svg, "bad.svg")
    assert res.is_valid is False
    assert res.status == "failed"
    assert len(res.errors) > 0


def test_validator_detects_forbidden_patterns():
    validator = SVGValidator()
    script_svg = (
        '<?xml version="1.0"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">\n'
        '  <script>alert(1)</script>\n'
        '</svg>'
    )
    res = validator.validate(script_svg, "bad_script.svg")
    assert any("forbidden" in err.lower() or "script" in err.lower() for err in res.errors)


def test_validator_detects_broken_defs_references():
    validator = SVGValidator()
    broken_svg = (
        '<?xml version="1.0"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">\n'
        '  <defs>\n'
        '    <linearGradient id="validGrad" />\n'
        '  </defs>\n'
        '  <rect fill="url(#missingGrad)" width="100" height="100" />\n'
        '</svg>'
    )
    res = validator.validate(broken_svg, "broken_ref.svg")
    assert any("broken" in w.lower() for w in res.warnings)


def test_validator_passes_clean_svg():
    validator = SVGValidator()
    clean_svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">\n'
        '  <defs>\n'
        '    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">\n'
        '      <stop offset="0%" stop-color="#0F172A" />\n'
        '      <stop offset="100%" stop-color="#1E293B" />\n'
        '    </linearGradient>\n'
        '  </defs>\n'
        '  <rect width="800" height="600" fill="url(#grad1)" />\n'
        '  <text x="50" y="80" fill="#FFFFFF" font-size="32">Headline Title</text>\n'
        '  <text x="50" y="120" fill="#94A3B8" font-size="16">Subtitle description text.</text>\n'
        '</svg>'
    )
    res = validator.validate(clean_svg, "clean.svg")
    assert res.is_valid is True
    assert res.status == "passed"
    assert res.quality_score >= 90.0
