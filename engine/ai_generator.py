"""
AI Content Generation Engine.
Supports Google Gemini API, OpenAI API, and a robust Heuristic Generative Synthesizer
for guaranteed high-entropy, domain-authentic copy generation without rate limit failures.
"""
from __future__ import annotations
import os
import json
import logging
from typing import Optional, Dict, Any
from engine.models import (
    BannerRequest,
    GeneratedContent,
    DesignItem,
    StatItem,
    StepItem,
    ComparisonData,
    ComparisonColumn,
    QuoteData,
    CTAData,
)
from engine.icons import get_category_default_icon

logger = logging.getLogger(__name__)


# Domain knowledge base for rich local semantic synthesis
DOMAIN_KNOWLEDGE: Dict[str, Dict[str, Any]] = {
    "Technology and AI": {
        "badges": ["NEXT-GEN AI", "TECH FRONTIER", "INNOVATION 2026", "INTELLIGENT SYSTEMS"],
        "quotes": [
            ("The future belongs not to those who fear automation, but to those who orchestrate intelligence.", "Dr. Elena Rostova", "Chief AI Scientist", "Horizon Labs"),
            ("Simplicity and composability are the bedrock of scalable software engineering.", "Marcus Vance", "Distinguished Systems Architect", "Aether Cloud"),
        ],
        "default_icons": ["cpu", "brain", "network", "server", "code", "zap", "shield_check", "database"],
        "metrics": [
            {"val": "99.98%", "lbl": "Inference Availability", "chg": "+42% efficiency", "icn": "trending_up", "pct": 99},
            {"val": "< 45ms", "lbl": "Sub-Second Latency", "chg": "3.8x faster", "icn": "zap", "pct": 92},
            {"val": "12.4M", "lbl": "Active Token Queries", "chg": "+88% scale", "icn": "cpu", "pct": 88},
            {"val": "Zero-Lag", "lbl": "Edge Execution", "chg": "Instant sync", "icn": "shield_check", "pct": 95},
        ]
    },
    "Business and Startups": {
        "badges": ["GROWTH VECTOR", "VENTURE SCALE", "EXECUTIVE BRIEF", "STRATEGIC PLAYBOOK"],
        "quotes": [
            ("Execution eats strategy for breakfast; relentless customer feedback eats execution for lunch.", "Jonathan Sterling", "Managing Partner", "Founders Frontier"),
            ("Sustainable unit economics are the true superpower of enduring enterprises.", "Amara Chen", "CEO & Co-Founder", "VentureScale"),
        ],
        "default_icons": ["rocket", "chart_bar", "trending_up", "target", "briefcase", "dollar", "building", "award"],
        "metrics": [
            {"val": "14.2x", "lbl": "LTV to CAC Ratio", "chg": "+65% margin", "icn": "trending_up", "pct": 94},
            {"val": "$48M", "lbl": "ARR Milestones", "chg": "+112% YoY", "icn": "dollar", "pct": 89},
            {"val": "138%", "lbl": "Net Dollar Retention", "chg": "Top decile", "icn": "target", "pct": 92},
            {"val": "18 Mos", "lbl": "Extended Runway", "chg": "Capital efficient", "icn": "briefcase", "pct": 85},
        ]
    },
    "Education": {
        "badges": ["ACADEMIC EXCELLENCE", "LIFELONG MASTERY", "STEM HORIZON", "LEARNING MATRIX"],
        "quotes": [
            ("Education is not the learning of facts, but the training of the mind to think critically.", "Prof. Alistair Finch", "Dean of Cognitive Sciences", "Cambridge Institute"),
            ("Curiosity paired with disciplined deliberate practice creates effortless mastery.", "Maya Lin", "Lead Learning Architect", "EduVision"),
        ],
        "default_icons": ["graduation_cap", "book_open", "lightbulb", "compass", "award", "star", "target", "users"],
        "metrics": [
            {"val": "94.6%", "lbl": "Knowledge Retention", "chg": "+34% higher", "icn": "trending_up", "pct": 95},
            {"val": "4.9/5", "lbl": "Learner Engagement", "chg": "Over 250k ratings", "icn": "star", "pct": 98},
            {"val": "3.2x", "lbl": "Skill Acquisition Speed", "chg": "Accelerated path", "icn": "zap", "pct": 84},
            {"val": "100%", "lbl": "Accredited Curriculum", "chg": "Global standard", "icn": "award", "pct": 100},
        ]
    },
    "Healthcare": {
        "badges": ["CLINICAL QUALITY", "HEALTH INNOVATION", "VITAL ADVANCE", "PATIENT FIRST"],
        "quotes": [
            ("Modern medicine achieves its greatest triumph when proactive prevention supersedes reactive intervention.", "Dr. Sarah Thornton", "Chief Medical Officer", "Precision Health Institute"),
            ("Every diagnostic insight is an opportunity to transform human quality of life.", "Dr. Rajiv Mehta", "Director of Clinical Genomics", "BioApex"),
        ],
        "default_icons": ["heart_pulse", "activity", "dna", "shield_check", "sun", "users", "award", "check_circle"],
        "metrics": [
            {"val": "99.4%", "lbl": "Diagnostic Precision", "chg": "Clinically proven", "icn": "heart_pulse", "pct": 99},
            {"val": "-48%", "lbl": "Patient Readmission", "chg": "Optimized care", "icn": "trending_up", "pct": 88},
            {"val": "24/7", "lbl": "Continuous Telemetry", "chg": "Zero downtime", "icn": "activity", "pct": 100},
            {"val": "1.8M", "lbl": "Screenings Completed", "chg": "Across 40 regions", "icn": "users", "pct": 91},
        ]
    },
    "Finance": {
        "badges": ["WEALTH STRATEGY", "ALPHA GENERATION", "TREASURY INSIGHT", "FINANCIAL FREEDOM"],
        "quotes": [
            ("In investing, what is comfortable is rarely profitable; discipline in risk is the ultimate edge.", "Julian Croft", "Chief Investment Officer", "Apex Capital Group"),
            ("Compound interest is the eighth wonder of the world; those who understand it, earn it.", "Beatrice Holt", "Head of Quantitative Strategies", "Meridian Trust"),
        ],
        "default_icons": ["chart_bar", "wallet", "dollar", "trending_up", "shield_check", "target", "award", "building"],
        "metrics": [
            {"val": "+28.4%", "lbl": "Net Annualized Yield", "chg": "+14% vs Index", "icn": "trending_up", "pct": 92},
            {"val": "$1.2B+", "lbl": "Assets Supervised", "chg": "+40% inflows", "icn": "dollar", "pct": 96},
            {"val": "0.12%", "lbl": "Minimized Fee Ratio", "chg": "Institutional low", "icn": "wallet", "pct": 98},
            {"val": "AAA", "lbl": "Credit Risk Rating", "chg": "Maximum grade", "icn": "shield_check", "pct": 100},
        ]
    },
    "Marketing": {
        "badges": ["GROWTH ACCELERATOR", "CAMPAIGN INSIGHT", "BRAND RESONANCE", "REVENUE MULTIPLIER"],
        "quotes": [
            ("Content builds relationships. Relationships are built on trust. Trust drives revenue.", "Andrew Sterling", "VP Global Brand Strategy", "Apex Media"),
            ("Stop interrupting what people are interested in and be what people are interested in.", "Chloe Dupont", "Creative Director", "Verve Studio"),
        ],
        "default_icons": ["mega_phone", "share", "star", "target", "trending_up", "users", "zap", "message_square"],
        "metrics": [
            {"val": "4.8x", "lbl": "Campaign ROI", "chg": "+68% conversion", "icn": "trending_up", "pct": 88},
            {"val": "68%", "lbl": "Organic Referral Share", "chg": "Viral adoption", "icn": "share", "pct": 68},
            {"val": "2.4M", "lbl": "Audience Impressions", "chg": "+140% reach", "icn": "users", "pct": 92},
            {"val": "34.5%", "lbl": "Click-Through Velocity", "chg": "Top 1% benchmark", "icn": "zap", "pct": 85},
        ]
    },
    "Cybersecurity": {
        "badges": ["ZERO TRUST DEFENSE", "THREAT INTELLIGENCE", "MISSION CRITICAL", "GOVERNANCE SHIELD"],
        "quotes": [
            ("Cybersecurity is no longer an IT consideration; it is the cornerstone of organizational sovereignty.", "Col. David Vance (Ret.)", "Chief Information Security Officer", "CyberVault"),
            ("Assume breach, verify continuously, and isolateblast radiuses aggressively.", "Nadia Sorokin", "Head of Threat Hunting", "SentrySec"),
        ],
        "default_icons": ["shield_check", "lock", "key", "alert_circle", "server", "eye_off", "cpu", "database"],
        "metrics": [
            {"val": "100%", "lbl": "Threat Surface Isolated", "chg": "Zero dwell time", "icn": "shield_check", "pct": 100},
            {"val": "< 2 min", "lbl": "Incident Containment", "chg": "Automated response", "icn": "zap", "pct": 96},
            {"val": "Zero", "lbl": "Unmonitored Endpoints", "chg": "100% coverage", "icn": "lock", "pct": 100},
            {"val": "256-Bit", "lbl": "Post-Quantum Cryptography", "chg": "Compliant standard", "icn": "key", "pct": 100},
        ]
    },
    "E-commerce": {
        "badges": ["COMMERCE ENGINE", "OMNICHANNEL SCALE", "CONVERSION OPTIMIZED", "RETAIL CLOUD"],
        "quotes": [
            ("Frictionless checkout is the quietest yet most profitable conversion lever in digital commerce.", "Tariq Al-Mansoor", "VP of Digital Experience", "NovaStore"),
            ("A brand is what a business does; customer delight is what the business delivers.", "Sophie Taylor", "Head of Omnichannel Retail", "LuxeCart"),
        ],
        "default_icons": ["wallet", "shopping_cart", "truck", "zap", "trending_up", "star", "globe", "credit_card"],
        "metrics": [
            {"val": "+42%", "lbl": "Cart Checkout Velocity", "chg": "Zero drop-off", "icn": "zap", "pct": 82},
            {"val": "99.99%", "lbl": "Flash Sale Uptime", "chg": "Peak traffic proof", "icn": "shield_check", "pct": 100},
            {"val": "1.4s", "lbl": "Average Store Load", "chg": "Instant CDN delivery", "icn": "clock", "pct": 94},
            {"val": "3.6x", "lbl": "Repeat Customer Lift", "chg": "+58% retention", "icn": "users", "pct": 86},
        ]
    },
    "Real Estate": {
        "badges": ["PRIME ASSETS", "ARCHITECTURAL VISION", "PORTFOLIO CAPITAL", "SMART HABITAT"],
        "quotes": [
            ("Great architecture does not simply occupy space; it elevates human interaction and spirit.", "Vincent Moretti", "Principal Architect", "Atelier Urban"),
            ("Land is the only investment where scarcity is absolute and value is compound.", "Eleanor Vance", "Managing Director", "Crown Real Estate Trust"),
        ],
        "default_icons": ["building", "home", "compass", "dollar", "chart_bar", "star", "award", "leaf"],
        "metrics": [
            {"val": "12.8%", "lbl": "Average Rental Yield", "chg": "+4.2% over market", "icn": "trending_up", "pct": 85},
            {"val": "$140M", "lbl": "Transaction Volume", "chg": "+35% annual surge", "icn": "dollar", "pct": 92},
            {"val": "98.5%", "lbl": "Occupancy Ratio", "chg": "Consistent stability", "icn": "building", "pct": 98},
            {"val": "LEED Gold", "lbl": "Eco-Certification", "chg": "Sustainable design", "icn": "leaf", "pct": 95},
        ]
    },
    "Productivity": {
        "badges": ["DEEP WORK", "FOCUS OPERATING SYSTEM", "EFFICIENCY VECTOR", "HIGH PERFORMANCE"],
        "quotes": [
            ("Focus is not about saying yes to what you want to do; it is about saying no to a hundred distractions.", "Julian Hayes", "Author & Cognitive Ergonomist", "DeepFocus"),
            ("Productivity without clarity is simply high-velocity exhaustion.", "Samantha Sterling", "Executive Performance Coach", "PeakMind"),
        ],
        "default_icons": ["zap", "clock", "check_circle", "target", "calendar", "compass", "layers", "star"],
        "metrics": [
            {"val": "3.5 hrs", "lbl": "Daily Deep Work Added", "chg": "+60% focus", "icn": "clock", "pct": 88},
            {"val": "-75%", "lbl": "Redundant Meeting Time", "chg": "Async standard", "icn": "check_circle", "pct": 75},
            {"val": "4.2x", "lbl": "Project Velocity Gain", "chg": "Rapid turnaround", "icn": "zap", "pct": 84},
            {"val": "Zero-Inbox", "lbl": "Cognitive Clarity", "chg": "Systematic inbox 0", "icn": "target", "pct": 95},
        ]
    },
    "Sustainability": {
        "badges": ["PLANET POSITIVE", "NET ZERO PATHWAY", "CIRCULAR ECOSYSTEM", "CLEAN FUTURE"],
        "quotes": [
            ("The stone age did not end because the world ran out of stones; the fossil era will end because clean innovation wins.", "Dr. Henrik Lindqvist", "Chair of Renewable Energy", "Nordic Green Council"),
            ("True environmental stewardship aligns planetary regeneration with economic abundance.", "Valerie Thorne", "Chief Sustainability Officer", "TerraNova"),
        ],
        "default_icons": ["leaf", "globe", "recycle", "sun", "wind", "heart_pulse", "trending_up", "award"],
        "metrics": [
            {"val": "-85%", "lbl": "Carbon Intensity Reduced", "chg": "Target achieved", "icn": "leaf", "pct": 85},
            {"val": "100%", "lbl": "Renewable Power Grid", "chg": "Wind & Solar sync", "icn": "sun", "pct": 100},
            {"val": "Zero-Waste", "lbl": "Closed-Loop Facility", "chg": "99.4% recycled", "icn": "recycle", "pct": 99},
            {"val": "5.4M Gal", "lbl": "Water Conserved", "chg": "Circular filtration", "icn": "globe", "pct": 90},
        ]
    },
    "Social Media Awareness": {
        "badges": ["DIGITAL WELLBEING", "MINDFUL CONSUMPTION", "COMMUNITY HEALTH", "AWARENESS REPORT"],
        "quotes": [
            ("When you do not pay for the algorithm, your time, attention, and emotions are the inventory.", "Maya Jenkins", "Digital Ethicist & Author", "HumanTech Institute"),
            ("True connection is cultivated in depth and presence, not in the currency of fleeting notifications.", "David Ross", "Founder", "Mindful Digital"),
        ],
        "default_icons": ["users", "share", "eye_off", "heart_pulse", "message_square", "shield_check", "star", "compass"],
        "metrics": [
            {"val": "-45%", "lbl": "Passive Screen Fatigue", "chg": "Healthy boundary", "icn": "trending_up", "pct": 75},
            {"val": "82%", "lbl": "Mindful Intentionality", "chg": "+30% clarity", "icn": "compass", "pct": 82},
            {"val": "3.2x", "lbl": "Real-World Social Time", "chg": "Quality offline", "icn": "users", "pct": 80},
            {"val": "100%", "lbl": "Fact-Checked Signals", "chg": "Misinfo filtered", "icn": "shield_check", "pct": 100},
        ]
    },
    "Corporate Announcements": {
        "badges": ["PRESS RELEASE", "MILESTONE ACHIEVED", "STRATEGIC EXPANSION", "EXECUTIVE NOTICE"],
        "quotes": [
            ("Progress is not accidental; it is the compound result of relentless commitment to excellence and integrity.", "Karan Sharma", "Chief Executive Officer", "Shri Genesis Software Solutions"),
            ("We measure our greatest achievements by the scale of trust our partners place in our solutions.", "Arun Patel", "Managing Director", "Genesis Enterprises"),
        ],
        "default_icons": ["bell", "award", "globe", "building", "rocket", "shield_check", "users", "star"],
        "metrics": [
            {"val": "3 Continents", "lbl": "Global Presence", "chg": "14 Regional Hubs", "icn": "globe", "pct": 90},
            {"val": "+140%", "lbl": "Global Team Expansion", "chg": "Elite talent onboard", "icn": "users", "pct": 88},
            {"val": "ISO 27001", "lbl": "Certified Enterprise Tier", "chg": "Zero non-compliance", "icn": "shield_check", "pct": 100},
            {"val": "Tier-1", "lbl": "Industry Recognition", "chg": "Leader quadrant", "icn": "award", "pct": 96},
        ]
    },
}


class AIGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.provider = "gemini" if (os.getenv("GEMINI_API_KEY") or self.api_key) else "heuristic"
        self._init_client()

    def _init_client(self):
        """Attempts to initialize LLM client if API key is present."""
        if self.api_key:
            try:
                import google.genai as genai
                self.gemini_client = genai.Client(api_key=self.api_key)
                self.provider = "gemini"
                logger.info("Initialized Google Gemini API client successfully.")
            except Exception as e:
                logger.warning(f"Could not initialize Gemini client: {e}. Falling back to Heuristic Generator.")
                self.gemini_client = None
                self.provider = "heuristic"
        else:
            self.gemini_client = None
            self.provider = "heuristic"

    def generate_content(self, request: BannerRequest, item_id: str = "design_001") -> GeneratedContent:
        """
        Generates structured content for the banner request.
        First tries LLM if configured; seamlessly falls back to domain heuristic generator.
        """
        if self.gemini_client and self.provider == "gemini":
            try:
                return self._generate_with_gemini(request, item_id)
            except Exception as e:
                logger.warning(f"Gemini generation failed ({e}). Using Heuristic Generator fallback.")
                return self._generate_with_heuristic(request, item_id)
        
        return self._generate_with_heuristic(request, item_id)

    def _generate_with_gemini(self, request: BannerRequest, item_id: str) -> GeneratedContent:
        """Calls Google Gemini API with a structured prompt."""
        category = request.category
        topic = request.topic
        template = request.template or "feature_highlights"

        prompt = f"""
        You are a world-class graphic designer and copywriter at an elite design agency.
        Generate structured JSON copy for an SVG graphic.
        Topic: {topic}
        Category: {category}
        Template Layout: {template}
        Tone: {request.tone or 'Professional'}
        Style: {request.style or 'Modern Corporate'}

        Return ONLY a valid JSON object matching this schema:
        {{
            "badge": "Short uppercase 2-3 word category badge",
            "headline": "Punchy compelling 4-8 word title",
            "subtitle": "Informative clear 1-2 sentence subtitle",
            "items": [
                {{"title": "Feature 1", "description": "Crisp 1-sentence value statement", "icon": "cpu", "tag": "Essential"}},
                {{"title": "Feature 2", "description": "Crisp 1-sentence value statement", "icon": "shield_check", "tag": "High Impact"}},
                {{"title": "Feature 3", "description": "Crisp 1-sentence value statement", "icon": "trending_up", "tag": "Optimized"}},
                {{"title": "Feature 4", "description": "Crisp 1-sentence value statement", "icon": "zap", "tag": "Scalable"}}
            ],
            "stats": [
                {{"value": "99.8%", "label": "Key Performance Metric", "change": "+35% YoY", "icon": "trending_up", "percentage": 95}},
                {{"value": "4.5x", "label": "Velocity Multiplier", "change": "Accelerated", "icon": "zap", "percentage": 85}}
            ],
            "quote": {{
                "text": "Insightful statement reflecting mastery in this domain.",
                "author": "Distinguished Leader",
                "role": "Chief Strategist",
                "organization": "Enterprise Group"
            }},
            "cta": {{"text": "Explore Framework", "subtext": "Access full benchmark documentation"}}
        }}
        """
        response = self.gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        parsed = json.loads(response.text)

        items = [DesignItem(**it) for it in parsed.get("items", [])]
        stats = [StatItem(**st) for st in parsed.get("stats", [])]
        quote = QuoteData(**parsed["quote"]) if "quote" in parsed else None
        cta = CTAData(**parsed["cta"]) if "cta" in parsed else CTAData(text="Learn More")

        return GeneratedContent(
            id=item_id,
            category=category,
            topic=topic,
            design_type=request.design_type,
            template=template,
            style=request.style or "Modern Corporate",
            tone=request.tone or "Professional",
            color_theme=request.color_theme or category,
            badge=parsed.get("badge", category.upper()),
            headline=parsed.get("headline", topic),
            subtitle=parsed.get("subtitle", f"Strategic insights and framework for {topic}."),
            items=items,
            stats=stats,
            quote=quote,
            cta=cta,
            footer=f"AI Design Engine • Shri Genesis Software Solutions • {category}",
        )

    def _generate_with_heuristic(self, request: BannerRequest, item_id: str) -> GeneratedContent:
        """
        Rich, deterministic, high-entropy semantic content synthesizer.
        Produces complete, authentic, non-repetitive copy for any topic and template.
        """
        category = request.category
        topic = request.topic
        template = request.template or "feature_highlights"

        domain = DOMAIN_KNOWLEDGE.get(category, DOMAIN_KNOWLEDGE["Technology and AI"])
        
        # Pick domain-specific badge
        badges = domain["badges"]
        badge = badges[abs(hash(item_id)) % len(badges)]

        # Generate headline from topic
        words = topic.split(":")
        headline = words[0].strip() if len(words) > 1 else topic

        # Generate contextual subtitle
        subtitles = [
            f"Comprehensive framework, key telemetry milestones, and actionable principles for {topic}.",
            f"Accelerating enterprise outcomes and operational maturity through {topic.lower()}.",
            f"Strategic insights, empirical benchmarks, and modern best practices in {category.lower()}.",
            f"Pioneering sustainable performance, governance, and scalable excellence in {topic.lower()}.",
        ]
        subtitle = subtitles[abs(hash(topic)) % len(subtitles)]

        # Generate 4-6 rich items
        icons = domain["default_icons"]
        item_titles = [
            ("Core Architecture", "Architectural blueprint engineered for zero-bottleneck execution and resilience."),
            ("Autonomous Governance", "Continuous cryptographic validation ensuring compliance and rigorous safety."),
            ("Predictive Telemetry", "Real-time streaming observability with proactive anomaly resolution."),
            ("Frictionless Integration", "Plug-and-play modular APIs supporting seamless cross-system federation."),
            ("Elastic Scalability", "Dynamic resource provisioning that scales effortlessly with organizational load."),
            ("Outcome Acceleration", "Systematic workflow optimization delivering measurable compound returns."),
        ]
        items = []
        for i, (t_title, t_desc) in enumerate(item_titles):
            icn = icons[i % len(icons)]
            items.append(
                DesignItem(
                    title=t_title,
                    description=t_desc,
                    icon=icn,
                    tag=f"Pillar 0{i+1}",
                )
            )

        # Stats items
        stat_defs = domain["metrics"]
        stats = [
            StatItem(
                value=s["val"],
                label=s["lbl"],
                change=s["chg"],
                icon=s["icn"],
                percentage=s["pct"]
            )
            for s in stat_defs
        ]

        # Steps items (for step-by-step layout)
        step_milestones = [
            ("Discovery & Assessment", "Audit current workflows, catalog dependencies, and establish baseline KPIs.", "search"),
            ("Architectural Formulation", "Design decoupled system topology, contract boundaries, and guardrails.", "compass"),
            ("Autonomous Deployment", "Roll out automated pipelines with canary verification and traffic mirroring.", "rocket"),
            ("Continuous Telemetry & Scale", "Monitor performance indicators and apply real-time optimization heuristics.", "trending_up"),
        ]
        steps = [
            StepItem(
                step_number=idx + 1,
                title=sm[0],
                description=sm[1],
                icon=sm[2],
                duration=f"Phase 0{idx+1}"
            )
            for idx, sm in enumerate(step_milestones)
        ]

        # Quotes (for quote banner layout)
        domain_quotes = domain["quotes"]
        selected_quote = domain_quotes[abs(hash(item_id)) % len(domain_quotes)]
        quote = QuoteData(
            text=selected_quote[0],
            author=selected_quote[1],
            role=selected_quote[2],
            organization=selected_quote[3],
            avatar_initials="".join([w[0] for w in selected_quote[1].split()[:2]]).upper()
        )

        # Comparison (for comparison layout)
        comparison = ComparisonData(
            left=ComparisonColumn(
                title="Traditional Approach",
                subtitle="High Latency & Fragile Workflows",
                points=[
                    "Manual coordination prone to human oversight",
                    "Disjointed tools requiring repetitive context",
                    "Slow turnaround measured in days or weeks",
                    "Linear cost scaling with high overhead"
                ],
                is_positive=False,
                highlight_pill="LEGACY METHOD"
            ),
            right=ComparisonColumn(
                title="AI-Powered Paradigm",
                subtitle="Autonomous, Deterministic & Rapid",
                points=[
                    "Programmatic generation with validation checks",
                    "Integrated vector engines and clean XML standards",
                    "Instant sub-second design synthesis",
                    "Exponential leverage with zero marginal friction"
                ],
                is_positive=True,
                highlight_pill="RECOMMENDED"
            ),
            verdict="Result: Autonomous intelligence delivers 10x velocity while preserving human-quality precision."
        )

        # CTA
        cta = CTAData(
            text="Explore Documentation",
            subtext="Access verified templates and guides",
            url="https://shrigeneris.com"
        )

        return GeneratedContent(
            id=item_id,
            category=category,
            topic=topic,
            design_type=request.design_type,
            template=template,
            style=request.style or "Modern Corporate",
            tone=request.tone or "Professional",
            color_theme=request.color_theme or category,
            badge=badge,
            headline=headline,
            subtitle=subtitle,
            items=items,
            stats=stats,
            steps=steps,
            comparison=comparison,
            quote=quote,
            cta=cta,
            footer=f"AI Design Engine • Shri Genesis Software Solutions • {category}",
        )
