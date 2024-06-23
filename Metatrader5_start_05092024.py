# Metatrader5.py
import logging
import MetaTrader5 as mt5
# from MetaTrader5 import order_send
# Replace with your broker's login credentials
account = 81725731
password = "Tien-123"
server = "MetaQuotes-Demo"


mt5.initialize(account = 81725731, password = "Tien-123",server = "MetaQuotes-Demo")

# # Initialize connection to MetaTrader 5 terminal
# if not mt5.initialize():
#     print("Failed to connect to MetaTrader 5!")
#     exit()



# # Shutdown connection to MetaTrader 5 terminal
# mt5.shutdown()

def market_order(symbol,volume,order_type):
    tick = mt5.symbol_info_tick(symbol)
    order_dict = {'buy':0,'sell' :1}
    logging.basicConfig(level=logging.DEBUG)

    def fetch_tick_from_api():
        # Placeholder function, replace with actual implementation
        # Simulate a case where None might be returned
        return None

    def get_tick_data():
        tick = fetch_tick_from_api()
        if tick is None:
            logging.error("fetch_tick_from_api() returned None")
        return tick
    
    tick = get_tick_data()
    if tick is not None:
        price_dict = {'buy': tick.ask, 'sell': tick.bid}
    else:    
        logging.warning("tick is None, setting default values")
        price_dict = {'buy': None, 'sell': None}



    request = ({
            "action":mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": volume,
            "type": order_dict[order_type],
            "price":  price_dict[order_type],
            "deviation": 20,
            "magic": 100,
            "comment": "python market order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }) 

# def buy_limit(symbol, volume, price):
#     #order send
#     request = mt5.order_send({
#         "action":mt5.TRADE_ACTION_PENDING,
#         "symbol": "symbol",
#         "volume": volume,
#         "type": mt5.ORDER_TYPE_BUY_LIMIT,
#         "price":  price,
#         "deviation": 20,
#         "magic": 100,
#         "comment": "python market order",
#         "type_time": mt5.ORDER_TIME_GTC,
#         "type_filling": mt5.ORDER_FILLING_IOC,
#     })
#     print(request)


# buy_limit("GBPUSD",0.02, 1.26610)  

    order_result = mt5.order_send(request)
    print(order_result)
    return order_result

market_order('GBPUSD',0.05,'sell')

# if not mt5.login(account, password=password, server=server):
#     print("Failed to authenticate with MetaTrader 5 server!")
#     exit()

# --------------------------------------------

import MetaTrader5 as mt5
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Account MT5
account = 81725731
password = "Tien-123"
server = "MetaQuotes-Demo"


# mt5.initialize(account = 81725731, password = "Tien-123",server = "MetaQuotes-Demo")

# Connect to MetaTrader 5
if not mt5.initialize():
    logging.error("initialize() failed, error code =", mt5.last_error())
    quit()

# Set up account credentials
account = 81725731
password = "123"

# Login to the trading account
if not mt5.login(account, password):
    logging.error("login() failed, error code =", mt5.last_error())
    mt5.shutdown()
    quit()

logging.info("Connected to account:", account)

# Define the symbol to trade
symbol = "EURUSD"

# Ensure the symbol is available in Market Watch
if not mt5.symbol_select(symbol, True):
    logging.error("symbol_select({}) failed, error code =", symbol, mt5.last_error())
    mt5.shutdown()
    quit()

# Define a simple trading strategy
def simple_strategy():
    # Get the current tick
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        logging.warning(f"Failed to get tick for symbol {symbol}")
        return None

    # Simple strategy: buy if the bid price is below a certain threshold, sell if above
    buy_threshold = 1.1000
    sell_threshold = 1.1100

    if tick.bid < buy_threshold:
        return "buy"
    elif tick.ask > sell_threshold:
        return "sell"
    else:
        return None

# Function to place an order
def place_order(order_type):
    price = mt5.symbol_info_tick(symbol).ask if order_type == "buy" else mt5.symbol_info_tick(symbol).bid
    deviation = 20

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": 0.1,
        "type": mt5.ORDER_TYPE_BUY if order_type == "buy" else mt5.ORDER_TYPE_SELL,
        "price": price,
        "deviation": deviation,
        "magic": 234000,
        "comment": "Python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logging.error(f"Order send failed, retcode={result.retcode}")
        return False

    logging.info(f"Order send successful, {order_type} at price {price}")
    return True

# Main trading loop
while True:
    strategy_signal = simple_strategy()
    if strategy_signal:
        place_order(strategy_signal)

    # Wait for a certain period before the next iteration
    time.sleep(60)

# Shutdown MT5 connection
mt5.shutdown()
