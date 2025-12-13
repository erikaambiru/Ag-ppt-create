# -*- coding: utf-8 -*-
# =============================================================================
# Ag-ppt-create - AI-powered PPTX generation pipeline
# https://github.com/aktsmm/Ag-ppt-create
# 
# Copyright (c) aktsmm. Licensed under CC BY-NC-SA 4.0.
# DO NOT MODIFY THIS HEADER BLOCK.
# =============================================================================
"""
Validate content.json against schema and custom rules.

This script provides deterministic validation as a helper for Reviewer agent.
It checks:
1. JSON Schema compliance
2. Empty content detection
3. Image path existence
4. Text length warnings

Usage:
    python scripts/validate_content.py <content.json> [--images-dir <dir>]

Exit codes:
    0: PASS (no errors)
    1: FAIL (fatal errors found)
    2: WARN (warnings only, can continue)
"""

import argparse
import json
import sys
import io
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Fix Windows console encoding issues
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    import jsonschema
    from jsonschema import Draft7Validator, ValidationError
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    print("Warning: jsonschema not installed. Run: pip install jsonschema")


# Schema path
SCHEMA_PATH = Path(__file__).parent.parent / "workspace" / "content.schema.json"

# Validation thresholds
MAX_TITLE_LENGTH = 80
MAX_ITEM_LENGTH = 150
MAX_ITEMS_PER_SLIDE = 8
BULLET_SYMBOLS = ['•', '・', '●', '○', '-', '*', '+', '◆', '◇', '▪', '▫']


class ValidationResult:
    """Holds validation results."""
    
    def __init__(self):
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
    
    def add_error(self, error_type: str, location: str, message: str, suggestion: str = None):
        """Add a fatal error."""
        self.errors.append({
            "type": error_type,
            "location": location,
            "message": message,
            "suggestion": suggestion
        })
    
    def add_warning(self, warn_type: str, location: str, message: str, suggestion: str = None):
        """Add a warning."""
        self.warnings.append({
            "type": warn_type,
            "location": location,
            "message": message,
            "suggestion": suggestion
        })
    
    @property
    def status(self) -> str:
        """Get overall status."""
        if self.errors:
            return "FAIL"
        elif self.warnings:
            return "WARN"
        return "PASS"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "status": self.status,
            "fatal_errors": self.errors,
            "warnings": self.warnings,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings)
        }


def load_schema() -> Dict[str, Any]:
    """Load the JSON schema."""
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema not found: {SCHEMA_PATH}")
    
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_schema(content: Dict[str, Any], result: ValidationResult) -> None:
    """Validate against JSON Schema."""
    if not JSONSCHEMA_AVAILABLE:
        result.add_warning("schema", "global", "jsonschema not installed, skipping schema validation")
        return
    
    try:
        schema = load_schema()
        validator = Draft7Validator(schema)
        
        for error in validator.iter_errors(content):
            path = ".".join(str(p) for p in error.absolute_path) or "root"
            result.add_error(
                "schema",
                path,
                error.message,
                f"Check the schema at {SCHEMA_PATH}"
            )
    except FileNotFoundError as e:
        result.add_warning("schema", "global", str(e))
    except Exception as e:
        result.add_error("schema", "global", f"Schema validation failed: {e}")


def validate_empty_content(content: Dict[str, Any], result: ValidationResult) -> None:
    """Check for empty slides (content type without items)."""
    slides = content.get("slides", [])
    
    for i, slide in enumerate(slides):
        slide_type = slide.get("type", "unknown")
        location = f"slides[{i}]"
        
        # Skip if marked as _skip
        if slide.get("_skip"):
            continue
        
        # Check content slides must have items or image
        if slide_type == "content":
            has_items = bool(slide.get("items"))
            has_image = bool(slide.get("image"))
            if not has_items and not has_image:
                result.add_error(
                    "empty_content",
                    location,
                    f"Content slide at index {i} has no items or image",
                    "Add 'items' array or 'image' object, or change type to 'section'"
                )
        
        # Check agenda/summary must have items
        elif slide_type in ["agenda", "summary"]:
            if not slide.get("items"):
                result.add_error(
                    "empty_content",
                    location,
                    f"{slide_type.capitalize()} slide at index {i} has no items",
                    "Add 'items' array with agenda/summary points"
                )
        
        # Check photo must have image
        elif slide_type == "photo":
            if not slide.get("image"):
                result.add_error(
                    "empty_content",
                    location,
                    f"Photo slide at index {i} has no image",
                    "Add 'image' object with 'path' or 'url'"
                )
        
        # Check title/section must have title
        elif slide_type in ["title", "section"]:
            if not slide.get("title"):
                result.add_error(
                    "empty_content",
                    location,
                    f"{slide_type.capitalize()} slide at index {i} has no title",
                    "Add 'title' field"
                )
        
        # Check two_column must have items or left_items/right_items
        elif slide_type == "two_column":
            has_items = bool(slide.get("items"))
            has_columns = bool(slide.get("left_items")) or bool(slide.get("right_items"))
            if not has_items and not has_columns:
                result.add_error(
                    "empty_content",
                    location,
                    f"Two-column slide at index {i} has no content",
                    "Add 'left_items'/'right_items' (recommended) or 'items'"
                )
            elif has_items and not has_columns:
                # Warn: items is used but left_items/right_items is preferred
                result.add_warning(
                    "two_column_format",
                    location,
                    f"Two-column slide uses 'items' but 'left_items'/'right_items' is recommended",
                    "Replace 'items' with 'left_title', 'left_items', 'right_title', 'right_items' for proper 2-column layout"
                )


