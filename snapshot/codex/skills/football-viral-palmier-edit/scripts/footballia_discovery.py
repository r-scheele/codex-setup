#!/usr/bin/env python3
import argparse
import html
import json
import math
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen


BASE_URL = "https://footballia.eu"
DEFAULT_SINCE_YEAR = 2020

DEFAULT_SEED_URLS = [
    "https://footballia.eu/matches/fc-internazionale-fc-barcelona-champions-league-2024-2025",
    "https://footballia.eu/matches/paris-saint-germain-fc-internazionale-champions-league",
    "https://footballia.eu/matches/spain-england-euro-2024",
    "https://footballia.eu/matches/borussia-dortmund-real-madrid-champions-league-2023-2024",
    "https://footballia.eu/matches/manchester-city-real-madrid-champions-league-2022-2023",
    "https://footballia.eu/matches/manchester-city-real-madrid-champions-league-2023-2024",
    "https://footballia.eu/matches/manchester-city-real-madrid-champions-league-2021-2022",
    "https://footballia.eu/matches/real-madrid-chelsea-fc-champions-league-2021-2022",
    "https://footballia.eu/matches/manchester-city-aston-villa-premier-league-2021-2022",
    "https://footballia.eu/matches/manchester-united-manchester-city-premier-league-2024-2025",
    "https://footballia.eu/matches/sl-benfica-fc-barcelona-champions-league-2024-2025",
    "https://footballia.eu/matches/al-nassr-fc-inter-miami",
]

DEFAULT_CATALOGUE_URLS = [
    "https://footballia.eu/competitions/champions-league",
    "https://footballia.eu/competitions/euro",
    "https://footballia.eu/teams/real-madrid",
    "https://footballia.eu/teams/fc-barcelona",
    "https://footballia.eu/teams/manchester-city",
    "https://footballia.eu/teams/paris-saint-germain",
]

TEAM_KEYWORDS = [
    "real madrid",
    "fc barcelona",
    "barcelona",
    "manchester city",
    "manchester united",
    "psg",
    "paris saint-germain",
    "internazionale",
    "inter",
    "borussia dortmund",
    "chelsea",
    "liverpool",
    "arsenal",
    "spain",
    "england",
    "france",
    "argentina",
    "portugal",
    "al nassr",
    "inter miami",
]

COMPETITION_KEYWORDS = [
    "champions league",
    "euro",
    "world cup",
    "premier league",
    "la liga",
    "serie a",
    "copa america",
]

STAGE_KEYWORDS = [
    "semi-final",
    "semifinal",
    "quarter-final",
    "quarterfinal",
    "final",
    "derby",
    "clasico",
    "clásico",
]

EUROPE_US_AUDIENCE_KEYWORDS = [
    "champions league",
    "premier league",
    "euro",
    "world cup",
    "real madrid",
    "barcelona",
    "manchester city",
    "manchester united",
    "liverpool",
    "arsenal",
    "chelsea",
    "tottenham",
    "psg",
    "paris saint-germain",
    "inter",
    "internazionale",
    "borussia dortmund",
    "bayern",
    "spain",
    "england",
    "france",
    "portugal",
    "germany",
    "argentina",
    "inter miami",
    "messi",
    "ronaldo",
    "mbappe",
    "haaland",
    "vinicius",
    "bellingham",
    "lamine yamal",
]


def fetch_text(url, timeout=20):
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/126.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def clean_text(value):
    value = re.sub(r"<[^>]+>", " ", value or "")
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def first_match(pattern, text, flags=re.I | re.S, default=""):
    match = re.search(pattern, text or "", flags)
    return match.group(1).strip() if match else default


def parse_int(value, default=0):
    digits = re.sub(r"\D+", "", value or "")
    return int(digits) if digits else default


def season_year(season):
    if not season:
        return 0
    years = [int(y) for y in re.findall(r"(?:19|20)\d{2}", season)]
    if years:
        return max(years)
    match = re.search(r"((?:19|20)\d{2})\s*/\s*(\d{2})", season)
    if match:
        return int(match.group(1)[:2] + match.group(2))
    return 0


