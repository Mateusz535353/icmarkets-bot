import MetaTrader5 as mt5

if not mt5.initialize():
    print("❌ Nie udało się połączyć:", mt5.last_error())
    quit()

account_info = mt5.account_info()
print(f"🔎 Zalogowano na konto: {account_info.login} | Saldo: {account_info.balance} | Serwer: {account_info.server}")

symbol = "USTEC"
symbol_info = mt5.symbol_info(symbol)
if not symbol_info.visible:
    mt5.symbol_select(symbol, True)

tick = mt5.symbol_info_tick(symbol)
if tick is None:
    print("❌ Brak danych tickowych")
    mt5.shutdown()
    quit()

digits = symbol_info.digits
lot = 0.1
price = round(tick.ask, digits)
sl = round(price - 2.0, digits)
tp = round(price + 2.0, digits)

order = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "sl": sl,
    "tp": tp,
    "deviation": 5,
    "magic": 123456,
    "comment": "Test BUY via Python",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC
}

result = mt5.order_send(order)

if result.retcode != mt5.TRADE_RETCODE_DONE:
    print(f"❌ Błąd: {result.retcode}")
    print("📋 Szczegóły błędu:")
    print(result)
else:
    print("✅ Zlecenie zrealizowane!")
    print(result)

mt5.shutdown()
