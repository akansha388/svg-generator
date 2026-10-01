"""
Promotional Banner Template (1200x630).
Hero banner layout featuring punchy headline, value proposition chips, CTA button, and decorative vector visuals.
"""
from engine.models import GeneratedContent
from engine.palettes import get_palette
from engine.svg_builder import SVGBuilder
from engine.icons import render_icon


def render_promotional_banner(content: GeneratedContent) -> str:
    width = 1200
    height = 630
    palette = get_palette(content.color_theme or content.category)
    builder = SVGBuilder(width, height, palette)

    builder.draw_background(show_decorations=True)

    # Left content column: X = 80, Right visual area: X = 720 to 1120
    # Category badge
    builder.draw_badge(
        x=80,
        y=80,
        text=content.badge or content.category,
        icon_name="sparkles",
        badge_bg=palette.badge_bg,
        badge_color=palette.badge_text,
        font_size=12,
    )

    # Main Headline
    y_headline = builder.draw_text(
        x=80,
        y=155,
        text=content.headline,
        font_size=42,
        font_weight="800",
        color=palette.text_primary,
        max_chars=28,
        line_height_mult=1.18,
    )

    # Subtitle / description
    y_sub = builder.draw_text(
        x=80,
        y=y_headline + 40,
        text=content.subtitle,
        font_size=18,
        font_weight="400",
        color=palette.text_secondary,
        max_chars=44,
        line_height_mult=1.45,
    )

    # Value props chips (up to 3 horizontal/stacked items)
    items_to_show = content.items[:3]
    chip_y = y_sub + 36
    for item in items_to_show:
        builder.draw_card(
            x=80,
            y=chip_y,
            w=540,
            h=52,
            rx=12,
            fill="rgba(255, 255, 255, 0.04)",
            stroke="rgba(255, 255, 255, 0.12)",
            has_shadow=False,
        )
        # Item icon
        icon_svg = render_icon(
            item.icon or "check_circle",
            x=96,
            y=chip_y + 14,
            size=22,
            color=palette.primary_accent,
            stroke_width=2.0,
        )
        builder.elements.append(icon_svg)
        # Item title & text
        builder.draw_text(
            x=130,
            y=chip_y + 32,
            text=f"{item.title}: {item.description}"[:60] + ("..." if len(item.description) > 35 else ""),
            font_size=14,
            font_weight="600",
            color=palette.text_primary,
            max_chars=55,
        )
        chip_y += 62

    # Call to action button
    cta_text = content.cta.text if content.cta else "Get Started Now"
    builder.draw_cta_button(
        x=80,
        y=min(chip_y + 12, 520),
        text=cta_text,
        w=220,
        h=50,
    )

    # Right Hero Card / Visual Element
    hero_x = 680
    hero_y = 110
    hero_w = 440
    hero_h = 440
    
    # Outer decorative glow ring
    builder.elements.append(
        f'<circle cx="{hero_x + hero_w/2:.1f}" cy="{hero_y + hero_h/2:.1f}" r="210" '
        f'fill="none" stroke="{palette.primary_accent}" stroke-width="1.5" stroke-dasharray="6 6" opacity="0.35" />'
    )
    builder.elements.append(
        f'<circle cx="{hero_x + hero_w/2:.1f}" cy="{hero_y + hero_h/2:.1f}" r="235" '
        f'fill="none" stroke="{palette.secondary_accent}" stroke-width="1" stroke-dasharray="12 12" opacity="0.2" />'
    )

    # Main Hero Feature Card
    builder.draw_card(
        x=hero_x,
        y=hero_y,
        w=hero_w,
        h=hero_h,
        rx=24,
        fill=palette.card_bg,
        stroke=palette.card_border,
        stroke_width=1.5,
        has_shadow=True,
        accent_top_bar=True,
    )

    # Large Center Vector Illustration/Icon in Hero Card
    hero_icon_name = content.items[0].icon if content.items else "sparkles"
    builder.elements.append(
        f'<circle cx="{hero_x + hero_w/2:.1f}" cy="{hero_y + 120:.1f}" r="56" '
        f'fill="url(#accentGradient)" opacity="0.15" />'
    )
    hero_icon = render_icon(
        hero_icon_name,
        x=hero_x + hero_w/2 - 32,
        y=hero_y + 88,
        size=64,
        color=palette.highlight,
        stroke_width=1.8,
    )
    builder.elements.append(hero_icon)

    # Stat / Key Highlight inside hero card
    if content.stats:
        main_stat = content.stats[0]
        builder.draw_text(
            x=hero_x + hero_w/2,
            y=hero_y + 230,
            text=main_stat.value,
            font_size=48,
            font_weight="900",
            color=palette.text_primary,
            text_anchor="middle",
        )
        builder.draw_text(
            x=hero_x + hero_w/2,
            y=hero_y + 265,
            text=main_stat.label,
            font_size=15,
            font_weight="600",
            color=palette.text_secondary,
            text_anchor="middle",
        )
        if main_stat.percentage:
            builder.draw_progress_bar(
                x=hero_x + 50,
                y=hero_y + 295,
                w=hero_w - 100,
                h=8,
                percentage=main_stat.percentage,
                color=palette.primary_accent,
            )
    else:
        builder.draw_text(
            x=hero_x + hero_w/2,
            y=hero_y + 220,
            text="OPTIMIZED PERFORMANCE",
            font_size=18,
            font_weight="800",
            color=palette.text_primary,
            text_anchor="middle",
            letter_spacing="1.5px",
        )
        builder.draw_text(
            x=hero_x + hero_w/2,
            y=hero_y + 255,
            text="Engineered for Scalable Excellence",
            font_size=14,
            font_weight="500",
            color=palette.text_secondary,
            text_anchor="middle",
        )

    # Floating mini-metric pill in bottom corner of hero card
    builder.draw_card(
        x=hero_x + 40,
        y=hero_y + 350,
        w=hero_w - 80,
        h=54,
        rx=16,
        fill="rgba(255, 255, 255, 0.05)",
        stroke="rgba(255, 255, 255, 0.15)",
        has_shadow=False,
    )
    metric_icon = render_icon("shield_check", hero_x + 56, hero_y + 365, 22, palette.primary_accent)
    builder.elements.append(metric_icon)
    builder.draw_text(
        x=hero_x + 90,
        y=hero_y + 382,
        text="Verified Production Quality",
        font_size=14,
        font_weight="700",
        color=palette.text_primary,
    )

    builder.draw_footer(content.footer)
    return builder.to_svg()
