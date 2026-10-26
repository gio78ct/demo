# Offerte Hard Disk

Web app per confrontare le offerte su hard disk/SSD, ordinabili per prezzo, **€/TB** e sconto, con filtri per tipo (HDD/SSD/NAS), interno/esterno, capacità minima e prezzo massimo.

Solo libreria standard Python (nessuna dipendenza).

```
python3 app.py          # http://localhost:8000
python3 -m unittest discover tests
```

## Importazione CSV

Il pulsante **Importa CSV** nella pagina carica un file (solo per la sessione corrente) e lo aggiunge ai risultati; per dati permanenti modifica `data/offerte.csv`.

Separatore `,` o `;`, decimali anche in formato italiano (`1.299,90`). Colonne obbligatorie: `prodotto`, `prezzo`. Opzionali: `fonte`, `prezzo_listino` (serve per lo sconto), `url`, `tipo` (HDD/SSD/NAS), `forma` (interno/esterno), `capacita_tb`. Se `tipo`, `forma` o `capacita_tb` mancano vengono ricavati dal titolo.

## Fonti

| Fonte | Stato |
|---|---|
| `csv` | Legge `data/offerte.csv` (20 offerte raccolte da una ricerca web il 26/10/2026: prezzi indicativi, da verificare sul sito) |
| `ebay` | eBay Browse API (EBAY_IT). Attiva con `EBAY_CLIENT_ID` e `EBAY_CLIENT_SECRET` (developer.ebay.com). Non testata con credenziali reali |
| Amazon.it | Non implementata: serve la Product Advertising API (account Associates) |
| Trovaprezzi / idealo | Non implementate: non hanno API pubbliche e lo scraping può violare i ToS |

Per aggiungere una fonte: sottoclasse di `Source` in `offers/sources.py` che restituisce `Offer.build(...)`, poi registrarla in `SOURCES`.
