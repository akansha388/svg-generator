"""
Standalone SVG Quality & Validation CLI.
Inspects SVG files or directories and produces detailed QA audit reports.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from engine.validator import SVGValidator


def validate_file_or_dir(target_path: Path, output_json: str | None = None, verbose: bool = True):
    validator = SVGValidator()
    svg_files = []

    if target_path.is_file():
        svg_files = [target_path]
    elif target_path.is_dir():
        svg_files = list(target_path.rglob("*.svg"))
    else:
        print(f"Error: Path '{target_path}' does not exist.")
        return

    print(f"\n🔍 Auditing {len(svg_files)} SVG file(s) in: {target_path.resolve()}\n")

    results = []
    passed = 0
    warnings = 0
    failed = 0

    for idx, fpath in enumerate(svg_files, 1):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()

            res = validator.validate(
                svg_content=content,
                file_path=str(fpath),
                design_id=fpath.stem,
            )

            if res.is_valid:
                if res.status == "passed":
                    passed += 1
                else:
                    warnings += 1
            else:
                failed += 1

            results.append(res.model_dump())

            if verbose:
                icon = "✅" if res.status == "passed" else ("⚠️" if res.status == "warning" else "❌")
                print(f"[{idx:3d}/{len(svg_files)}] {icon} {fpath.name:<40} | Score: {res.quality_score:5.1f} | Size: {res.file_size_kb:4.1f}KB")
                if res.warnings:
                    for w in res.warnings:
                        print(f"      ⚠️  {w}")
                if res.errors:
                    for e in res.errors:
                        print(f"      ❌  {e}")

        except Exception as e:
            failed += 1
            print(f"[{idx:3d}/{len(svg_files)}] ❌ Error reading {fpath.name}: {e}")

    avg_score = round(sum(r["quality_score"] for r in results) / len(results), 1) if results else 0.0

    print("\n" + "=" * 60)
    print("📋 SVG VALIDATION AUDIT SUMMARY")
    print("=" * 60)
    print(f"Total Files Inspected:  {len(svg_files)}")
    print(f"Valid (Passed):         {passed}")
    print(f"Valid (With Warnings):  {warnings}")
    print(f"Failed / Invalid:       {failed}")
    print(f"Average Quality Score:  {avg_score} / 100")
    print(f"Success Rate:           {round(((passed + warnings) / len(svg_files) * 100), 1) if svg_files else 0}%")
    print("=" * 60 + "\n")

    if output_json:
        out_p = Path(output_json)
        with open(out_p, "w", encoding="utf-8") as f:
            json.dump({
                "total": len(svg_files),
                "passed": passed,
                "warnings": warnings,
                "failed": failed,
                "average_score": avg_score,
                "results": results,
            }, f, indent=2)
        print(f"Detailed JSON audit report saved to: {out_p.resolve()}")


def main():
    parser = argparse.ArgumentParser(description="SVG Validation & Quality Assurance CLI")
    parser.add_argument("path", type=str, nargs="?", default="outputs", help="Path to SVG file or directory")
    parser.add_argument("--json", type=str, default=None, help="Save audit report as JSON file")
    parser.add_argument("--quiet", action="store_true", help="Minimal console output")

    args = parser.parse_args()
    validate_file_or_dir(Path(args.path), output_json=args.json, verbose=not args.quiet)


if __name__ == "__main__":
    main()
