#!/usr/bin/env python3
"""Genera le pagine statiche del sito Punto da data/content.json e templates/."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "content.json"
TEMPLATES = ROOT / "templates"
BASE_URL = "https://pvunto.github.io"

PAGES = [
    {
        "key": "home",
        "output": "index.html",
        "title": "Punto — profilo personale di telecomunicazioni",
        "description": "Profilo personale di Punto: telecomunicazioni, musica, videogiochi, viaggi, radio e attività creative.",
        "keywords": "Punto, telecomunicazioni, musica, videogiochi, viaggi, radio, attività creative",
    },
    {
        "key": "music",
        "output": "musica.html",
        "title": "Musica e ascolti personali — Punto",
        "description": "Playlist quotidiane, colonne sonore, nuove scoperte musicali e collegamento al profilo Spotify di Punto.",
        "keywords": "Punto, musica, ascolti, playlist, colonne sonore, Spotify",
    },
    {
        "key": "games",
        "output": "giochi.html",
        "title": "Videogiochi preferiti e trailer — Punto",
        "description": "Quindici videogiochi preferiti, tra cui ARC Raiders e THE FINALS, con trailer e profilo Steam.",
        "keywords": "Punto, videogiochi, ARC Raiders, THE FINALS, Steam, trailer",
    },
    {
        "key": "projects",
        "output": "progetti.html",
        "title": "Progetti personali e portfolio — Punto",
        "description": "Progetti personali di Punto, con stato delle attività in corso e delle idee future.",
        "keywords": "Punto, progetti personali, portfolio, HTML, CSS, JavaScript",
    },
]
NAV_ITEMS = [
    ("home", "Home", "index.html"),
    ("music", "Musica", "musica.html"),
    ("games", "Giochi", "giochi.html"),
    ("projects", "Progetti", "progetti.html"),
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def asset_path(relative_path: str) -> Path:
    return ROOT / str(relative_path).removeprefix("./")


def read_data() -> dict:
    with DATA_PATH.open(encoding="utf-8") as source:
        data = json.load(source)
    if not data.get("games"):
        raise ValueError("Il catalogo deve contenere almeno un gioco.")
    ids = [game["id"] for game in data["games"]]
    if len(ids) != len(set(ids)):
        raise ValueError("Gli identificativi dei giochi devono essere univoci.")
    for game in data["games"]:
        for key in ("cover", "mobileCover"):
            asset = asset_path(game[key])
            if not asset.is_file():
                raise FileNotFoundError(f"Copertina mancante: {asset}")
    for image in (
        data["profile"]["photo"],
        "./assets/profilo-192.webp",
        "./assets/profilo-384.webp",
        "./assets/profilo-768.webp",
        "./assets/viaggio-alta-quota-480.webp",
        "./assets/viaggio-alta-quota-768.webp",
        "./assets/viaggio-cammino-480.webp",
        "./assets/viaggio-cammino-768.webp",
    ):
        asset = asset_path(image)
        if not asset.is_file():
            raise FileNotFoundError(f"Immagine mancante: {asset}")
    for trailer in data["trailers"]:
        asset = asset_path(trailer["thumbnail"])
        if not asset.is_file():
            raise FileNotFoundError(f"Miniatura trailer mancante: {asset}")
    for item in data["travel"]["items"]:
        for key in ("image", "mobileImage"):
            asset = asset_path(item[key])
            if not asset.is_file():
                raise FileNotFoundError(f"Immagine viaggio mancante: {asset}")
    return data


def absolutize_internal_urls(markup: str) -> str:
    """Trasforma i riferimenti locali relativi in percorsi dalla root del dominio."""
    def replace(match: re.Match[str]) -> str:
        name, value = match.group(1), match.group(2)
        value = re.sub(r"(^|,\s*)\./", r"\1/", value)
        return f'{name}="{value}"'

    return re.sub(r'\b(href|src|srcset)="([^"]*)"', replace, markup)


def nav_markup(active: str) -> str:
    links = []
    for key, label, path in NAV_ITEMS:
        current = ' aria-current="page"' if key == active else ""
        links.append(f'<a href="/{path}"{current}>{esc(label)}</a>')
    return "\n      ".join(links)


def base_page(page: dict, content: str, active: str | None = None, noindex: bool = False) -> str:
    template = (TEMPLATES / "base.html").read_text(encoding="utf-8")
    canonical = BASE_URL + ("/" if page["output"] == "index.html" else "/" + page["output"])
    canonical_link = "" if noindex else f'<link rel="canonical" href="{esc(canonical)}">'
    og_url = "" if noindex else f'<meta property="og:url" content="{esc(canonical)}">'
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ""
    values = {
        "__TITLE__": esc(page["title"]),
        "__DESCRIPTION__": esc(page["description"]),
        "__KEYWORDS__": esc(page.get("keywords", "")),
        "__CANONICAL_LINK__": canonical_link,
        "__OG_URL__": og_url,
        "__ROBOTS__": robots,
        "__PAGE__": esc(active or "not-found"),
        "__NAV__": nav_markup(active or ""),
        "__CONTENT__": content,
    }
    for token, value in values.items():
        template = template.replace(token, value)
    return absolutize_internal_urls(template)


def music_cards(data: dict) -> str:
    cards = []
    for item in data["music"]["listening"]:
        cards.append(
            '<article class="music-card">'
            f'<div class="music-card-top"><span>{esc(item["number"])}</span><span>{esc(item["category"])}</span></div>'
            f'<h3>{esc(item["title"])}</h3><p>{esc(item["description"])}</p>'
            '</article>'
        )
    return "\n".join(cards)


def music_details(data: dict) -> str:
    selections = data["music"]["selections"]
    labels = {"genres": "Generi", "artists": "Artisti", "albums": "Album", "songs": "Brani"}
    populated = [(labels[key], values) for key, values in selections.items() if values]
    if not populated:
        return '<p class="empty-note">Non sono ancora elencati generi, artisti, album o brani specifici.</p>'
    sections = []
    for label, values in populated:
        tags = "".join(f"<li>{esc(value)}</li>" for value in values)
        sections.append(f'<div class="selection-group"><h3>{esc(label)}</h3><ul>{tags}</ul></div>')
    return "\n".join(sections)


def game_cards(data: dict) -> str:
    cards = []
    for index, game in enumerate(data["games"], start=1):
        tags = "preferito attuale" if game.get("current") else "preferito"
        current_class = " is-current" if game.get("current") else ""
        current_label = (
            '<span class="current-label"><i aria-hidden="true"></i> ATTUALE</span>'
            if game.get("current") else '<span class="favorite-mark" aria-label="Preferito">★</span>'
        )
        mobile = esc(game["mobileCover"])
        cover = esc(game["cover"])
        title = esc(game["title"])
        cards.append(
            f'<article class="game-card{current_class}" data-game="{esc(game["id"])}" data-tags="{tags}">'
            f'<div class="game-art"><picture><source type="image/webp" srcset="{mobile} 320w, {cover} 460w" sizes="(max-width: 650px) 46vw, (max-width: 900px) 30vw, 22vw">'
            f'<img src="{cover}" width="460" height="215" alt="Copertina di {title}" loading="lazy" decoding="async"></picture>'
            f'<span class="art-index">{index:02d}</span></div>'
            f'<div class="game-card-copy"><div class="game-meta"><span>{esc(game["genre"].upper())}</span>{current_label}</div>'
            f'<h3>{title}</h3><p>{esc(game["description"])}</p></div></article>'
        )
    return "\n".join(cards)


def trailer_cards(data: dict) -> str:
    cards = []
    for video in data["trailers"]:
        video_id = str(video["id"])
        if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
            raise ValueError(f"ID YouTube non valido: {video_id}")
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        thumbnail = esc(video["thumbnail"])
        cards.append(
            f'<article class="trailer-card" id="trailer-{esc(video_id)}">'
            f'<div class="video-frame" data-video-id="{esc(video_id)}" data-video-title="{esc(video["title"])}">'
            f'<button class="video-load" type="button" aria-label="Riproduci {esc(video["title"])}">'
            f'<img src="{thumbnail}" width="720" height="405" alt="" loading="lazy" decoding="async">'
            '<span class="play-button" aria-hidden="true">▶</span><span class="video-disclosure">PLAYER CARICATO SU RICHIESTA</span></button>'
            '</div>'
            f'<div class="trailer-info"><p class="eyebrow dark-eyebrow">{esc(video["label"])}</p>'
            f'<h3>{esc(video["title"])}</h3><p>{esc(video["description"])}</p>'
            f'<div class="trailer-links"><a href="{esc(video_url)}" target="_blank" rel="noopener noreferrer">Apri su YouTube ↗</a>'
            f'<a href="{esc(video["source"])}" target="_blank" rel="noopener noreferrer">Canale ufficiale ↗</a></div></div></article>'
        )
    return "\n".join(cards)


def travel_cards(data: dict) -> str:
    cards = []
    for item in data["travel"]["items"]:
        image = esc(item["image"])
        mobile = esc(item["mobileImage"])
        cards.append(
            f'<article class="travel-card"><div class="travel-card-top"><span>{esc(item["number"])}</span><span>ARCHIVIO VISIVO</span></div>'
            f'<picture><source type="image/webp" srcset="{mobile} 480w, {image} {int(item["width"])}w" sizes="(max-width: 700px) 88vw, (max-width: 1000px) 43vw, 36vw">'
            f'<img src="{image}" width="{int(item["width"])}" height="{int(item["height"])}" alt="{esc(item["alt"])}" loading="lazy" decoding="async"></picture>'
            f'<div class="travel-card-copy"><p class="travel-subtitle">{esc(item["subtitle"])}</p><h3>{esc(item["title"])}</h3><p>{esc(item["description"])}</p></div></article>'
        )
    return "\n".join(cards)


def coordinate_cards(data: dict) -> str:
    return "\n".join(
        f'<article class="coordinate-card"><span>{index:02d}</span><h3>{esc(item["title"])}</h3><p>{esc(item["description"])}</p></article>'
        for index, item in enumerate(data["travel"]["coordinates"], start=1)
    )


def radio_metrics(data: dict) -> str:
    radio = data["radio"]
    fields = [
        ("Modalità", radio["mode"]),
        ("Potenza indicata", radio["power"]),
        ("Stato esemplificativo", radio["status"]),
        ("Canale", radio["channel"]),
    ]
    return "\n".join(f'<div class="radio-metric"><dt>{esc(label)}</dt><dd>{esc(value)}</dd></div>' for label, value in fields)


def radio_areas(data: dict) -> str:
    return "\n".join(
        f'<article class="radio-area-card"><div><h3>{esc(item["title"])}</h3><span>{esc(item["tag"])}</span></div><p>{esc(item["description"])}</p></article>'
        for item in data["radio"]["areas"]
    )


def radio_register(data: dict) -> str:
    return "\n".join(
        f'<article class="register-card"><h3>{esc(item["title"])}</h3><p>{esc(item["description"])}</p></article>'
        for item in data["radio"]["register"]
    )


def hobby_cards(data: dict) -> str:
    return "\n".join(
        f'<article class="hobby-card"><span>{index:02d}</span><h3>{esc(item["title"])}</h3><p>{esc(item["description"])}</p></article>'
        for index, item in enumerate(data["hobbies"]["items"], start=1)
    )


def project_card(project: dict, number: int) -> str:
    links = []
    if project.get("repository"):
        links.append(f'<a href="{esc(project["repository"])}" target="_blank" rel="noopener noreferrer">Repository ↗</a>')
    if project.get("live"):
        links.append(f'<a href="{esc(project["live"])}" target="_blank" rel="noopener noreferrer">Versione online ↗</a>')
    link_markup = "".join(links)
    return (
        f'<article class="project-card"><div class="project-top"><span>{number:02d} / {esc(project["category"])}</span>'
        f'<span class="project-status">{esc(project["status"])}</span></div>'
        f'<h3>{esc(project["name"])}</h3><p>{esc(project["description"])}</p>'
        f'<div class="project-links">{link_markup}</div></article>'
    )


def future_projects(data: dict) -> str:
    projects = data["projects"]["future"]
    if not projects:
        return '<p class="empty-note">Non sono ancora state indicate idee future da pubblicare.</p>'
    return "\n".join(project_card(project, index) for index, project in enumerate(projects, start=1))


def render(data: dict) -> None:
    outputs = {
        "home": (TEMPLATES / "home.html").read_text(encoding="utf-8"),
        "music": (TEMPLATES / "music.html").read_text(encoding="utf-8"),
        "games": (TEMPLATES / "games.html").read_text(encoding="utf-8"),
        "projects": (TEMPLATES / "projects.html").read_text(encoding="utf-8"),
        "not_found": (TEMPLATES / "404.html").read_text(encoding="utf-8"),
    }
    radio = data["radio"]
    hobbies = data["hobbies"]
    replacements = {
        "home": {
            "__PROFILE_INTRO__": esc(data["profile"]["intro"]),
            "__PROFILE_ABOUT__": esc(data["profile"]["about"]),
            "__PROFILE_PHOTO__": esc(data["profile"]["photo"].replace("profilo.webp", "profilo-768.webp")),
            "__PROFILE_PHOTO_ALT__": esc(data["profile"]["photoAlt"]),
            "__TRAVEL_INTRO__": esc(data["travel"]["intro"]),
            "__TRAVEL_CARDS__": travel_cards(data),
            "__TRAVEL_COORDINATES__": coordinate_cards(data),
            "__RADIO_INTRO__": esc(radio["intro"]),
            "__RADIO_FREQUENCY__": esc(radio["frequency"]),
            "__RADIO_UNIT__": esc(radio["unit"]),
            "__RADIO_METRICS__": radio_metrics(data),
            "__RADIO_NOTE__": esc(radio["note"]),
            "__RADIO_AREAS__": radio_areas(data),
            "__RADIO_REGISTER__": radio_register(data),
            "__HOBBIES_INTRO__": esc(hobbies["intro"]),
            "__HOBBIES_APPROACH__": esc(hobbies["approach"]),
            "__HOBBY_CARDS__": hobby_cards(data),
        },
        "music": {
            "__MUSIC_CARDS__": music_cards(data),
            "__MUSIC_DETAILS__": music_details(data),
            "__SUPERFAN_STATUS__": esc(data["music"]["superfan"]["status"]),
            "__SPOTIFY_URL__": esc(data["music"]["spotify"]),
            "__SUPERFAN_URL__": esc(data["music"]["superfan"]["url"]),
        },
        "games": {
            "__GAME_COUNT__": str(len(data["games"])),
            "__CURRENT_COUNT__": str(sum(bool(game.get("current")) for game in data["games"])),
            "__CURRENT_GAME_LABEL__": esc(
                "I titoli attuali sono " + ", ".join(game["title"] for game in data["games"] if game.get("current")) + "."
            ) if any(game.get("current") for game in data["games"]) else "Non ho indicato titoli attuali.",
            "__GAME_CARDS__": game_cards(data),
            "__TRAILER_CARDS__": trailer_cards(data),
        },
        "projects": {
            "__CURRENT_PROJECTS__": "\n".join(
                project_card(project, index) for index, project in enumerate(data["projects"]["current"], start=1)
            ) or '<p class="empty-note">Non ci sono progetti attuali da mostrare.</p>',
            "__FUTURE_PROJECTS__": future_projects(data),
        },
    }
    page_data = {page["key"]: dict(page) for page in PAGES}
    current_titles = [game["title"] for game in data["games"] if game.get("current")]
    page_data["games"]["description"] = (
        f"{len(data['games'])} videogiochi preferiti nel profilo di Punto. "
        + (f"Titoli attuali: {', '.join(current_titles)}." if current_titles else "")
    )
    for key, page in page_data.items():
        body = outputs[key]
        for token, value in replacements.get(key, {}).items():
            body = body.replace(token, value)
        destination = ROOT / page["output"]
        destination.write_text(base_page(page, body, active=key), encoding="utf-8")
        print(f"Creato {destination.name}")

    not_found_page = {
        "key": "not-found",
        "output": "404.html",
        "title": "Pagina non trovata — Punto",
        "description": "La pagina richiesta non è disponibile. Torna al sito personale di Punto.",
        "keywords": "Punto, pagina non trovata",
    }
    (ROOT / "404.html").write_text(base_page(not_found_page, outputs["not_found"], noindex=True), encoding="utf-8")
    print("Creato 404.html")

    sitemap = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for page in PAGES:
        path = "/" if page["output"] == "index.html" else "/" + page["output"]
        sitemap.append(f"  <url><loc>{BASE_URL}{path}</loc></url>")
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n", encoding="utf-8")
    print("Aggiornati sitemap.xml e robots.txt")


def main() -> None:
    data = read_data()
    render(data)


if __name__ == "__main__":
    main()
