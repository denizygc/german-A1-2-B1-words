#!/usr/bin/env python3

import json
import re
import time
from pathlib import Path

from deep_translator import GoogleTranslator
from deep_translator.exceptions import TranslationNotFound


ROOT = Path(__file__).resolve().parent.parent
INDEX_HTML = ROOT / "index.html"
CACHE_JSON = ROOT / "translation-build-cache.json"
OUTPUT_JS = ROOT / "gloss-translations.js"

SOURCE_LEVELS = ("a1Questions", "a2Questions", "b1Questions")
TARGET_LANGUAGES = {
    "tr": "tr",
    "it": "it",
    "fr": "fr",
    "ar": "ar",
    "fa": "fa",
    "zh": "zh-CN",
    "ja": "ja",
}

CHUNK_SIZE = 80
PAUSE_SECONDS = 0.25


def load_questions():
    text = INDEX_HTML.read_text(encoding="utf-8")
    all_questions = []
    for name in SOURCE_LEVELS:
        match = re.search(rf"const {name} = (\[.*?\]);", text, re.S)
        if not match:
            raise RuntimeError(f"Could not find {name} in index.html")
        all_questions.extend(json.loads(match.group(1)))
    return all_questions


def extract_unique_glosses():
    seen = set()
    unique = []
    for question in load_questions():
        gloss = question.get("eng") if question.get("type") == "artikel" else question.get("ans")
        if gloss and gloss not in seen:
            seen.add(gloss)
            unique.append(gloss)
    return unique


def translate_chunk(translator, chunk):
    try:
        joined = "\n".join(chunk)
        translated = translator.translate(joined)
        lines = translated.splitlines()
        if len(lines) == len(chunk):
            return lines
    except TranslationNotFound:
        pass
    return [translate_line(translator, item) for item in chunk]


def translate_line(translator, text):
    candidates = [
        text,
        text.replace("/", " / "),
        text.replace("/", " or "),
        text.replace("/", ", "),
        text.replace("-->", "->"),
        text.replace("-->", ""),
    ]

    seen = set()
    for candidate in candidates:
        candidate = candidate.strip()
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        try:
            translated = translator.translate(candidate)
            if translated:
                return translated
        except Exception:
            continue

    print(f"WARNING: fallback kept English for: {text}")
    return text


def load_cache(glosses):
    if not CACHE_JSON.exists():
        return {
            "keys": glosses,
            "translations": {lang: [] for lang in TARGET_LANGUAGES},
        }

    data = json.loads(CACHE_JSON.read_text(encoding="utf-8"))
    if data.get("keys") != glosses:
        raise RuntimeError("Gloss list changed. Delete translation-build-cache.json and rerun.")
    for lang in TARGET_LANGUAGES:
        data.setdefault("translations", {}).setdefault(lang, [])
    return data


def save_cache(cache):
    CACHE_JSON.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def build_output(cache):
    keys_json = json.dumps(cache["keys"], ensure_ascii=False, separators=(",", ":"))
    translations_json = json.dumps(cache["translations"], ensure_ascii=False, separators=(",", ":"))
    content = (
        "window.GLOSS_KEYS = "
        + keys_json
        + ";\nwindow.GLOSS_TRANSLATIONS = "
        + translations_json
        + ";\n"
    )
    OUTPUT_JS.write_text(content, encoding="utf-8")


def main():
    glosses = extract_unique_glosses()
    cache = load_cache(glosses)

    for lang, target_code in TARGET_LANGUAGES.items():
        translated = cache["translations"][lang]
        if len(translated) > len(glosses):
            raise RuntimeError(f"Too many cached items for {lang}")

        translator = GoogleTranslator(source="en", target=target_code)
        index = len(translated)

        while index < len(glosses):
            chunk = glosses[index:index + CHUNK_SIZE]
            batch = translate_chunk(translator, chunk)
            translated.extend(batch)
            cache["translations"][lang] = translated
            index = len(translated)
            save_cache(cache)
            print(f"{lang}: {index}/{len(glosses)}")
            time.sleep(PAUSE_SECONDS)

    for lang, values in cache["translations"].items():
        if len(values) != len(glosses):
            raise RuntimeError(f"Incomplete translation set for {lang}: {len(values)}/{len(glosses)}")

    build_output(cache)
    print(f"Wrote {OUTPUT_JS.name}")


if __name__ == "__main__":
    main()
