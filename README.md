# Punto — Personal field notes

Sito personale statico pubblicato su GitHub Pages, costruito con HTML, CSS e JavaScript senza build o backend.

## Direzione visiva

Un archivio personale editoriale e tecnico: fondo neutro, tipografia forte, griglie asimmetriche, numerazioni, metadata e un unico accento verde acido. Il sistema mantiene il concetto di **personal field notes** evitando l’estetica SaaS e il classico portfolio da sviluppatore.

## Contenuti

- profilo e statement personale di Punto;
- interessi: musica, videogiochi, viaggi e radioamatorialità;
- formazione all’ITIS Max Planck di Lancenigo di Villorba, specializzazione telecomunicazioni;
- hobby: modellismo, Warhammer 40,000, giochi da tavolo, stampa 3D, collezionismo e fumetti;
- attività recenti organizzate come archivio personale;
- pagina musicale con profilo Spotify;
- pagina videogiochi con preferiti, rotazione, trailer di THE FINALS e sincronizzazione Steam;
- contatti via email, Discord e Spotify;
- layout responsive, micro-interazioni hover e scroll reveal accessibile.

## Struttura

```text
.
├── index.html       # Profilo, interessi, formazione e contatti
├── hobby.html       # Hobby e attività personali
├── music.html       # Ascolti e profilo Spotify
├── games.html       # Videogiochi e sincronizzazione Steam
├── style.css        # Sistema visivo responsive
├── script.js        # Reveal, navigazione e micro-interazioni
└── .nojekyll        # Disabilita il processing Jekyll
```

## Pubblicazione

In **Settings → Pages**, selezionare **Deploy from a branch**, branch `main`, cartella `/ (root)`.

URL: <https://pvunto.github.io>

## Aggiornamento automatico Steam

Il workflow `.github/workflows/update-steam-games.yml` controlla ogni ora il profilo pubblico `76561199097297410` e aggiorna `games.html` con i giochi recenti e i generi individuati.

- non richiede password o Steam Guard;
- usa i dati pubblici del profilo e il catalogo pubblico Steam;
- se Steam risponde con un limite temporaneo, mantiene la pagina precedente e riprova;
- può essere avviato manualmente da **Actions → Update Steam games → Run workflow**.

### Playtime totale

Per calcolare il totale delle ore, aggiungere il secret `STEAM_API_KEY` in **Settings → Secrets and variables → Actions → New repository secret**. Senza il secret, la pagina mostra `N/D ore` senza inventare dati.
