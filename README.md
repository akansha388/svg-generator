# AI-Powered SVG Banner & Infographic Generation Engine

> **Shri Genesis Software Solutions — Gen AI Technical Assessment**  
> An automated, production-grade vector graphics engine that synthesizes professional SVG banners and infographics across multiple categories, layout paradigms, and color systems.

---

## 🌟 Overview & Key Capabilities

The **AI-Powered SVG Banner & Infographic Generation Engine** is an enterprise-grade automated pipeline designed to bridge the gap between Generative AI content synthesis and deterministic, high-quality vector rendering.

- **104 Production-Ready Vector Graphics:** Automatically generates 104 diverse SVG designs across 13 business and technical categories.
- **10 Distinct Layout Templates:** Promotional Banners, Educational Infographics, Statistics Showcases, Step-by-Step Roadmaps, Quote Banners, Announcement Banners, Comparison Layouts, Feature Highlights, List Infographics, and Corporate Social Graphics.
- **Dual-Engine Generative AI Layer:** Native integration with **Google Gemini 2.5 Flash** (via `google-genai` SDK) and OpenAI API, backed by a deterministic **Domain Semantic Synthesizer** for instant, 100% reliable offline generation.
- **Handcrafted Vector Icon Library:** 45+ clean, original vector SVG path icons (normalized to `24x24` viewBox) with zero external or proprietary dependencies.
- **12 Accessible Color Palettes:** WCAG AAA-compliant color systems featuring dark obsidian bases, vibrant accent gradients, and glassmorphic card fills.
- **Automated Validation Suite:** Rigorous XML well-formedness, viewBox verification, WCAG contrast calculation, text bounds overflow checking, defs resolution, and AI prompt artifact sanitization.
- **Interactive Visual Contact Sheet:** Standalone HTML5 web gallery with category filters, layout filters, live SVG zoom modal, and one-click SVG source code copying.

---

## 🏗️ Architecture & System Design

