"""
Core SVG vector primitives and assembly engine.
Produces standards-compliant, responsive, clean, and self-contained SVG files.
"""
from __future__ import annotations
import html
from typing import List, Optional, Tuple
from engine.palettes import ColorPalette
from engine.icons import render_icon


def escape_text(text: str) -> str:
    """Escapes special XML characters in text content."""
    if not text:
        return ""
    return html.escape(str(text), quote=True)


def wrap_text(text: str, max_chars: int) -> List[str]:
    """Wraps text into multiple lines based on maximum character length per line."""
    if not text:
        return []
    words = text.split()
    lines = []
    current_line = []
    current_len = 0
    for word in words:
        if current_len + len(word) + (1 if current_line else 0) <= max_chars:
            current_line.append(word)
            current_len += len(word) + (1 if len(current_line) > 1 else 0)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            current_len = len(word)
    if current_line:
        lines.append(" ".join(current_line))
    return lines


class SVGBuilder:
    def __init__(self, width: int, height: int, palette: ColorPalette):
        self.width = width
        self.height = height
        self.palette = palette
        self.defs: List[str] = []
        self.elements: List[str] = []
        self._init_standard_defs()

    def _init_standard_defs(self):
        """Initializes gradients, filters, and patterns in <defs>."""
        # Main background gradient
        self.defs.append(f"""
        <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{self.palette.bg_start}" />
            <stop offset="100%" stop-color="{self.palette.bg_end}" />
        </linearGradient>""")
        
        # Primary accent gradient
        self.defs.append(f"""
        <linearGradient id="accentGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="{self.palette.primary_accent}" />
            <stop offset="100%" stop-color="{self.palette.secondary_accent}" />
        </linearGradient>""")

        # Highlight gradient
        self.defs.append(f"""
        <linearGradient id="highlightGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{self.palette.secondary_accent}" />
            <stop offset="100%" stop-color="{self.palette.highlight}" />
        </linearGradient>""")

        # Soft Card Drop Shadow Filter
        self.defs.append("""
        <filter id="cardShadow" x="-10%" y="-10%" width="125%" height="125%">
            <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="0.35"/>
        </filter>""")

        # Glow Filter for Accents
        self.defs.append(f"""
        <filter id="accentGlow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="8" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>""")

        # Subtle Dot Grid Pattern
        self.defs.append("""
        <pattern id="dotGrid" x="0" y="0" width="32" height="32" patternUnits="userSpaceOnUse">
            <circle cx="2" cy="2" r="1.2" fill="rgba(255, 255, 255, 0.05)" />
        </pattern>""")

    def add_def(self, def_content: str):
        """Adds a custom definition to the defs section."""
        self.defs.append(def_content)

    def draw_background(self, show_decorations: bool = True):
        """Draws the canvas background with gradient and ambient vector lighting."""
        # Base background rect
        self.elements.append(
            f'<rect width="{self.width}" height="{self.height}" fill="url(#bgGradient)" />'
        )
        
        # Dotted grid overlay
        self.elements.append(
            f'<rect width="{self.width}" height="{self.height}" fill="url(#dotGrid)" />'
        )

        if show_decorations:
            # Subtle ambient light orbs
            orb_r1 = min(self.width, self.height) * 0.45
            self.elements.append(
                f'<circle cx="{self.width * 0.85:.1f}" cy="{self.height * 0.15:.1f}" r="{orb_r1:.1f}" '
                f'fill="{self.palette.primary_accent}" opacity="0.12" filter="blur(60px)" />'
            )
            orb_r2 = min(self.width, self.height) * 0.35
            self.elements.append(
                f'<circle cx="{self.width * 0.1:.1f}" cy="{self.height * 0.85:.1f}" r="{orb_r2:.1f}" '
                f'fill="{self.palette.secondary_accent}" opacity="0.08" filter="blur(50px)" />'
            )
            # Decorative subtle corner accent lines
            self.elements.append(
                f'<path d="M 0,{self.height * 0.25} L {self.width * 0.15},0" '
                f'stroke="rgba(255,255,255,0.04)" stroke-width="1.5" />'
            )
            self.elements.append(
                f'<path d="M {self.width * 0.85},{self.height} L {self.width},{self.height * 0.75}" '
                f'stroke="rgba(255,255,255,0.04)" stroke-width="1.5" />'
            )

    def draw_card(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        rx: float = 16.0,
        fill: Optional[str] = None,
        stroke: Optional[str] = None,
        stroke_width: float = 1.0,
        has_shadow: bool = True,
        accent_top_bar: bool = False,
    ):
        """Draws a modern rounded surface/card with glassmorphism border and shadow."""
        card_fill = fill or self.palette.card_bg
        card_stroke = stroke or self.palette.card_border
        shadow_attr = 'filter="url(#cardShadow)"' if has_shadow else ""
        
        self.elements.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" '
            f'fill="{card_fill}" stroke="{card_stroke}" stroke-width="{stroke_width}" {shadow_attr} />'
        )

        if accent_top_bar:
            # Top accent stripe
            self.elements.append(
                f'<path d="M {x+rx:.1f},{y:.1f} H {x+w-rx:.1f}" stroke="url(#accentGradient)" '
                f'stroke-width="3" stroke-linecap="round" />'
            )

    def draw_badge(
        self,
        x: float,
        y: float,
        text: str,
        icon_name: Optional[str] = None,
        badge_bg: Optional[str] = None,
        badge_color: Optional[str] = None,
        font_size: int = 12,
    ):
        """Draws a pill-shaped category or highlight badge."""
        clean_text = escape_text(text.upper())
        bg = badge_bg or self.palette.badge_bg
        color = badge_color or self.palette.badge_text
        
        # Approximate text length
        text_w = len(clean_text) * (font_size * 0.65)
        badge_w = text_w + (36 if icon_name else 24)
        badge_h = font_size + 14
        
        self.elements.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{badge_w:.1f}" height="{badge_h:.1f}" rx="{badge_h/2:.1f}" '
            f'fill="{bg}" stroke="{color}" stroke-width="1" stroke-opacity="0.35" />'
        )

        text_x = x + 12
        if icon_name:
            icon_svg = render_icon(
                icon_name=icon_name,
                x=x + 8,
                y=y + (badge_h - 14) / 2,
                size=14,
                color=color,
                stroke_width=2.0
            )
            self.elements.append(icon_svg)
            text_x = x + 28

        self.elements.append(
            f'<text x="{text_x:.1f}" y="{y + (badge_h/2) + (font_size*0.35):.1f}" '
            f'fill="{color}" font-family="system-ui, -apple-system, sans-serif" '
            f'font-size="{font_size}" font-weight="700" letter-spacing="1.2px">{clean_text}</text>'
        )

    def draw_text(
        self,
        x: float,
        y: float,
        text: str,
        font_size: int = 16,
        font_weight: str = "normal",
        color: Optional[str] = None,
        max_chars: Optional[int] = None,
        line_height_mult: float = 1.35,
        letter_spacing: Optional[str] = None,
        text_anchor: str = "start",
    ) -> float:
        """
        Draws text with optional word wrapping and returns the final Y position.
        Uses standard cross-platform system font stacks.
        """
        if not text:
            return y
        
        text_color = color or self.palette.text_primary
        spacing_attr = f'letter-spacing="{letter_spacing}" ' if letter_spacing else ""
        lines = wrap_text(text, max_chars) if max_chars else [text]
        line_height = font_size * line_height_mult
        
        tspan_parts = []
        for i, line in enumerate(lines):
            clean_line = escape_text(line)
            if i == 0:
                tspan_parts.append(f'<tspan x="{x:.1f}">{clean_line}</tspan>')
            else:
                tspan_parts.append(f'<tspan x="{x:.1f}" dy="{line_height:.1f}">{clean_line}</tspan>')

        svg_text = (
            f'<text x="{x:.1f}" y="{y:.1f}" fill="{text_color}" '
            f'font-family="system-ui, -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif" '
            f'font-size="{font_size}" font-weight="{font_weight}" {spacing_attr}text-anchor="{text_anchor}">'
            f'{"".join(tspan_parts)}'
            f'</text>'
        )
        self.elements.append(svg_text)
        return y + (len(lines) - 1) * line_height

    def draw_cta_button(
        self,
        x: float,
        y: float,
        text: str,
        w: float = 180.0,
        h: float = 48.0,
        rx: float = 24.0,
    ):
        """Draws a prominent call-to-action button."""
        clean_text = escape_text(text)
        # Button background with gradient
        self.elements.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" '
            f'fill="url(#accentGradient)" filter="url(#cardShadow)" />'
        )
        # Text
        self.elements.append(
            f'<text x="{x + 24:.1f}" y="{y + (h/2) + 5:.1f}" fill="#FFFFFF" '
            f'font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="700">'
            f'{clean_text}</text>'
        )
        # Arrow Icon
        arrow_svg = render_icon(
            "arrow_right",
            x=x + w - 32,
            y=y + (h - 18) / 2,
            size=18,
            color="#FFFFFF",
            stroke_width=2.5,
        )
        self.elements.append(arrow_svg)

    def draw_progress_bar(
        self,
        x: float,
        y: float,
        w: float,
        h: float = 8.0,
        percentage: int = 75,
        color: Optional[str] = None,
    ):
        """Draws a sleek progress/capacity bar."""
        fill_w = max(4.0, (w * min(100, max(0, percentage))) / 100.0)
        bar_fill = color or self.palette.primary_accent
        
        # Track background
        self.elements.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h/2:.1f}" '
            f'fill="rgba(255, 255, 255, 0.12)" />'
        )
        # Active progress fill
        self.elements.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{fill_w:.1f}" height="{h:.1f}" rx="{h/2:.1f}" '
            f'fill="{bar_fill}" />'
        )

    def draw_footer(self, text: Optional[str] = None):
        """Draws standard unobtrusive watermark / attribution footer line."""
        footer_text = escape_text(text or "AI Design Engine • Shri Genesis Software Solutions")
        y = self.height - 24
        
        # Subtle horizontal divider
        self.elements.append(
            f'<line x1="60" y1="{y - 14:.1f}" x2="{self.width - 60}" y2="{y - 14:.1f}" '
            f'stroke="rgba(255, 255, 255, 0.08)" stroke-width="1" />'
        )
        
        # Attribution text
        self.elements.append(
            f'<text x="{self.width / 2:.1f}" y="{y:.1f}" fill="{self.palette.text_secondary}" '
            f'font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="500" '
            f'opacity="0.65" text-anchor="middle" letter-spacing="0.8px">{footer_text}</text>'
        )

    def to_svg(self) -> str:
        """Renders the complete SVG string."""
        defs_block = "\n".join(self.defs)
        elements_block = "\n  ".join(self.elements)
        
        return (
            f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {self.width} {self.height}" '
            f'width="{self.width}" height="{self.height}">\n'
            f'  <defs>\n{defs_block}\n  </defs>\n'
            f'  {elements_block}\n'
            f'</svg>'
        )
