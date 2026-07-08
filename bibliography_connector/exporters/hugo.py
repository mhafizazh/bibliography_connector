from pathlib import Path
import json
import re
from datetime import date

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

class HugoExporter:
    def __init__(self, output_dir, json_file):
        self.output_dir = Path(output_dir)
        self.json_file = Path(json_file)
    def export(self, items):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        for item in items:
            filename = self.output_dir / f"{item['key']}.md"
            title = (item.get("title") or "").replace('"', '\\"')
            date = item.get("date")
            url = item.get("url") or ""
            content = f"""---
title: "{title}"
date: "{date}"
---
URL: {url}
"""
            filename.write_text(content, encoding="utf-8")
        self.json_file.write_text(
            json.dumps(items, indent=2, cls=DateEncoder),
            encoding="utf-8"
        )