```
┌────────────────────────────────────────────────────────────────────────┐
│                        SYSTEM ARCHITECTURE FLOW                        │
└────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │   AI Semantics Layer (Google Gemini / Domain Engine)   │
       │   - Ingests topic, category, tone, and design type     │
       │   - Synthesizes headlines, subtitles, KPIs, and icons  │
       │   - Enforces strict Pydantic v2 data models            │
       └────────────────────────────────────────────────────────┘
                                    │
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │   Vector Rendering Engine (engine/svg_builder.py)      │
       │   - Mathematical coordinate positioning                │
       │   - Dynamic text wrapping (<tspan x="..." dy="...">)   │
       │   - 12 WCAG-compliant color palettes                   │
       │   - 45+ handcrafted vector icons                       │
       └────────────────────────────────────────────────────────┘
                                    │
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │   10 Specialized Layout Builders (engine/templates/)   │
       │   - Promotional Banner (1200x630)                      │
       │   - Educational Infographic (800x1200)                 │
       │   - Statistics Showcase (1200x800)                     │
       │   - Step-by-Step Process (1000x1300)                   │
       │   - Quote Banner (1080x1080)                           │
       │   - Announcement Banner (1200x630)                     │
       │   - Comparison Layout (1200x800)                       │
       │   - Feature Highlights (1200x900)                      │
       │   - List Infographic (800x1200)                        │
       │   - Corporate Social (1080x1080)                       │
       └────────────────────────────────────────────────────────┘
                                    │
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │   Automated QA & Validation (engine/validator.py)      │
       │   - XML parser verification (xml.etree.ElementTree)    │
       │   - ViewBox & scaling attributes check                 │
       │   - WCAG 2.1 relative luminance contrast check         │
       │   - Text overflow boundary heuristics                  │
       │   - Zero AI prompt leaks or tracking scripts           │
       └────────────────────────────────────────────────────────┘
                                    │
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │   Deliverables & Output Artifacts                      │
       │   - outputs/{category}/*.svg (104 files)               │
       │   - outputs/manifest.json & execution_summary.json     │
       │   - preview/index.html (Interactive Contact Sheet)     │
       │   - preview/representative/ (14 Curated Highlights)    │
       └────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
svg-generator/
│
├── engine/                       # Core engine package
│   ├── __init__.py               # Public exports
│   ├── models.py                 # Pydantic data schemas & validation models
│   ├── palettes.py               # 12 accessible color palettes & WCAG math
│   ├── icons.py                  # 45+ handcrafted vector SVG icons
│   ├── svg_builder.py            # Low-level vector builder, gradients, cards
│   ├── catalog.py                # 104 curated topics across 13 categories
│   ├── ai_generator.py           # Gemini API + Semantic Heuristic Synthesizer
│   ├── validator.py              # Automated SVG quality assurance suite
│   └── templates/                # 10 specialized layout templates
│       ├── __init__.py           # Template registry and router
│       ├── promotional_banner.py
│       ├── educational_infographic.py
│       ├── statistics_showcase.py
│       ├── step_by_step_process.py
│       ├── quote_banner.py
│       ├── announcement_banner.py
│       ├── comparison_layout.py
│       ├── feature_highlights.py
│       ├── list_infographic.py
│       └── corporate_social.py
│
├── outputs/                      # 104 Generated SVG designs by category
│   ├── Technology and AI/
│   ├── Business and Startups/
│   ├── Education/
│   ├── Healthcare/
│   ├── Finance/
│   ├── Marketing/
│   ├── Cybersecurity/
│   ├── E-commerce/
│   ├── Real Estate/
│   ├── Productivity/
│   ├── Sustainability/
│   ├── Social Media Awareness/
│   ├── Corporate Announcements/
│   ├── manifest.json             # Complete metadata catalog of all 104 SVGs
│   └── execution_summary.json    # Aggregated run metrics
│
├── preview/                      # Visualization & Contact Sheet
│   ├── index.html                # Interactive HTML gallery & inspector
│   └── representative/           # Curated set of 14 showcase designs
│
├── tests/                        # Pytest automated test suite
│   ├── test_templates.py         # Tests all 10 layout renderers
│   ├── test_validator.py         # Tests QA checks, syntax, and security
│   └── test_ai_generator.py      # Tests content generation & fallback
│
├── docs/                         # Additional documentation
│   ├── TECHNICAL_REPORT.md       # Comprehensive 4-page technical report
│   └── EXECUTION_REPORT.md       # Detailed execution audit and metrics
│
├── generate.py                   # Main CLI generation script
├── validate.py                   # Standalone QA audit script
├── build_preview.py              # Contact sheet builder & curator
├── requirements.txt              # Python package dependencies
├── .env.example                  # Environment variable configuration template
├── TECHNICAL_REPORT.md           # Architecture & technical report
├── EXECUTION_REPORT.md           # Execution metrics & audit report
└── README.md                     # Main documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10+** (Tested on Python 3.13.3)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### 2. Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/akansha388/svg-generator.git
cd svg-generator

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration (Optional)
The system runs completely offline out-of-the-box using the built-in Semantic Heuristic Synthesizer. To enable live Google Gemini AI generation:

```bash
# Copy environment template
cp .env.example .env

# Set your Gemini API key in .env or via shell:
export GEMINI_API_KEY="your-gemini-api-key"
```

---

## 💻 Running the Redesigned Web Application & Studio

You can launch the complete interactive web application with real-time generation and visual browsing:

```bash
# Start the web studio & API server
python app.py
```
Open **`http://localhost:5000`** in any web browser.

Alternatively, you can open `preview/index.html` directly or serve it statically:
```bash
python -m http.server 8000
# Open http://localhost:8000/preview/
```

### 🌿 Redesigned Natural & Modern Web Studio Features
1. **Gallery & Contact Sheet (104):** Filter and search all 104 generated SVGs with category chips, layout filters, and card zoom.
2. **Representative Showcase (14):** Curated set of the top 14 highlight designs with rationale notes.
3. **Live Studio Generator:** Dynamic on-the-fly SVG generation with topic randomizer, palette selector, layout picker, live preview canvas, and immediate code copy / file download!
4. **Automated Quality Audit:** Visual QA scorecards, 100% pass metrics, and the 7-stage validation checklist.
5. **Palettes & Handcrafted Icons:** Interactive design tokens and 45+ vector icon previews.

