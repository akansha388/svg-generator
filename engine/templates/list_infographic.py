"""
List Infographic Template (800x1200).
Vertical listicle layout featuring ranked index badges (01-05), horizontal cards, icons, and takeaway summaries.
"""
from engine.models import GeneratedContent
from engine.palettes import get_palette
from engine.svg_builder import SVGBuilder
from engine.icons import render_icon


def render_list_infographic(content: GeneratedContent) -> str:
    width = 800
    height = 1200
    palette = get_palette(content.color_theme or content.category)
    builder = SVGBuilder(width, height, palette)

    builder.draw_background(show_decorations=True)

    # Header
    builder.draw_badge(
        x=60,
        y=60,
        text=f"TOP STRATEGIES • {content.category.upper()}",
        icon_name="star",
        badge_bg=palette.badge_bg,
        badge_color=palette.badge_text,
        font_size=11,
    )

    y_headline = builder.draw_text(
        x=60,
        y=125,
        text=content.headline,
        font_size=32,
        font_weight="800",
        color=palette.text_primary,
        max_chars=34,
        line_height_mult=1.2,
    )

    y_sub = builder.draw_text(
        x=60,
        y=y_headline + 30,
        text=content.subtitle,
        font_size=16,
        font_weight="400",
        color=palette.text_secondary,
        max_chars=55,
        line_height_mult=1.4,
    )

    # 5 Ranked List Cards
    card_x = 60
    card_w = width - 120
    card_h = 135
    gap_y = 18
    start_y = max(y_sub + 40, 255)

    items_to_render = content.items[:5]
    default_items = [
        {"title": "Automate Foundational Workflows", "desc": "Standardize repeatable pipelines to eliminate cognitive friction and overhead.", "icon": "zap"},
        {"title": "Implement Continuous Auditing", "desc": "Maintain observability with automated compliance telemetry and audit logs.", "icon": "shield_check"},
        {"title": "Prioritize Modularity & Decoupling", "desc": "Architect isolated micro-components that evolve without ripple regressions.", "icon": "layers"},
        {"title": "Optimize Feedback Loops", "desc": "Shorten validation intervals from hours to milliseconds with rapid CI feedback.", "icon": "trending_up"},
        {"title": "Measure Outcome-Driven Metrics", "desc": "Align operational performance against quantified business KPIs and delivery targets.", "icon": "target"},
    ]

    for i in range(5):
        cy = start_y + i * (card_h + gap_y)

        if i < len(items_to_render):
            it = items_to_render[i]
            title = it.title
            desc = it.description
            icn = it.icon or "check_circle"
            tag = it.tag or f"Priority Level {i+1}"
        else:
            d = default_items[i]
            title = d["title"]
            desc = d["desc"]
            icn = d["icon"]
            tag = f"Priority Level {i+1}"

        # Card container
        builder.draw_card(
            x=card_x,
            y=cy,
            w=card_w,
            h=card_h,
            rx=16,
            fill=palette.card_bg,
            stroke=palette.card_border,
            stroke_width=1.2,
            has_shadow=True,
            accent_top_bar=False,
        )

        # Ranked Number Pill (01, 02, etc.)
        builder.elements.append(
            f'<rect x="{card_x + 20:.1f}" y="{cy + 20:.1f}" width="46" height="46" rx="12" '
            f'fill="url(#accentGradient)" />'
        )
        builder.draw_text(
            x=card_x + 43,
            y=cy + 49,
            text=f"0{i+1}",
            font_size=18,
            font_weight="800",
            color="#FFFFFF",
            text_anchor="middle",
        )

        # Icon next to number
        builder.elements.append(
            render_icon(icn, card_x + 85, cy + 28, 28, palette.highlight, 2.0)
        )

        # Priority tag at top right
        builder.draw_badge(
            x=card_x + card_w - 140,
            y=cy + 18,
            text=tag[:16],
            badge_bg="rgba(255, 255, 255, 0.05)",
            badge_color=palette.text_accent,
            font_size=10,
        )

        # Title
        builder.draw_text(
            x=card_x + 130,
            y=cy + 45,
            text=title,
            font_size=17,
            font_weight="700",
            color=palette.text_primary,
            max_chars=34,
        )

        # Description
        builder.draw_text(
            x=card_x + 130,
            y=cy + 75,
            text=desc,
            font_size=13,
            font_weight="400",
            color=palette.text_secondary,
            max_chars=54,
            line_height_mult=1.35,
        )

    builder.draw_footer(content.footer)
    return builder.to_svg()
