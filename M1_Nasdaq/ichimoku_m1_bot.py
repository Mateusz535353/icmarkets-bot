# ichimoku_m1_bot.py
# Bot M1 Nasdaq v1.0 - tylko na podstawie pozycji ceny względem chmury Ichimoku

import MetaTrader5 as mt5
import pandas as pd
import time
from datetime import datetime

# Parametry
SYMBOL = "USTEC"
TIMEFRAME = mt5.TIMEFRAME_M1
ICHIMOKU_SETTINGS = (9, 26, 52)  # Tenkan, Kijun, Senkou
MAGIC = 123456  # Identyfikator pozycji tego bota

# Inicjalizacja MT5
if not mt5.initialize():
    print("MT5 initialization failed")
    quit()

# Zamknięcie istniejących pozycji (na start)
def close_all():
    positions = mt5.positions_get(symbol=SYMBOL)
    if positions:
        for pos in positions:
            order_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(SYMBOL).bid if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(SYMBOL).ask
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": SYMBOL,
                "volume": pos.volume,
                "type": order_type,
                "position": pos.ticket,
                "price": price,
                "deviation": 10,
                "magic": MAGIC,
                "comment": "Close position",
            }
            mt5.order_send(request)

# Funkcja obliczająca chmurę Ichimoku na dataframe
def calculate_ichimoku(data):
    nine_high = data['high'].rolling(window=9).max()
    nine_low = data['low'].rolling(window=9).min()
    tenkan_sen = (nine_high + nine_low) / 2

    twenty_six_high = data['high'].rolling(window=26).max()
    twenty_six_low = data['low'].rolling(window=26).min()
    kijun_sen = (twenty_six_high + twenty_six_low) / 2

    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)
    senkou_span_b = ((data['high'].rolling(window=52).max() + data['low'].rolling(window=52).min()) / 2).shift(26)

    return senkou_span_a, senkou_span_b

# Funkcja pobierająca dane z MT5
def get_data():
    rates = mt5.copy_rates_from_pos(SYMBOL, TIMEFRAME, 0, 100)
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

# Sprawdzenie, czy mamy otwartą pozycję

def get_current_position():
    positions = mt5.positions_get(symbol=SYMBOL)
    for pos in positions:
        if pos.magic == MAGIC:
            return pos.type
    return None

# Główna pętla robota
while True:
    df = get_data()
    senkou_a, senkou_b = calculate_ichimoku(df)
    current_price = df['close'].iloc[-1]
    span_a = senkou_a.iloc[-27]  # bo shift(26) + świeca 0 = -27
    span_b = senkou_b.iloc[-27]

    upper_cloud = max(span_a, span_b)
    lower_cloud = min(span_a, span_b)

    pos = get_current_position()

    if pos is None:
        if current_price > upper_cloud:
            # otwieramy LONG
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": SYMBOL,
                "volume": 1.0,
                "type": mt5.ORDER_TYPE_BUY,
                "price": mt5.symbol_info_tick(SYMBOL).ask,
                "deviation": 10,
                "magic": MAGIC,
                "comment": "Open LONG",
            }
            mt5.order_send(request)

        elif current_price < lower_cloud:
            # otwieramy SHORT
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": SYMBOL,
                "volume": 1.0,
                "type": mt5.ORDER_TYPE_SELL,
                "price": mt5.symbol_info_tick(SYMBOL).bid,
                "deviation": 10,
                "magic": MAGIC,
                "comment": "Open SHORT",
            }
            mt5.order_send(request)

    elif pos == mt5.ORDER_TYPE_BUY and current_price < lower_cloud:
        close_all()
        # otwórz SHORT
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": SYMBOL,
            "volume": 1.0,
            "type": mt5.ORDER_TYPE_SELL,
            "price": mt5.symbol_info_tick(SYMBOL).bid,
            "deviation": 10,
            "magic": MAGIC,
            "comment": "Switch to SHORT",
        }
        mt5.order_send(request)

    elif pos == mt5.ORDER_TYPE_SELL and current_price > upper_cloud:
        close_all()
        # otwórz LONG
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": SYMBOL,
            "volume": 1.0,
            "type": mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(SYMBOL).ask,
            "deviation": 10,
            "magic": MAGIC,
            "comment": "Switch to LONG",
        }
        mt5.order_send(request)

    time.sleep(60)
