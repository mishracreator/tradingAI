import yfinance as yf
import ta

def analyze_market(symbol, name):
    print(f"\n===== {name} ANALYSIS =====")

    data = yf.download(symbol, period="2y", interval="1d")
    data.columns = data.columns.get_level_values(0)

    data['EMA200'] = ta.trend.ema_indicator(close=data['Close'], window=200)
    data['RSI'] = ta.momentum.rsi(close=data['Close'], window=14)
    data['MACD'] = ta.trend.macd_diff(close=data['Close'])

    latest = data.iloc[-1]

    price = latest['Close']
    ema = latest['EMA200']
    rsi = latest['RSI']
    macd = latest['MACD']

    print("Price:", round(price, 2))
    print("EMA200:", round(ema, 2))
    print("RSI:", round(rsi, 2))
    print("MACD:", round(macd, 5))

    if price > ema and rsi > 50 and macd > 0:
        decision = "CALL (BUY)"
    elif price < ema and rsi < 50 and macd < 0:
        decision = "PUT (SELL)"
    else:
        decision = "NO TRADE"

    print("Decision:", decision)


# ===== USER INPUT =====

print("\nMarkets Available:")
print("1 - NIFTY 50")
print("2 - EUR/USD")
print("3 - BTC")

choice = input("\nEnter market number: ")

if choice == "1":
    analyze_market("^NSEI", "NIFTY 50")
elif choice == "2":
    analyze_market("EURUSD=X", "EUR/USD")
elif choice == "3":
    analyze_market("BTC-USD", "BTC")
else:
    print("Invalid choice.")
