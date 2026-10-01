"""
Curated color palettes and WCAG contrast calculation tools.
Designed for professional vector graphics, high visual harmony, and legibility.
"""
from __future__ import annotations
from typing import Dict, Any, Tuple
import math


class ColorPalette:
    def __init__(
        self,
        name: str,
        category_affinity: str,
        bg_start: str,
        bg_end: str,
        primary_accent: str,
        secondary_accent: str,
        highlight: str,
        card_bg: str,
        card_border: str,
        text_primary: str,
        text_secondary: str,
        text_accent: str,
        badge_bg: str,
        badge_text: str,
        shadow_color: str = "rgba(0, 0, 0, 0.45)",
    ):
        self.name = name
        self.category_affinity = category_affinity
        self.bg_start = bg_start
        self.bg_end = bg_end
        self.primary_accent = primary_accent
        self.secondary_accent = secondary_accent
        self.highlight = highlight
        self.card_bg = card_bg
        self.card_border = card_border
        self.text_primary = text_primary
        self.text_secondary = text_secondary
        self.text_accent = text_accent
        self.badge_bg = badge_bg
        self.badge_text = badge_text
        self.shadow_color = shadow_color

    def to_dict(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "bg_start": self.bg_start,
            "bg_end": self.bg_end,
            "primary_accent": self.primary_accent,
            "secondary_accent": self.secondary_accent,
            "highlight": self.highlight,
            "card_bg": self.card_bg,
            "card_border": self.card_border,
            "text_primary": self.text_primary,
            "text_secondary": self.text_secondary,
            "text_accent": self.text_accent,
            "badge_bg": self.badge_bg,
            "badge_text": self.badge_text,
            "shadow_color": self.shadow_color,
        }


