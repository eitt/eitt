#!/usr/bin/env python3
"""Fetch ORCID works and update README + data/publications.md."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ORCID_ID = "0000-0002-4129-9163"
ORCID_WORKS_URL = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"
OUTPUT_PATH = Path("data/publications.md")
README_PATH = Path("README.md")
START_MARKER = "<!-- START_PUBLICATIONS -->"
END_MARKER = "<!-- END_PUBLICATIONS -->"


@dataclass
class Work:
    title: str
    year: str
    doi: str | None
    source: str | None


def _safe_text(value: str) -> str:
    return value.strip().replace("\n", " ")


def _extract_year(summary: dict) -> str:
    pub_date = summary.get("publication-date") or {}
    year = (pub_date.get("year") or {}).get("value")
    if year:
        return str(year)
    return "n.d."


def _extract_title(summary: dict) -> str:
    title_obj = (summary.get("title") or {}).get("title") or {}
    title = title_obj.get("value")
    if title:
        return _safe_text(str(title))
    return "Untitled work"


def _extract_source(summary: dict) -> str | None:
    source = (summary.get("journal-title") or {}).get("value")
    if source:
        return _safe_text(str(source))
    return None


def _extract_doi(summary: dict) -> str | None:
    ext_ids = summary.get("external-ids") or {}
    ext_id_list = ext_ids.get("external-id") or []
    for item in ext_id_list:
        id_type = str(item.get("external-id-type", "")).lower()
        id_value = item.get("external-id-value")
        if id_type == "doi" and id_value:
            cleaned = re.sub(r"^https?://(dx\.)?doi\.org/", "", str(id_value), flags=re.I)
            return cleaned.strip()
    return None


def fetch_works() -> list[Work]:
    req = Request(
        ORCID_WORKS_URL,
        headers={
            "Accept": "application/json",
            "User-Agent": "github-profile-readme-updater/1.0",
        },
    )

    with urlopen(req, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    groups = payload.get("group") or []
    works: list[Work] = []

    for group in groups:
        summaries = group.get("work-summary") or []
        for summary in summaries:
            works.append(
                Work(
                    title=_extract_title(summary),
                    year=_extract_year(summary),
                    doi=_extract_doi(summary),
                    source=_extract_source(summary),
                )
            )

    works.sort(key=lambda w: (w.year.isdigit(), w.year, w.title.lower()), reverse=True)
    return works


def _publication_lines(works: Iterable[Work]) -> list[str]:
    lines: list[str] = []
    listed = 0
    for work in works:
        if listed >= 12:
            break
        source_txt = f"*{work.source}*" if work.source else ""
        doi_txt = f" — DOI: https://doi.org/{work.doi}" if work.doi else ""
        line = f"- **{work.title}** ({work.year}) {source_txt}{doi_txt}".strip()
        lines.append(line)
        listed += 1

    if listed == 0:
        lines.append("- No publications returned by the ORCID API at this time.")

    return lines


def build_markdown(works: Iterable[Work]) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "<!-- AUTO-GENERATED: run scripts/update_publications.py -->",
        f"_Last updated: {ts}_",
        "",
        *_publication_lines(works),
        "",
        f"Full record: https://orcid.org/{ORCID_ID}",
    ]
    return "\n".join(lines) + "\n"


def write_publications_file(markdown: str) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(markdown, encoding="utf-8")


def update_readme(publication_lines: list[str]) -> None:
    if not README_PATH.exists():
        return

    readme = README_PATH.read_text(encoding="utf-8")
    pattern = re.compile(f"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}", re.S)
    replacement = START_MARKER + "\n" + "\n".join(publication_lines) + "\n" + END_MARKER
    updated = pattern.sub(replacement, readme)

    if updated != readme:
        README_PATH.write_text(updated, encoding="utf-8")


def main() -> int:
    try:
        works = fetch_works()
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        fallback = "\n".join(
            [
                "<!-- AUTO-GENERATED: fallback content due to API fetch failure -->",
                f"_Last attempted update: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_",
                "",
                f"- Unable to fetch ORCID works automatically (`{type(exc).__name__}`).",
                f"- Visit the ORCID record directly: https://orcid.org/{ORCID_ID}",
                "",
            ]
        )
        write_publications_file(fallback)
        return 1

    publication_lines = _publication_lines(works)
    markdown = build_markdown(works)
    write_publications_file(markdown)
    update_readme(publication_lines)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
