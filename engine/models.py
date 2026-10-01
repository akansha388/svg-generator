"""
Data models for the AI-Powered SVG Banner & Infographic Generation Engine.
"""
from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DesignItem(BaseModel):
    title: str
    description: str
    icon: str = "sparkles"
    tag: Optional[str] = None
    value: Optional[str] = None


class StatItem(BaseModel):
    value: str
    label: str
    change: Optional[str] = None
    icon: str = "chart_bar"
    percentage: Optional[int] = None


class StepItem(BaseModel):
    step_number: int
    title: str
    description: str
    icon: str = "check_circle"
    duration: Optional[str] = None


class ComparisonColumn(BaseModel):
    title: str
    subtitle: Optional[str] = None
    points: List[str]
    is_positive: bool = True
    highlight_pill: Optional[str] = None


class ComparisonData(BaseModel):
    left: ComparisonColumn
    right: ComparisonColumn
    verdict: Optional[str] = None


class QuoteData(BaseModel):
    text: str
    author: str
    role: str
    organization: Optional[str] = None
    avatar_initials: Optional[str] = None


class CTAData(BaseModel):
    text: str
    subtext: Optional[str] = None
    url: Optional[str] = None


class GeneratedContent(BaseModel):
    id: str
    category: str
    topic: str
    design_type: str = "Infographic"  # "Banner" or "Infographic"
    template: str
    style: str = "Modern Corporate"
    tone: str = "Professional"
    color_theme: str = "Modern Corporate"
    badge: str
    headline: str
    subtitle: str
    items: List[DesignItem] = Field(default_factory=list)
    stats: List[StatItem] = Field(default_factory=list)
    steps: List[StepItem] = Field(default_factory=list)
    comparison: Optional[ComparisonData] = None
    quote: Optional[QuoteData] = None
    cta: Optional[CTAData] = None
    footer: str = "AI Design Engine • Shri Genesis Software Solutions"
    layout_width: int = 1200
    layout_height: int = 630
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BannerRequest(BaseModel):
    category: str
    topic: str
    design_type: str = "Infographic"
    template: Optional[str] = None
    style: Optional[str] = None
    tone: Optional[str] = None
    color_theme: Optional[str] = None
    dimensions: Optional[str] = None  # e.g., "1200x630", "800x1200", "1080x1080"


class ValidationCheck(BaseModel):
    name: str
    passed: bool
    details: str


class ValidationResult(BaseModel):
    svg_file: str
    id: str
    category: str
    topic: str
    template: str
    is_valid: bool
    quality_score: float  # 0 to 100
    status: str  # "passed", "warning", "failed"
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    checks: List[ValidationCheck] = Field(default_factory=list)
    file_size_kb: float = 0.0
    element_count: int = 0
    contrast_ratio: Optional[float] = None