def validate_items_format(content: Dict[str, Any], result: ValidationResult) -> None:
    """Check that items are string arrays, not object arrays.
    
    content.json schema requires items to be string[]:
      ✅ "items": ["item1", "item2"]
      ❌ "items": [{"text": "item1", "bullet": true}]
    
    Object format is only valid for replacements.json (preserve method).
    """
    slides = content.get("slides", [])
    
    for i, slide in enumerate(slides):
        location = f"slides[{i}]"
        
        # Check items array
        items = slide.get("items", [])
        for j, item in enumerate(items):
            if isinstance(item, dict):
                result.add_error(
                    "items_format",
                    f"{location}.items[{j}]",
                    f"Item is an object but should be a string",
                    "Use string array format: \"items\": [\"item1\", \"item2\"] instead of object format"
                )
                break  # Report only first occurrence per slide
        
        # Check left_items
        left_items = slide.get("left_items", [])
        for j, item in enumerate(left_items):
            if isinstance(item, dict):
                result.add_error(
                    "items_format",
                    f"{location}.left_items[{j}]",
                    f"Item is an object but should be a string",
                    "Use string array format for left_items"
                )
                break
        
        # Check right_items
        right_items = slide.get("right_items", [])
        for j, item in enumerate(right_items):
            if isinstance(item, dict):
                result.add_error(
                    "items_format",
                    f"{location}.right_items[{j}]",
                    f"Item is an object but should be a string",
                    "Use string array format for right_items"
                )
                break


def validate_bullet_symbols(content: Dict[str, Any], result: ValidationResult) -> None:
    """Check for manual bullet symbols in text."""
    slides = content.get("slides", [])
    
    for i, slide in enumerate(slides):
        # Check items
        for j, item in enumerate(slide.get("items", [])):
            if isinstance(item, str):
                for sym in BULLET_SYMBOLS:
                    if item.startswith(sym):
                        result.add_error(
                            "bullet_symbol",
                            f"slides[{i}].items[{j}]",
                            f"Manual bullet symbol '{sym}' found at start of item",
                            "Remove the bullet symbol - it will be added automatically"
                        )
                        break


def validate_image_paths(content: Dict[str, Any], result: ValidationResult, images_dir: Path = None) -> None:
    """Check that image paths exist."""
    slides = content.get("slides", [])
    base_dir = images_dir or Path(".")
    
    for i, slide in enumerate(slides):
        image = slide.get("image")
        if not image:
            continue
        
        # Check local path
        path = image.get("path")
        if path:
            image_path = base_dir / path
            if not image_path.exists():
                # Try alternate extensions
                stem = image_path.stem
                parent = image_path.parent
                found = False
                for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp"]:
                    alt_path = parent / f"{stem}{ext}"
                    if alt_path.exists():
                        found = True
                        result.add_warning(
                            "image_path",
                            f"slides[{i}].image.path",
                            f"Image not found at {path}, but found at {alt_path.name}",
                            f"Update path to '{alt_path}'"
                        )
                        break
                
                if not found:
                    result.add_error(
                        "image_path",
                        f"slides[{i}].image.path",
                        f"Image not found: {path}",
                        "Check the path or run extract_images.py first"
                    )


