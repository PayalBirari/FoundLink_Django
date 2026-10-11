
import json
import os
import re
import urllib.request
import urllib.error


STOP_WORDS = {
    "i", "me", "my", "the", "a", "an", "is", "was", "were",
    "have", "has", "had", "lost", "found", "find", "looking",
    "for", "near", "at", "in", "on", "to", "of", "and", "with",
    "it", "this", "that", "item", "please", "help", "can", "you",
}


def extract_search_terms(query):
    """Use Gemini when configured; fall back to ordinary keyword search."""
    fallback = {
        "keywords": [
            word for word in re.findall(r"[a-zA-Z0-9]+", query.lower())
            if len(word) > 1 and word not in STOP_WORDS
        ]
    }

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return fallback, False

    prompt = (
        "Extract useful search keywords from this lost-item description. "
        "Include item type, color, brand, category, and location when present. "
        "Do not invent details. Return only valid JSON in this format: "
        '{"keywords":["blue","water bottle","library"],'
        '"category":"","location":""}. '
        "Description: " + query[:1000]
    )

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-2.5-flash:generateContent?key=" + api_key
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.1}
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            result = json.loads(response.read().decode("utf-8"))

        answer = result["candidates"][0]["content"]["parts"][0]["text"]
        answer = answer.strip()

        if answer.startswith("```"):
            answer = re.sub(r"^```(?:json)?\s*", "", answer)
            answer = re.sub(r"\s*```$", "", answer)

        terms = json.loads(answer)

        if not isinstance(terms, dict):
            return fallback, False

        keywords = terms.get("keywords", [])
        if not isinstance(keywords, list):
            keywords = []

        terms["keywords"] = [
            str(word).lower().strip()
            for word in keywords
            if isinstance(word, str) and word.strip()
        ]

        return terms, True

    except Exception:
        # If Gemini fails or reaches its limit, continue with keyword search.
        return fallback, False


def find_matching_found_items(query, found_items):
    """Rank found reports using available details and return match reasons."""
    terms, ai_used = extract_search_terms(query)

    keywords = terms.get("keywords", [])
    category = str(terms.get("category", "")).lower().strip()
    location = str(terms.get("location", "")).lower().strip()

    matches = []

    for item in found_items:
        name = (item.item_name or "").lower()
        item_category = (item.category or "").lower()
        item_location = (item.location or "").lower()
        description = (item.description or "").lower()

        score = 0
        reasons = []

        for keyword in keywords:
            keyword = keyword.strip()
            if not keyword:
                continue

            if keyword in name:
                score += 5
                reasons.append("Item name matches: " + keyword)
            elif keyword in item_category:
                score += 4
                reasons.append("Category matches: " + keyword)
            elif keyword in item_location:
                score += 3
                reasons.append("Location matches: " + keyword)
            elif keyword in description:
                score += 2
                reasons.append("Description matches: " + keyword)

        if category and category in item_category:
            score += 4
            reasons.append("Category matches your description")

        if location and location in item_location:
            score += 3
            reasons.append("Location matches your description")

        if score > 0:
            matches.append({
                "item": item,
                "score": score,
                "reasons": list(dict.fromkeys(reasons))[:4],
            })

    matches.sort(key=lambda match: match["score"], reverse=True)
    return matches[:30], ai_used
