# Offerte Hard Disk

Web app per confrontare le offerte su hard disk/SSD, ordinabili per prezzo, **€/TB** e sconto, con filtri per tipo (HDD/SSD/NAS), interno/esterno, capacità minima e prezzo massimo.

Solo libreria standard Python (nessuna dipendenza).

```
python3 app.py          # http://localhost:8000
python3 -m unittest discover tests
```

## Fonti

| Fonte | Stato |
|---|---|
| `demo` | Dati di esempio, sempre disponibile |
| `ebay` | eBay Browse API (EBAY_IT). Attiva con `EBAY_CLIENT_ID` e `EBAY_CLIENT_SECRET` (developer.ebay.com). Non testata con credenziali reali |
| Amazon.it | Non implementata: serve la Product Advertising API (account Associates) |
| Trovaprezzi / idealo | Non implementate: non hanno API pubbliche e lo scraping può violare i ToS |

Per aggiungere una fonte: sottoclasse di `Source` in `offers/sources.py` che restituisce `Offer.build(...)`, poi registrarla in `SOURCES`.
