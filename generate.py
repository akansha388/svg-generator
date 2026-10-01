"""
Main CLI generation engine for AI-Powered SVG Banners and Infographics.
Supports generating single custom designs or batch-generating the entire 100+ catalog.
"""
from __future__ import annotations
import os
import sys
import time
import json
import argparse
import re
from pathlib import Path
from typing import List, Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from engine.models import BannerRequest
from engine.ai_generator import AIGenerator
from engine.templates import render_template, TEMPLATE_REGISTRY
from engine.validator import SVGValidator
from engine.catalog import CATALOG_TOPICS


def slugify(text: str) -> str:
    """Converts a string into a clean filesystem slug."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "_", text).strip("_")[:40]


def sanitize_folder_name(name: str) -> str:
    """Sanitizes folder name for Windows and Unix."""
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()


def run_batch_generation(
    catalog: List[Dict[str, Any]],
    output_dir: Path,
    api_key: str | None = None,
    verbose: bool = True,
) -> Dict[str, Any]:
    """Generates all designs in the catalog and validates each output."""
    output_dir.mkdir(parents=True, exist_ok=True)
    ai_gen = AIGenerator(api_key=api_key)
    validator = SVGValidator()

    manifest: List[Dict[str, Any]] = []
    start_time = time.time()
    success_count = 0
    warning_count = 0
    fail_count = 0

    print(f"\n🚀 Starting batch generation of {len(catalog)} SVG designs...")
    print(f"📁 Output Directory: {output_dir.resolve()}\n")

    for idx, item in enumerate(catalog, 1):
        item_start = time.time()
        item_id = item["id"]
        category = item["category"]
        topic = item["topic"]
        template = item["template"]
        style = item.get("style", "Modern Corporate")
        color_theme = item.get("color_theme", category)

        cat_folder = output_dir / sanitize_folder_name(category)
        cat_folder.mkdir(parents=True, exist_ok=True)

        slug = slugify(topic)
        file_name = f"{item_id}_{slug}.svg"
        file_path = cat_folder / file_name

        try:
            req = BannerRequest(
                category=category,
                topic=topic,
                design_type=item.get("design_type", "Infographic"),
                template=template,
                style=style,
                color_theme=color_theme,
            )
            content = ai_gen.generate_content(req, item_id=item_id)
            svg_content = render_template(template, content)

            # Write SVG file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(svg_content)

            # Validate generated SVG
            relative_path = f"outputs/{sanitize_folder_name(category)}/{file_name}"
            val_res = validator.validate(
                svg_content=svg_content,
                file_path=relative_path,
                design_id=item_id,
                category=category,
                topic=topic,
                template=template,
            )

            if val_res.is_valid:
                if val_res.status == "passed":
                    success_count += 1
                else:
                    warning_count += 1
            else:
                fail_count += 1

            duration_ms = round((time.time() - item_start) * 1000, 1)

            entry = {
                "id": item_id,
                "category": category,
                "topic": topic,
                "design_type": item.get("design_type", "Infographic"),
                "template": template,
                "color_theme": color_theme,
                "svg_file": relative_path,
                "file_size_kb": val_res.file_size_kb,
                "validation_status": val_res.status,
                "quality_score": val_res.quality_score,
                "contrast_ratio": val_res.contrast_ratio,
                "generation_time_ms": duration_ms,
                "warnings": val_res.warnings,
                "errors": val_res.errors,
            }
            manifest.append(entry)

            if verbose:
                status_icon = "✅" if val_res.status == "passed" else ("⚠️" if val_res.status == "warning" else "❌")
                print(f"[{idx:3d}/{len(catalog)}] {status_icon} {item_id:<9} | {category[:18]:<18} | {template[:20]:<20} | Score: {val_res.quality_score:5.1f} | {duration_ms:5.1f}ms")

        except Exception as e:
            fail_count += 1
            print(f"[{idx:3d}/{len(catalog)}] ❌ Error generating {item_id} ({topic}): {e}")

    total_time = round(time.time() - start_time, 2)
    avg_time = round((total_time / len(catalog)) * 1000, 1) if catalog else 0.0
    avg_score = round(sum(m["quality_score"] for m in manifest) / len(manifest), 1) if manifest else 0.0

    # Write Manifest JSON
    manifest_path = output_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    summary = {
        "total_generated": len(manifest),
        "successful_outputs": success_count,
        "warning_outputs": warning_count,
        "failed_outputs": fail_count,
        "total_execution_time_sec": total_time,
        "average_time_per_design_ms": avg_time,
        "average_quality_score": avg_score,
        "manifest_path": str(manifest_path),
    }

    summary_path = output_dir / "execution_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 65)
    print("📊 BATCH GENERATION EXECUTION SUMMARY")
    print("=" * 65)
    print(f"Total Designs Generated:    {summary['total_generated']}")
    print(f"Fully Passed:               {summary['successful_outputs']}")
    print(f"Passed with Minor Warnings: {summary['warning_outputs']}")
    print(f"Failed Outputs:             {summary['failed_outputs']}")
    print(f"Average Quality Score:      {summary['average_quality_score']} / 100")
    print(f"Total Execution Time:       {summary['total_execution_time_sec']}s")
    print(f"Average Time per Design:    {summary['average_time_per_design_ms']}ms")
    print(f"Manifest Saved To:          {manifest_path}")
    print("=" * 65 + "\n")

    return summary


def run_single_generation(
    category: str,
    topic: str,
    template: str,
    output_path: str,
    color_theme: str | None = None,
    api_key: str | None = None,
):
    """Generates a single custom SVG design from command-line arguments."""
    ai_gen = AIGenerator(api_key=api_key)
    validator = SVGValidator()

    print(f"Generating single SVG for: '{topic}' in '{category}' (Template: {template})...")
    req = BannerRequest(
        category=category,
        topic=topic,
        template=template,
        color_theme=color_theme or category,
    )
    content = ai_gen.generate_content(req, item_id="custom_001")
    svg_content = render_template(template, content)

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(svg_content)

    val = validator.validate(svg_content, str(out_file), "custom_001", category, topic, template)
    print(f"Saved to: {out_file.resolve()}")
    print(f"Validation Status: {val.status.upper()} (Score: {val.quality_score}/100)")
    if val.warnings:
        print(f"Warnings: {val.warnings}")
    if val.errors:
        print(f"Errors: {val.errors}")


def main():
    parser = argparse.ArgumentParser(description="AI-Powered SVG Banner & Infographic Generation Engine")
    parser.add_argument("--batch-all", action="store_true", help="Generate all 100+ designs from catalog")
    parser.add_argument("--count", type=int, default=None, help="Generate first N designs from catalog")
    parser.add_argument("--category", type=str, help="Category name for custom generation")
    parser.add_argument("--topic", type=str, help="Topic title for custom generation")
    parser.add_argument(
        "--template",
        type=str,
        choices=list(TEMPLATE_REGISTRY.keys()),
        default="promotional_banner",
        help="Template layout style"
    )
    parser.add_argument("--color-theme", type=str, default=None, help="Color theme name")
    parser.add_argument("--output", type=str, default="custom_design.svg", help="Output file path")
    parser.add_argument("--output-dir", type=str, default="outputs", help="Output directory for batch")
    parser.add_argument("--api-key", type=str, default=None, help="Google Gemini or OpenAI API Key")

    args = parser.parse_args()

    if args.batch_all or args.count:
        catalog = CATALOG_TOPICS
        if args.count:
            catalog = catalog[:args.count]
        run_batch_generation(catalog, Path(args.output_dir), api_key=args.api_key)
    elif args.category and args.topic:
        run_single_generation(
            category=args.category,
            topic=args.topic,
            template=args.template,
            output_path=args.output,
            color_theme=args.color_theme,
            api_key=args.api_key,
        )
    else:
        # Default behavior: run batch all
        run_batch_generation(CATALOG_TOPICS, Path(args.output_dir), api_key=args.api_key)


if __name__ == "__main__":
    main()
