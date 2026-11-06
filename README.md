# Punto — sito personale

Sito statico in italiano per **https://pvunto.github.io/**. Mantiene HTML, CSS e JavaScript, senza framework o dipendenze runtime. Le pagine contengono già i testi e i metadati prima dell’esecuzione di JavaScript; menu, filtri, video e feedback sono miglioramenti progressivi.

## Aggiornare i contenuti

Modifica `data/content.json`, quindi esegui dalla radice del repository:

```bash
python3 build_site.py
```

Il generatore usa la libreria standard di Python e aggiorna `index.html`, `musica.html`, `giochi.html`, `progetti.html`, `404.html`, `sitemap.xml` e `robots.txt`. I template in `templates/` compongono le pagine; non modificare a mano i file HTML generati, perché la build li sovrascrive.

Il file JSON contiene profilo, musica, giochi, trailer, viaggi, radio, attività creative e progetti. Per aggiungere un gioco, aggiungi un oggetto all’array `games` con `id`, `title`, `genre`, `description`, `cover` e `mobileCover`; imposta `current: true` per segnalarlo come attuale. Tutti i titoli nell’elenco sono trattati come preferiti. Le miniature responsive devono essere copiate in `assets/`.

Per aggiornare i trailer, cambia l’ID YouTube, la descrizione e il canale in `trailers`. Il poster va conservato localmente in `assets/` e il suo percorso indicato nel campo `thumbnail`. L’iframe viene creato soltanto dopo il clic su Riproduci. Per aggiornare la musica, modifica `music.listening` o aggiungi le selezioni specifiche nei campi `music.selections`; il profilo Spotify è in `music.spotify`. Progetti correnti e futuri sono negli array omonimi sotto `projects`.

La foto originale del profilo resta in `assets/profilo.webp` e non viene sovrascritta dal processo di ottimizzazione. Per rigenerare le varianti WebP responsive dopo averla sostituita, installa Pillow e lancia `python3 tools/optimize_profile.py`.

## Superfan

Le pagine ufficiali consultate sono il [sito Superfan](https://www.superfan.social/) e le [FAQ](https://www.superfan.social/faqs). Non vi è stata trovata documentazione pubblica verificabile di API o widget per incorporare un profilo; non è stata quindi aggiunta un’integrazione non documentata. La pagina Musica rimanda al servizio ufficiale. Se fornisci un URL pubblico del tuo profilo, si può sostituire il collegamento esterno generico con quello diretto.

## Performance e accessibilità

Le foto del profilo e dei viaggi usano varianti WebP responsive; le copertine dei giochi sono responsive e lazy-loaded. I poster locali dei trailer non contattano YouTube: il player usa `youtube-nocookie.com` soltanto dopo l’interazione. Non ci sono librerie JavaScript o font remoti. Menu e filtri hanno etichette ARIA, il modulo feedback apre una bozza GitHub senza inviarla automaticamente e le animazioni rispettano `prefers-reduced-motion`.

## Pubblicazione e archivio

GitHub Pages pubblica la cartella radice del branch `main`. Dopo la build e le verifiche locali, integra il branch di lavoro in `main` e fai push; Pages pubblicherà le pagine statiche, la sitemap e la pagina 404. Il branch `legacy-site` conserva la versione precedente e non va modificato.
