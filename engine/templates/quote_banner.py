"""
Quote Banner Template (1080x1080).
Square thought leadership layout with large vector quotation glyphs, centered typography, and speaker card.
"""
from engine.models import GeneratedContent
from engine.palettes import get_palette
from engine.svg_builder import SVGBuilder
from engine.icons import render_icon


def render_quote_banner(content: GeneratedContent) -> str:
    width = 1080
    height = 1080
    palette = get_palette(content.color_theme or content.category)
    builder = SVGBuilder(width, height, palette)

    builder.draw_background(show_decorations=True)

    # Ambient center glow orb
    builder.elements.append(
        f'<circle cx="{width/2:.1f}" cy="{height/2:.1f}" r="320" '
        f'fill="{palette.primary_accent}" opacity="0.08" filter="blur(80px)" />'
    )

    # Header category pill
    builder.draw_badge(
        x=width / 2 - 110,
        y=100,
        text=f"{content.category.upper()} INSIGHT",
        icon_name="sparkles",
        badge_bg=palette.badge_bg,
        badge_color=palette.badge_text,
        font_size=12,
    )

    # Large Vector Quote Glyph in background
    quote_glyph = (
        f'<g transform="translate({width/2 - 70:.1f}, 170) scale(4.5)" opacity="0.18" fill="{palette.highlight}">'
        f'<path d="M3 21c3 0 7-1 7-8V5c0-1.25-.75-2-2-2H4c-1.25 0-2 .75-2 2v6c0 1.25.75 2 2 2h4c0 3-1 5-5 5v3zm11 0c3 0 7-1 7-8V5c0-1.25-.75-2-2-2h-4c-1.25 0-2 .75-2 2v6c0 1.25.75 2 2 2h4c0 3-1 5-5 5v3z"/>'
        f'</g>'
    )
    builder.elements.append(quote_glyph)

    # Resolve Quote text
    if content.quote:
        q_text = f'"{content.quote.text}"'
        author_name = content.quote.author
        author_role = content.quote.role
        author_org = content.quote.organization or "Industry Visionary"
        initials = content.quote.avatar_initials or "".join([w[0] for w in author_name.split()[:2]]).upper()
    else:
        q_text = f'"{content.headline}"'
        author_name = "Distinguished Leader"
        author_role = "Chief Strategist"
        author_org = f"{content.category} Advisory Group"
        initials = "DL"

    # Quote Main Text (Centered, large display typography)
    y_quote = builder.draw_text(
        x=width / 2,
        y=330,
        text=q_text,
        font_size=34,
        font_weight="700",
        color=palette.text_primary,
        max_chars=34,
        line_height_mult=1.35,
        text_anchor="middle",
    )

    # Supporting context / subtitle
    y_sub = builder.draw_text(
        x=width / 2,
        y=y_quote + 45,
        text=content.subtitle,
        font_size=17,
        font_weight="400",
        color=palette.text_secondary,
        max_chars=50,
        line_height_mult=1.4,
        text_anchor="middle",
    )

    # Author Card at bottom
    author_card_w = 460
    author_card_h = 110
    card_x = (width - author_card_w) / 2
    card_y = min(y_sub + 60, 800)

    builder.draw_card(
        x=card_x,
        y=card_y,
        w=author_card_w,
        h=author_card_h,
        rx=20,
        fill=palette.card_bg,
        stroke=palette.card_border,
        stroke_width=1.2,
        has_shadow=True,
    )

    # Author Avatar Monogram Circle
    avatar_cx = card_x + 60
    avatar_cy = card_y + author_card_h / 2
    builder.elements.append(
        f'<circle cx="{avatar_cx:.1f}" cy="{avatar_cy:.1f}" r="32" fill="url(#accentGradient)" />'
    )
    builder.draw_text(
        x=avatar_cx,
        y=avatar_cy + 7,
        text=initials,
        font_size=18,
        font_weight="800",
        color="#FFFFFF",
        text_anchor="middle",
    )

    # Author Details
    builder.draw_text(
        x=card_x + 110,
        y=card_y + 45,
        text=author_name,
        font_size=20,
        font_weight="800",
        color=palette.text_primary,
    )
    builder.draw_text(
        x=card_x + 110,
        y=card_y + 72,
        text=f"{author_role} • {author_org}",
        font_size=14,
        font_weight="500",
        color=palette.text_secondary,
        max_chars=36,
    )

    builder.draw_footer(content.footer)
    return builder.to_svg()
