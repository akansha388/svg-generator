"""
Educational Infographic Template (800x1200).
Vertical knowledge guide with 4 concept cards, hierarchy indicators, and summary key takeaways.
"""
from engine.models import GeneratedContent
from engine.palettes import get_palette
from engine.svg_builder import SVGBuilder
from engine.icons import render_icon


def render_educational_infographic(content: GeneratedContent) -> str:
    width = 800
    height = 1200
    palette = get_palette(content.color_theme or content.category)
    builder = SVGBuilder(width, height, palette)

    builder.draw_background(show_decorations=True)

    # Header section
    builder.draw_badge(
        x=60,
        y=60,
        text=f"EDUCATIONAL GUIDE • {content.category.upper()}",
        icon_name="graduation_cap",
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

    # Concept cards: 4 stacked cards
    card_x = 60
    card_w = width - 120
    card_h = 160
    start_y = max(y_sub + 40, 260)
    
    items_to_render = content.items[:4]
    current_y = start_y

    for idx, item in enumerate(items_to_render):
        # Card container
        builder.draw_card(
            x=card_x,
            y=current_y,
            w=card_w,
            h=card_h,
            rx=16,
            fill=palette.card_bg,
            stroke=palette.card_border,
            stroke_width=1.2,
            has_shadow=True,
            accent_top_bar=False,
        )

        # Number pill / Index
        builder.elements.append(
            f'<rect x="{card_x + 20:.1f}" y="{current_y + 20:.1f}" width="40" height="40" rx="10" '
            f'fill="url(#accentGradient)" />'
        )
        builder.draw_text(
            x=card_x + 40,
            y=current_y + 45,
            text=f"0{idx+1}",
            font_size=16,
            font_weight="800",
            color="#FFFFFF",
            text_anchor="middle",
        )

        # Vector Icon
        icon_svg = render_icon(
            item.icon or "lightbulb",
            x=card_x + 75,
            y=current_y + 25,
            size=30,
            color=palette.highlight,
            stroke_width=2.0,
        )
        builder.elements.append(icon_svg)

        # Concept Title
        builder.draw_text(
            x=card_x + 120,
            y=current_y + 45,
            text=item.title,
            font_size=18,
            font_weight="700",
            color=palette.text_primary,
            max_chars=40,
        )

        # Concept Description
        builder.draw_text(
            x=card_x + 120,
            y=current_y + 75,
            text=item.description,
            font_size=14,
            font_weight="400",
            color=palette.text_secondary,
            max_chars=55,
            line_height_mult=1.35,
        )

        # Takeaway Pill at bottom of card
        tag_text = item.tag or f"Key Takeaway #{idx+1}"
        builder.draw_badge(
            x=card_x + 120,
            y=current_y + 115,
            text=tag_text,
            icon_name="check_circle",
            badge_bg="rgba(255, 255, 255, 0.05)",
            badge_color=palette.primary_accent,
            font_size=10,
        )

        current_y += card_h + 20

    # Summary Takeaway Card at bottom
    if current_y + 110 < height - 60:
        builder.draw_card(
            x=card_x,
            y=current_y + 10,
            w=card_w,
            h=90,
            rx=16,
            fill="url(#accentGradient)",
            stroke="none",
            has_shadow=True,
        )
        builder.elements.append(
            render_icon("target", card_x + 30, current_y + 40, 32, "#FFFFFF", 2.2)
        )
        builder.draw_text(
            x=card_x + 80,
            y=current_y + 45,
            text="CORE TAKEAWAY",
            font_size=14,
            font_weight="800",
            color="#FFFFFF",
            letter_spacing="1.2px",
        )
        summary_text = (
            content.stats[0].label if content.stats else "Mastering these foundational principles drives scalable success."
        )
        builder.draw_text(
            x=card_x + 80,
            y=current_y + 72,
            text=summary_text,
            font_size=14,
            font_weight="500",
            color="#FFFFFF",
            max_chars=60,
        )

    builder.draw_footer(content.footer)
    return builder.to_svg()