---

## 💻 CLI Usage & Commands

### 1. Generate All 104 SVGs (Batch Mode)
Generates the complete 104-design catalog spanning 13 categories and 10 layouts:

```bash
python generate.py
```

### 2. Generate a Subset of Designs
Generate only the first N designs from the catalog:

```bash
python generate.py --count 10
```

### 3. Generate a Single Custom Design
Programmatically generate a customized SVG banner or infographic:

```bash
python generate.py \
  --category "Cybersecurity" \
  --topic "Zero-Trust Cloud Governance" \
  --template "feature_highlights" \
  --color-theme "Crimson Shield" \
  --output "outputs/custom_zero_trust.svg"
```

Available layout choices for `--template`:
- `promotional_banner` (1200x630)
- `educational_infographic` (800x1200)
- `statistics_showcase` (1200x800)
- `step_by_step_process` (1000x1300)
- `quote_banner` (1080x1080)
- `announcement_banner` (1200x630)
- `comparison_layout` (1200x800)
- `feature_highlights` (1200x900)
- `list_infographic` (800x1200)
- `corporate_social` (1080x1080)

---

## 🔍 Validation & Quality Assurance

Run the automated quality assurance suite on any directory of SVGs:

```bash
# Audit all generated outputs
python validate.py outputs

# Export detailed validation audit report to JSON
python validate.py outputs --json outputs/validation_audit.json
```

The validator checks:
1. **XML Syntax:** Well-formedness check via `xml.etree.ElementTree`.
2. **ViewBox & Scale:** Valid, responsive viewBox coordinates matching aspect ratios.
3. **Clean Code & Security:** Absence of `<script>`, `javascript:`, prompt leaks, or template delimiters.
4. **Defs Integrity:** Resolution of all internal `url(#gradient)` and filter references.
5. **Text Bounds & Overflow:** Heuristic calculation preventing text extending past margins.
6. **WCAG Color Contrast:** Relative luminance contrast calculation adhering to WCAG AAA standards.
7. **Semantic Hierarchy:** Distinction between headline scale and body copy.

---

## 🖼️ Interactive Contact Sheet & Preview Gallery

To build or refresh the interactive contact sheet and curate the representative set:

```bash
python build_preview.py
```

To view the interactive gallery:
1. Open `preview/index.html` in any browser, or start a local server:
   ```bash
   python -m http.server 8000
   ```
2. Navigate to `http://localhost:8000/preview/` in your browser.
3. Features available in the viewer:
   - Filter by all 13 categories.
   - Filter by all 10 layout templates.
   - Live search by topic or keywords.
   - Toggle **Representative Set (14 Highlights)** button.
   - Click any card to inspect full high-resolution SVG, view metadata, and copy SVG source code.

---

## 🧪 Automated Testing

Execute the test suite using `pytest`:

```bash
pytest tests/ -v
```

All 16 unit tests verify:
- Complete validity and compliance across all 10 templates.
- Validator detection of malformed XML, security exploits, and broken defs references.
- Schema integrity of the AI generation pipeline.

---

## 📊 Summary Metrics

- **Total Generated Designs:** 104
- **Pass Rate:** 100.0% (104 / 104 Passed)
- **Average Quality Score:** 100.0 / 100
- **Total Execution Time:** 0.32 seconds (3.1 ms / design)
- **Categories Covered:** 13
- **Templates Exercised:** 10

---

## ⚖️ Originality & IP Compliance

In accordance with Section 4.C (*Originality Compliance and Intellectual Property*):
- **100% Original Vector Assets:** All 45+ icons, cards, gradients, and layout templates were authored specifically for this engine.
- **Zero Copyrighted Assets:** No third-party proprietary fonts, trademarked logos, or copyrighted stock assets were used.
- **Clean SVG Standards:** SVGs are self-contained and render identically across all modern web browsers (Chrome, Firefox, Safari, Edge) and vector graphics software (Figma, Adobe Illustrator, Inkscape).

---

## 📄 License & Attribution

Developed for the **Shri Genesis Software Solutions** Gen AI Technical Assessment.  
Licensed under the **MIT License**.
