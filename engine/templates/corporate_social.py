"""
Corporate Social Media Graphic Template (1080x1080).
Square multi-channel social media post with corporate header, focal takeaway card, 3 KPI pill cards, and engagement prompt.
"""
from engine.models import GeneratedContent
from engine.palettes import get_palette
from engine.svg_builder import SVGBuilder
from engine.icons import render_icon


def render_corporate_social(content: GeneratedContent) -> str:
    width = 1080
    height = 1080
    palette = get_palette(content.color_theme or content.category)
    builder = SVGBuilder(width, height, palette)

    builder.draw_background(show_decorations=True)

    # Top Brand Bar
    builder.elements.append(
        f'<circle cx="85" cy="85" r="14" fill="url(#accentGradient)" />'
    )
    builder.draw_text(
        x=115,
        y=92,
        text=content.category.upper(),
        font_size=16,
        font_weight="800",
        color=palette.text_primary,
        letter_spacing="1.5px",
    )
    builder.draw_badge(
        x=width - 230,
        y=70,
        text="EXECUTIVE BRIEFING",
        icon_name="shield_check",
        badge_bg=palette.badge_bg,
        badge_color=palette.badge_text,
        font_size=11,
    )

    # Headline
    y_headline = builder.draw_text(
        x=80,
        y=175,
        text=content.headline,
        font_size=42,
        font_weight="900",
        color=palette.text_primary,
        max_chars=32,
        line_height_mult=1.18,
    )

    # Subtitle
    y_sub = builder.draw_text(
        x=80,
        y=y_headline + 40,
        text=content.subtitle,
        font_size=18,
        font_weight="400",
        color=palette.text_secondary,
        max_chars=54,
        line_height_mult=1.4,
    )

    # Central Insight Card
    center_y = max(y_sub + 45, 340)
    card_w = width - 160
    card_h = 240

    builder.draw_card(
        x=80,
        y=center_y,
        w=card_w,
        h=card_h,
        rx=24,
        fill=palette.card_bg,
        stroke=palette.card_border,
        stroke_width=1.5,
        has_shadow=True,
        accent_top_bar=True,
    )

    # Top icon in card
    builder.elements.append(
        render_icon("target", 115, center_y + 35, 32, palette.highlight, 2.0)
    )
    builder.draw_text(
        x=160,
        y=center_y + 57,
        text="STRATEGIC IMPERATIVE",
        font_size=14,
        font_weight="800",
        color=palette.text_accent,
        letter_spacing="1.2px",
    )

    # Main Insight Body Text
    insight_text = (
        content.items[0].description if content.items
        else "Organizations transitioning to automated intelligence workflows observe 3.5x faster cycle times and superior resilience."
    )
    builder.draw_text(
        x=115,
        y=center_y + 115,
        text=insight_text,
        font_size=20,
        font_weight="600",
        color=palette.text_primary,
        max_chars=46,
        line_height_mult=1.4,
    )

    # 3 Stat Pill Cards in row below center card
    stats_y = center_y + card_h + 35
    stat_w = (card_w - 40) / 3
    stat_h = 175
    gap_stat = 20

    stats_to_display = content.stats[:3]
    default_stats = [
        {"val": "+185%", "lbl": "Annual Efficiency", "icn": "trending_up"},
        {"val": "99.9%", "lbl": "System Reliability", "icn": "shield_check"},
        {"val": "10x", "lbl": "Time to Value", "icn": "zap"},
    ]

    for i in range(3):
        sx = 80 + i * (stat_w + gap_stat)
        if i < len(stats_to_display):
            v = stats_to_display[i].value
            l = stats_to_display[i].label
            c = stats_to_display[i].icon or "chart_bar"
        else:
            v = default_stats[i]["val"]
            l = default_stats[i]["lbl"]
            c = default_stats[i]["icn"]

        builder.draw_card(
            x=sx,
            y=stats_y,
            w=stat_w,
            h=stat_h,
            rx=20,
            fill=palette.card_bg,
            stroke=palette.card_border,
            stroke_width=1.2,
            has_shadow=True,
        )

        builder.elements.append(
            render_icon(c, sx + 24, stats_y + 24, 26, palette.highlight, 2.0)
        )

        builder.draw_text(
            x=sx + 24,
            y=stats_y + 95,
            text=v,
            font_size=34,
            font_weight="900",
            color=palette.text_primary,
        )

        builder.draw_text(
            x=sx + 24,
            y=stats_y + 130,
            text=l,
            font_size=14,
            font_weight="500",
            color=palette.text_secondary,
            max_chars=18,
            line_height_mult=1.25,
        )

    # Bottom Engagement bar
    builder.draw_footer(content.footer)
    return builder.to_svg()