def extract_competition_and_season(text):
    pairs = re.findall(
        r'<a[^>]+href=["\']/competitions/[^"\']+["\'][^>]*>(.*?)</a>\s*([12]\d{3}(?:[-/][12]?\d{2,4})?)',
        text,
        re.I | re.S,
    )
    for competition, season in pairs:
        competition = clean_text(competition)
        if competition and "footballia" not in competition.lower():
            return competition, season.strip()

    plain = clean_text(text)
    match = re.search(
        r"((?:Champions League|Euro|World Cup|Premier League|La Liga|Serie A|Copa America)[^0-9]{0,40})"
        r"([12]\d{3}(?:[-/][12]?\d{2,4})?)",
        plain,
        re.I,
    )
    if match:
        return clean_text(match.group(1)), match.group(2).strip()
    return "", ""


def parse_score(text):
    match = re.search(
        r'<div[^>]+class=["\'][^"\']*\bresult\b[^"\']*["\'][^>]*>.*?'
        r'<span[^>]*>\s*(\d+)\s*:\s*(\d+)',
        text,
        re.I | re.S,
    )
    if not match:
        raw = clean_text(first_match(r'class=["\'][^"\']*result[^"\']*["\'][^>]*>(.{0,300})', text))
        match = re.search(r"\b(\d+)\s*:\s*(\d+)\b", raw)
    if not match:
        return "", 0
    home = int(match.group(1))
    away = int(match.group(2))
    return f"{home}:{away}", home + away


def parse_stage(text):
    raw_stage = clean_text(first_match(r'class=["\'][^"\']*\bstage\b[^"\']*["\'][^>]*>(.*?)</', text))
    plain = raw_stage or clean_text(text)
    normalized = plain.lower()
    if re.search(r"\b(cuartos de final|quarter[- ]finals?)\b", normalized, re.I):
        return "Quarter-Final"
    if re.search(r"\b(semi[- ]finals?|semifinals?)\b", normalized, re.I):
        return "Semi-Final"
    if re.search(r"\bfinals?\b", normalized, re.I):
        return "Final"
    match = re.search(r"\b(Week\s+\d+|Group stage|Round of 16)\b", plain, re.I)
    return match.group(1) if match else ""