def validate_text_length(content: Dict[str, Any], result: ValidationResult) -> None:
    """Check for text that might overflow."""
    slides = content.get("slides", [])
    
    for i, slide in enumerate(slides):
        # Check title length
        title = slide.get("title", "")
        if len(title) > MAX_TITLE_LENGTH:
            result.add_warning(
                "overflow",
                f"slides[{i}].title",
                f"Title length ({len(title)}) exceeds {MAX_TITLE_LENGTH} characters",
                "Consider shortening the title"
            )
        
        # Check items
        items = slide.get("items", [])
        if len(items) > MAX_ITEMS_PER_SLIDE:
            result.add_warning(
                "overflow",
                f"slides[{i}].items",
                f"Too many items ({len(items)}) - recommend max {MAX_ITEMS_PER_SLIDE}",
                "Consider splitting into multiple slides"
            )
        
        for j, item in enumerate(items):
            if isinstance(item, str) and len(item) > MAX_ITEM_LENGTH:
                result.add_warning(
                    "overflow",
                    f"slides[{i}].items[{j}]",
                    f"Item length ({len(item)}) exceeds {MAX_ITEM_LENGTH} characters",
                    "Consider shortening or splitting the item"
                )


def validate_structure(content: Dict[str, Any], result: ValidationResult) -> None:
    """Check for structural issues (agenda, summary presence)."""
    slides = content.get("slides", [])
    if not slides:
        result.add_error("structure", "slides", "No slides found", "Add at least one slide")
        return
    
    types = [s.get("type") for s in slides]
    
    # Check title slide is first
    if types[0] != "title":
        result.add_warning(
            "structure",
            "slides[0]",
            "First slide is not a title slide",
            "Consider adding a title slide at the beginning"
        )
    
    # Check agenda exists (for presentations with 5+ slides)
    if len(slides) >= 5 and "agenda" not in types:
        result.add_warning(
            "structure",
            "slides",
            "No agenda slide found in presentation with 5+ slides",
            "Consider adding an agenda slide after the title"
        )
    
    # Check summary/closing exists (for presentations with 5+ slides)
    if len(slides) >= 5:
        has_summary = "summary" in types
        has_closing = "closing" in types
        
        # Also check for content slides with summary-like titles
        summary_keywords = ["まとめ", "summary", "結論", "conclusion", "おわりに", "closing"]
        for slide in slides:
            title = slide.get("title", "").lower()
            if any(keyword in title for keyword in summary_keywords):
                has_summary = True
                break
        
        if not has_summary and not has_closing:
            result.add_warning(
                "structure",
                "slides",
                "No summary or closing slide found",
                "Consider adding a summary or closing slide at the end"
            )


def validate_content(content_path: str, images_dir: str = None) -> ValidationResult:
    """Run all validations on a content.json file."""
    result = ValidationResult()
    
    # Load content
    try:
        with open(content_path, "r", encoding="utf-8") as f:
            content = json.load(f)
    except json.JSONDecodeError as e:
        result.add_error("json", "file", f"Invalid JSON: {e}")
        return result
    except FileNotFoundError:
        result.add_error("file", "file", f"File not found: {content_path}")
        return result
    
    # Determine images directory
    content_dir = Path(content_path).parent.parent if images_dir is None else None
    img_dir = Path(images_dir) if images_dir else content_dir
    
    # Run validations
    validate_schema(content, result)
    validate_empty_content(content, result)
    validate_items_format(content, result)  # Check items are string[], not object[]
    validate_bullet_symbols(content, result)
    validate_image_paths(content, result, img_dir)
    validate_text_length(content, result)
    validate_structure(content, result)
    
    return result


def print_result(result: ValidationResult) -> None:
    """Print validation result in a human-readable format."""
    status_icon = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}[result.status]
    
    print(f"\n{status_icon} Validation {result.status}")
    print("=" * 50)
    
    if result.errors:
        print(f"\n❌ Errors ({len(result.errors)}):")
        for err in result.errors:
            print(f"  [{err['type']}] {err['location']}")
            print(f"    {err['message']}")
            if err.get('suggestion'):
                print(f"    → {err['suggestion']}")
    
    if result.warnings:
        print(f"\n⚠️ Warnings ({len(result.warnings)}):")
        for warn in result.warnings:
            print(f"  [{warn['type']}] {warn['location']}")
            print(f"    {warn['message']}")
            if warn.get('suggestion'):
                print(f"    → {warn['suggestion']}")
    
    if not result.errors and not result.warnings:
        print("\n  All checks passed!")
    
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Validate content.json for PPTX generation",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("content", help="Path to content.json file")
    parser.add_argument("--images-dir", "-i", help="Base directory for image paths")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    
    args = parser.parse_args()
    
    result = validate_content(args.content, args.images_dir)
    
    if args.json:
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    else:
        print_result(result)
    
    # Exit code
    if result.errors:
        sys.exit(1)
    elif result.warnings and args.strict:
        sys.exit(1)
    elif result.warnings:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
