#!/usr/bin/env python3
"""
XHS Mindmap Visualizer
======================
Generates Mermaid mindmap from analyzed travel notes.

Usage:
    python visualizer.py --input analyzed.json --destination "黄山"
"""

import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
OUTPUT_DIR = SKILL_DIR / "output"


def escape_mermaid(text: str) -> str:
    """Escape special characters for Mermaid."""
    # Remove or replace problematic characters
    text = text.replace('"', "'")
    text = text.replace('(', "（")
    text = text.replace(')', "）")
    text = text.replace('[', "【")
    text = text.replace(']', "】")
    text = text.replace('\n', ' ')
    # Truncate long titles
    if len(text) > 40:
        text = text[:37] + "..."
    return text


def generate_mindmap(categorized: dict, destination: str = "旅行") -> str:
    """Generate Mermaid mindmap syntax."""
    lines = ["mindmap"]
    lines.append(f"  root(({destination}攻略))")
    
    # Category icons
    icons = {
        "交通": "🚗",
        "住宿": "🏨",
        "饮食": "🍜",
        "优惠": "💰",
        "学生": "🎓",
        "攻略": "📋",
        "其他": "📌"
    }
    
    for category, notes in categorized.items():
        if not notes:
            continue
        
        icon = icons.get(category, "📌")
        lines.append(f"    {icon} {category}")
        
        # Limit to top 5 notes per category
        for note in notes[:5]:
            title = escape_mermaid(note.get('title', '无标题'))
            lines.append(f"      {title}")
    
    return "\n".join(lines)


def generate_markdown_report(categorized: dict, destination: str, mindmap: str) -> str:
    """Generate a complete markdown report."""
    report = []
    report.append(f"# {destination}旅行攻略\n")
    report.append(f"*数据来源: 小红书 | 由 XHS Travel Planner 自动生成*\n")
    
    # Mindmap section
    report.append("## 思维导图\n")
    report.append("```mermaid")
    report.append(mindmap)
    report.append("```\n")
    
    # Detailed sections
    report.append("## 详细内容\n")
    
    icons = {
        "交通": "🚗",
        "住宿": "🏨", 
        "饮食": "🍜",
        "优惠": "💰",
        "学生": "🎓",
        "攻略": "📋",
        "其他": "📌"
    }
    
    for category, notes in categorized.items():
        if not notes:
            continue
        
        icon = icons.get(category, "📌")
        report.append(f"### {icon} {category}\n")
        
        for i, note in enumerate(notes[:10], 1):
            title = note.get('title', '无标题')
            link = note.get('link', '')
            author = note.get('author', '')
            likes = note.get('likes', '')
            
            if link:
                report.append(f"{i}. [{title}]({link})")
            else:
                report.append(f"{i}. {title}")
            
            if author or likes:
                report.append(f"   - 作者: {author} | 点赞: {likes}")
        
        report.append("")
    
    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="XHS Mindmap Visualizer")
    parser.add_argument("--input", type=str, default="analyzed.json", help="Input analyzed JSON")
    parser.add_argument("--destination", type=str, default="旅行", help="Destination name")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = OUTPUT_DIR / input_path
    
    if not input_path.exists():
        print(f"[ERROR] File not found: {input_path}")
        return
    
    categorized = json.loads(input_path.read_text(encoding='utf-8'))
    
    # Generate mindmap
    mindmap = generate_mindmap(categorized, args.destination)
    
    # Generate full report
    report = generate_markdown_report(categorized, args.destination, mindmap)
    
    # Save outputs
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    mindmap_file = OUTPUT_DIR / "mindmap.mmd"
    mindmap_file.write_text(mindmap, encoding='utf-8')
    print(f"[INFO] Mindmap saved to {mindmap_file}")
    
    report_file = OUTPUT_DIR / f"{args.destination}_攻略.md"
    report_file.write_text(report, encoding='utf-8')
    print(f"[INFO] Report saved to {report_file}")
    
    # Print mindmap to console
    print("\n=== Generated Mindmap ===\n")
    print(mindmap)


if __name__ == "__main__":
    main()