def parse_match_page(text, url):
    title = clean_text(first_match(r"<h1[^>]*>(.*?)</h1>", text))
    if not title:
        title = clean_text(first_match(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)', text))
    if not title:
        title = clean_text(first_match(r"<title[^>]*>(.*?)</title>", text)).replace(" - Footballia", "")

    competition, season = extract_competition_and_season(text)
    date = clean_text(first_match(r'class=["\'][^"\']*playing_date[^"\']*["\'][^>]*>(.*?)</', text))
    if not date:
        date = first_match(
            r"\b((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},\s+[12]\d{3})\b",
            clean_text(text),
        )

    year = season_year(season)
    if not year and date:
        year = parse_int(first_match(r"\b([12]\d{3})\b", date))

    views = parse_int(first_match(r"([0-9][0-9,.\s]*)\s+Views\b", clean_text(text)))
    language = first_match(r"\bViews\s+([A-Z][A-Za-z]+)\b", clean_text(text))
    file_count = parse_int(first_match(r"divided\s+in\s+(\d+)\s+files?", clean_text(text)), default=1)
    score, total_goals = parse_score(text)
    goal_timestamps = [int(x) for x in re.findall(r'data-video-start-position=["\'](\d+)["\']', text)]
    if not total_goals and goal_timestamps:
        total_goals = len(goal_timestamps)

    candidate = {
        "url": url,
        "title": title or url.rsplit("/", 1)[-1].replace("-", " ").title(),
        "competition": competition,
        "season": season,
        "year": year,
        "date": date,
        "views": views,
        "language": language,
        "file_count": file_count,
        "score": score,
        "total_goals": total_goals,
        "goal_timestamps": goal_timestamps,
        "stage": parse_stage(text),
    }
    candidate["rank_reasons"] = candidate_reasons(candidate)
    return candidate


def is_recent_candidate(candidate, since_year=DEFAULT_SINCE_YEAR):
    return int(candidate.get("year") or 0) >= since_year


def candidate_reasons(candidate):
    reasons = []
    title = f"{candidate.get('title', '')} {candidate.get('competition', '')} {candidate.get('stage', '')}".lower()
    goals = int(candidate.get("total_goals") or 0)
    if is_recent_candidate(candidate):
        reasons.append(f"{candidate.get('year')} source")
    if goals >= 5:
        reasons.append(f"{goals} goals/event markers")
    elif goals >= 3:
        reasons.append("multi-goal match")
    if int(candidate.get("views") or 0) >= 10000:
        reasons.append("strong Footballia view signal")
    if any(k in title for k in COMPETITION_KEYWORDS):
        reasons.append("high-interest competition")
    if any(k in title for k in TEAM_KEYWORDS):
        reasons.append("recognizable teams")
    if any(k in title for k in STAGE_KEYWORDS):
        reasons.append("high-stakes stage")
    if is_europe_us_audience_fit(candidate):
        reasons.append("Europe/US audience fit")
    return reasons or ["usable Footballia match"]


def is_europe_us_audience_fit(candidate):
    text = " ".join(
        str(candidate.get(k) or "") for k in ["title", "competition", "season", "stage", "language", "url"]
    ).lower()
    if (candidate.get("language") or "").lower() == "english":
        return True
    return any(keyword in text for keyword in EUROPE_US_AUDIENCE_KEYWORDS)


def rank_candidate(candidate, since_year=DEFAULT_SINCE_YEAR, query_terms=None):
    query_terms = [q.lower() for q in (query_terms or []) if q.strip()]
    year = int(candidate.get("year") or 0)
    goals = int(candidate.get("total_goals") or 0)
    views = int(candidate.get("views") or 0)
    files = int(candidate.get("file_count") or 0)
    text = " ".join(
        str(candidate.get(k) or "") for k in ["title", "competition", "season", "stage", "url"]
    ).lower()

    score = 0.0
    if year >= since_year:
        score += 300 + (year - since_year) * 35
    else:
        score -= 1000 + max(0, since_year - year) * 50
    score += min(280, math.log10(max(views, 1)) * 45)
    score += min(360, goals * 55)
    score += min(80, len(candidate.get("goal_timestamps") or []) * 12)
    score += 30 if files > 1 else 0
    score += 80 if any(k in text for k in COMPETITION_KEYWORDS) else 0
    score += 80 if any(k in text for k in TEAM_KEYWORDS) else 0
    score += 70 if any(k in text for k in STAGE_KEYWORDS) else 0
    score += 160 if is_europe_us_audience_fit(candidate) else 0
    for term in query_terms:
        score += 120 if term in text else -20
    return round(score, 2)


def extract_match_links(text, base_url):
    links = set()
    for href in re.findall(r'href=["\']([^"\']*/matches/[^"#?]+)["\']', text, re.I):
        links.add(urljoin(base_url, html.unescape(href)))
    return sorted(links)


def catalogue_page_urls(text, base_url, page_limit):
    pages = {base_url}
    page_numbers = []
    for href, page_number in re.findall(r'href=["\']([^"\']*[?&]page=(\d+)[^"\']*)["\']', text, re.I):
        page_numbers.append(int(page_number))
        pages.add(urljoin(base_url, html.unescape(href)))
    if page_numbers:
        max_page = max(page_numbers)
        start = max(1, max_page - page_limit + 1)
        for page in range(start, max_page + 1):
            pages.add(f"{base_url.split('?')[0]}?page={page}")
    return sorted(pages)


def discover_from_catalogues(catalogue_urls, page_limit, sleep_seconds=0.25):
    match_urls = set()
    for catalogue_url in catalogue_urls:
        try:
            first_page = fetch_text(catalogue_url)
        except Exception as exc:
            print(f"warning: could not fetch catalogue {catalogue_url}: {exc}", file=sys.stderr)
            continue
        for page_url in catalogue_page_urls(first_page, catalogue_url, page_limit):
            try:
                page_text = first_page if page_url == catalogue_url else fetch_text(page_url)
            except Exception as exc:
                print(f"warning: could not fetch catalogue page {page_url}: {exc}", file=sys.stderr)
                continue
            match_urls.update(extract_match_links(page_text, page_url))
            time.sleep(sleep_seconds)
    return sorted(match_urls)


def write_outputs(out_dir, payload, limit):
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "footballia_candidates.json"
    md_path = out_dir / "footballia_candidates.md"
    selected_path = out_dir / "selected_footballia_match.json"

    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    if payload.get("selected"):
        selected_path.write_text(json.dumps(payload["selected"], indent=2, ensure_ascii=False) + "\n")

    lines = [
        "# Footballia 2020-Present Source Candidates",
        "",
        f"Generated: {payload['generated_at']}",
        f"Since year: {payload['since_year']}",
        "",
    ]
    selected = payload.get("selected")
    if selected:
        lines.extend(
            [
                "## Selected",
                "",
                f"[{selected['title']}]({selected['url']})",
                "",
                f"Score: {selected['viral_score']}; season: {selected.get('season') or 'unknown'}; "
                f"result: {selected.get('score') or 'unknown'}; views: {selected.get('views') or 0:,}",
                "",
                "Reasons: " + ", ".join(selected.get("rank_reasons") or []),
                "",
            ]
        )
    lines.extend(["## Ranked Candidates", ""])
    for i, record in enumerate(payload["records"][:limit], 1):
        lines.append(f"{i}. [{record['title']}]({record['url']})")
        lines.append(
            f"   Score: {record['viral_score']}; season: {record.get('season') or 'unknown'}; "
            f"result: {record.get('score') or 'unknown'}; views: {record.get('views') or 0:,}"
        )
        lines.append(f"   Why: {', '.join(record.get('rank_reasons') or [])}")
    md_path.write_text("\n".join(lines) + "\n")
    return md_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--since-year", type=int, default=DEFAULT_SINCE_YEAR)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--max-match-pages", type=int, default=40)
    parser.add_argument("--catalogue-page-limit", type=int, default=4)
    parser.add_argument("--url", action="append", default=[], help="Footballia match URL to include")
    parser.add_argument("--seed-url", action="append", default=[], help="Alias for --url")
    parser.add_argument("--catalogue-url", action="append", default=[], help="Footballia team/competition URL to crawl")
    parser.add_argument("--query", action="append", default=[], help="Team, player, competition, or theme to boost")
    parser.add_argument("--no-defaults", action="store_true", help="Do not include default 2020-present seed matches")
    parser.add_argument("--no-catalogue-crawl", action="store_true", help="Skip default catalogue crawling")
    args = parser.parse_args()

    match_urls = set(args.url + args.seed_url)
    if not args.no_defaults:
        match_urls.update(DEFAULT_SEED_URLS)

    catalogue_urls = list(args.catalogue_url)
    if not args.no_catalogue_crawl:
        catalogue_urls.extend(DEFAULT_CATALOGUE_URLS)
    if catalogue_urls:
        match_urls.update(discover_from_catalogues(catalogue_urls, args.catalogue_page_limit))

    records = []
    for url in sorted(match_urls)[: args.max_match_pages]:
        try:
            text = fetch_text(url)
            candidate = parse_match_page(text, url)
        except Exception as exc:
            print(f"warning: could not fetch match {url}: {exc}", file=sys.stderr)
            continue
        if not is_recent_candidate(candidate, args.since_year):
            continue
        candidate["viral_score"] = rank_candidate(candidate, args.since_year, args.query)
        candidate["rank_reasons"] = candidate_reasons(candidate)
        records.append(candidate)
        time.sleep(0.2)

    records.sort(key=lambda item: item.get("viral_score", 0), reverse=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "since_year": args.since_year,
        "query": args.query,
        "selected": records[0] if records else None,
        "records": records,
    }
    md_path = write_outputs(Path(args.out_dir).expanduser(), payload, args.limit)
    print(md_path)
    if payload["selected"]:
        print(f"SELECTED_URL={payload['selected']['url']}")
        print(f"SELECTED_TITLE={payload['selected']['title']}")
    return 0 if records else 2


if __name__ == "__main__":
    raise SystemExit(main())
