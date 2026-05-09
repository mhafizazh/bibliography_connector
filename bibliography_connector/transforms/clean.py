def clean_items(items):
    cleaned = []

    for item in items:
        data = item.get("data", {})

        cleaned.append({
            "key": data.get("key"),
            "title": data.get("title"),
            "date": data.get("date"),
            "url": data.get("url"),
        })

    return cleaned