# 12 Curated, WCAG-compliant design palettes
PALETTES: Dict[str, ColorPalette] = {
    "Modern Corporate": ColorPalette(
        name="Modern Corporate",
        category_affinity="Business, Technology, Announcements",
        bg_start="#0F172A",  # Slate 900
        bg_end="#1E293B",    # Slate 800
        primary_accent="#3B82F6",  # Blue 500
        secondary_accent="#06B6D4", # Cyan 500
        highlight="#60A5FA",  # Blue 400
        card_bg="rgba(30, 41, 59, 0.72)",
        card_border="rgba(148, 163, 184, 0.22)",
        text_primary="#F8FAFC",  # Slate 50
        text_secondary="#94A3B8", # Slate 400
        text_accent="#38BDF8",  # Sky 400
        badge_bg="rgba(59, 130, 246, 0.18)",
        badge_text="#60A5FA",
    ),
    "Cyberpunk Tech": ColorPalette(
        name="Cyberpunk Tech",
        category_affinity="Technology, Cybersecurity, AI",
        bg_start="#0A0A14",
        bg_end="#151226",
        primary_accent="#8B5CF6",  # Purple 500
        secondary_accent="#06B6D4", # Cyan 500
        highlight="#EC4899",  # Pink 500
        card_bg="rgba(24, 20, 43, 0.75)",
        card_border="rgba(139, 92, 246, 0.35)",
        text_primary="#FFFFFF",
        text_secondary="#A5B4FC",
        text_accent="#22D3EE",
        badge_bg="rgba(139, 92, 246, 0.22)",
        badge_text="#C084FC",
    ),
    "Emerald Growth": ColorPalette(
        name="Emerald Growth",
        category_affinity="Sustainability, Health, Finance",
        bg_start="#062C21",
        bg_end="#0B3C2D",
        primary_accent="#10B981",  # Emerald 500
        secondary_accent="#14B8A6", # Teal 500
        highlight="#34D399",  # Emerald 400
        card_bg="rgba(11, 60, 45, 0.70)",
        card_border="rgba(52, 211, 153, 0.25)",
        text_primary="#F0FDF4",
        text_secondary="#86EFAC",
        text_accent="#6EE7B7",
        badge_bg="rgba(16, 185, 129, 0.20)",
        badge_text="#A7F3D0",
    ),
    "FinTech Gold": ColorPalette(
        name="FinTech Gold",
        category_affinity="Finance, Real Estate, Business",
        bg_start="#0A0E17",
        bg_end="#141B2D",
        primary_accent="#EAB308",  # Amber/Gold 500
        secondary_accent="#F59E0B", # Amber 500
        highlight="#FDE047",  # Yellow 300
        card_bg="rgba(20, 27, 45, 0.78)",
        card_border="rgba(234, 179, 8, 0.28)",
        text_primary="#FEF9C3",
        text_secondary="#CBD5E1",
        text_accent="#FACC15",
        badge_bg="rgba(234, 179, 8, 0.16)",
        badge_text="#FDE047",
    ),
    "Sunset Gradient": ColorPalette(
        name="Sunset Gradient",
        category_affinity="Marketing, E-commerce, Social Media",
        bg_start="#2A082C",
        bg_end="#3B0D2D",
        primary_accent="#F43F5E",  # Rose 500
        secondary_accent="#F97316", # Orange 500
        highlight="#FB923C",  # Orange 400
        card_bg="rgba(48, 14, 40, 0.72)",
        card_border="rgba(244, 63, 94, 0.32)",
        text_primary="#FFF1F2",
        text_secondary="#FDA4AF",
        text_accent="#FB7185",
        badge_bg="rgba(244, 63, 94, 0.20)",
        badge_text="#FECDD3",
    ),
    "Deep Oceanic": ColorPalette(
        name="Deep Oceanic",
        category_affinity="Technology, Healthcare, Education",
        bg_start="#081F38",
        bg_end="#0D2D4F",
        primary_accent="#0284C7",  # Sky 600
        secondary_accent="#0D9488", # Teal 600
        highlight="#38BDF8",  # Sky 400
        card_bg="rgba(13, 45, 79, 0.74)",
        card_border="rgba(56, 189, 248, 0.25)",
        text_primary="#F0F9FF",
        text_secondary="#BAE6FD",
        text_accent="#7DD3FC",
        badge_bg="rgba(2, 132, 199, 0.20)",
        badge_text="#7DD3FC",
    ),
    "Royal Amethyst": ColorPalette(
        name="Royal Amethyst",
        category_affinity="Education, Productivity, Corporate",
        bg_start="#1D0E38",
        bg_end="#2E1065",
        primary_accent="#9333EA",  # Purple 600
        secondary_accent="#C026D3", # Fuchsia 600
        highlight="#D8B4FE",  # Purple 300
        card_bg="rgba(46, 16, 101, 0.68)",
        card_border="rgba(192, 38, 211, 0.28)",
        text_primary="#FAF5FF",
        text_secondary="#D8B4FE",
        text_accent="#E879F9",
        badge_bg="rgba(147, 51, 234, 0.20)",
        badge_text="#E9D5FF",
    ),
    "Crimson Shield": ColorPalette(
        name="Crimson Shield",
        category_affinity="Cybersecurity, Announcements, Real Estate",
        bg_start="#180C14",
        bg_end="#2A111B",
        primary_accent="#E11D48",  # Rose 600
        secondary_accent="#DC2626", # Red 600
        highlight="#FB7185",  # Rose 400
        card_bg="rgba(42, 17, 27, 0.76)",
        card_border="rgba(225, 29, 72, 0.30)",
        text_primary="#FFF1F2",
        text_secondary="#E2E8F0",
        text_accent="#F43F5E",
        badge_bg="rgba(225, 29, 72, 0.20)",
        badge_text="#FDA4AF",
    ),
    "Nordic Minimal": ColorPalette(
        name="Nordic Minimal",
        category_affinity="Productivity, Business, Education",
        bg_start="#111827",  # Gray 900
        bg_end="#1F2937",    # Gray 800
        primary_accent="#6366F1",  # Indigo 500
        secondary_accent="#818CF8", # Indigo 400
        highlight="#A5B4FC",  # Indigo 300
        card_bg="rgba(31, 41, 55, 0.70)",
        card_border="rgba(129, 140, 248, 0.20)",
        text_primary="#F9FAFB",
        text_secondary="#9CA3AF",
        text_accent="#818CF8",
        badge_bg="rgba(99, 102, 241, 0.18)",
        badge_text="#C7D2FE",
    ),
    "Solar Energy": ColorPalette(
        name="Solar Energy",
        category_affinity="Sustainability, Technology, Marketing",
        bg_start="#1A130B",
        bg_end="#2E1C0A",
        primary_accent="#EA580C",  # Orange 600
        secondary_accent="#CA8A04", # Yellow 600
        highlight="#FDBA74",  # Orange 300
        card_bg="rgba(46, 28, 10, 0.72)",
        card_border="rgba(234, 88, 12, 0.26)",
        text_primary="#FFF7ED",
        text_secondary="#FED7AA",
        text_accent="#FB923C",
        badge_bg="rgba(234, 88, 12, 0.20)",
        badge_text="#FFEDD5",
    ),
    "Teal Horizon": ColorPalette(
        name="Teal Horizon",
        category_affinity="Healthcare, Sustainability, E-commerce",
        bg_start="#04202C",
        bg_end="#083344",
        primary_accent="#0D9488",  # Teal 600
        secondary_accent="#06B6D4", # Cyan 500
        highlight="#2DD4BF",  # Teal 400
        card_bg="rgba(8, 51, 68, 0.70)",
        card_border="rgba(45, 212, 191, 0.25)",
        text_primary="#F0FDFA",
        text_secondary="#99F6E4",
        text_accent="#5EEAD4",
        badge_bg="rgba(13, 148, 136, 0.20)",
        badge_text="#CCFBF1",
    ),
    "Obsidian Luxe": ColorPalette(
        name="Obsidian Luxe",
        category_affinity="Real Estate, Corporate, Finance",
        bg_start="#0D0D11",
        bg_end="#1A1A22",
        primary_accent="#D97706",  # Amber 600
        secondary_accent="#B45309", # Amber 700
        highlight="#FCD34D",  # Amber 300
        card_bg="rgba(26, 26, 34, 0.82)",
        card_border="rgba(217, 119, 6, 0.30)",
        text_primary="#FFFBEB",
        text_secondary="#CBD5E1",
        text_accent="#FBBF24",
        badge_bg="rgba(217, 119, 6, 0.18)",
        badge_text="#FDE68A",
    ),
}


