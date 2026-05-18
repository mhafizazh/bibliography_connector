from pathlib import Path
import json
import re
class HugoExporter:
    def __init__(self, output_dir, json_file):
        self.output_dir = Path(output_dir)
        self.json_file = Path(json_file)
    def export(self, items):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        for item in items:
            filename = self.output_dir / f"{item['key']}.md"
            title = item.get("title", "").replace('"', '\\"')
            date = self._parse_date(item.get("date", ""))
            url = item.get("url", "")
            content = f"""---
title: "{title}"
date: "{date}"
---
URL: {url}
"""
            filename.write_text(content, encoding="utf-8")
        self.json_file.write_text(
            json.dumps(items, indent=2),
            encoding="utf-8"
        )
        
    @staticmethod
    def _parse_date(date_str):
        if not date_str:
            return "1970-01-01"
        match = re.search(r'\b(\d{4})\b', date_str)
        return f"{match.group(1)}-01-01" if match else "1970-01-01"