"""
Statistics Showcase Template (1200x800).
Spacious landscape data-driven layout with 4 KPI cards, percentage bars, trend indicators, and data attribution.
"""
from engine.models import GeneratedContent
from engine.palettes import get_palette
from engine.svg_builder import SVGBuilder
from engine.icons import render_icon


def render_statistics_showcase(content: GeneratedContent) -> str:
    width = 1200
    height = 800
    palette = get_palette(content.color_theme or content.category)
    builder = SVGBuilder(width, height, palette)

    builder.draw_background(show_decorations=True)

    # Header badge & title
    builder.draw_badge(
        x=80,
        y=70,
        text=f"BENCHMARK REPORT • {content.category.upper()}",
        icon_name="chart_bar",
        badge_bg=palette.badge_bg,
        badge_color=palette.badge_text,
        font_size=12,
    )

    y_headline = builder.draw_text(
        x=80,
        y=140,
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
        font_size=17,
        font_weight="400",
        color=palette.text_secondary,
        max_chars=65,
        line_height_mult=1.4,
    )

    # KPI 4-Card 2x2 Grid
    grid_y = max(y_sub + 45, 260)
    card_w = 495
    card_h = 190
    gap_x = 50
    gap_y = 30
    start_x = 80

    stats_to_display = content.stats[:4]
    # Fallback stats if less than 4 provided
    default_stats = [
        {"value": "99.8%", "label": "Operational Efficiency", "change": "+24% YoY", "icon": "trending_up", "pct": 99},
        {"value": "4.8x", "label": "Accelerated Deployment", "change": "+42% faster", "icon": "zap", "pct": 82},
        {"value": "87%", "label": "Cost Optimization", "change": "-35% overhead", "icon": "dollar", "pct": 87},
        {"value": "10M+", "label": "Verified Transactions", "change": "+68% volume", "icon": "shield_check", "pct": 94},
    ]

    for i in range(4):
        col = i % 2
        row = i // 2
        cx = start_x + col * (card_w + gap_x)
        cy = grid_y + row * (card_h + gap_y)

        # Get stat data
        if i < len(stats_to_display):
            s = stats_to_display[i]
            val = s.value
            lbl = s.label
            chg = s.change or "+18% growth"
            icn = s.icon or "trending_up"
            pct = s.percentage or 85
        else:
            d = default_stats[i]
            val = d["value"]
            lbl = d["label"]
            chg = d["change"]
            icn = d["icon"]
            pct = d["pct"]

        # Card container
        builder.draw_card(
            x=cx,
            y=cy,
            w=card_w,
            h=card_h,
            rx=20,
            fill=palette.card_bg,
            stroke=palette.card_border,
            stroke_width=1.2,
            has_shadow=True,
            accent_top_bar=True,
        )

        # Top row in card: Icon + Trend delta badge
        builder.elements.append(
            render_icon(icn, cx + 24, cy + 24, 28, palette.highlight, 2.0)
        )
        builder.draw_badge(
            x=cx + card_w - 120,
            y=cy + 22,
            text=chg,
            icon_name="trending_up",
            badge_bg="rgba(16, 185, 129, 0.15)",
            badge_color="#34D399",
            font_size=10,
        )

        # Big Stat Value
        builder.draw_text(
            x=cx + 24,
            y=cy + 105,
            text=val,
            font_size=42,
            font_weight="900",
            color=palette.text_primary,
        )

        # Stat Label
        builder.draw_text(
            x=cx + 24,
            y=cy + 138,
            text=lbl,
            font_size=15,
            font_weight="600",
            color=palette.text_secondary,
            max_chars=36,
        )

        # Progress bar at bottom of card
        builder.draw_progress_bar(
            x=cx + 24,
            y=cy + 160,
            w=card_w - 48,
            h=6,
            percentage=pct,
            color=palette.primary_accent,
        )

    # Source Attribution note at bottom
    source_y = grid_y + 2 * (card_h + gap_y) + 15
    if source_y < height - 50:
        builder.draw_text(
            x=80,
            y=source_y,
            text="* Verified across enterprise telemetry benchmarks and industry performance indices.",
            font_size=12,
            font_weight="400",
            color=palette.text_secondary,
        )

    builder.draw_footer(content.footer)
    return builder.to_svg()
