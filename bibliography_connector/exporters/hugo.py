from pathlib import Path
import json

class HugoExporter:
    def __init__(self, output_dir, json_file):
        self.output_dir = Path(output_dir)
        self.json_file = Path(json_file)

    def export(self, items):
        self.output_dir.mkdir(parents=True, exist_ok=True)

        for item in items:
            filename = self.output_dir / f"{item['key']}.md"

            content = f"""---
title: "{item['title']}"
date: "{item['date']}"
---

URL: {item['url']}
"""

            filename.write_text(content, encoding="utf-8")

        self.json_file.write_text(
            json.dumps(items, indent=2),
            encoding="utf-8"
        )