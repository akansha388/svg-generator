"""
Step-by-Step Process Template (1000x1300).
Vertical workflow and roadmap infographic featuring numbered milestone nodes, connected line track, and detail cards.
"""
from engine.models import GeneratedContent
from engine.palettes import get_palette
from engine.svg_builder import SVGBuilder
from engine.icons import render_icon


def render_step_by_step_process(content: GeneratedContent) -> str:
    width = 1000
    height = 1300
    palette = get_palette(content.color_theme or content.category)
    builder = SVGBuilder(width, height, palette)

    builder.draw_background(show_decorations=True)

    # Header
    builder.draw_badge(
        x=80,
        y=65,
        text=f"STEP-BY-STEP WORKFLOW • {content.category.upper()}",
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
        max_chars=38,
        line_height_mult=1.18,
    )

    y_sub = builder.draw_text(
        x=80,
        y=y_headline + 35,
        text=content.subtitle,
        font_size=16,
        font_weight="400",
        color=palette.text_secondary,
        max_chars=60,
        line_height_mult=1.4,
    )

    # Connecting vertical track line
    timeline_x = 130
    start_y = max(y_sub + 45, 270)
    step_spacing = 185
    steps_count = min(len(content.steps) if content.steps else len(content.items), 5)
    if steps_count < 3:
        steps_count = 4

    end_y = start_y + (steps_count - 1) * step_spacing

    # Background line track
    builder.elements.append(
        f'<line x1="{timeline_x}" y1="{start_y}" x2="{timeline_x}" y2="{end_y}" '
        f'stroke="rgba(255, 255, 255, 0.15)" stroke-width="4" stroke-linecap="round" />'
    )
    # Active gradient track overlay
    builder.elements.append(
        f'<line x1="{timeline_x}" y1="{start_y}" x2="{timeline_x}" y2="{end_y}" '
        f'stroke="url(#accentGradient)" stroke-width="3" stroke-linecap="round" stroke-dasharray="6 6" />'
    )

    # Steps loop
    for i in range(steps_count):
        node_y = start_y + i * step_spacing

        # Step data resolution
        if content.steps and i < len(content.steps):
            st = content.steps[i]
            title = st.title
            desc = st.description
            icn = st.icon or "check_circle"
            dur = st.duration or f"Phase {i+1}"
        elif content.items and i < len(content.items):
            it = content.items[i]
            title = it.title
            desc = it.description
            icn = it.icon or "check_circle"
            dur = f"Phase {i+1}"
        else:
            title = f"Execution Stage {i+1}"
            desc = "Implement core milestones according to defined specifications and telemetry metrics."
            icn = "check_circle"
            dur = f"Phase {i+1}"

        # Milestone Circle Node on the line
        builder.elements.append(
            f'<circle cx="{timeline_x}" cy="{node_y}" r="26" fill="{palette.card_bg}" '
            f'stroke="url(#accentGradient)" stroke-width="3" filter="url(#cardShadow)" />'
        )
        builder.draw_text(
            x=timeline_x,
            y=node_y + 6,
            text=f"{i+1}",
            font_size=18,
            font_weight="800",
            color="#FFFFFF",
            text_anchor="middle",
        )

        # Step Content Card to the right of node
        card_x = timeline_x + 55
        card_w = width - card_x - 80
        card_h = 145

        builder.draw_card(
            x=card_x,
            y=node_y - 30,
            w=card_w,
            h=card_h,
            rx=16,
            fill=palette.card_bg,
            stroke=palette.card_border,
            stroke_width=1.2,
            has_shadow=True,
            accent_top_bar=False,
        )

        # Icon inside card
        builder.elements.append(
            render_icon(icn, card_x + 20, node_y - 10, 26, palette.highlight, 2.0)
        )

        # Step Phase Tag
        builder.draw_badge(
            x=card_x + card_w - 110,
            y=node_y - 18,
            text=dur,
            badge_bg="rgba(255, 255, 255, 0.05)",
            badge_color=palette.text_accent,
            font_size=10,
        )

        # Step Title
        builder.draw_text(
            x=card_x + 60,
            y=node_y + 10,
            text=title,
            font_size=18,
            font_weight="700",
            color=palette.text_primary,
            max_chars=36,
        )

        # Step Description
        builder.draw_text(
            x=card_x + 60,
            y=node_y + 40,
            text=desc,
            font_size=14,
            font_weight="400",
            color=palette.text_secondary,
            max_chars=55,
            line_height_mult=1.35,
        )

    # Completion Banner at bottom
    comp_y = end_y + 75
    if comp_y + 70 < height - 50:
        builder.draw_card(
            x=80,
            y=comp_y,
            w=width - 160,
            h=65,
            rx=16,
            fill="url(#accentGradient)",
            stroke="none",
            has_shadow=True,
        )
        builder.elements.append(
            render_icon("award", 110, comp_y + 18, 28, "#FFFFFF", 2.2)
        )
        builder.draw_text(
            x=155,
            y=comp_y + 40,
            text="SUCCESS MILESTONE: End-to-end verified delivery ready for deployment.",
            font_size=15,
            font_weight="700",
            color="#FFFFFF",
        )

    builder.draw_footer(content.footer)
    return builder.to_svg()
