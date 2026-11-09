# Punto — sito personale

Sito statico in italiano per **https://pvunto.github.io/**. Mantiene HTML, CSS e JavaScript, senza framework o dipendenze runtime. Le pagine contengono già i testi e i metadati prima dell’esecuzione di JavaScript; menu, filtri, video e feedback sono miglioramenti progressivi.

## Aggiornare i contenuti

Modifica `data/content.json`, quindi esegui dalla radice del repository:

```bash
python3 build_site.py
```

Il generatore usa la libreria standard di Python e aggiorna `index.html`, `musica.html`, `giochi.html`, `progetti.html`, `404.html`, `sitemap.xml` e `robots.txt`. I template in `templates/` compongono le pagine; non modificare a mano i file HTML generati, perché la build li sovrascrive.

Il file JSON contiene profilo, musica, giochi, trailer, attività creative e progetti. Il blocco Viaggi è stato rimosso dalla Home; l’interesse personale per i viaggi resta nel profilo. L’interesse per radio e telecomunicazioni resta nel profilo, senza pannelli o configurazioni dimostrative. Per aggiungere un gioco, aggiungi un oggetto all’array `games` con `id`, `title`, `genre`, `description`, `cover` e `mobileCover`; imposta `current: true` per segnalarlo come attuale. Tutti i titoli nell’elenco sono trattati come preferiti. Le miniature responsive devono essere copiate in `assets/`.

Per aggiornare i trailer, cambia l’ID YouTube, la descrizione e il canale in `trailers`. Il poster va conservato localmente in `assets/` e il suo percorso indicato nel campo `thumbnail`. L’iframe viene creato soltanto dopo il clic su Riproduci. Per aggiornare la musica, modifica `music.spotify`, `music.categories` e `music.albums`. Ogni album contiene titolo, artista, brano associato, pagina album e playlist Spotify, testo alternativo e percorsi alle copertine locali 320/640 WebP. Gli stati dei progetti sono raccolti negli array `projects.current`, `projects.future` e `projects.completed`; gli array vuoti mostrano una nota, non schede fittizie.

La foto originale del profilo resta in `assets/profilo.webp` e non viene sovrascritta dal processo di ottimizzazione. Per rigenerare le varianti WebP responsive dopo averla sostituita, installa Pillow e lancia `python3 tools/optimize_profile.py`.

## Superfan

La pagina Musica espone un solo link esterno al [sito Superfan](https://www.superfan.social/); non integra player, widget, API o dati simulati. Non è stato fornito un URL personale Superfan.

## Performance e accessibilità

La foto personale originale resta in `assets/profilo.webp` e non viene sovrascritta dal processo di ottimizzazione; la pagina la mostra senza ritagli. Le immagini dei giochi e degli album hanno varianti WebP responsive. I poster dei trailer sono locali e il player usa `youtube-nocookie.com` soltanto dopo l’interazione. Non ci sono librerie JavaScript o font remoti. Menu e filtri hanno etichette ARIA, il modulo contatti apre una bozza Issue GitHub senza inviarla automaticamente e le transizioni rispettano `prefers-reduced-motion`.

## Pubblicazione e archivio

GitHub Pages pubblica la cartella radice del branch `main`. Dopo la build e le verifiche locali, integra il branch di lavoro in `main` e fai push; Pages pubblicherà le pagine statiche, la sitemap e la pagina 404. Il branch `legacy-site` conserva la versione precedente e non va modificato.
