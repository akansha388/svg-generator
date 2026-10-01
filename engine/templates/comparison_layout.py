"""
Comparison Layout Template (1200x800).
Side-by-side comparative infographic comparing two methodologies, systems, or architectures.
"""
from engine.models import GeneratedContent
from engine.palettes import get_palette
from engine.svg_builder import SVGBuilder
from engine.icons import render_icon


def render_comparison_layout(content: GeneratedContent) -> str:
    width = 1200
    height = 800
    palette = get_palette(content.color_theme or content.category)
    builder = SVGBuilder(width, height, palette)

    builder.draw_background(show_decorations=True)

    # Header section
    builder.draw_badge(
        x=80,
        y=65,
        text=f"COMPARATIVE EVALUATION • {content.category.upper()}",
        icon_name="compass",
        badge_bg=palette.badge_bg,
        badge_color=palette.badge_text,
        font_size=12,
    )

    y_headline = builder.draw_text(
        x=80,
        y=135,
        text=content.headline,
        font_size=36,
        font_weight="800",
        color=palette.text_primary,
        max_chars=40,
        line_height_mult=1.18,
    )

    y_sub = builder.draw_text(
        x=80,
        y=y_headline + 35,
        text=content.subtitle,
        font_size=16,
        font_weight="400",
        color=palette.text_secondary,
        max_chars=65,
        line_height_mult=1.4,
    )

    # Side-by-Side Dual Panels
    panel_y = max(y_sub + 40, 255)
    panel_w = 495
    panel_h = 360
    left_x = 80
    right_x = 625

    # Resolve comparison points
    if content.comparison:
        left_title = content.comparison.left.title
        left_subtitle = content.comparison.left.subtitle or "Traditional Manual Workflow"
        left_points = content.comparison.left.points[:4]
        right_title = content.comparison.right.title
        right_subtitle = content.comparison.right.subtitle or "Automated AI-Driven Solution"
        right_points = content.comparison.right.points[:4]
        verdict = content.comparison.verdict
    else:
        left_title = "Traditional Approach"
        left_subtitle = "High Friction & Slow Iteration"
        left_points = [
            "Manual configuration prone to human error",
            "Siloed tools requiring disconnected context",
            "Slow release velocity measured in weeks",
            "Linear scaling costs with diminishing ROI"
        ]
        right_title = "Next-Gen AI Solution"
        right_subtitle = "Automated, Autonomous & Scalable"
        right_points = [
            "Deterministic validation & continuous governance",
            "Unified agentic workflows with context synthesis",
            "Instant programmatic output generation",
            "Exponential leverage with minimal marginal overhead"
        ]
        verdict = "Verdict: Next-gen architecture accelerates delivery cycles by 5x while eliminating bottlenecks."

    # LEFT PANEL (Muted / Warning Tone)
    builder.draw_card(
        x=left_x,
        y=panel_y,
        w=panel_w,
        h=panel_h,
        rx=20,
        fill="rgba(30, 20, 25, 0.75)",
        stroke="rgba(239, 68, 68, 0.25)",
        stroke_width=1.5,
        has_shadow=True,
    )
    # Left Header
    builder.draw_badge(
        x=left_x + 24,
        y=panel_y + 24,
        text="LEGACY STANDARD",
        icon_name="alert_circle",
        badge_bg="rgba(239, 68, 68, 0.15)",
        badge_color="#F87171",
        font_size=10,
    )
    builder.draw_text(
        x=left_x + 24,
        y=panel_y + 80,
        text=left_title,
        font_size=22,
        font_weight="700",
        color="#FCA5A5",
        max_chars=26,
    )
    builder.draw_text(
        x=left_x + 24,
        y=panel_y + 105,
        text=left_subtitle,
        font_size=13,
        font_weight="400",
        color="#E2E8F0",
    )

    # Left Points (Red Crossmarks)
    pt_y = panel_y + 145
    for pt in left_points:
        # Crossmark icon
        builder.elements.append(
            render_icon("x_mark", left_x + 24, pt_y - 12, 18, "#EF4444", 2.2)
        )
        builder.draw_text(
            x=left_x + 52,
            y=pt_y,
            text=pt,
            font_size=14,
            font_weight="500",
            color="#E2E8F0",
            max_chars=38,
            line_height_mult=1.3,
        )
        pt_y += 45

    # RIGHT PANEL (Accent / Positive Tone)
    builder.draw_card(
        x=right_x,
        y=panel_y,
        w=panel_w,
        h=panel_h,
        rx=20,
        fill="rgba(10, 35, 30, 0.78)",
        stroke="rgba(52, 211, 153, 0.35)",
        stroke_width=1.5,
        has_shadow=True,
        accent_top_bar=True,
    )
    # Right Header
    builder.draw_badge(
        x=right_x + 24,
        y=panel_y + 24,
        text="RECOMMENDED CHOICE",
        icon_name="check_circle",
        badge_bg="rgba(16, 185, 129, 0.2)",
        badge_color="#34D399",
        font_size=10,
    )
    builder.draw_text(
        x=right_x + 24,
        y=panel_y + 80,
        text=right_title,
        font_size=22,
        font_weight="700",
        color="#6EE7B7",
        max_chars=26,
    )
    builder.draw_text(
        x=right_x + 24,
        y=panel_y + 105,
        text=right_subtitle,
        font_size=13,
        font_weight="400",
        color="#D1FAE5",
    )

    # Right Points (Green Checkmarks)
    pt_y = panel_y + 145
    for pt in right_points:
        builder.elements.append(
            render_icon("check", right_x + 24, pt_y - 12, 18, "#10B981", 2.5)
        )
        builder.draw_text(
            x=right_x + 52,
            y=pt_y,
            text=pt,
            font_size=14,
            font_weight="600",
            color="#F0FDF4",
            max_chars=38,
            line_height_mult=1.3,
        )
        pt_y += 45

    # Bottom Verdict Pill / Banner
    verd_y = panel_y + panel_h + 24
    if verd_y + 45 < height - 40:
        builder.draw_card(
            x=left_x,
            y=verd_y,
            w=width - 160,
            h=50,
            rx=14,
            fill=palette.card_bg,
            stroke=palette.card_border,
            stroke_width=1.0,
            has_shadow=False,
        )
        builder.elements.append(
            render_icon("zap", left_x + 18, verd_y + 14, 22, palette.highlight, 2.0)
        )
        builder.draw_text(
            x=left_x + 50,
            y=verd_y + 31,
            text=verdict or "Autonomous architecture achieves 10x throughput with zero compromises on quality.",
            font_size=13,
            font_weight="600",
            color=palette.text_primary,
            max_chars=80,
        )

    builder.draw_footer(content.footer)
    return builder.to_svg()
