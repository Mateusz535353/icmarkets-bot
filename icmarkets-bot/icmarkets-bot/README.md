# IC Markets Trading Bot (MT5 + Python)

Projekt zawiera prosty zestaw skryptów do otwierania i zamykania pozycji na platformie MetaTrader 5 przez API Python.

## Pliki:
- `open_order.py` – otwiera pozycję BUY na `USTEC` z TP i SL
- `close_all_positions.py` – zamyka wszystkie otwarte pozycje na `USTEC`
- `config/settings.txt` – miejsce na przyszłe ustawienia
- `log/` – folder na logi transakcji

## Wymagania:
- MetaTrader 5 uruchomiony i zalogowany
- `pip install MetaTrader5`
- Konto IC Markets (demo lub real)

## Przenoszenie na VPS:
Po zakończeniu prac na komputerze lokalnym, cały folder można łatwo sklonować na VPS z GitHuba.
