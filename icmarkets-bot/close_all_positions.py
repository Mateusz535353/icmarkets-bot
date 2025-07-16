import MetaTrader5 as mt5

if not mt5.initialize():
    print("❌ Nie udało się połączyć:", mt5.last_error())
    quit()

symbol = "USTEC"
positions = mt5.positions_get(symbol=symbol)

if positions is None or len(positions) == 0:
    print(f"ℹ️ Brak otwartych pozycji na {symbol}")
    mt5.shutdown()
    quit()

for pos in positions:
    ticket = pos.ticket
    volume = pos.volume
    position_type = pos.type
    close_type = mt5.ORDER_TYPE_SELL if position_type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
    price = mt5.symbol_info_tick(symbol).bid if position_type == mt5.POSITION_TYPE_BUY else mt5.symbol_info_tick(symbol).ask
    digits = mt5.symbol_info(symbol).digits
    price = round(price, digits)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "position": ticket,
        "symbol": symbol,
        "volume": volume,
        "type": close_type,
        "price": price,
        "deviation": 5,
        "magic": 123456,
        "comment": "Zamknięcie pozycji",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }

    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Nie udało się zamknąć pozycji {ticket}: {result.retcode}")
        print(result)
    else:
        print(f"✅ Pozycja {ticket} zamknięta!")

mt5.shutdown()
