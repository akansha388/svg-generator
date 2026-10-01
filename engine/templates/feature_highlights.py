"""
Feature Highlights Template (1200x900).
Grid-based feature matrix displaying up to 6 distinct capability cards with vector icons and detail copy.
"""
from engine.models import GeneratedContent
from engine.palettes import get_palette
from engine.svg_builder import SVGBuilder
from engine.icons import render_icon


def render_feature_highlights(content: GeneratedContent) -> str:
    width = 1200
    height = 900
    palette = get_palette(content.color_theme or content.category)
    builder = SVGBuilder(width, height, palette)

    builder.draw_background(show_decorations=True)

    # Header
    builder.draw_badge(
        x=80,
        y=65,
        text=f"KEY CAPABILITIES • {content.category.upper()}",
        icon_name="sparkles",
        badge_bg=palette.badge_bg,
        badge_color=palette.badge_text,
        font_size=12,
    )

    y_headline = builder.draw_text(
        x=80,
        y=135,
        text=content.headline,
        font_size=38,
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

    # 3x2 Grid Setup (6 cards)
    grid_y = max(y_sub + 45, 260)
    card_w = 325
    card_h = 220
    gap_x = 32
    gap_y = 28
    start_x = 80

    items_to_show = content.items[:6]
    default_items = [
        {"title": "Intelligent Automation", "desc": "Eliminate routine bottlenecks with autonomous event-driven processing.", "icon": "cpu"},
        {"title": "Zero-Trust Architecture", "desc": "Continuous cryptographic authorization and granular policy isolation.", "icon": "shield_check"},
        {"title": "Real-Time Telemetry", "desc": "High-frequency streaming metrics with predictive anomaly detection.", "icon": "chart_bar"},
        {"title": "Elastic Scalability", "desc": "Seamless dynamic provisioning across multi-region environments.", "icon": "cloud"},
        {"title": "Developer Ergonomics", "desc": "Clean API contracts, type-safe SDKs, and declarative configuration.", "icon": "code"},
        {"title": "Continuous Optimization", "desc": "Algorithmic resource reallocation lowering latency by up to 45%.", "icon": "zap"},
    ]

    for i in range(6):
        col = i % 3
        row = i // 3
        cx = start_x + col * (card_w + gap_x)
        cy = grid_y + row * (card_h + gap_y)

        if i < len(items_to_show):
            title = items_to_show[i].title
            desc = items_to_show[i].description
            icn = items_to_show[i].icon or "sparkles"
            tag = items_to_show[i].tag or f"Feature 0{i+1}"
        else:
            d = default_items[i]
            title = d["title"]
            desc = d["desc"]
            icn = d["icon"]
            tag = f"Feature 0{i+1}"

        # Card container with top accent bar
        builder.draw_card(
            x=cx,
            y=cy,
            w=card_w,
            h=card_h,
            rx=18,
            fill=palette.card_bg,
            stroke=palette.card_border,
            stroke_width=1.2,
            has_shadow=True,
            accent_top_bar=True,
        )

        # Icon with background circle
        builder.elements.append(
            render_icon(
                icon_name=icn,
                x=cx + 24,
                y=cy + 24,
                size=32,
                color=palette.highlight,
                stroke_width=2.0,
                background_circle=True,
                bg_color="rgba(255, 255, 255, 0.05)",
                bg_radius=22.0,
            )
        )

        # Feature index pill
        builder.draw_badge(
            x=cx + card_w - 95,
            y=cy + 20,
            text=tag[:10],
            badge_bg="rgba(255, 255, 255, 0.06)",
            badge_color=palette.text_accent,
            font_size=9,
        )

        # Feature title
        builder.draw_text(
            x=cx + 24,
            y=cy + 95,
            text=title,
            font_size=18,
            font_weight="700",
            color=palette.text_primary,
            max_chars=22,
        )

        # Feature description
        builder.draw_text(
            x=cx + 24,
            y=cy + 125,
            text=desc,
            font_size=13,
            font_weight="400",
            color=palette.text_secondary,
            max_chars=34,
            line_height_mult=1.4,
        )

        # "Learn More" subtle link
        builder.draw_text(
            x=cx + 24,
            y=cy + 195,
            text="Explore capability →",
            font_size=12,
            font_weight="600",
            color=palette.primary_accent,
        )

    builder.draw_footer(content.footer)
    return builder.to_svg()
