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
        "title": "Punto — profilo personale",
        "description": "Profilo personale di Punto: musica, videogiochi, viaggi e attività creative.",
        "keywords": "Punto, musica, videogiochi, viaggi, attività creative",
    },
    {
        "key": "music",
        "output": "musica.html",
        "title": "Musica e ascolti personali — Punto",
        "description": "Quattro copertine di album presenti nei mix pubblici Spotify di Punto, aree d’ascolto e collegamento al profilo.",
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
        "description": "Progetti personali di Punto, organizzati per stato: in corso, idee future e completati.",
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
    ):
        asset = asset_path(image)
        if not asset.is_file():
            raise FileNotFoundError(f"Immagine mancante: {asset}")
    for trailer in data["trailers"]:
        asset = asset_path(trailer["thumbnail"])
        if not asset.is_file():
            raise FileNotFoundError(f"Miniatura trailer mancante: {asset}")
    if not data["music"].get("albums"):
        raise ValueError("La pagina Musica deve contenere almeno un album.")
    for album in data["music"]["albums"]:
        for key in ("cover", "mobileCover"):
            asset = asset_path(album[key])
            if not asset.is_file():
                raise FileNotFoundError(f"Copertina album mancante: {asset}")
        if not album["playlistUrl"].startswith("https://open.spotify.com/playlist/"):
            raise ValueError(f"URL playlist Spotify non valido: {album['playlistUrl']}")
        if not album["albumUrl"].startswith("https://open.spotify.com/album/"):
            raise ValueError(f"URL album Spotify non valido: {album['albumUrl']}")
    for stage in ("current", "future", "completed"):
        if not isinstance(data["projects"].get(stage), list):
            raise ValueError(f"Lo stato progetti '{stage}' deve essere un array.")
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


def music_categories(data: dict) -> str:
    return "\n".join(
        f'<li class="music-focus-item"><span class="music-focus-number">{esc(item["number"])}</span>'
        f'<div><h3>{esc(item["title"])}</h3><p>{esc(item["description"])}</p></div></li>'
        for item in data["music"]["categories"]
    )


def music_albums(data: dict) -> str:
    cards = []
    for index, album in enumerate(data["music"]["albums"], start=1):
        title = esc(album["title"])
        artist = esc(album["artist"])
        album_url = esc(album["albumUrl"])
        playlist_url = esc(album["playlistUrl"])
        cover = esc(album["cover"])
        mobile = esc(album["mobileCover"])
        cards.append(
            f'<article class="album-panel album-panel--{index:02d}">'
            f'<a class="album-cover" href="{album_url}" target="_blank" rel="noopener noreferrer" aria-label="Apri l’album {title} di {artist} su Spotify">'
            f'<picture><source type="image/webp" srcset="{mobile} 320w, {cover} 640w" sizes="(max-width: 380px) 82vw, (max-width: 700px) 42vw, (max-width: 1000px) 34vw, 28vw">'
            f'<img src="{cover}" width="640" height="640" alt="{esc(album["alt"])}" loading="lazy" decoding="async"></picture></a>'
            f'<div class="album-copy"><p class="album-playlist-label"><span>{index:02d}</span> MIX / {esc(album["playlistTitle"])}</p>'
            f'<h3>{title}</h3><p class="album-artist">{artist}</p>'
            f'<p class="album-track"><span>BRANO</span> “{esc(album["track"])}”</p>'
            f'<a class="album-playlist-link" href="{playlist_url}" target="_blank" rel="noopener noreferrer">Apri il mix Spotify <span aria-hidden="true">↗</span></a></div></article>'
        )
    return "\n".join(cards)


