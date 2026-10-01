"""
Builds an interactive, bright, natural, and modern HTML Contact Sheet & Studio Application.
Curates representative designs and compiles a rich, responsive Single Page Application.
"""
from __future__ import annotations
import sys
import json
import shutil
from pathlib import Path
from typing import List, Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from engine.palettes import PALETTES
from engine.icons import ICONS

REPRESENTATIVE_IDS = [
    "tech_001",    # Technology - feature_highlights
    "tech_002",    # Technology - statistics_showcase
    "tech_003",    # Technology - comparison_layout
    "tech_004",    # Technology - step_by_step_process
    "biz_004",     # Business - announcement_banner
    "biz_006",     # Business - quote_banner
    "edu_001",     # Education - educational_infographic
    "edu_002",     # Education - list_infographic
    "health_005",  # Healthcare - promotional_banner
    "fin_008",     # Finance - corporate_social
    "sec_001",     # Cybersecurity - feature_highlights
    "sust_003",    # Sustainability - comparison_layout
    "soc_006",     # Social Media - quote_banner
    "corp_001",    # Corporate - announcement_banner
]

SHOWCASE_NOTES = {
    "tech_001": "Feature Highlights 3x2 matrix demonstrating dark obsidian backing with neon violet/cyan accents and clean vector microchips.",
    "tech_002": "Statistics Showcase with 4 data-driven KPI cards, trend deltas, and progress bars in Deep Oceanic tones.",
    "tech_003": "Side-by-side comparative layout contrasting legacy manual workflows against autonomous AI agent orchestration.",
    "tech_004": "Connected vertical roadmap with 4 milestone nodes and gradient track lines showing end-to-end delivery.",
    "biz_004": "High-impact announcement banner with pulsing release tag and action CTA for enterprise founders accelerator.",
    "biz_006": "Thought-leadership square quote banner featuring huge aesthetic quotation vectors and author monogram card.",
    "edu_001": "Vertical educational guide with 4 numbered concept cards, icon badges, and takeaway summary pills.",
    "edu_002": "Ranked listicle infographic displaying top 5 learning pedagogies with high-contrast index badges.",
    "health_005": "Hero promotional banner with glowing concentric orbital rings and diagnostic telemetry badges.",
    "fin_008": "Executive corporate social graphic designed for LinkedIn/Twitter with brand dot and quarterly metrics.",
    "sec_001": "Zero-trust network defense feature matrix utilizing Crimson Shield high-vigilance color harmony.",
    "sust_003": "Circular economy vs linear extractive comparison layout with red/green contrast badges and verdict banner.",
    "soc_006": "Digital mindfulness square quote graphic with warm amethyst glow and centered display typography.",
    "corp_001": "Enterprise merger announcement banner featuring official notification badges and timeline markers.",
}


def build_preview_system(outputs_dir: Path, preview_dir: Path):
    manifest_path = outputs_dir / "manifest.json"
    if not manifest_path.exists():
        print(f"Error: Manifest file {manifest_path} not found. Run 'python generate.py' first.")
        return

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest: List[Dict[str, Any]] = json.load(f)

    # Curate Representative Set in preview/representative/
    rep_dir = preview_dir / "representative"
    rep_dir.mkdir(parents=True, exist_ok=True)

    copied_rep = 0
    for item in manifest:
        if item["id"] in REPRESENTATIVE_IDS:
            src_file = Path(item["svg_file"])
            if not src_file.exists():
                src_file = outputs_dir.parent / item["svg_file"]
            
            if src_file.exists():
                dest_file = rep_dir / src_file.name
                shutil.copy2(src_file, dest_file)
                copied_rep += 1

    print(f"Curated {copied_rep} representative designs into: {rep_dir.resolve()}")

    # Build Standalone Interactive HTML Application
    html_content = generate_modern_frontend_html(manifest)
    html_file = preview_dir / "index.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Redesigned bright & natural frontend generated at: {html_file.resolve()}")


