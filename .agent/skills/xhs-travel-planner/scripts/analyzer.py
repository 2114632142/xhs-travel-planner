#!/usr/bin/env python3
"""
XHS Content Analyzer
====================
Categorizes scraped notes by travel-related keywords.

Usage:
    python analyzer.py --input xhs_results.json
"""

import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
KEYWORDS_FILE = SKILL_DIR / "references" / "keywords.json"
OUTPUT_DIR = SKILL_DIR / "output"


def load_keywords():
    """Load category keywords from config."""
    if KEYWORDS_FILE.exists():
        config = json.loads(KEYWORDS_FILE.read_text(encoding='utf-8'))
        return config.get('categories', {})
    return {
        "交通": ["交通", "高铁", "自驾"],
        "住宿": ["酒店", "民宿", "住宿"],
        "饮食": ["美食", "必吃", "餐厅"],
        "优惠": ["优惠", "免费", "白嫖"],
        "学生": ["学生", "大学生", "学生票"],
        "攻略": ["攻略", "行程", "路线"]
    }


def categorize_note(title: str, categories: dict) -> list:
    """Return list of matching categories for a note."""
    matched = []
    title_lower = title.lower()
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title_lower or keyword in title:
                matched.append(category)
                break
    
    return matched if matched else ["其他"]


def analyze(input_file: Path):
    """Analyze and categorize notes."""
    if not input_file.exists():
        print(f"[ERROR] File not found: {input_file}")
        return None
    
    notes = json.loads(input_file.read_text(encoding='utf-8'))
    categories = load_keywords()
    
    # Categorize each note
    categorized = {cat: [] for cat in categories.keys()}
    categorized["其他"] = []
    
    for note in notes:
        title = note.get('title', '')
        matched_cats = categorize_note(title, categories)
        
        for cat in matched_cats:
            if cat not in categorized:
                categorized[cat] = []
            categorized[cat].append(note)
    
    # Remove duplicates within categories
    for cat in categorized:
        seen_titles = set()
        unique = []
        for note in categorized[cat]:
            if note['title'] not in seen_titles:
                seen_titles.add(note['title'])
                unique.append(note)
        categorized[cat] = unique
    
    # Statistics
    print("\n=== 分类统计 ===")
    for cat, items in categorized.items():
        if items:
            print(f"  {cat}: {len(items)} 篇")
    
    # Save result
    output_file = OUTPUT_DIR / "analyzed.json"
    output_file.write_text(
        json.dumps(categorized, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f"\n[INFO] Analyzed results saved to {output_file}")
    
    return categorized


def main():
    parser = argparse.ArgumentParser(description="XHS Content Analyzer")
    parser.add_argument("--input", type=str, required=True, help="Input JSON file from scraper")
    
    args = parser.parse_args()
    input_path = Path(args.input)
    
    # Handle relative paths
    if not input_path.is_absolute():
        input_path = OUTPUT_DIR / input_path
    
    analyze(input_path)


if __name__ == "__main__":
    main()
