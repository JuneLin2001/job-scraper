LABEL_KEYWORDS = {
    "TypeScript": ["TypeScript", "TS"],
    "React": ["React"],
    "Vue": ["Vue"],
    "單元測試": ["單元測試", "Unit Testing", "Jest", "Vitest"],
    "端對端測試": ["端對端測試", "E2E Testing", "Cypress", "Playwright"],
    "新創": ["新創團隊", "Startup"],
    "CI/CD": ["CI/CD", "自動化部署", "Pipeline"],
    "雲端": ["AWS", "GCP", "Google Cloud", "Azure"],
    "Junior": ["Junior"],
    "Senior": ["Senior", "資深"],
}


def extract_labels_from_description(description: str):
    description_lower = description.lower()
    labels = set()

    for label, keywords in LABEL_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in description_lower:
                labels.add(label)
                break
    return list(labels)
