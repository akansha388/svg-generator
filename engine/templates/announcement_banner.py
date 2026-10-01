"""
Announcement Banner Template (1200x630).
High-impact landscape announcement layout with release badge, date pill, headline, feature highlights, and action button.
"""
from engine.models import GeneratedContent
from engine.palettes import get_palette
from engine.svg_builder import SVGBuilder
from engine.icons import render_icon


def render_announcement_banner(content: GeneratedContent) -> str:
    width = 1200
    height = 630
    palette = get_palette(content.color_theme or content.category)
    builder = SVGBuilder(width, height, palette)

    builder.draw_background(show_decorations=True)

    # Header Badges: Pulsing "ANNOUNCEMENT" + Category tag + Date
    builder.draw_badge(
        x=80,
        y=70,
        text="OFFICIAL ANNOUNCEMENT",
        icon_name="bell",
        badge_bg="rgba(239, 68, 68, 0.2)",
        badge_color="#F87171",
        font_size=11,
    )
    builder.draw_badge(
        x=290,
        y=70,
        text=content.category.upper(),
        icon_name="sparkles",
        badge_bg=palette.badge_bg,
        badge_color=palette.badge_text,
        font_size=11,
    )

    # Main Headline
    y_headline = builder.draw_text(
        x=80,
        y=150,
        text=content.headline,
        font_size=40,
        font_weight="800",
        color=palette.text_primary,
        max_chars=36,
        line_height_mult=1.18,
    )

    # Subtitle
    y_sub = builder.draw_text(
        x=80,
        y=y_headline + 35,
        text=content.subtitle,
        font_size=17,
        font_weight="400",
        color=palette.text_secondary,
        max_chars=60,
        line_height_mult=1.4,
    )

    # 3 Horizontal Announcement Feature Highlights
    card_y = max(y_sub + 40, 275)
    card_w = 325
    card_h = 165
    gap = 32
    start_x = 80

    items_to_show = content.items[:3]
    default_items = [
        {"title": "Breakthrough Capabilities", "desc": "Next-gen architecture delivering higher precision and throughput.", "icon": "zap"},
        {"title": "Enterprise Security", "desc": "Hardened governance controls with end-to-end data integrity.", "icon": "shield_check"},
        {"title": "Immediate Availability", "desc": "Seamless rollout accessible across all active regions and platforms.", "icon": "globe"},
    ]

    for i in range(3):
        cx = start_x + i * (card_w + gap)
        if i < len(items_to_show):
            title = items_to_show[i].title
            desc = items_to_show[i].description
            icn = items_to_show[i].icon or "check_circle"
        else:
            title = default_items[i]["title"]
            desc = default_items[i]["desc"]
            icn = default_items[i]["icon"]

        builder.draw_card(
            x=cx,
            y=card_y,
            w=card_w,
            h=card_h,
            rx=16,
            fill=palette.card_bg,
            stroke=palette.card_border,
            stroke_width=1.2,
            has_shadow=True,
            accent_top_bar=True,
        )

        builder.elements.append(
            render_icon(icn, cx + 22, card_y + 24, 26, palette.highlight, 2.0)
        )

        builder.draw_text(
            x=cx + 22,
            y=card_y + 80,
            text=title,
            font_size=17,
            font_weight="700",
            color=palette.text_primary,
            max_chars=22,
        )

        builder.draw_text(
            x=cx + 22,
            y=card_y + 108,
            text=desc,
            font_size=13,
            font_weight="400",
            color=palette.text_secondary,
            max_chars=32,
            line_height_mult=1.35,
        )

    # Bottom Action Bar with CTA Button & Timestamp
    bot_y = card_y + card_h + 30
    if bot_y < height - 60:
        builder.draw_cta_button(
            x=80,
            y=bot_y,
            text=content.cta.text if content.cta else "Read Full Release",
            w=210,
            h=46,
        )
        builder.draw_text(
            x=320,
            y=bot_y + 28,
            text="• Live in production • Version 2026.4",
            font_size=13,
            font_weight="500",
            color=palette.text_secondary,
        )

    builder.draw_footer(content.footer)
    return builder.to_svg()
