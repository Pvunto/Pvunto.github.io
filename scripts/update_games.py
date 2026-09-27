#!/usr/bin/env python3
"""Update the Games page from the public Steam profile.

The script intentionally uses public HTML plus the public Steam store details
endpoint, so no Steam password or API key is required.
"""
from __future__ import annotations

import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError
from pathlib import Path

PROFILE_URL = "https://steamcommunity.com/profiles/76561199097297410/"
ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "games.html"


def get(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "AlbertoFieldNotes/1.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                return response.read().decode("utf-8", "ignore")
        except (HTTPError, URLError):
            if attempt == 2:
                raise
            time.sleep(4 * (attempt + 1))


def clean(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def extract_games(profile: str) -> list[dict[str, str]]:
    starts = [m.start() for m in re.finditer(r'<div class="recent_game">', profile)]
    games = []
    for index, start in enumerate(starts):
        block = profile[start : starts[index + 1] if index + 1 < len(starts) else len(profile)]
        app = re.search(r'href="https://steamcommunity\.com/app/(\d+)"', block)
        title = re.search(r'<div class="game_name">\s*<a[^>]*>(.*?)</a>', block, re.S)
        details = re.search(r'<div class="game_info_details">(.*?)</div>', block, re.S)
        if not (app and title):
            continue
        detail = clean(details.group(1)) if details else "recentemente"
        hours = re.search(r"([\d.]+)\s*hrs? on record", detail, re.I)
        played = re.search(r"last played on\s*(.*)$", detail, re.I)
        games.append({
            "appid": app.group(1),
            "title": clean(title.group(1)),
            "detail": detail,
            "hours": hours.group(1) if hours else "—",
            "played": played.group(1) if played else "recentemente",
        })
    favorite = re.search(
        r'<div class="showcase_item_detail_title">.*?href="https://steamcommunity\.com/app/(\d+)".*?>(.*?)</a>',
        profile,
        re.S,
    )
    if favorite and not any(item["appid"] == favorite.group(1) for item in games):
        games.append({
            "appid": favorite.group(1),
            "title": clean(favorite.group(2)),
            "detail": "gioco preferito del profilo",
            "hours": "—",
            "played": "preferito",
        })
    return games[:6]


def genres_for(appid: str) -> list[str]:
    special = {
        "4000": ["Sandbox", "Social", "Physics"],
        "2073850": ["Competitive FPS", "Destruction"],
        "481510": ["Narrative Adventure", "Indie"],
        "431960": ["Creative", "Customization"],
    }
    if appid in special:
        return special[appid]
    try:
        raw = get(f"https://store.steampowered.com/api/appdetails?appids={appid}&l=english&cc=us")
        payload = json.loads(raw).get(appid, {}).get("data", {})
        return [item["description"] for item in payload.get("genres", [])[:3]] or ["Steam rotation"]
    except Exception:
        return ["Steam rotation"]


def profile_count(profile: str) -> str:
    match = re.search(r">Games</a>\s*(?:<[^>]+>\s*)?(\d+)", profile)
    return match.group(1) if match else "119"


def total_playtime_hours() -> int | None:
    api_key = os.environ.get("STEAM_API_KEY", "").strip()
    if not api_key:
        return None
    try:
        raw = get(
            "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?"
            f"key={api_key}&steamid=76561199097297410&format=json"
        )
        payload = json.loads(raw)
        minutes = sum(item.get("playtime_forever", 0) for item in payload.get("response", {}).get("games", []))
        return round(minutes / 60)
    except Exception as error:
        print(f"Steam total playtime unavailable: {error}")
        return None


def card(game: dict[str, str], index: int) -> str:
    title = html.escape(game["title"].upper())
    appid = game["appid"]
    url = f"https://store.steampowered.com/app/{appid}/"
    genres = genres_for(appid)
    genre_text = " / ".join(html.escape(item) for item in genres)
    descriptions = {
        "4000": "il posto dove creare caos con gli amici.",
        "2073850": "ritmo, squadre e arene che cambiano.",
        "481510": "personaggi, atmosfera e storie che restano.",
        "431960": "anche il desktop può avere una colonna sonora.",
    }
    description = descriptions.get(appid, "un titolo che è entrato nella rotazione recente.")
    favorite = " favorite-row" if appid == "481510" else ""
    fav = " <mark>FAV</mark>" if appid == "481510" else ""
    hours = f"{html.escape(game['hours'])} h su Steam" if game["hours"] != "—" else "profilo pubblico"
    return f'''      <a class="row game-row reveal{favorite}" href="{url}" target="_blank" rel="noreferrer"><small>{index:02d}</small><div><h2>{title}{fav}</h2><p>{genre_text} — {description}</p><em>{hours} · giocato {html.escape(game["played"])}</em></div><b>↗</b></a>'''


def replace_block(source: str, name: str, replacement: str) -> str:
    pattern = rf"(<!-- STEAM AUTO START:{name} -->).*?(<!-- STEAM AUTO END:{name} -->)"
    updated, count = re.subn(pattern, rf"\1\n{replacement}\n    \2", source, flags=re.S)
    if count != 1:
        raise RuntimeError(f"marker block {name!r} not found")
    return updated


def main() -> int:
    try:
        profile = get(PROFILE_URL)
    except (HTTPError, URLError) as error:
        print(f"Steam non disponibile ({error}); lascio games.html invariato.")
        return 0
    games = extract_games(profile)
    if not games:
        print("No recent public games found; leaving games.html unchanged.")
        return 0
    total = profile_count(profile)
    max_hours = max((float(item["hours"]) for item in games if item["hours"] != "—"), default=0)
    status = "ONLINE" if "Currently Online" in profile else "OFFLINE"
    stats = f'''    <section class="steam-stats reveal"><div><span>{html.escape(total)}</span><b>giochi<br />nel profilo</b></div><div><span>{max_hours:g}h</span><b>record personale<br />recente</b></div><div><span>{status}</span><b>ultimo check<br />profilo pubblico</b></div></section>'''
    total_hours = total_playtime_hours()
    totals = (
        f'''    <section class="total-playtime reveal is-synced"><div><p class="eyebrow">TOTAL PLAYTIME / STEAM API</p><h2>{total_hours:,} <span>ore</span></h2><p>Tempo complessivo registrato sui giochi visibili del profilo Steam.</p></div><strong>SYNC<br />OK</strong></section>'''
        if total_hours is not None
        else '''    <section class="total-playtime reveal"><div><p class="eyebrow">TOTAL PLAYTIME / STEAM API</p><h2>N/D <span>ore</span></h2><p>Imposta il secret STEAM_API_KEY nelle Actions della repository per calcolare il totale del profilo.</p></div><strong>SYNC<br />LOCKED</strong></section>'''
    )
    rotation = '''    <section class="rows game-rotation"><div class="rotation-head"><p class="eyebrow">CURRENT ROTATION</p><span>aggiornato automaticamente da Steam</span></div>\n''' + "\n".join(card(game, i) for i, game in enumerate(games, 1)) + "\n    </section>"
    genre_set = []
    for game in games:
        for genre in genres_for(game["appid"]):
            if genre not in genre_set:
                genre_set.append(genre)
    chips = "".join(f"<b>{index:02d} / {html.escape(genre.upper())}</b>" for index, genre in enumerate(genre_set[:6], 1))
    genre_board = f'''    <section class="genre-board reveal"><p class="eyebrow">GENRE SIGNAL</p><h2>Le mie<br /><span>frequenze.</span></h2><div class="genre-chips">{chips}</div></section>'''
    source = PAGE.read_text()
    source = replace_block(source, "STATS", stats)
    source = replace_block(source, "TOTALS", totals)
    source = replace_block(source, "ROTATION", rotation)
    source = replace_block(source, "GENRES", genre_board)
    PAGE.write_text(source)
    print(f"Updated games.html with {len(games)} public recent games.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