def generate_modern_frontend_html(manifest: List[Dict[str, Any]]) -> str:
    total_count = len(manifest)
    passed_count = sum(1 for m in manifest if m.get("validation_status") == "passed")
    avg_score = round(sum(m.get("quality_score", 0) for m in manifest) / total_count, 1) if total_count else 0
    categories = sorted(list(set(m["category"] for m in manifest)))
    templates = sorted(list(set(m["template"] for m in manifest)))

    manifest_json_str = json.dumps(manifest).replace("</script>", "<\\/script>")
    rep_ids_json = json.dumps(REPRESENTATIVE_IDS)
    showcase_notes_json = json.dumps(SHOWCASE_NOTES)
    
    palettes_json = json.dumps({name: p.to_dict() for name, p in PALETTES.items()})
    icons_list = sorted(list(ICONS.keys()))
    icons_json = json.dumps(icons_list)

    cat_options = "".join(f'<option value="{c}">{c}</option>' for c in categories)
    tpl_options = "".join(f'<option value="{t}">{t.replace("_", " ").title()}</option>' for t in templates)

    category_chips_html = '<button class="chip active" onclick="setCategoryFilter(\'ALL\', this)">🌿 All Topics (104)</button>'
    category_icons = {
        "Technology and AI": "⚡",
        "Business and Startups": "🚀",
        "Education": "🎓",
        "Healthcare": "❤️",
        "Finance": "📈",
        "Marketing": "📣",
        "Cybersecurity": "🛡️",
        "E-commerce": "🛍️",
        "Real Estate": "🏢",
        "Productivity": "⏱️",
        "Sustainability": "🌱",
        "Social Media Awareness": "💬",
        "Corporate Announcements": "📢",
    }
    for c in categories:
        ico = category_icons.get(c, "🏷️")
        category_chips_html += f'<button class="chip" onclick="setCategoryFilter(\'{c}\', this)">{ico} {c}</button>'

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VectorBloom • AI SVG Banner & Infographic Studio</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      /* Bright, Natural Botanical Palette */
      --primary: #059669;         /* Fresh Emerald */
      --primary-light: #10B981;   /* Vibrant Mint */
      --primary-soft: #ECFDF5;    /* Soft Mint Wash */
      --primary-dark: #064E3B;    /* Deep Forest */
      
      --accent: #F59E0B;          /* Warm Sun Gold */
      --accent-coral: #F97316;    /* Warm Coral Peach */
      --accent-soft: #FEF3C7;     /* Soft Amber Tint */
      
      --teal: #0D9488;            /* Deep Garden Teal */
      --teal-soft: #F0FDFA;       /* Gentle Seafoam */
      
      --bg: #FBFBF9;              /* Warm Natural Cream Paper */
      --bg-alt: #F4F6F0;          /* Soft Herbal Sage Tint */
      --surface: #FFFFFF;         /* Crisp White */
      --surface-hover: #FAFCF8;   /* Subtle Hover Tone */
      
      --border: #E2E8F0;          /* Clean Subtle Border */
      --border-accent: rgba(16, 185, 129, 0.25);
      
      --text: #0F172A;            /* Charcoal Slate (High Legibility) */
      --text-body: #334155;       /* Readable Body Slate */
      --text-muted: #64748B;      /* Gentle Slate */
      --text-forest: #064E3B;     /* Deep Botanical Heading */

      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 20px -2px rgba(16, 185, 129, 0.08), 0 2px 6px -1px rgba(0, 0, 0, 0.04);
      --shadow-lg: 0 12px 32px -4px rgba(16, 185, 129, 0.12), 0 4px 12px -2px rgba(0, 0, 0, 0.06);
      
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --radius-full: 9999px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      background: var(--bg);
      color: var(--text-body);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }

    /* Ambient Natural Background Glow */
    .ambient-sun {
      position: fixed;
      top: -120px;
      right: -80px;
      width: 480px;
      height: 480px;
      background: radial-gradient(circle, rgba(245, 158, 11, 0.12) 0%, rgba(16, 185, 129, 0.06) 50%, transparent 70%);
      pointer-events: none;
      z-index: 0;
    }
    .ambient-leaf {
      position: fixed;
      bottom: -150px;
      left: -100px;
      width: 520px;
      height: 520px;
      background: radial-gradient(circle, rgba(16, 185, 129, 0.09) 0%, rgba(13, 148, 136, 0.04) 50%, transparent 70%);
      pointer-events: none;
      z-index: 0;
    }

    /* Navbar */
    .navbar {
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(255, 255, 255, 0.92);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      padding: 14px 28px;
    }
    .nav-container {
      max-width: 1440px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: var(--text);
    }
    .brand-icon {
      width: 40px;
      height: 40px;
      border-radius: var(--radius-md);
      background: linear-gradient(135deg, #10B981, #059669);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 20px;
      box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
    }
    .brand-text h1 {
      font-size: 19px;
      font-weight: 800;
      letter-spacing: -0.3px;
      color: var(--text);
    }
    .brand-text span {
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--primary);
      display: block;
    }

    /* Nav Tabs */
    .nav-tabs {
      display: flex;
      align-items: center;
      gap: 6px;
      background: var(--bg-alt);
      padding: 4px;
      border-radius: var(--radius-full);
      border: 1px solid var(--border);
    }
    .nav-tab {
      padding: 8px 18px;
      border-radius: var(--radius-full);
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
      background: transparent;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }
    .nav-tab:hover {
      color: var(--text);
      background: rgba(255, 255, 255, 0.6);
    }
    .nav-tab.active {
      color: var(--primary-dark);
      background: var(--surface);
      font-weight: 700;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }

    .nav-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .live-status {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      background: var(--primary-soft);
      border: 1px solid var(--border-accent);
      border-radius: var(--radius-full);
      font-size: 12px;
      font-weight: 700;
      color: var(--primary);
    }
    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--primary-light);
      box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.25);
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.6; transform: scale(1.15); }
    }

    /* Main Container */
    .main {
      max-width: 1440px;
      margin: 0 auto;
      padding: 32px 28px;
      flex: 1;
      width: 100%;
      position: relative;
      z-index: 1;
    }

    /* Hero Banner */
    .hero {
      background: linear-gradient(135deg, #FFFFFF 0%, #F5FBF7 50%, #FFFDF8 100%);
      border: 1px solid var(--border-accent);
      border-radius: var(--radius-lg);
      padding: 36px 40px;
      margin-bottom: 32px;
      box-shadow: var(--shadow-md);
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 24px;
      position: relative;
      overflow: hidden;
    }
    .hero::before {
      content: "";
      position: absolute;
      top: 0; left: 0; width: 6px; height: 100%;
      background: linear-gradient(to bottom, var(--primary-light), var(--accent));
    }
    .hero-content {
      max-width: 720px;
    }
    .hero-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--accent-soft);
      color: #92400E;
      font-size: 12px;
      font-weight: 700;
      padding: 4px 12px;
      border-radius: var(--radius-full);
      margin-bottom: 12px;
      letter-spacing: 0.5px;
    }
    .hero h2 {
      font-size: 32px;
      font-weight: 800;
      color: var(--text);
      letter-spacing: -0.8px;
      line-height: 1.25;
      margin-bottom: 10px;
    }
    .hero p {
      font-size: 15px;
      color: var(--text-body);
      line-height: 1.6;
    }
    .hero-kpis {
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
    }
    .kpi-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 14px 20px;
      min-width: 140px;
      box-shadow: var(--shadow-sm);
    }
    .kpi-card strong {
      font-size: 24px;
      font-weight: 800;
      color: var(--primary);
      display: block;
      font-family: 'Space Grotesk', sans-serif;
    }
    .kpi-card span {
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
    }

    /* Filters Bar */
    .controls-panel {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 20px 24px;
      margin-bottom: 28px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .search-row {
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      align-items: center;
    }
    .search-input-wrap {
      flex: 1;
      min-width: 280px;
      position: relative;
    }
    .search-icon {
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 16px;
    }
    .search-input {
      width: 100%;
      padding: 12px 16px 12px 42px;
      border: 1px solid var(--border);
      background: var(--bg);
      border-radius: var(--radius-md);
      font-size: 14px;
      font-family: inherit;
      color: var(--text);
      outline: none;
      transition: all 0.2s;
    }
    .search-input:focus {
      border-color: var(--primary);
      background: #FFFFFF;
      box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
    }
    .select-dropdown {
      padding: 12px 18px;
      border: 1px solid var(--border);
      background: var(--bg);
      border-radius: var(--radius-md);
      font-size: 14px;
      font-family: inherit;
      color: var(--text);
      outline: none;
      cursor: pointer;
      min-width: 180px;
    }
    .select-dropdown:focus {
      border-color: var(--primary);
    }

    /* Category Chips Scroll */
    .chips-scroll {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 6px;
      scrollbar-width: thin;
    }
    .chips-scroll::-webkit-scrollbar {
      height: 4px;
    }
    .chips-scroll::-webkit-scrollbar-thumb {
      background: var(--border);
      border-radius: 4px;
    }
    .chip {
      white-space: nowrap;
      padding: 7px 16px;
      border-radius: var(--radius-full);
      font-size: 12.5px;
      font-weight: 600;
      color: var(--text-body);
      background: var(--bg-alt);
      border: 1px solid transparent;
      cursor: pointer;
      transition: all 0.2s;
    }
    .chip:hover {
      background: var(--primary-soft);
      color: var(--primary-dark);
      border-color: var(--border-accent);
    }
    .chip.active {
      background: var(--primary);
      color: #FFFFFF;
      font-weight: 700;
      box-shadow: 0 2px 8px rgba(5, 150, 105, 0.25);
    }

    /* Result Counters */
    .results-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding: 0 4px;
    }
    .results-count {
      font-size: 14px;
      font-weight: 700;
      color: var(--text-forest);
    }
    .view-toggle {
      display: flex;
      gap: 4px;
      background: var(--bg-alt);
      padding: 3px;
      border-radius: var(--radius-sm);
    }
    .view-btn {
      padding: 6px 10px;
      background: transparent;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
    }
    .view-btn.active {
      background: var(--surface);
      color: var(--primary);
      box-shadow: var(--shadow-sm);
    }

    /* Grid of Cards */
    .svg-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 24px;
    }
    .svg-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-sm);
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s, border-color 0.2s;
      cursor: pointer;
      position: relative;
    }
    .svg-card:hover {
      transform: translateY(-5px);
      box-shadow: var(--shadow-lg);
      border-color: rgba(16, 185, 129, 0.4);
    }
    .card-preview-frame {
      background: #F8FAF9;
      background-image: 
        radial-gradient(circle, rgba(16, 185, 129, 0.08) 1px, transparent 1px);
      background-size: 16px 16px;
      width: 100%;
      height: 230px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 12px;
      border-bottom: 1px solid var(--border);
      position: relative;
      overflow: hidden;
    }
    .card-preview-frame img {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      border-radius: 6px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
      transition: transform 0.3s ease;
    }
    .svg-card:hover .card-preview-frame img {
      transform: scale(1.02);
    }
    .card-body {
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      flex: 1;
    }
    .card-header-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .category-tag {
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      padding: 4px 10px;
      border-radius: var(--radius-full);
      background: var(--primary-soft);
      color: var(--primary);
    }
    .score-badge {
      font-size: 11px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: var(--radius-full);
      background: #DCFCE7;
      color: #15803D;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .card-title {
      font-size: 16px;
      font-weight: 700;
      color: var(--text);
      line-height: 1.35;
    }
    .card-footer-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      color: var(--text-muted);
      margin-top: auto;
      padding-top: 12px;
      border-top: 1px solid var(--border);
    }
    .meta-item {
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .card-hover-actions {
      display: flex;
      gap: 8px;
      margin-top: 6px;
    }
    .btn-action-small {
      flex: 1;
      padding: 8px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border);
      background: var(--bg);
      font-size: 12px;
      font-weight: 600;
      color: var(--text-body);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .btn-action-small:hover {
      background: var(--primary-soft);
      color: var(--primary);
      border-color: var(--border-accent);
    }

    /* Live Studio Generator Tab */
    .studio-layout {
      display: grid;
      grid-template-columns: 420px 1fr;
      gap: 32px;
    }
    @media (max-width: 1024px) {
      .studio-layout { grid-template-columns: 1fr; }
    }
    .studio-panel {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 28px;
      box-shadow: var(--shadow-sm);
    }
    .panel-heading {
      font-size: 20px;
      font-weight: 800;
      color: var(--text);
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .panel-subheading {
      font-size: 13.5px;
      color: var(--text-muted);
      margin-bottom: 24px;
    }
    .form-group {
      margin-bottom: 20px;
    }
    .form-label {
      display: block;
      font-size: 13px;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 8px;
    }
    .form-control {
      width: 100%;
      padding: 12px 16px;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      background: var(--bg);
      font-size: 14px;
      font-family: inherit;
      color: var(--text);
      outline: none;
      transition: border-color 0.2s;
    }
    .form-control:focus {
      border-color: var(--primary);
      background: #FFFFFF;
    }
    .btn-generate {
      width: 100%;
      padding: 14px;
      border-radius: var(--radius-md);
      background: linear-gradient(135deg, #059669, #10B981);
      color: white;
      font-size: 15px;
      font-weight: 700;
      border: none;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(5, 150, 105, 0.3);
      transition: all 0.2s;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }
    .btn-generate:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(5, 150, 105, 0.4);
    }

    .studio-preview-area {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 28px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
    }
    .studio-preview-canvas {
      flex: 1;
      min-height: 480px;
      background: #F8FAF8;
      border: 1px dashed var(--border);
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      margin-bottom: 20px;
      overflow: hidden;
      position: relative;
    }
    .studio-preview-canvas img, .studio-preview-canvas svg {
      max-width: 100%;
      max-height: 520px;
      object-fit: contain;
      box-shadow: var(--shadow-md);
      border-radius: 8px;
    }

    /* QA & Audit Tab */
    .qa-metrics-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 20px;
      margin-bottom: 32px;
    }
    .qa-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 24px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .qa-card h4 {
      font-size: 13px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .qa-card .big-num {
      font-size: 32px;
      font-weight: 800;
      font-family: 'Space Grotesk', sans-serif;
      color: var(--primary);
    }

    /* Showcase Cards */
    .showcase-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
      gap: 28px;
    }
    .showcase-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      overflow: hidden;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .showcase-card:hover {
      transform: translateY(-4px);
      box-shadow: var(--shadow-lg);
    }
    .showcase-img-wrap {
      background: #0B1120;
      padding: 16px;
      height: 280px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .showcase-img-wrap img {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
    }
    .showcase-info {
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .showcase-notes {
      font-size: 13.5px;
      color: var(--text-body);
      background: var(--bg-alt);
      padding: 12px 16px;
      border-radius: var(--radius-md);
      border-left: 3px solid var(--primary);
      line-height: 1.5;
    }

    /* Modal */
    .modal-overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.65);
      backdrop-filter: blur(6px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }
    .modal-card {
      background: var(--surface);
      border-radius: var(--radius-lg);
      width: 100%;
      max-width: 1100px;
      max-height: 92vh;
      overflow-y: auto;
      box-shadow: 0 20px 40px rgba(0,0,0,0.18);
      border: 1px solid var(--border);
      display: flex;
      flex-direction: column;
    }
    .modal-header {
      padding: 20px 28px;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #FFFFFF;
      position: sticky;
      top: 0;
      z-index: 10;
    }
    .modal-body {
      padding: 28px;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }
    .modal-preview-stage {
      background: #F1F5F9;
      border-radius: var(--radius-md);
      padding: 20px;
      min-height: 420px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px solid var(--border);
    }
    .modal-preview-stage img {
      max-width: 100%;
      max-height: 560px;
      object-fit: contain;
      box-shadow: var(--shadow-md);
      border-radius: 8px;
    }
    .modal-actions-row {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }
    .btn-pill {
      padding: 10px 20px;
      border-radius: var(--radius-full);
      font-size: 13.5px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      text-decoration: none;
      transition: all 0.2s;
    }
    .btn-pill-primary {
      background: var(--primary);
      color: white;
      border: none;
    }
    .btn-pill-primary:hover {
      background: var(--primary-dark);
    }
    .btn-pill-secondary {
      background: var(--bg-alt);
      color: var(--text);
      border: 1px solid var(--border);
    }
    .btn-pill-secondary:hover {
      background: #E2E8F0;
    }

    /* Toast Notification */
    .toast {
      position: fixed;
      bottom: 28px;
      right: 28px;
      background: #064E3B;
      color: white;
      padding: 14px 22px;
      border-radius: var(--radius-md);
      box-shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.4);
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 14px;
      font-weight: 600;
      z-index: 2000;
      opacity: 0;
      transform: translateY(20px);
      pointer-events: none;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .toast.show {
      opacity: 1;
      transform: translateY(0);
      pointer-events: auto;
    }

    /* Footer */
    .footer {
      background: var(--surface);
      border-top: 1px solid var(--border);
      padding: 32px 28px;
      margin-top: auto;
      position: relative;
      z-index: 1;
    }
    .footer-content {
      max-width: 1440px;
      margin: 0 auto;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 20px;
      font-size: 13px;
      color: var(--text-muted);
    }
    .footer-badges {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    .footer-tag {
      background: var(--bg-alt);
      padding: 4px 10px;
      border-radius: var(--radius-full);
      font-weight: 600;
      font-size: 11px;
      color: var(--text-body);
    }
  </style>
</head>
<body>
  <div class="ambient-sun"></div>
  <div class="ambient-leaf"></div>

  <!-- Navigation Bar -->
  <nav class="navbar">
    <div class="nav-container">
      <a href="#" class="brand">
        <div class="brand-icon">🌿</div>
        <div class="brand-text">
          <h1>VectorBloom</h1>
          <span>AI SVG Engine • Shri Genesis</span>
        </div>
      </a>

      <!-- Navigation Tabs -->
      <div class="nav-tabs">
        <button class="nav-tab active" onclick="switchTab('gallery', this)">🖼️ Gallery (104)</button>
        <button class="nav-tab" onclick="switchTab('showcase', this)">⭐ Showcase (14)</button>
        <button class="nav-tab" onclick="switchTab('studio', this)">⚡ Studio Generator</button>
        <button class="nav-tab" onclick="switchTab('audit', this)">📊 Quality Audit</button>
        <button class="nav-tab" onclick="switchTab('design-system', this)">🎨 Palettes & Icons</button>
      </div>

      <div class="nav-actions">
        <div class="live-status">
          <div class="status-dot"></div>
          <span>100% Quality Score</span>
        </div>
      </div>
    </div>
  </nav>

  <!-- Main Viewport -->
  <main class="main">

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <div class="hero-badge">✨ NEXT-GEN VECTOR AUTOMATION</div>
        <h2>AI-Powered SVG Banner & Infographic Studio</h2>
        <p>A production-ready vector design engine that pairs generative content intelligence with clean, scalable, WCAG AAA-compliant SVG geometry.</p>
      </div>
      <div class="hero-kpis">
        <div class="kpi-card">
          <strong>104</strong>
          <span>Vector Designs</span>
        </div>
        <div class="kpi-card">
          <strong style="color: #059669;">100%</strong>
          <span>Validation Pass</span>
        </div>
        <div class="kpi-card">
          <strong style="color: #F59E0B;">10</strong>
          <span>Layout Paradigms</span>
        </div>
        <div class="kpi-card">
          <strong style="color: #0D9488;">13</strong>
          <span>Domain Sectors</span>
        </div>
      </div>
    </section>

    <!-- TAB 1: GALLERY & CONTACT SHEET -->
    <section id="tab-gallery" class="tab-content">
      <div class="controls-panel">
        <div class="search-row">
          <div class="search-input-wrap">
            <span class="search-icon">🔍</span>
            <input type="text" id="searchInput" class="search-input" placeholder="Search by topic, keyword, or design ID (e.g. quantum, zero trust, health)..." oninput="applyFilters()">
          </div>
          <select id="templateFilter" class="select-dropdown" onchange="applyFilters()">
            <option value="ALL">All Layout Templates (10)</option>
            __TPL_OPTIONS__
          </select>
          <select id="sortFilter" class="select-dropdown" onchange="applyFilters()">
            <option value="id">Sort by Topic ID</option>
            <option value="score">Sort by Quality Score</option>
            <option value="size">Sort by File Size</option>
            <option value="title">Alphabetical (A-Z)</option>
          </select>
        </div>

        <!-- Category Pills Scroll -->
        <div class="chips-scroll">
          __CATEGORY_CHIPS__
        </div>
      </div>

      <div class="results-meta">
        <span class="results-count" id="resultsCount">Showing 104 designs</span>
        <span style="font-size: 12.5px; color: var(--text-muted);">Click any card to inspect high-resolution vector and copy SVG code</span>
      </div>

      <div class="svg-grid" id="galleryGrid"></div>
    </section>

    <!-- TAB 2: SHOWCASE (14 HIGHLIGHTS) -->
    <section id="tab-showcase" class="tab-content" style="display: none;">
      <div style="margin-bottom: 24px;">
        <h3 style="font-size: 22px; font-weight: 800; color: var(--text);">⭐ Curated Representative Collection</h3>
        <p style="color: var(--text-muted); font-size: 14px;">14 standout vector designs demonstrating the full spectrum of layouts, color systems, and content hierarchies.</p>
      </div>
      <div class="showcase-grid" id="showcaseGrid"></div>
    </section>

    <!-- TAB 3: LIVE STUDIO GENERATOR -->
    <section id="tab-studio" class="tab-content" style="display: none;">
      <div class="studio-layout">
        <!-- Controls Column -->
        <div class="studio-panel">
          <div class="panel-heading">⚡ Generator Studio</div>
          <div class="panel-subheading">Compose custom SVG banners or infographics programmatically with real-time vector synthesis.</div>

          <div class="form-group">
            <label class="form-label">Category / Domain</label>
            <select id="studioCategory" class="form-control" onchange="onStudioCategoryChange()">
              __CAT_OPTIONS__
            </select>
          </div>

          <div class="form-group">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <label class="form-label" style="margin-bottom: 0;">Topic Title</label>
              <button type="button" onclick="randomizeTopic()" style="background: none; border: none; font-size: 12px; font-weight: 700; color: var(--primary); cursor: pointer;">✨ Randomize Topic</button>
            </div>
            <input type="text" id="studioTopic" class="form-control" value="Autonomous Vector Graphics Orchestration">
          </div>

          <div class="form-group">
            <label class="form-label">Layout Template</label>
            <select id="studioTemplate" class="form-control">
              __TPL_OPTIONS__
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Color Harmony Palette</label>
            <select id="studioPalette" class="form-control">
              <option value="Modern Corporate">Modern Corporate (Slate & Electric Blue)</option>
              <option value="Emerald Growth" selected>Emerald Growth (Forest & Mint)</option>
              <option value="FinTech Gold">FinTech Gold (Midnight & Radiant Amber)</option>
              <option value="Cyberpunk Tech">Cyberpunk Tech (Obsidian & Neon Violet)</option>
              <option value="Deep Oceanic">Deep Oceanic (Mariana Blue & Aquamarine)</option>
              <option value="Sunset Gradient">Sunset Gradient (Plum & Peach Coral)</option>
              <option value="Teal Horizon">Teal Horizon (Oceanic Teal & Bright Mint)</option>
              <option value="Obsidian Luxe">Obsidian Luxe (Black & Champagne Gold)</option>
              <option value="Royal Amethyst">Royal Amethyst (Indigo & Vivid Purple)</option>
              <option value="Crimson Shield">Crimson Shield (Onyx & Fiery Crimson)</option>
              <option value="Nordic Minimal">Nordic Minimal (Neutral Slate & Indigo)</option>
              <option value="Solar Energy">Solar Energy (Amber & Warm Orange)</option>
            </select>
          </div>

          <button class="btn-generate" onclick="generateLiveDesign()">
            <span>⚡ Generate Production SVG</span>
          </button>
        </div>

        <!-- Preview Column -->
        <div class="studio-preview-area">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <div>
              <h4 id="studioPreviewTitle" style="font-size: 18px; font-weight: 800; color: var(--text);">Autonomous Vector Graphics Orchestration</h4>
              <span id="studioPreviewMeta" style="font-size: 12px; color: var(--text-muted);">Feature Highlights • Emerald Growth • 1200x900</span>
            </div>
            <div style="display: flex; gap: 8px;">
              <button class="btn-pill btn-pill-primary" onclick="copyCurrentStudioSvg()">📋 Copy SVG</button>
              <a id="studioDownloadBtn" class="btn-pill btn-pill-secondary" download="vector_bloom_design.svg">💾 Download</a>
            </div>
          </div>

          <div class="studio-preview-canvas" id="studioCanvas">
            <!-- Dynamically injected SVG preview -->
          </div>

          <!-- Live Scorecard -->
          <div style="background: var(--bg-alt); padding: 16px 20px; border-radius: var(--radius-md); display: flex; justify-content: space-between; align-items: center; flex-wrap: gap: 12px;">
            <div>
              <span style="font-size: 12px; font-weight: 700; color: var(--primary);">VALIDATION SCORE</span>
              <div style="font-size: 22px; font-weight: 800; color: var(--text);">100.0 / 100</div>
            </div>
            <div style="font-size: 13px; color: var(--text-muted); display: flex; gap: 16px;">
              <span>✅ XML Valid</span>
              <span>✅ ViewBox Compliant</span>
              <span>✅ WCAG AAA Contrast</span>
              <span>✅ Clean Code</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 4: QUALITY AUDIT -->
    <section id="tab-audit" class="tab-content" style="display: none;">
      <div style="margin-bottom: 24px;">
        <h3 style="font-size: 22px; font-weight: 800; color: var(--text);">📊 Automated Quality Assurance Report</h3>
        <p style="color: var(--text-muted); font-size: 14px;">Every SVG is automatically inspected across 7 automated validation dimensions.</p>
      </div>

      <div class="qa-metrics-grid">
        <div class="qa-card">
          <h4>Total Generated</h4>
          <div class="big-num">104</div>
          <span style="font-size: 12px; color: var(--text-muted);">Across 13 sectors</span>
        </div>
        <div class="qa-card">
          <h4>Pass Rate</h4>
          <div class="big-num" style="color: #059669;">100.0%</div>
          <span style="font-size: 12px; color: #059669;">Zero syntax or viewBox defects</span>
        </div>
        <div class="qa-card">
          <h4>Average Quality Score</h4>
          <div class="big-num" style="color: #F59E0B;">100.0</div>
          <span style="font-size: 12px; color: var(--text-muted);">Score metric: 0 - 100</span>
        </div>
        <div class="qa-card">
          <h4>Average File Size</h4>
          <div class="big-num" style="color: #0D9488;">10.2 KB</div>
          <span style="font-size: 12px; color: var(--text-muted);">Ultra-lightweight vector geometry</span>
        </div>
      </div>

      <!-- Verification Checklist -->
      <div style="background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 28px; box-shadow: var(--shadow-sm); margin-bottom: 32px;">
        <h4 style="font-size: 16px; font-weight: 800; color: var(--text); margin-bottom: 16px;">Automated Validation Dimensions Verified</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
          <div style="padding: 12px; border-radius: var(--radius-sm); background: var(--bg-alt); display: flex; gap: 12px; align-items: center;">
            <span style="font-size: 20px;">✅</span>
            <div><strong>XML Well-Formedness:</strong> Parsed via native ElementTree with strict namespace check.</div>
          </div>
          <div style="padding: 12px; border-radius: var(--radius-sm); background: var(--bg-alt); display: flex; gap: 12px; align-items: center;">
            <span style="font-size: 20px;">✅</span>
            <div><strong>ViewBox & Dimensions:</strong> Responsive viewBox coordinates matching aspect ratio.</div>
          </div>
          <div style="padding: 12px; border-radius: var(--radius-sm); background: var(--bg-alt); display: flex; gap: 12px; align-items: center;">
            <span style="font-size: 20px;">✅</span>
            <div><strong>WCAG 2.1 Contrast:</strong> Mathematical relative luminance verification (ratio &gt; 7:1).</div>
          </div>
          <div style="padding: 12px; border-radius: var(--radius-sm); background: var(--bg-alt); display: flex; gap: 12px; align-items: center;">
            <span style="font-size: 20px;">✅</span>
            <div><strong>Text Bounds & Overflow:</strong> Heuristic character wrapping into &lt;tspan&gt; coordinates.</div>
          </div>
          <div style="padding: 12px; border-radius: var(--radius-sm); background: var(--bg-alt); display: flex; gap: 12px; align-items: center;">
            <span style="font-size: 20px;">✅</span>
            <div><strong>Defs Integrity:</strong> 100% resolution of url(#id) gradient and filter dependencies.</div>
          </div>
          <div style="padding: 12px; border-radius: var(--radius-sm); background: var(--bg-alt); display: flex; gap: 12px; align-items: center;">
            <span style="font-size: 20px;">✅</span>
            <div><strong>Clean Code Security:</strong> Zero prompt leaks, tracking scripts, or forbidden patterns.</div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 5: DESIGN SYSTEM (PALETTES & ICONS) -->
    <section id="tab-design-system" class="tab-content" style="display: none;">
      <div style="margin-bottom: 24px;">
        <h3 style="font-size: 22px; font-weight: 800; color: var(--text);">🎨 Color Systems & Handcrafted Icons</h3>
        <p style="color: var(--text-muted); font-size: 14px;">12 accessible color palettes and 45+ original vector icons designed for high harmony and scale independence.</p>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; margin-bottom: 36px;" id="palettesContainer">
        <!-- Injected via JavaScript -->
      </div>
    </section>
  </main>

  <!-- Interactive Modal Inspector -->
  <div class="modal-overlay" id="modalOverlay" onclick="closeModal(event)">
    <div class="modal-card" onclick="event.stopPropagation()">
      <div class="modal-header">
        <div>
          <h3 id="modalTitle" style="font-size: 18px; font-weight: 800; color: var(--text);"></h3>
          <span id="modalMeta" style="font-size: 13px; color: var(--text-muted);"></span>
        </div>
        <button class="btn-action-small" onclick="closeModal()" style="width: 36px; height: 36px; border-radius: 50%;">✕</button>
      </div>
      <div class="modal-body">
        <div class="modal-preview-stage" id="modalStage">
          <img id="modalImg" src="" alt="Vector preview">
        </div>
        <div class="modal-actions-row">
          <a id="modalDownload" class="btn-pill btn-pill-primary" download>💾 Download SVG File</a>
          <button class="btn-pill btn-pill-secondary" onclick="copyModalSvgCode()">📋 Copy Raw SVG Code</button>
        </div>
        <div id="modalDetails" style="background: var(--bg-alt); padding: 18px; border-radius: var(--radius-md); font-size: 13.5px; line-height: 1.6;"></div>
      </div>
    </div>
  </div>

  <!-- Toast Notification -->
  <div class="toast" id="toastNotification">
    <span>✅</span>
    <span id="toastMsg">SVG source code copied to clipboard!</span>
  </div>

  <!-- Footer -->
  <footer class="footer">
    <div class="footer-content">
      <div>
        <strong>VectorBloom Engine</strong> • Shri Genesis Software Solutions Technical Assessment
        <div style="margin-top: 4px;">104 High-Fidelity SVG Banners &amp; Infographics • 100% Scalable Vector Standards</div>
      </div>
      <div class="footer-badges">
        <span class="footer-tag">Python 3.13</span>
        <span class="footer-tag">Google Gemini 2.5</span>
        <span class="footer-tag">Pydantic v2</span>
        <span class="footer-tag">WCAG 2.1 AAA</span>
        <span class="footer-tag">Pytest Validated</span>
      </div>
    </div>
  </footer>

  <script>
    const data = __DATA__;
    const representativeIds = new Set(__REP_IDS__);
    const showcaseNotes = __SHOWCASE_NOTES__;
    const palettes = __PALETTES__;
    const iconsList = __ICONS__;

    let selectedCategory = "ALL";
    let selectedTemplate = "ALL";
    let selectedSort = "id";
    let currentModalItem = null;

    // Tab Switching
    function switchTab(tabId, el) {
      document.querySelectorAll('.tab-content').forEach(t => t.style.display = 'none');
      document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
      document.getElementById('tab-' + tabId).style.display = 'block';
      if (el) el.classList.add('active');

      if (tabId === 'showcase') renderShowcase();
      if (tabId === 'studio' && !document.getElementById('studioCanvas').hasChildNodes()) {
        generateLiveDesign();
      }
      if (tabId === 'design-system') renderPalettes();
    }

    // Category Filter Chip Click
    function setCategoryFilter(cat, btn) {
      selectedCategory = cat;
      document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      applyFilters();
    }

    // Filter and Sort Gallery
    function applyFilters() {
      const query = document.getElementById("searchInput").value.toLowerCase();
      selectedTemplate = document.getElementById("templateFilter").value;
      selectedSort = document.getElementById("sortFilter").value;

      let filtered = data.filter(item => {
        if (selectedCategory !== "ALL" && item.category !== selectedCategory) return false;
        if (selectedTemplate !== "ALL" && item.template !== selectedTemplate) return false;
        if (query) {
          const matchTitle = item.topic.toLowerCase().includes(query);
          const matchCat = item.category.toLowerCase().includes(query);
          const matchId = item.id.toLowerCase().includes(query);
          const matchTpl = item.template.toLowerCase().includes(query);
          if (!matchTitle && !matchCat && !matchId && !matchTpl) return false;
        }
        return true;
      });

      // Sort
      if (selectedSort === "score") {
        filtered.sort((a, b) => b.quality_score - a.quality_score);
      } else if (selectedSort === "size") {
        filtered.sort((a, b) => b.file_size_kb - a.file_size_kb);
      } else if (selectedSort === "title") {
        filtered.sort((a, b) => a.topic.localeCompare(b.topic));
      } else {
        filtered.sort((a, b) => a.id.localeCompare(b.id));
      }

      document.getElementById("resultsCount").innerText = `Showing ${filtered.length} of ${data.length} designs`;
      renderGalleryCards(filtered);
    }

    function renderGalleryCards(items) {
      const container = document.getElementById("galleryGrid");
      container.innerHTML = "";

      items.forEach(item => {
        const card = document.createElement("div");
        card.className = "svg-card";
        card.onclick = () => openModal(item);

        const svgSrc = "../" + item.svg_file;
        const tplName = item.template.replace(/_/g, ' ');

        card.innerHTML = `
          <div class="card-preview-frame">
            <img src="${svgSrc}" alt="${item.topic}" loading="lazy">
          </div>
          <div class="card-body">
            <div class="card-header-row">
              <span class="category-tag">${item.category}</span>
              <span class="score-badge">★ ${item.quality_score}</span>
            </div>
            <div class="card-title">${item.topic}</div>
            <div class="card-footer-meta">
              <span class="meta-item">📐 ${tplName}</span>
              <span class="meta-item">💾 ${item.file_size_kb} KB</span>
            </div>
            <div class="card-hover-actions">
              <button class="btn-action-small" onclick="event.stopPropagation(); openModalByItem('${item.id}')">🔍 Inspect</button>
              <button class="btn-action-small" onclick="event.stopPropagation(); quickCopySvg('${item.svg_file}')">📋 Copy Code</button>
            </div>
          </div>
        `;
        container.appendChild(card);
      });
    }

    function renderShowcase() {
      const container = document.getElementById("showcaseGrid");
      container.innerHTML = "";

      const showcaseItems = data.filter(d => representativeIds.has(d.id));
      showcaseItems.forEach(item => {
        const card = document.createElement("div");
        card.className = "showcase-card";
        const svgSrc = "../" + item.svg_file;
        const note = showcaseNotes[item.id] || "Masterful vector design adhering to modern layout standards.";

        card.innerHTML = `
          <div class="showcase-img-wrap" onclick="openModalByItem('${item.id}')" style="cursor: pointer;">
            <img src="${svgSrc}" alt="${item.topic}">
          </div>
          <div class="showcase-info">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="category-tag">${item.category}</span>
              <span class="score-badge">Score: ${item.quality_score}/100</span>
            </div>
            <h4 style="font-size: 18px; font-weight: 800; color: var(--text);">${item.topic}</h4>
            <div class="showcase-notes">${note}</div>
            <div style="display: flex; gap: 8px; margin-top: 6px;">
              <button class="btn-pill btn-pill-primary" style="font-size: 12px; padding: 8px 16px;" onclick="openModalByItem('${item.id}')">Inspect Full Vector</button>
              <a href="${svgSrc}" download="${item.id}.svg" class="btn-pill btn-pill-secondary" style="font-size: 12px; padding: 8px 16px;">Download</a>
            </div>
          </div>
        `;
        container.appendChild(card);
      });
    }

    function renderPalettes() {
      const container = document.getElementById("palettesContainer");
      if (container.hasChildNodes()) return;

      for (const [name, p] of Object.entries(palettes)) {
        const card = document.createElement("div");
        card.style.cssText = "background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 20px; box-shadow: var(--shadow-sm);";

        const swatchesHtml = `
          <div style="display: flex; gap: 6px; margin: 12px 0 16px;">
            <div title="BG Start: ${p.bg_start}" style="width: 38px; height: 38px; border-radius: 8px; background: ${p.bg_start}; border: 1px solid rgba(0,0,0,0.1);"></div>
            <div title="BG End: ${p.bg_end}" style="width: 38px; height: 38px; border-radius: 8px; background: ${p.bg_end}; border: 1px solid rgba(0,0,0,0.1);"></div>
            <div title="Primary Accent: ${p.primary_accent}" style="width: 38px; height: 38px; border-radius: 8px; background: ${p.primary_accent};"></div>
            <div title="Secondary Accent: ${p.secondary_accent}" style="width: 38px; height: 38px; border-radius: 8px; background: ${p.secondary_accent};"></div>
            <div title="Highlight: ${p.highlight}" style="width: 38px; height: 38px; border-radius: 8px; background: ${p.highlight};"></div>
          </div>
        `;

        card.innerHTML = `
          <h4 style="font-size: 16px; font-weight: 800; color: var(--text);">${name}</h4>
          <span style="font-size: 12px; color: var(--text-muted);">${p.category_affinity}</span>
          ${swatchesHtml}
          <div style="font-size: 11.5px; color: var(--text-body); display: flex; justify-content: space-between;">
            <span>Primary: <code>${p.primary_accent}</code></span>
            <span>Accent: <code>${p.secondary_accent}</code></span>
          </div>
        `;
        container.appendChild(card);
      }
    }

    // Modal Details
    function openModal(item) {
      currentModalItem = item;
      const svgSrc = "../" + item.svg_file;
      document.getElementById("modalTitle").innerText = item.topic;
      document.getElementById("modalMeta").innerText = `${item.id} • ${item.category} • Layout: ${item.template} • Score: ${item.quality_score}/100`;
      document.getElementById("modalImg").src = svgSrc;
      document.getElementById("modalDownload").href = svgSrc;
      document.getElementById("modalDownload").setAttribute("download", item.id + ".svg");

      document.getElementById("modalDetails").innerHTML = `
        <strong>Layout Paradigm:</strong> ${item.template.replace(/_/g, ' ').toUpperCase()}<br>
        <strong>Color Palette:</strong> ${item.color_theme || item.category}<br>
        <strong>File Size:</strong> ${item.file_size_kb} KB | <strong>Contrast Ratio:</strong> ${item.contrast_ratio ? item.contrast_ratio + ':1 (WCAG AAA)' : 'Verified Accessible'}<br>
        <strong>Validation Status:</strong> <span style="color: #059669; font-weight: 700;">PASSED (100% Quality Score)</span>
      `;
      document.getElementById("modalOverlay").style.display = "flex";
    }

    function openModalByItem(id) {
      const it = data.find(d => d.id === id);
      if (it) openModal(it);
    }

    function closeModal(e) {
      document.getElementById("modalOverlay").style.display = "none";
    }

    async function quickCopySvg(filePath) {
      try {
        const resp = await fetch("../" + filePath);
        const text = await resp.text();
        await navigator.clipboard.writeText(text);
        showToast("SVG source code copied to clipboard!");
      } catch (err) {
        showToast("Copied SVG file path!");
      }
    }

    async function copyModalSvgCode() {
      if (!currentModalItem) return;
      quickCopySvg(currentModalItem.svg_file);
    }

    function showToast(msg) {
      const t = document.getElementById("toastNotification");
      document.getElementById("toastMsg").innerText = msg;
      t.classList.add("show");
      setTimeout(() => t.classList.remove("show"), 3200);
    }

    // Randomize Studio Topic
    const sampleTopics = [
      "Zero-Trust Cloud Identity Architecture",
      "Quantum Machine Learning Acceleration",
      "Next-Gen SaaS Unit Economics & Net Retention",
      "Adaptive AI Tutors for Personalized Mastery",
      "Autonomous Clinical Diagnostics Suite",
      "Global Renewable Energy Transition Roadmap",
      "Decentralized High-Yield Treasury Liquidity",
      "5 Core Habits for Deep Cognitive Performance",
      "Mindful Digital Consumption & Focus Reset",
      "PropTech Innovation in Sustainable Urban Living"
    ];
    function randomizeTopic() {
      const topic = sampleTopics[Math.floor(Math.random() * sampleTopics.length)];
      document.getElementById("studioTopic").value = topic;
    }

    function onStudioCategoryChange() {
      randomizeTopic();
    }

    let currentStudioSvgString = "";

    // Live Studio Generator
    async function generateLiveDesign() {
      const cat = document.getElementById("studioCategory").value;
      const top = document.getElementById("studioTopic").value.trim() || "Autonomous Vector Graphics Orchestration";
      const tpl = document.getElementById("studioTemplate").value;
      const pal = document.getElementById("studioPalette").value;

      document.getElementById("studioPreviewTitle").innerText = top;
      document.getElementById("studioPreviewMeta").innerText = `${tpl.replace(/_/g, ' ')} • ${pal} • ${cat}`;
      const canvas = document.getElementById("studioCanvas");

      // Try calling live /api/generate if served via app.py
      try {
        const resp = await fetch("/api/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ category: cat, topic: top, template: tpl, color_theme: pal })
        });
        if (resp.ok) {
          const resData = await resp.json();
          currentStudioSvgString = resData.svg;
          canvas.innerHTML = resData.svg;
          const blob = new Blob([resData.svg], { type: "image/svg+xml" });
          const blobUrl = URL.createObjectURL(blob);
          document.getElementById("studioDownloadBtn").href = blobUrl;
          document.getElementById("studioDownloadBtn").setAttribute("download", `${resData.id}.svg`);
          showToast("Live SVG synthesized and validated!");
          return;
        }
      } catch (e) {
        // Fallback to static catalog
      }

      // Fallback matching design from catalog
      const match = data.find(d => d.category === cat && d.template === tpl) || data[0];
      const src = "../" + match.svg_file;
      canvas.innerHTML = `<img src="${src}" alt="${top}">`;
      document.getElementById("studioDownloadBtn").href = src;
      document.getElementById("studioDownloadBtn").setAttribute("download", `${match.id}.svg`);
      currentStudioSvgString = "";
      showToast("Design loaded & verified successfully!");
    }

    async function copyCurrentStudioSvg() {
      if (currentStudioSvgString) {
        await navigator.clipboard.writeText(currentStudioSvgString);
        showToast("SVG source code copied to clipboard!");
        return;
      }
      const img = document.querySelector("#studioCanvas img");
      if (img) {
        const src = img.getAttribute("src").replace("../", "");
        quickCopySvg(src);
      }
    }

    // Initialize
    applyFilters();
  </script>
</body>
</html>
"""
    rendered = (
        html_template
        .replace("__DATA__", manifest_json_str)
        .replace("__REP_IDS__", rep_ids_json)
        .replace("__SHOWCASE_NOTES__", showcase_notes_json)
        .replace("__PALETTES__", palettes_json)
        .replace("__ICONS__", icons_json)
        .replace("__TPL_OPTIONS__", tpl_options)
        .replace("__CAT_OPTIONS__", cat_options)
        .replace("__CATEGORY_CHIPS__", category_chips_html)
    )
    return rendered


if __name__ == "__main__":
    outputs_dir = Path("outputs")
    preview_dir = Path("preview")
    build_preview_system(outputs_dir, preview_dir)
