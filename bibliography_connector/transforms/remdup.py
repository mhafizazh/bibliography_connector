def remdup_items(items):
    seen = set()
    result = []

    for item in items:
        key = item["key"]

        if key not in seen:
            seen.add(key)
            result.append(item)

    return result