def get_palette(name_or_category: str) -> ColorPalette:
    """Retrieve a palette by exact name or fuzzy category match."""
    if name_or_category in PALETTES:
        return PALETTES[name_or_category]
    
    # Try fuzzy matching against category affinity
    lowered = name_or_category.lower()
    for palette in PALETTES.values():
        if lowered in palette.category_affinity.lower() or lowered in palette.name.lower():
            return palette
    
    # Default to Modern Corporate
    return PALETTES["Modern Corporate"]


# WCAG Contrast Calculation Helpers
def hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    """Convert hex string (#RRGGBB) to (r, g, b) tuple."""
    hex_code = hex_code.lstrip("#")
    if len(hex_code) == 3:
        hex_code = "".join([c * 2 for c in hex_code])
    if len(hex_code) != 6:
        return (255, 255, 255)
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))


def get_relative_luminance(rgb: Tuple[int, int, int]) -> float:
    """Compute relative luminance according to WCAG 2.1 specs."""
    normalized = []
    for c in rgb:
        s = c / 255.0
        if s <= 0.03928:
            normalized.append(s / 12.92)
        else:
            normalized.append(((s + 0.055) / 1.055) ** 2.4)
    r, g, b = normalized
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def calculate_contrast_ratio(color1_hex: str, color2_hex: str) -> float:
    """Compute contrast ratio between two hex colors (1.0 to 21.0)."""
    rgb1 = hex_to_rgb(color1_hex)
    rgb2 = hex_to_rgb(color2_hex)
    l1 = get_relative_luminance(rgb1)
    l2 = get_relative_luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)
