"""
Template registry and router for SVG layout generators.
"""
from typing import Dict, Callable
from engine.models import GeneratedContent
from engine.templates.promotional_banner import render_promotional_banner
from engine.templates.educational_infographic import render_educational_infographic
from engine.templates.statistics_showcase import render_statistics_showcase
from engine.templates.step_by_step_process import render_step_by_step_process
from engine.templates.quote_banner import render_quote_banner
from engine.templates.announcement_banner import render_announcement_banner
from engine.templates.comparison_layout import render_comparison_layout
from engine.templates.feature_highlights import render_feature_highlights
from engine.templates.list_infographic import render_list_infographic
from engine.templates.corporate_social import render_corporate_social

TEMPLATE_REGISTRY: Dict[str, Callable[[GeneratedContent], str]] = {
    "promotional_banner": render_promotional_banner,
    "educational_infographic": render_educational_infographic,
    "statistics_showcase": render_statistics_showcase,
    "step_by_step_process": render_step_by_step_process,
    "quote_banner": render_quote_banner,
    "announcement_banner": render_announcement_banner,
    "comparison_layout": render_comparison_layout,
    "feature_highlights": render_feature_highlights,
    "list_infographic": render_list_infographic,
    "corporate_social": render_corporate_social,
}

TEMPLATE_DIMENSIONS: Dict[str, tuple[int, int]] = {
    "promotional_banner": (1200, 630),
    "educational_infographic": (800, 1200),
    "statistics_showcase": (1200, 800),
    "step_by_step_process": (1000, 1300),
    "quote_banner": (1080, 1080),
    "announcement_banner": (1200, 630),
    "comparison_layout": (1200, 800),
    "feature_highlights": (1200, 900),
    "list_infographic": (800, 1200),
    "corporate_social": (1080, 1080),
}


def render_template(template_name: str, content: GeneratedContent) -> str:
    """Renders the specified template with content, falling back to promotional_banner if unknown."""
    renderer = TEMPLATE_REGISTRY.get(template_name, render_promotional_banner)
    return renderer(content)