def game_cards(data: dict) -> str:
    cards = []
    for index, game in enumerate(data["games"], start=1):
        tags = "preferito attuale" if game.get("current") else "preferito"
        current_class = " is-current" if game.get("current") else ""
        if game.get("current"):
            layout = "feature"
        elif index <= 10:
            layout = "standard"
        elif index <= 12:
            layout = "wide"
        else:
            layout = "compact"
        current_label = (
            '<span class="current-label"><i aria-hidden="true"></i> ATTUALE</span>'
            if game.get("current") else '<span class="favorite-mark" role="img" aria-label="Preferito">★</span>'
        )
        mobile = esc(game["mobileCover"])
        cover = esc(game["cover"])
        title = esc(game["title"])
        cards.append(
            f'<article class="game-card game-card--{layout}{current_class}" data-game="{esc(game["id"])}" data-layout="{layout}" data-tags="{tags}">'
            f'<div class="game-art"><picture><source type="image/webp" srcset="{mobile} 320w, {cover} 460w" sizes="(max-width: 500px) 90vw, (max-width: 700px) 46vw, (max-width: 900px) 30vw, 22vw">'
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
    status_class = re.sub(r"[^a-z0-9]+", "-", project["status"].casefold()).strip("-")
    return (
        f'<article class="project-card"><div class="project-top"><span>{number:02d} / {esc(project["category"])}</span>'
        f'<span class="project-status project-status--{esc(status_class)}">{esc(project["status"])}</span></div>'
        f'<h3>{esc(project["name"])}</h3><p>{esc(project["description"])}</p>'
        f'<div class="project-links">{link_markup}</div></article>'
    )


def future_projects(data: dict) -> str:
    projects = data["projects"]["future"]
    if not projects:
        return '<p class="empty-note">Le idee future verranno aggiunte qui quando saranno definite.</p>'
    return "\n".join(project_card(project, index) for index, project in enumerate(projects, start=1))


def completed_projects(data: dict) -> str:
    projects = data["projects"]["completed"]
    if not projects:
        return '<p class="empty-note">Non sono ancora elencati progetti completati.</p>'
    return "\n".join(project_card(project, index) for index, project in enumerate(projects, start=1))


def render(data: dict) -> None:
    outputs = {
        "home": (TEMPLATES / "home.html").read_text(encoding="utf-8"),
        "music": (TEMPLATES / "music.html").read_text(encoding="utf-8"),
        "games": (TEMPLATES / "games.html").read_text(encoding="utf-8"),
        "projects": (TEMPLATES / "projects.html").read_text(encoding="utf-8"),
        "not_found": (TEMPLATES / "404.html").read_text(encoding="utf-8"),
    }
    hobbies = data["hobbies"]
    replacements = {
        "home": {
            "__PROFILE_INTRO__": esc(data["profile"]["intro"]),
            "__PROFILE_ABOUT__": esc(data["profile"]["about"]),
            "__PROFILE_PHOTO__": esc(data["profile"]["photo"].replace("profilo.webp", "profilo-768.webp")),
            "__PROFILE_PHOTO_ALT__": esc(data["profile"]["photoAlt"]),
            "__HOBBIES_INTRO__": esc(hobbies["intro"]),
            "__HOBBIES_APPROACH__": esc(hobbies["approach"]),
            "__HOBBY_CARDS__": hobby_cards(data),
        },
        "music": {
            "__MUSIC_OVERVIEW__": esc(data["music"]["overview"]),
            "__MUSIC_CATEGORIES__": music_categories(data),
            "__MUSIC_ALBUMS__": music_albums(data),
            "__ALBUM_COUNT__": str(len(data["music"]["albums"])),
            "__SUPERFAN_URL__": esc(data["music"]["superfanUrl"]),
            "__SPOTIFY_URL__": esc(data["music"]["spotify"]),
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
            "__CURRENT_PROJECT_COUNT__": str(len(data["projects"]["current"])),
            "__CURRENT_PROJECTS__": "\n".join(
                project_card(project, index) for index, project in enumerate(data["projects"]["current"], start=1)
            ) or '<p class="empty-note">Non ci sono progetti attuali da mostrare.</p>',
            "__FUTURE_PROJECTS__": future_projects(data),
            "__COMPLETED_PROJECTS__": completed_projects(data),
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
