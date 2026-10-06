# Punto — Personal field notes

Sito personale statico pubblicato su GitHub Pages, costruito con HTML, CSS e JavaScript senza build o backend.

## Direzione visiva

Un archivio personale editoriale e tecnico ispirato ai pannelli broadcast di **THE FINALS**: fondo nero, griglie HUD, tipografia forte, bordi tecnici e accenti signal red, yellow e cyan.

## Contenuti

- profilo e statement personale di Punto;
- interessi: musica, videogiochi, viaggi e radioamatorialità;
- formazione all’ITIS Max Planck di Lancenigo di Villorba, specializzazione telecomunicazioni;
- pagina Radioamatorialità con pannello di controllo, spettro e registro tecnico;
- hobby: modellismo, Warhammer 40,000, giochi da tavolo, stampa 3D, collezionismo e fumetti;
- pagina musicale con profilo Spotify;
- pagina videogiochi con preferiti, filtri, rotazione, trailer di THE FINALS e sincronizzazione Steam;
- contatti via email, Discord e Spotify;
- menu mobile accessibile, layout responsive, micro-interazioni hover e scroll reveal.

## Struttura

```text
.
├── index.html       # Profilo, interessi, formazione e contatti
├── hobby.html       # Hobby e attività personali
├── music.html       # Ascolti e profilo Spotify
├── games.html       # Videogiochi, filtri e sincronizzazione Steam
├── radio.html       # Radioamatorialità e pannello di controllo
├── style.css        # Sistema visivo responsive
├── script.js        # Menu mobile, filtri, reveal e micro-interazioni
└── .nojekyll        # Disabilita il processing Jekyll
```

## Pubblicazione

In **Settings → Pages**, selezionare **Deploy from a branch**, branch `main`, cartella `/ (root)`.

URL: <https://pvunto.github.io>

## Aggiornamento automatico Steam

Il workflow `.github/workflows/update-steam-games.yml` controlla una volta al giorno il profilo pubblico `76561199097297410` e aggiorna `games.html` con i giochi recenti e i generi individuati.

- non richiede password o Steam Guard;
- usa i dati pubblici del profilo e il catalogo pubblico Steam;
- esclude titoli tecnici come `Spacewar` dalla lista visibile;
- mostra la data e l’ora dell’ultimo controllo;
- se Steam risponde con un limite temporaneo o non è disponibile, mantiene la pagina precedente e riprova;
- può essere avviato manualmente da **Actions → Update Steam games → Run workflow**;
- il profilo può essere cambiato tramite la variabile `STEAM_PROFILE_ID` nel workflow, se necessario.

### Playtime totale

Se è disponibile il secret `STEAM_API_KEY` in **Settings → Secrets and variables → Actions → New repository secret**, il workflow mostra anche il totale delle ore. In caso contrario la pagina presenta un collegamento diretto al profilo Steam senza mostrare dati tecnici o valori inventati.

### Contatti

La homepage collega ora il profilo GitHub `Pvunto` e il profilo Spotify pubblico.
