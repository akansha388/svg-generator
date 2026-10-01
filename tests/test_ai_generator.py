"""
Unit tests for AI Generator across categories and templates.
"""
from engine.ai_generator import AIGenerator
from engine.models import BannerRequest


def test_ai_generator_produces_structured_content():
    ai = AIGenerator()
    req = BannerRequest(
        category="Cybersecurity",
        topic="Zero Trust Network Access & Identity Architecture",
        template="feature_highlights",
    )
    content = ai.generate_content(req, item_id="sec_test_01")
    assert content.category == "Cybersecurity"
    assert content.headline != ""
    assert content.subtitle != ""
    assert len(content.items) >= 4
    assert len(content.stats) >= 2


def test_ai_generator_quotes_and_steps():
    ai = AIGenerator()
    req_quote = BannerRequest(
        category="Finance",
        topic="Wealth Accumulation Principles",
        template="quote_banner",
    )
    content_quote = ai.generate_content(req_quote, item_id="quote_01")
    assert content_quote.quote is not None
    assert content_quote.quote.text != ""
    assert content_quote.quote.author != ""

    req_step = BannerRequest(
        category="Business and Startups",
        topic="Lean Startup Iteration Workflow",
        template="step_by_step_process",
    )
    content_step = ai.generate_content(req_step, item_id="step_01")
    assert content_step.steps is not None
    assert len(content_step.steps) >= 3
